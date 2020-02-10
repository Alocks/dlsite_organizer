import requests
import shutil
import os
from bs4 import BeautifulSoup

HEADER = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML,\
          like Gecko) Chrome/79.0.3945.130 Safari/537.36 OPR/66.0.3515.72'}
RJ_LIST = [i for i in os.listdir('.') if 'RJ' in i]
if not os.path.exists('output'):
    os.mkdir('output')


def parser(rj):
    x = rj.find('RJ')
    rj_code = rj[x:x+8]
    print(rj_code, rj)
    url = 'https://www.dlsite.com/maniax/work/=/product_id/' + rj_code + '.html'
    try:
        soup = BeautifulSoup(requests.get(url, headers=HEADER).text, "html.parser")
    except:
        print(rj_code + ' not found!')
    img_url = soup.find('meta', {'name': 'twitter:image:src'})['content'].strip()
    return {'title': soup.find('a', {'itemprop': 'url'}).text.strip(),
            'folder': rj,
            'circle': soup.find('span', {'class': 'maker_name'}).text.strip(),
            'rj': rj_code,
            'rg': soup.find('span', {'class': 'maker_name'}).find('a')['href'].split('/')[-1].split('.')[0],
            'img_file': requests.get(img_url, stream=True),
            'img_filename': img_url.split('/')[-1]}


def organizer(le_dictionary):
    for i in le_dictionary:
        circle_folder = '{}[{}]'.format(i['circle'], i['rg'])
        new_folder = '{}[{}]'.format(i['title'], i['rj'])
        with open(i['folder']+'/'+i['img_filename'], 'wb') as f:
            shutil.copyfileobj(i['img_file'].raw, f)
        os.rename(i['folder'], new_folder)
        if not os.path.exists('output/'+circle_folder):
            os.mkdir('output/' + circle_folder)
        shutil.move(new_folder, 'output/' + circle_folder)


metadata = [parser(rj) for rj in RJ_LIST]
organizer(metadata)
