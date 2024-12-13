// server/src/main.cpp

#include <arpa/inet.h>
#include <errno.h>
#include <fcntl.h>
#include <netinet/in.h>
#include <signal.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/select.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <unistd.h>

#include <algorithm>
#include <iostream>
#include <map>
#include <mutex>
#include <string>
#include <thread>
#include <vector>

#include "../include/json.hpp"

using json = nlohmann::json;

// Constants
#define MAXLINE 4096
#define SERV_PORT 8555
#define LISTENQ 10
#define MAXCLIENT 100

// Struct to represent a connected user
struct User {
    int sockfd;
    std::string name;
    int cursor_x;
    int cursor_y;
    std::string color;

    User(int fd, const std::string& uname, const std::string& ucolor)
        : sockfd(fd), name(uname), cursor_x(0), cursor_y(0), color(ucolor) {}
};

// Global variables
std::map<int, User> users; // sockfd -> User
std::vector<std::string> shared_buffer = {""}; // Document lines
std::mutex users_mutex; // Mutex for thread safety

// Utility function to send data over a socket
ssize_t Writen(int fd, const void *vptr, size_t n) {
    size_t      nleft;
    ssize_t     nwritten;
    const char *ptr;

    ptr = (const char*)vptr;
    nleft = n;
    while (nleft > 0) {
        if ( (nwritten = write(fd, ptr, nleft)) <= 0 ) {
            if (nwritten < 0 && errno == EINTR)
                nwritten = 0;   // and call write() again
            else
                return -1;      // error
        }

        nleft -= nwritten;
        ptr += nwritten;
    }
    return n;
}

// Function to broadcast a JSON message to all clients except optionally one
void broadcast_message(const json& message, int exclude_fd = -1) {
    std::lock_guard<std::mutex> lock(users_mutex);
    std::string msg_str = message.dump() + "\n";
    for (const auto& [fd, user] : users) {
        if (fd != exclude_fd) {
            if (Writen(fd, msg_str.c_str(), msg_str.length()) < 0) {
                perror("Broadcast Writen error");
            }
        }
    }
}

// Function to send a JSON message to a single client
void send_message(int fd, const json& message) {
    std::string msg_str = message.dump() + "\n";
    if (Writen(fd, msg_str.c_str(), msg_str.length()) < 0) {
        perror("Send Writen error");
    }
}

// Function to assign a unique color to a user
std::string assign_color() {
    // Simple color assignment (could be improved to ensure uniqueness)
    static std::vector<std::string> colors = {
        "#FF5733", "#33FF57", "#3357FF", "#F333FF", "#FF33A8",
        "#33FFF5", "#FF8C33", "#8C33FF", "#33FF8C", "#FF3333"
    };
    static int index = 0;
    if (index >= colors.size()) index = 0;
    return colors[index++];
}

