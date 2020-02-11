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

csv_columns = ['은행', '카드명', '혜택', '분류']
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

food = ['커피', '스타벅스', '투썸플레이스', '폴바셋', '커피빈', '이디야', '카페베네', '치킨', '피자', '레스토랑', '아웃백',
        'VIPS', '차이나팩토리', '베이커리', '패스트푸드', '음식점', '주점', '뚜레쥬르', '파리바게트', '버거', '디저트',
        '배달의민족', '미스터도넛']
life = ['대중교통', '버스', '지하철', '택시', '철도', 'T-money', '티머니', '편의점', '병원', '병의원', '의원', '한의원',
        '약국', '마트', '렌탈', '자동이체', '보험', '조산원', '산후조리원', '웅진코웨이', '상조', '학원', '유치원', '유학원',
        '교육', '골프', '시장', '렌터카', '학자금', '토익', '텝스', 'YBM', '파고다', '해커스', '문고', '드러그스토어',
        '슈퍼마켓', 'GS25', '전화영어', '국제학생증']
shopping = ['백화점', '쇼핑', '마트', '포인트', '하이마트', '11번가', '홈쇼핑', '가맹점', '상품', 'YES24', '도서', '서점',
            '방송', '임대관리비', '온라인몰', '부가세', '뷰티스토어', '위메프', '아울렛', '올리브영', '옥션', 'G마켓', '의류']
oil = ['주유', '충전', '주유소', 'LPG충전소', '주차장', '통행료', '자동차', '유가보조금', '전기차']
tel = ['통신', '휴대폰', 'KT', 'SKT', 'LGU+', '알뜰폰', '휴대전화']
over = ['공항', '항공', '여행', '호텔', '해외', '국제선', '국내선', '숙박', '환전', '외환']
culture = ['영화관', 'CGV', '롯데시네마', '메가박스', '놀이공원', '미술관', '공연', '박물관', '문화', '레저', '뮤지컬', '연극']

for data in cards:
    data['분류'] = ''
    for i in food:
        if i in data.get('혜택'):
            data['분류'] += '1, '
            break
    for i in life:
        if i in data.get('혜택'):
            data['분류'] += '2, '
            break
    for i in shopping:
        if i in data.get('혜택'):
            data['분류'] += '3, '
            break
    for i in oil:
        if i in data.get('혜택'):
            data['분류'] += '4, '
            break
    for i in tel:
        if i in data.get('혜택'):
            data['분류'] += '5, '
            break
    for i in over:
        if i in data.get('혜택'):
            data['분류'] += '6, '
            break
    for i in culture:
        if i in data.get('혜택'):
            data['분류'] += '7, '
            break
    data['분류'] = data['분류'].strip()

csv_file = "woori_result.csv"
try:
    with open(csv_file, 'w', newline='', encoding='euc-kr') as f:
        writer = csv.DictWriter(f, fieldnames=csv_columns)
        writer.writeheader()
        for data in cards:
            writer.writerow(data)

except IOError:
    print('I/O err')


