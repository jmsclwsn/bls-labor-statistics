"""requests practice"""

import requests
import bs4
import csv


def make_soup():
    url = r'https://www.bls.gov/ooh/occupation-finder.htm?pay=&education=&' \
          r'training=&newjobs=&growth=&submit=GO'
    r = requests.get(url)
    r = r.text
    soup = bs4.BeautifulSoup(r, 'html.parser')
    return soup


def store_soup():
    soup = make_soup()
    with open('soupprac.html', 'w') as file:
        file.write(str(soup))


def reheat_soup():
    with open('soupprac.html', 'r') as file:
        soup = bs4.BeautifulSoup(file, 'html.parser')
    return soup


def get_headers():
    soup = reheat_soup()
    head = soup.thead
    head = head.text.replace(' ', '')
    head = head.strip('\n')
    head = head.split('\n')
    return head


def get_body():
    data = []
    soup = reheat_soup()
    body = soup.find('tbody')
    count = 0
    for item in body.findAll('td'):
        pitem = item.text
        item = pitem.lstrip()
        data.append(item)
    return data


def combine_body_head():
    with open('blsjoboutlook4.2019.csv', 'w') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', lineterminator='\n')
        headers = get_headers()
        body = get_body()
        writer.writerow(headers)
        start = 0
        end = 6
        while end <= len(body):
            writer.writerow(body[start:end])
            start = end
            end += 6
    print('Done!')


combine_body_head()
body = get_body()


#decision: write header, write body directly under header cells, counted
#

#why write binary when using csv? seen in a few threads SO
#answer: to avoid non-ascii characters from being modified or removed
# same in python 3?
#try dictwriter next
#write files in binary mode