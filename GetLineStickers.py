import requests, os, bs4, json

# 半自動化
# 用法：輸入貼圖名字(不用一樣，但越接近越不會出錯)
print("自動下載 Line 貼圖")
print("用法：輸入貼圖名字(不用一樣，但越接近越不會出錯)")
print("注意事項：請勿輸入特殊符號(ex. & % $)，如果不確定可以試試看，如果跳出錯誤訊息代表不行")
value = input("輸入貼圖名字：")
base = "https://store.line.me"
api = "https://store.line.me/api/search/sticker"
headers = {
    "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36 Edg/95.0.1020.40'
}
url = "https://store.line.me/api/search/sticker" + f"?query={value}&offset=0&limit=36&type=ALL&includeFacets=true"
print(url)
response = requests.get(url, headers=headers)
# print(response.url)
# print(response.status_code)
# print(response.text)
target = json.loads(response.text)

if target["totalCount"] == 0:
    print("請檢查是否輸入正確名稱，或這是否有特殊符號喔！")
else:
    url = base + target["items"][0]["productUrl"][:-2] + "zh-Hant"
    # print(url)

    response = requests.get(url, headers=headers)
    soup = bs4.BeautifulSoup(response.text, "html.parser")
    name = soup.find("p", class_="mdCMN38Item01Ttl").string
    print(f"正在下載 {name}!")
    img = soup.find_all("span", class_="mdCMN09Image")
    # class="mdCMN09Image"

    os.makedirs(value, exist_ok=True)
    index = 1
    for i in img:
        if len(i["class"]) != 1:
            continue
        stickerURL = i.get("style")[21:107]
        response = requests.get(stickerURL)
        imageFile = open(os.path.join(value, f"{index}.png"), 'wb')
        for chunk in response.iter_content(100000):
            imageFile.write(chunk)
        imageFile.close

        print(f"正在下載 {name} 中的第 {index} 個貼圖")
        index += 1

    print(f"完成下載 {name}")