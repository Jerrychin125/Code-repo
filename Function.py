import os
import statistics as stc
import matplotlib.dates as mdate
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib as mpl
import pandas as pd
import numpy as np

# ---－－－－－－－－－－－－－－－－－－－－－－－－－ #
# 1. 取得歷年的每月平均，並且放置在同一張圖表內做為比對 #
# ---－－－－－－－－－－－－－－－－－－－－－－－－－ #

def Get_Month_avg_plot():
    # 設定顏色，不然會重複
    cnames = [
        # '#00FFFF',
        '#7FFFD4',
        '#0000FF',
        '#8A2BE2',
        '#A52A2A',
        '#5F9EA0',
        '#D2691E',
        '#FF7F50',
        '#DC143C',
        '#00FFFF',
        '#00008B',
        # '#808080',
        '#008000',
        '#90EE90',
        '#00FF00',
        '#32CD32',
        '#FAF0E6',
        '#FF00FF',
        '#000080',
        '#FFA500',
        '#FFC0CB',
        '#800080',
        '#FF0000',
        '#2E8B57',
        '#008080',
        '#EE82EE',
        '#FFFF00'
    ]

    Year_Month_avg = []
    for year in range(97, 110):
        Each_Month_avg = []
        for month in range(1, 13):

            # Processing the CSV data

            try:
                f = open(f'RadioCSV/{year}年/{year}年{month:02d}月.csv', 'r')
                raw_data = f.read().strip()
            except UnicodeDecodeError:
                f = open(
                    f'RadioCSV/{year}年/{year}年{month:02d}月.csv', 'r', encoding='utf-8')
                raw_data = f.read().strip()
            except FileNotFoundError:
                break

            line_split = raw_data.split('\n')
            data = [s.split(',') for s in line_split]
            data = list(filter(lambda a: a != '', data))
            if data[0][0] == "GPS":
                del data[0]
            else:
                del data[1]

            # use for 97 year. That year is pretty weird, something really strange occur.
            try:
                idx = data[0].index('金門')
            except ValueError:
                idx = data[0].index('����')

            Kinmen_list = [data[i][idx] for i in range(1, len(data)) if data[i][idx] != '']
            Kinmen_list = list(map(float, Kinmen_list))

            Each_Month_avg.append(stc.mean(Kinmen_list))

        Year_Month_avg.append(Each_Month_avg)

    # Draw Graph

    os.makedirs('pic', exist_ok=True)

    from pylab import mpl
    mpl.rcParams['font.sans-serif'] = ['Microsoft YaHei']
    mpl.rcParams['axes.unicode_minus'] = False
    mpl.rcParams['figure.figsize'] = 8, 6

    plt.xlabel('月')
    plt.ylabel('平均環境輻射量(μSv)')
    plt.title(f'金門氣象站測站歷年每月月平均變化圖')

    for i in range(0, len(Year_Month_avg)):
        if len(Year_Month_avg[i])< 12:
            x = np.arange(1, len(Year_Month_avg[i]+1, 1), 1)
            plt.plot(x, Year_Month_avg[i], 'o-', label=f"{96+i+1}", color=cnames[i])
            plt.xticks(np.arange(min(x), max(x)+1, 1.0))
            # plt.show()
        else:
            x = np.arange(1, 13, 1)
            plt.plot(x, Year_Month_avg[i], 'o-', label=f"{96+i+1}", color=cnames[i])
            plt.xticks(np.arange(min(x), max(x)+1, 1.0))
            # plt.show()

    plt.xticks(np.arange(min(np.arange(1, 13, 1)), max(np.arange(1, 13, 1))+1, 1.0))
    plt.grid(True,linestyle = "--",color = 'gray' ,linewidth = '0.5',axis='both')
    plt.legend()
    plt.savefig(f"./pic/金門氣象站測站歷年每月月平均變化圖.png", dpi=300)
    plt.clf()
    print(f"金門：金門氣象站測站歷年每月月平均變化圖 已下載完成")