// Function to handle client communication
void handle_client(int connfd) {
    char buffer[MAXLINE];
    ssize_t n;

    // Prompt for username
    std::string prompt = "Enter your username: ";
    if (Writen(connfd, prompt.c_str(), prompt.length()) < 0) {
        perror("Prompt Writen error");
        close(connfd);
        return;
    }

    // Read username
    n = read(connfd, buffer, MAXLINE-1);
    if (n <= 0) {
        printf("Client disconnected before sending username.\n");
        close(connfd);
        return;
    }
    buffer[n] = '\0';
    std::string username(buffer);
    // Remove any trailing newline characters
    username.erase(std::remove(username.begin(), username.end(), '\n'), username.end());
    username.erase(std::remove(username.begin(), username.end(), '\r'), username.end());

    // Validate username
    bool valid = std::all_of(username.begin(), username.end(), [](char c) {
        return std::isalnum(c) || c == '-' || c == '_';
    });
    bool taken = false;

    {
        std::lock_guard<std::mutex> lock(users_mutex);
        for (const auto& [fd, user] : users) {
            if (user.name == username) {
                taken = true;
                break;
            }
        }
    }

    if (!valid) {
        json error_msg = {
            {"packet_type", "message"},
            {"data", {
                {"message_type", "error_newname_invalid"},
                {"message", "Invalid username. Use only letters, numbers, '-', '_'."}
            }}
        };
        send_message(connfd, error_msg);
        close(connfd);
        printf("Invalid username from socket %d. Connection closed.\n", connfd);
        return;
    }

    if (taken) {
        json error_msg = {
            {"packet_type", "message"},
            {"data", {
                {"message_type", "error_newname_taken"},
                {"message", "Username already taken. Choose another one."}
            }}
        };
        send_message(connfd, error_msg);
        close(connfd);
        printf("Username '%s' already taken. Connection closed.\n", username.c_str());
        return;
    }

    // Assign color
    std::string user_color = assign_color();

    // Add user to the map
    {
        std::lock_guard<std::mutex> lock(users_mutex);
        users.emplace(connfd, User(connfd, username, user_color));
    }

    // Send success message with current buffer and collaborators
    json success_msg = {
        {"packet_type", "message"},
        {"data", {
            {"message_type", "connect_success"},
            {"name", username},
            {"color", user_color},
            {"collaborators", json::array()},
            {"buffer", shared_buffer}
        }}
    };

    {
        std::lock_guard<std::mutex> lock(users_mutex);
        for (const auto& [fd, user] : users) {
            if (fd != connfd) {
                success_msg["data"]["collaborators"].push_back({
                    {"name", user.name},
                    {"color", user.color},
                    {"cursor", { {"x", user.cursor_x}, {"y", user.cursor_y} }}
                });
            }
        }
    }

    send_message(connfd, success_msg);

    // Notify other users about the new connection
    json notify_msg = {
        {"packet_type", "user_event"},
        {"data", {
            {"event", "user_connected"},
            {"user", {
                {"name", username},
                {"color", user_color},
                {"cursor", { {"x", 0}, {"y", 0} }}
            }}
        }}
    };
    broadcast_message(notify_msg, connfd);
    printf("User '%s' connected on socket %d.\n", username.c_str(), connfd);

    // Main loop to handle client messages
    while (true) {
        n = read(connfd, buffer, MAXLINE-1);
        if (n <= 0) {
            if (n == 0)
                printf("User '%s' disconnected.\n", username.c_str());
            else
                perror("Read error");
            break;
        }
        buffer[n] = '\0';
        std::string msg_str(buffer);
        // Split messages by newline
        size_t pos = 0;
        while ((pos = msg_str.find('\n')) != std::string::npos) {
            std::string line = msg_str.substr(0, pos);
            msg_str.erase(0, pos + 1);
            if (line.empty()) continue;
            try {
                json received = json::parse(line);
                if (!received.contains("packet_type")) {
                    // Invalid message
                    json error_msg = {
                        {"packet_type", "message"},
                        {"data", {
                            {"message_type", "error"},
                            {"message", "Invalid message format."}
                        }}
                    };
                    send_message(connfd, error_msg);
                    continue;
                }

                std::string packet_type = received["packet_type"];
                if (packet_type == "update") {
                    if (!received.contains("data")) {
                        json error_msg = {
                            {"packet_type", "message"},
                            {"data", {
                                {"message_type", "error"},
                                {"message", "No data field in update message."}
                            }}
                        };
                        send_message(connfd, error_msg);
                        continue;
                    }

                    json data = received["data"];

                    // Handle buffer updates
                    if (data.contains("buffer")) {
                        std::lock_guard<std::mutex> lock(users_mutex);
                        shared_buffer = data["buffer"].get<std::vector<std::string>>();

                        // Broadcast buffer update
                        json buffer_update = {
                            {"packet_type", "buffer_update"},
                            {"data", {
                                {"buffer", shared_buffer}
                            }}
                        };
                        broadcast_message(buffer_update);
                    }

                    // Handle cursor updates
                    if (data.contains("cursor")) {
                        int new_x = data["cursor"]["x"];
                        int new_y = data["cursor"]["y"];

                        {
                            std::lock_guard<std::mutex> lock(users_mutex);
                            users[connfd].cursor_x = new_x;
                            users[connfd].cursor_y = new_y;
                        }

                        // Broadcast cursor update
                        json cursor_update = {
                            {"packet_type", "cursor_update"},
                            {"data", {
                                {"user", username},
                                {"cursor", { {"x", new_x}, {"y", new_y} }}
                            }}
                        };
                        broadcast_message(cursor_update, connfd);
                    }
                }
                else {
                    // Unknown packet_type
                    json error_msg = {
                        {"packet_type", "message"},
                        {"data", {
                            {"message_type", "error"},
                            {"message", "Unknown packet_type."}
                        }}
                    };
                    send_message(connfd, error_msg);
                }
            }
            catch (json::parse_error& e) {
                // JSON parsing error
                json error_msg = {
                    {"packet_type", "message"},
                    {"data", {
                        {"message_type", "error"},
                        {"message", "Invalid JSON format."}
                    }}
                };
                send_message(connfd, error_msg);
            }
        }
    }

    // Remove user from the map and notify others
    {
        std::lock_guard<std::mutex> lock(users_mutex);
        users.erase(connfd);
    }

    // Notify other users about the disconnection
    json disconnect_msg = {
        {"packet_type", "user_event"},
        {"data", {
            {"event", "user_disconnected"},
            {"user", {
                {"name", username}
            }}
        }}
    };
    broadcast_message(disconnect_msg, connfd);

    close(connfd);
}

