#  -*- coding: utf-8 -*-
from __future__ import unicode_literals
import sys
reload(sys)
sys.setdefaultencoding('tis-620')

# import neccessary libraries
import requests
import pandas as pd
import bs4 as bs
import MySQLdb

# set pandas encoding to utf-8
pd.options.display.encoding = str('tis-620')
#pd.options.display.encoding = str('tis-620')
# set header to agent
from fake_useragent import UserAgent
ua = UserAgent()
urls = ["https://horoscope.thaiorc.com/lottery/stats/lotto-sunday.php?ay=2538",
        "https://horoscope.thaiorc.com/lottery/stats/lotto-monday.php?ay=2538",
        "https://horoscope.thaiorc.com/lottery/stats/lotto-tueday.php?ay=2538",
        "https://horoscope.thaiorc.com/lottery/stats/lotto-wednesday.php?ay=2538",
        "https://horoscope.thaiorc.com/lottery/stats/lotto-thursday.php?ay=2538",
        "https://horoscope.thaiorc.com/lottery/stats/lotto-friday.php?ay=2538",
        "https://horoscope.thaiorc.com/lottery/stats/lotto-saturday.php?ay=2538"]
day_names = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']

def convert(content):
    #print content
    result = ''
    for char in content:
        asciichar = char.encode('ascii',errors="backslashreplace")[2:]
        if asciichar =='':
            utf8char = char.encode('utf-8')
        else:
            try:
                hexchar =  asciichar.decode('hex')
            except:
                #print asciichar
                utf8char = ' '
            try:
                utf8char = hexchar.encode('utf-8')
            except:
                #print hexchar
                utf8char = ' '
            #print utf8char

        result = result + utf8char
        #print result
    return result

def main():
    df_lottery = list()
    for url, day_name in zip(urls, day_names):
        new_sess = requests.Session()
        new_sess.headers.update({'User-Agent': ua.random})
        req = new_sess.get(url)

        soup = bs.BeautifulSoup(req.text, 'html5lib')
        table = soup.find_all('td', {'class': 'brd_bottom'})
        #print(table[-1])
        trs = table[-1].find_all('tr')
        #print(tr)

        for (i, row) in enumerate(trs):
            if i > 1:
                tds = row.find_all('td')
                day = convert(tds[0].text.strip())
                try:
                    month = convert(tds[1].text.strip())
                except:
                    month = 'unknown'
                year = convert(tds[2].text.strip())
                print(day + " " + month + " " + year)

                first_price_front = tds[3].text.strip()
                first_price_behind = tds[4].text.strip()
                first_price = first_price_front + first_price_behind
                print(first_price)

                last_second_price = tds[5].text.strip()

                last_third_price = []
                last_third_price.append([tds[7].text.strip(), tds[8].text.strip(), tds[9].text.strip(), tds[10].text.strip()])
                print(last_third_price)

                df_lottery.append([day_name, day, month, year, first_price, last_second_price, last_third_price])

    column_name = ['day_name', 'day', 'month', 'year', 'first_price', 'last_second_price', 'last_third_price']

    df = pd.DataFrame(df_lottery, columns=column_name)
    print(df)
    df.to_csv("lottery.csv", encoding="tis-620")




if __name__ == '__main__':
    main()
