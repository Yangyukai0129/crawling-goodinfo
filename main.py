import requests
from bs4 import BeautifulSoup
import pandas as pd
import json



class GoodInfo():
    def __init__(self):
        self.headers = {
            'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
        }
        self.Nums = []
        self.data = []

    def search(self, stockNums):
        try:
            self.Nums = stockNums.split(",")
            for stockNum in self.Nums:
                url = f'https://goodinfo.tw/tw/StockBzPerformance.asp?STOCK_ID={stockNum}'
                res = requests.get(url, headers=self.headers)
                # print(res)
                res.encoding = 'utf-8'
                soup = BeautifulSoup(res.text,'html.parser')
                txtFinDetailData = soup.find_all('table',class_='b1 p4_2 r10 box_shadow')

                for tr in txtFinDetailData:
                    stock_data = {}
                    # 股票名稱
                    title = tr.find('a').getText()
                    stock_data.update({'stock_name': title})

                    # 其他資料
                    rows = tr.find_all('tr')
                    odd_rows = []
                    even_rows = []

                    for i, row in enumerate(rows):
                        if i == 0:  # 如果是第一個迴圈迭代，跳過
                            continue
                        # 有些資料沒有使用空白進行分割，導致資料有問題!!!!
                        # text = row.getText().split(' ')
                        if i % 2 == 1:
                            row_data = [cell.text.strip() for cell in row.find_all(['th', 'td'])]
                            odd_rows.append(row_data)
                        else:
                            row_data = [cell.text.strip() for cell in row.find_all(['th', 'td'])]
                            even_rows.append(row_data)
                        # print(row.text)

                    for odd, even in zip(odd_rows, even_rows):
                        for i in range(len(odd)):
                            stock_data[even[i]] = odd[i]
                    
                    self.data.append(stock_data)

            with open('./output.json', 'w', encoding='UTF-8-sig') as f:
                    json.dump(self.data, f, ensure_ascii=False)

        except Exception as e:
            print(e)

if __name__ == "__main__":
    GoodInfo = GoodInfo()
    GoodInfo.search('2330,1101')