# ---－－－－－－－－－－－－－－－－－－－－－－－－ #
# 2. 取得年平均輻射量變化，以利觀察每年分的差異量 #
# ---－－－－－－－－－－－－－－－－－－－－－－－－ #

def Get_Year_avg_plot():
    Each_Year_avg = []
    for year in range(97, 110):
        Each_Month_avg = []
        for month in range(1, 13):

            # Processing the CSV data

            try:
                f = open(f'RadioCSV/{year}年/{year}年{month:02d}月.csv', 'r')
                raw_data = f.read().strip()
            except UnicodeDecodeError:
                f = open(
                    f'RadioCSV/{year}年/{year}年{month:02d}月.csv', 'r', encoding='utf-8')
                raw_data = f.read().strip()
            except FileNotFoundError:
                break

            line_split = raw_data.split('\n')
            data = [s.split(',') for s in line_split]
            data = list(filter(lambda a: a != '', data))
            if data[0][0] == "GPS":
                del data[0]
            else:
                del data[1]

            try:
                idx = data[0].index('金門')
            # use for 97 year. That year is pretty weird, something really strange occur.
            except ValueError:
                idx = data[0].index('����')

            Kinmen_list = [data[i][idx] for i in range(1, len(data)) if data[i][idx] != '']
            Kinmen_list = list(map(float, Kinmen_list))

            Each_Month_avg.append(stc.mean(Kinmen_list))
            # Each_Month_avg.append( sum(Kinmen_list) / len(Kinmen_list) )

        Each_Year_avg.append(stc.mean(Each_Month_avg))

    # Draw Graph

    os.makedirs('pic', exist_ok=True)

    from pylab import mpl
    mpl.rcParams['font.sans-serif'] = ['Microsoft YaHei']
    mpl.rcParams['axes.unicode_minus'] = False
    mpl.rcParams['figure.figsize'] = 8, 6

    plt.xlabel('年')
    plt.ylabel('平均環境輻射劑量(μSv/h)')
    plt.title(f'金門氣象站測站年平均輻射量變化圖')

    x = np.arange(97, 97+len(Each_Year_avg), 1)
    plt.plot(x, Each_Year_avg, 'o-')
    plt.xticks(np.arange(min(x), max(x)+1, 1.0), rotation=45)
    plt.grid(True,linestyle = "--",color = 'gray' ,linewidth = '0.5',axis='both')
    plt.savefig(f"./pic/金門氣象站測站年平均輻射量變化圖.png", dpi=300)
    # plt.show()
    plt.clf()
    print(f"金門：金門氣象站測站年平均輻射量變化圖 已下載完成")

# ---－－－－－－－－－－－－－－－－－－－－－－－－－ #
# 3. 取得不同年份金門與榮湖月平均變化比較，比較兩者差異 #
# ---－－－－－－－－－－－－－－－－－－－－－－－－－ #