int main() {
    int listenfd, connfd;
    socklen_t clilen;
    struct sockaddr_in cliaddr, servaddr;

    // Ignore SIGPIPE to prevent server from crashing when writing to a closed socket
    signal(SIGPIPE, SIG_IGN);

    // Create listening socket
    if ( (listenfd = socket(AF_INET, SOCK_STREAM, 0)) < 0 ) {
        perror("Socket creation failed");
        exit(1);
    }

    // Set socket options to reuse address
    int opt = 1;
    if (setsockopt(listenfd, SOL_SOCKET, SO_REUSEADDR, (char *)&opt, sizeof(opt)) < 0) {
        perror("setsockopt");
        close(listenfd);
        exit(1);
    }

    // Bind the socket
    memset(&servaddr, 0, sizeof(servaddr));
    servaddr.sin_family = AF_INET;
    servaddr.sin_addr.s_addr = htonl(INADDR_ANY);
    servaddr.sin_port = htons(SERV_PORT);

    if ( bind(listenfd, (struct sockaddr *) &servaddr, sizeof(servaddr)) < 0 ) {
        perror("Bind failed");
        close(listenfd);
        exit(1);
    }

    // Listen
    if ( listen(listenfd, LISTENQ) < 0 ) {
        perror("Listen failed");
        close(listenfd);
        exit(1);
    }

    printf("Server started on port %d.\n", SERV_PORT);

    // Main loop to accept connections
    while (true) {
        clilen = sizeof(cliaddr);
        if ( (connfd = accept(listenfd, (struct sockaddr *) &cliaddr, &clilen)) < 0 ) {
            perror("Accept failed");
            continue;
        }

        // Check if maximum clients reached
        {
            std::lock_guard<std::mutex> lock(users_mutex);
            if (users.size() >= MAXCLIENT) {
                std::string msg = "Server full. Try again later.\n";
                Writen(connfd, msg.c_str(), msg.length());
                close(connfd);
                printf("Refused connection from %s:%d - server full.\n",
                       inet_ntoa(cliaddr.sin_addr), ntohs(cliaddr.sin_port));
                continue;
            }
        }

        // Create a new thread to handle the client
        std::thread client_thread(handle_client, connfd);
        client_thread.detach();
    }

    close(listenfd);
    return 0;
}