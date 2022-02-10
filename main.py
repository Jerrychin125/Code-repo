import requests, os, bs4
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib as mpl 
import numpy as np 
import statistics

def crawl_and_save_csv():
    url = "https://www.aec.gov.tw/trmc/monitoring/history.html"
    os.makedirs('RadioCSV', exist_ok=True)
    for year in range(97, 110):
        data = {"y":str(year)}
        head = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36"
        }

        response = requests.post(url, data=data).text

        soup = bs4.BeautifulSoup(response, 'html.parser')
        csvs = soup.select('.w_in_t div a')

        name = f"{year}年" # csvs[0].get('title')[7:(10+(year >= 100))]
        os.makedirs(f'RadioCSV/{name}', exist_ok=True)

        for csv in csvs:
            CSVurl = "https://www.aec.gov.tw" + csv.get('href')
            name2 = csv.get('title')[7:(13+(year >= 100))]

            response = requests.get(CSVurl)

            # If u wanna download csv files, remove the comments below
            Files = open(f'./RadioCSV/{name}/{name2}.csv', 'wb')
            Files.write(response.content)
            Files.close()

            print(f"{name2} 的 CSV 資料以下載")
            
# Main code

def main():

    # crawl_and_save_csv()

    import Function as func
    func.Get_Month_avg_plot()
    func.Get_Year_avg_plot()
    func.Get_JungHu_vs_Kinmen()
    func.Get_Yangming_vs_Kinmen()
    func.Get_10years_24hr_avg()
    func.Get_Yangming_Junghu_Kinmen()
    func.Get_Yangming_Junghu_Kinmen_years()

    print("All jobs have been done!")

if(__name__=="__main__"):
    main()