def Get_JungHu_vs_Kinmen():
    Kinmen_Year_avg = []
    JungHu_Year_avg = []
    for year in range(108, 110):
        Kinmen_Month_avg = []
        JungHu_Month_avg = []
        for month in range(1, 13):

            # Processing the CSV data

            try:
                f = open(f'RadioCSV/{year}年/{year}年{month:02d}月.csv', 'r')
                raw_data = f.read().strip()
            except UnicodeDecodeError:
                f = open(
                    f'RadioCSV/{year}年/{year}年{month:02d}月.csv', 'r', encoding='utf-8')
                raw_data = f.read().strip()
            except FileNotFoundError:
                break

            line_split = raw_data.split('\n')
            data = [s.split(',') for s in line_split]
            data = list(filter(lambda a: a != '', data))
            if data[0][0] == "GPS":
                del data[0]
            else:
                del data[1]

            Kinmen_idx = data[0].index('金門')
            JungHu_idx = data[0].index('榮湖')

            Kinmen_list = [data[i][Kinmen_idx] for i in range(1, len(data)) if data[i][Kinmen_idx] != '']
            Kinmen_list = list(map(float, Kinmen_list))

            JungHu_list = [data[i][JungHu_idx] for i in range(1, len(data)) if data[i][JungHu_idx] != '']
            JungHu_list = list(map(float, JungHu_list))

            Kinmen_Month_avg.append(stc.mean(Kinmen_list))
            JungHu_Month_avg.append(stc.mean(JungHu_list))

        Kinmen_Year_avg.append(Kinmen_Month_avg)
        JungHu_Year_avg.append(JungHu_Month_avg)

    # Draw Graph

    os.makedirs('./pic/KinmenJunghu', exist_ok=True)

    from pylab import mpl
    mpl.rcParams['font.sans-serif'] = ['Microsoft YaHei']
    mpl.rcParams['axes.unicode_minus'] = False
    mpl.rcParams['figure.figsize'] = 8, 6

    for year in range(108, 110, 1):
        plt.xlabel('月')
        plt.ylabel('平均環境輻射劑量(μSv/h)')
        plt.title(f'民國{year}年金門氣象站測站與榮湖淨水廠測站環境輻射劑量月平均變化比較圖')

        if year == 110:
            x = np.arange(1, 8, 1)
            plt.plot(x, Kinmen_Year_avg[year-108], 'o-', label="金門")
            plt.plot(x, JungHu_Year_avg[year-108], 'o-', label="榮湖")
            plt.xticks(np.arange(min(x), max(x)+1, 1.0))
            # plt.show()
        else:
            x = np.arange(1, 13, 1)
            plt.plot(x, Kinmen_Year_avg[year-108], 'o-', label="金門")
            plt.plot(x, JungHu_Year_avg[year-108], 'o-', label="榮湖")
            plt.xticks(np.arange(min(x), max(x)+1, 1.0))
            # plt.show()

        plt.xticks(np.arange(min(np.arange(1, 13, 1)), max(np.arange(1, 13, 1))+1, 1.0))
        plt.grid(True,linestyle = "--",color = 'gray' ,linewidth = '0.5',axis='both')
        plt.legend()
        plt.savefig(f"./pic/KinmenJunghu/民國{year}年金門氣象站測站與榮湖淨水廠測站環境輻射劑量月平均變化比較圖.png", dpi=300)
        plt.clf()
    print(f"金門與榮湖：民國{year}年金門氣象站測站與榮湖淨水廠測站環境輻射劑量月平均變化比較圖 已下載完成")

# ---－－－－－－－－－－－－－－－－－－－－－－－－－－－ #
# 4. 取得不同年份年金門與陽明山月平均變化比較，比較兩者差異 #
# ---－－－－－－－－－－－－－－－－－－－－－－－－－－－ #

