from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup as bs
import csv


path = 'C:\workspace\python\webdriver\chromedriver.exe'
driver = webdriver.Chrome(path)

#vvip-프리미엄-할인형-포인트형-혜택별(7)-체크(5)
cardCategory = ['https://sccd.wooribank.com/ccd/Dream?withyou=CDCIF0147',
                'https://sccd.wooribank.com/ccd/Dream?withyou=CDCIF0022',
                'https://sccd.wooribank.com/ccd/Dream?withyou=CDCIF0148',
                'https://sccd.wooribank.com/ccd/Dream?withyou=CDCIF0149',
                'https://sccd.wooribank.com/ccd/Dream?withyou=CDCIF0021',
                'https://sccd.wooribank.com/ccd/Dream?withyou=CDCIF0021&CTGR_CD=C200015',
                'https://sccd.wooribank.com/ccd/Dream?withyou=CDCIF0021&CTGR_CD=C200010',
                'https://sccd.wooribank.com/ccd/Dream?withyou=CDCIF0021&CTGR_CD=C200014',
                'https://sccd.wooribank.com/ccd/Dream?withyou=CDCIF0021&CTGR_CD=C200013',
                'https://sccd.wooribank.com/ccd/Dream?withyou=CDCIF0021&CTGR_CD=C200034',
                'https://sccd.wooribank.com/ccd/Dream?withyou=CDCIF0021&CTGR_CD=C200018',
                'https://sccd.wooribank.com/ccd/Dream?withyou=CDCIF0023',
                'https://sccd.wooribank.com/ccd/Dream?withyou=CDCIF0023&CTGR_CD=C200033',
                'https://sccd.wooribank.com/ccd/Dream?withyou=CDCIF0023&CTGR_CD=C200007',
                'https://sccd.wooribank.com/ccd/Dream?withyou=CDCIF0023&CTGR_CD=C200008',
                'https://sccd.wooribank.com/ccd/Dream?withyou=CDCIF0023&CTGR_CD=C200023']

csv_columns = ['은행', '카드명', '혜택']
cards = []

for i in range(0, len(cardCategory)):
    driver.get(cardCategory[i])
    html = driver.page_source
    soup = bs(html, 'html.parser')
    n = soup.find('p', {'class': 'p-card-notice'})
    if n:
        if i in range(4, 11):
            cnt = int(''.join(filter(str.isdigit, n.find_all('em')[1].text)))
        else:
            cards.append({'은행': '우리은행', '카드명': soup.find('h3', {'class': 'title-cd'}).text.strip(),
                         '혜택': soup.find('div', {'class': 'list-cd'}).text.strip().replace('\n\n\n', ', ')})
            cnt = int(''.join(filter(str.isdigit, n.find_all('em')[0].text)))
        if cnt % 10 > 0:
            cnt = cnt // 10 + 1
        else:
            cnt = cnt // 10
        for j in range(cnt):
            for name, bf in zip(soup.select('div.card-text > dl > dt > a'),
                                soup.find_all('div', {'class': 'grid-col2'})):
                cards.append({'은행': '우리은행', '카드명': name.text.strip(), '혜택': bf.text.strip().replace('\n\n\n', ', ')})
            if (j+1) == cnt:
                break
            nextPage = driver.find_element_by_xpath('//a[@class = "direction next"]')
            nextPage.send_keys('\n')
            html = driver.page_source
            soup = bs(html, 'html.parser')
    else:
        if i == 1: #프리미엄카드만 다름
            for name, bf in zip(soup.find_all('p', {'class': 'list-cd-name'}),
                                soup.find_all('ul', {'class': 'cd-txt w470'})):
                cards.append({'은행': '우리은행', '카드명': name.text.strip(), '혜택': bf.text.strip().replace('\n\n\n', ', ')})
        else:
            for name, bf in zip(soup.find_all('h3', {'class': 'title-cd'}),
                                soup.find_all('div', {'class': 'list-cd'})):
                cards.append({'은행': '우리은행', '카드명': name.text.strip(), '혜택': bf.text.strip().replace('\n\n\n', ', ')})

csv_file = "woori_result.csv"
try:
    with open(csv_file, 'w', newline='', encoding='euc-kr') as f:
        writer = csv.DictWriter(f, fieldnames=csv_columns)
        writer.writeheader()
        for data in cards:
            writer.writerow(data)
except IOError:
    print('I/O err')