def Get_Yangming_vs_Kinmen():

    Kinmen_Year_avg = []
    YangmingMT_Year_avg = []
    for year in range(97, 110):
        Kinmen_Month_avg = []
        YangmingMT_Month_avg = []
        for month in range(1, 13):

            # Processing the CSV data

            try:
                f = open(f'RadioCSV/{year}年/{year}年{month:02d}月.csv', 'r')
                raw_data = f.read().strip()
            except UnicodeDecodeError:
                f = open(
                    f'RadioCSV/{year}年/{year}年{month:02d}月.csv', 'r', encoding='utf-8')
                raw_data = f.read().strip()
            except FileNotFoundError:
                break

            line_split = raw_data.split('\n')
            data = [s.split(',') for s in line_split]
            data = list(filter(lambda a: a != '', data))
            if data[0][0] == "GPS":
                del data[0]
            else:
                del data[1]

            # use for 97 year. That year is pretty weird, something really strange occur.
            try:
                Kinmen_idx = data[0].index('金門')
                YangmingMT_idx = data[0].index('陽明山')
            except ValueError:
                Kinmen_idx = data[0].index('����')
                YangmingMT_idx = data[0].index('�����s')

            Kinmen_list = [data[i][Kinmen_idx] for i in range(1, len(data)) if data[i][Kinmen_idx] != '']
            Kinmen_list = list(map(float, Kinmen_list))

            YangmingMT_list = [data[i][YangmingMT_idx] for i in range(1, len(data)) if data[i][YangmingMT_idx] != '']
            YangmingMT_list = list(map(float, YangmingMT_list))

            Kinmen_Month_avg.append(stc.mean(Kinmen_list))
            YangmingMT_Month_avg.append(stc.mean(YangmingMT_list))

        Kinmen_Year_avg.append(Kinmen_Month_avg)
        YangmingMT_Year_avg.append(YangmingMT_Month_avg)

        f.close()

    from pylab import mpl
    mpl.rcParams['font.sans-serif'] = ['Microsoft YaHei']
    mpl.rcParams['axes.unicode_minus'] = False

    os.makedirs('./pic/KinmenYangming', exist_ok=True)

    for idx in range(0, 13, 1):
        plt.xlabel('月')
        plt.ylabel('平均環境輻射劑量(μSv/h)')
        plt.title(f'民國{idx+97}年金門氣象站測站與陽明山測站環境輻射劑量月平均變化比較圖')

        if len(Kinmen_Year_avg[idx]) != 12:
            x = np.arange(1, len(Kinmen_Year_avg[idx])+1, 1)
            plt.plot(x, Kinmen_Year_avg[idx], 'o-', label="金門")
            plt.plot(x, YangmingMT_Year_avg[idx], 'o-', label="陽明")
            plt.xticks(np.arange(min(x), max(x)+1, 1.0))
            # plt.show()
        else:
            x = np.arange(1, 13, 1)
            plt.plot(x, Kinmen_Year_avg[idx], 'o-', label="金門")
            plt.plot(x, YangmingMT_Year_avg[idx], 'o-', label="陽明")
            plt.xticks(np.arange(min(x), max(x)+1, 1.0))
            # plt.show()

        plt.xticks(np.arange(min(np.arange(1, 13, 1)), max(np.arange(1, 13, 1))+1, 1.0))
        plt.grid(True,linestyle = "--",color = 'gray' ,linewidth = '0.5',axis='both')
        plt.legend()
        plt.savefig(f"./pic/KinmenYangming/民國{idx+97}年金門氣象站測站與陽明山測站環境輻射劑量月平均變化比較圖.png", dpi=300)
        plt.clf()
        print(f"金門與陽明山：民國{idx+97}年金門氣象站測站與陽明山測站環境輻射劑量月平均變化比較圖")

# ---－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－ #
# 5. 取得金門氣象站測站與陽明山測站環境輻射劑量逐時變化，比較兩者差異 #
# ---－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－ #

def Get_10years_24hr_avg():
    Kinmen_24hr = []
    Junghu_24hr = []
    YangmingMT_24hr = []
    for i in range(0,24,1):
        Kinmen_24hr.append([])
        Junghu_24hr.append([])
        YangmingMT_24hr.append([])

    for year in range (97 , 110):
        for month in range (1 , 13) :
            
            # Processing the CSV data

            try:
                f = open(f'RadioCSV/{year}年/{year}年{month:02d}月.csv','r')
                raw_data = f.read().strip()
            except UnicodeDecodeError:
                f = open(f'RadioCSV/{year}年/{year}年{month:02d}月.csv','r', encoding='utf-8')
                raw_data = f.read().strip()
            except FileNotFoundError:
                break

            every_day = 0
            Kinmen_a_month_every_hour = 0
            RongHu_a_month_every_hour = 0
            
            line_split = raw_data.split('\n')
            data = [s.split(',') for s in line_split]

            if data[0][0] == "GPS":
                del data[0]
            else :
                del data[1]

            # use for 97 year. That year is pretty weird, something really strange occur.

            try:
                Kinmen_idx = data[0].index('金門')
                YangmingMT_idx = data[0].index('陽明山')
            except ValueError:
                Kinmen_idx = data[0].index('����')
                YangmingMT_idx = data[0].index('�����s')

            Kinmen_list = [ data[i][Kinmen_idx] for i in range(1,len(data)) ]
            # RongHu_list = list(map( float, [ data[i][RongHu_idx] for i in range(1,len(data)) if data[i][Junghu_idx] != '' ] ))
            YangmingMT_list = [ data[i][YangmingMT_idx] for i in range(1,len(data)) ]

            if year == 108 and month == 5:
                continue

            while True:
                for i in range(0, 24, 1):

                    # 金門
                    if Kinmen_list[i] != '':
                        Kinmen_24hr[i].append(float(Kinmen_list[i]))

                    # 陽明山
                    if YangmingMT_list[i] != '':
                        YangmingMT_24hr[i].append(float(YangmingMT_list[i]))
                
                del Kinmen_list[0:24]
                del YangmingMT_list[0:24]
                if len(Kinmen_list) == 0:
                    break

    for i in range(0, 24, 1):
        Kinmen_24hr[i] = stc.mean(Kinmen_24hr[i])
        YangmingMT_24hr[i] = stc.mean(YangmingMT_24hr[i])

    # Draw Graph

    from pylab import mpl
    mpl.rcParams['font.sans-serif'] = ['Microsoft YaHei']
    mpl.rcParams['axes.unicode_minus'] = False
    mpl.rcParams['figure.figsize'] = 8, 6

    plt.xlabel('時')
    plt.ylabel('平均環境輻射劑量(μSv/h)')
    plt.title(f'金門氣象站測站與陽明山測站環境輻射劑量逐時變化圖')

    x = np.arange(1, 25, 1)
    plt.plot(x, Kinmen_24hr, 'o-', label="金門")
    plt.plot(x, YangmingMT_24hr, 'o-', label="陽明山")
    plt.xticks(np.arange(min(x), max(x)+1, 1.0))
    # plt.show()

    plt.xticks(np.arange(min(np.arange(1, 25, 1)), max(np.arange(1, 25, 1))+1, 1.0))
    plt.grid(True,linestyle = "--",color = 'gray' ,linewidth = '0.5',axis='both')
    plt.legend()
    plt.savefig(f"./pic/KinmenYangming/金門氣象站測站與陽明山測站環境輻射劑量逐時變化圖.png", dpi=300)
    plt.clf()
    print(f"金門與陽明山：金門氣象站測站與陽明山測站環境輻射劑量逐時變化圖 已下載完成")

# ---－－－－－－－－－－－－－－－－－－－－－－－－－－－－－ #
# 6. 取得不同年份金門與榮湖與陽明山測站月平均變化，比較三者變化 #
# ---－－－－－－－－－－－－－－－－－－－－－－－－－－－－－ #

def Get_Yangming_Junghu_Kinmen():

    for year in range(108, 110):
        Kinmen_month = []
        Junghu_month = []
        YangmingMT_month = []
        for month in range(1, 13):

            # Processing the CSV data

            try:
                f = open(f'RadioCSV/{year}年/{year}年{month:02d}月.csv', 'r')
                raw_data = f.read().strip()
            except UnicodeDecodeError:
                f = open(
                    f'RadioCSV/{year}年/{year}年{month:02d}月.csv', 'r', encoding='utf-8')
                raw_data = f.read().strip()
            except FileNotFoundError:
                break

            line_split = raw_data.split('\n')
            data = [s.split(',') for s in line_split]
            if data[0][0] == "GPS":
                del data[0]
            else:
                del data[1]

            Kinmen_idx = data[0].index('金門')
            Junghu_idx = data[0].index('榮湖')
            YangmingMT_idx = data[0].index('陽明山')

            Kinmen_list = list(map(float, [data[i][Kinmen_idx] for i in range(1, len(data)) if data[i][Kinmen_idx] != '']))
            YangmingMT_list = list(map(float, [data[i][Junghu_idx] for i in range(1, len(data)) if data[i][Junghu_idx] != '']))
            Junghu_list = list(map(float, [data[i][YangmingMT_idx] for i in range(1, len(data)) if data[i][YangmingMT_idx] != '']))

            Kinmen_month.append(stc.mean(Kinmen_list))
            Junghu_month.append(stc.mean(Junghu_list))
            YangmingMT_month.append(stc.mean(YangmingMT_list))

        # Draw graph

        os.makedirs('./pic/KinmenYangmingJunghu', exist_ok=True)

        from pylab import mpl
        mpl.rcParams['font.sans-serif'] = ['Microsoft YaHei']
        mpl.rcParams['axes.unicode_minus'] = False
        mpl.rcParams['figure.figsize'] = 8, 6

        plt.xlabel('月')
        plt.ylabel('平均環境輻射劑量(μSv/h)')
        plt.title(f'民國{year}年金門氣象站測站與陽明山測站與榮湖淨水廠測站環境輻射劑量月平均變化圖')

        if year == 110:
            x = np.arange(1, 8, 1)
            plt.plot(x, Kinmen_month, 'o-', label="金門")
            plt.plot(x, Junghu_month, 'o-', label="榮湖")
            plt.plot(x, YangmingMT_month, 'o-', label="陽明山")
        else:
            x = np.arange(1, 13, 1)
            plt.plot(x, Kinmen_month, 'o-', label="金門")
            plt.plot(x, Junghu_month, 'o-', label="榮湖")
            plt.plot(x, YangmingMT_month, 'o-', label="陽明山")

        plt.xticks(np.arange(min(np.arange(1, 13, 1)),  max(np.arange(1, 13, 1))+1, 1.0))
        plt.grid(True,linestyle = "--",color = 'gray' ,linewidth = '0.5',axis='both')
        plt.legend()
        plt.savefig(f"./pic/KinmenYangmingJunghu/民國{year}年金門氣象站測站與陽明山測站與榮湖淨水廠測站環境輻射劑量月平均變化圖.png", dpi=300)
        # plt.show()
        plt.clf()
        print(f"金門與與榮湖陽明山：民國{year}年金門氣象站測站與陽明山測站與榮湖淨水廠測站環境輻射劑量月平均變化圖 已下載完成")

# ---－－－－－－－－－－－－－－－－－－－－－－ #
# 7. 取得金門與陽明山與榮湖逐年變化，比較三者變化 #
# ---－－－－－－－－－－－－－－－－－－－－－－ #

def Get_Yangming_Junghu_Kinmen_years():
    Kinmen_year_avg = []
    Kinmen_year_all = 0
    Kinmen_date_counter = 0

    YangmingMT_year_avg = []
    YangmingMT_year_all = 0
    YangmingMT_date_counter = 0

    Junghu_year_avg = []
    Junghu_year_all = 0
    Junghu_date_counter = 0


    for year in range(97 , 110):
        Kinmen_month_all = 0
        YangmingMT_month_all = 0
        Junghu_month_all = 0
        Kinmen_date_counter = 0
        YangmingMT_date_counter = 0
        Junghu_date_counter = 0
        for month in range(1 , 13): 

            # Processing the CSV data
            try:
                f = open(f'RadioCSV/{year}年/{year}年{month:02d}月.csv','r')
                raw_data = f.read().strip()
            except UnicodeDecodeError:
                f = open(f'RadioCSV/{year}年/{year}年{month:02d}月.csv','r',encoding='utf-8')
                raw_data = f.read().strip()
            except FileNotFoundError:
                break

            line_split = raw_data.split('\n')
            data = [s.split(',') for s in line_split]
            data = list(filter(lambda a: a != '', data))
            if data[0][0] == "GPS":
                del data[0]
            else:
                del data[1]
                    
            # 拿到金門的data_list / 陽明山的data_list / 榮湖的data_list
            Kinmen_idx = data[0].index('金門')
            Kinmen_list = [data[i][Kinmen_idx] for i in range(1,len(data)) if data[i][Kinmen_idx] != '']
            Kinmen_list = list(map(float, Kinmen_list))

            YangmingMT_idx = data[0].index('陽明山')
            YangmingMT_list = [data[i][YangmingMT_idx] for i in range(1,len(data)) if data[i][YangmingMT_idx] != '']
            YangmingMT_list = list(map(float, YangmingMT_list))

            try :
                Junghu_idx = data[0].index('榮湖')
                Junghu_list = [data[i][Junghu_idx] for i in range(1,len(data)) if data[i][Junghu_idx] != '']
                Junghu_list = list(map(float, Junghu_list))
            except :
                pass

            # 拿到金門年平均 / 陽明山的年平均 / 榮湖的年平均
            # 金門年平均 : Kinmen_year_avg[]
            # 陽明山年平均 : YangmingMT_year_avg[]
            # 榮湖年平均 : Junghu_year_avg[]
            for i in range(1, len(Kinmen_list)):
                if Kinmen_list[i] != '' and Kinmen_list[i] != '0':
                    Kinmen_month_all += float(Kinmen_list[i])
                    Kinmen_date_counter += 1

            for i in range(1, len(YangmingMT_list)):
                if  YangmingMT_list[i] != '' and YangmingMT_list[i] != '0':
                    YangmingMT_month_all += float(YangmingMT_list[i])
                    YangmingMT_date_counter += 1
                    
            try :
                for i in range(1, len(Junghu_list)):
                    if  Junghu_list[i] != '' and Junghu_list[i] != '0':
                        Junghu_month_all += float(Junghu_list[i])
                        Junghu_date_counter += 1
            except :
                pass
            
        Kinmen_year_avg.append( Kinmen_month_all / Kinmen_date_counter )
        YangmingMT_year_avg.append( YangmingMT_month_all / YangmingMT_date_counter )
        try :
            Junghu_year_avg.append( Junghu_month_all / Junghu_date_counter )
        except :
            pass

    # Draw Graph

    from pylab import mpl
    mpl.rcParams['font.sans-serif'] = ['Microsoft YaHei']
    mpl.rcParams['axes.unicode_minus'] = False
    mpl.rcParams['figure.figsize'] = 8, 6

    plt.xlabel('年')
    plt.ylabel('平均環境輻射劑量(μSv/h)')
    plt.title(f'金門與陽明山與榮湖測站環境輻射劑量逐年變化圖')

    x = np.arange(97, 110, 1)
    plt.plot(x, Kinmen_year_avg, 'o-', label="金門")
    plt.plot(np.arange(108, 110, 1), Junghu_year_avg, 'o-', label="榮湖")
    plt.plot(x, YangmingMT_year_avg, 'o-', label="陽明山")
    plt.xticks(np.arange(min(x), max(x)+1, 1.0))
    # plt.show()
    
    plt.grid(True,linestyle = "--",color = 'gray' ,linewidth = '0.5',axis='both')

    plt.xticks(np.arange(min(np.arange(97, 110, 1)), max(np.arange(97, 110, 1))+1, 1.0), rotation=90)
    plt.legend()
    plt.savefig(f"./pic/KinmenYangmingJunghu/金門與陽明山與榮湖測站環境輻射劑量逐年變化圖.png", dpi=300)
    plt.clf()
    print(f"金門與陽明山與榮湖：金門與陽明山與榮湖測站環境輻射劑量逐年變化 已下載完成")
