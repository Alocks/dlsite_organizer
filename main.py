import requests
import shutil
import os
from bs4 import BeautifulSoup

HEADER = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML,\
          like Gecko) Chrome/79.0.3945.130 Safari/537.36 OPR/66.0.3515.72'}
RJ_LIST = [i for i in os.listdir('.') if i.startswith('RJ')]
if not os.path.exists('output'):
    os.mkdir('output')

def parser(rj):
    url = 'https://www.dlsite.com/maniax/work/=/product_id/' + rj + '.html'
    response = requests.get(url, headers=HEADER)
    soup = BeautifulSoup(response.text, "html.parser")
    img_url = soup.find('meta', attrs={'name': 'twitter:image:src'})['content'].strip()
    return {'title': soup.find('a', {'itemprop': 'url'}).text.strip(),
            'folder': rj,
            'circle': soup.find('span', {'class': 'maker_name'}).text.strip(),
            'rg': soup.find('span', {'class': 'maker_name'}).find('a')['href'].split('/')[-1].split('.')[0],
            'img_file': requests.get(img_url, stream=True),
            'img_filename': img_url.split('/')[-1]}


def organizer(le_dictionary):
    for i in le_dictionary:
        circle_folder = '{}[{}]'.format(i['circle'], i['rg'])
        new_folder = '{}[{}]'.format(i['title'], i['folder'])
        with open(i['folder']+'/'+i['img_filename'], 'wb') as f:
            shutil.copyfileobj(i['img_file'].raw, f)
        os.rename(i['folder'], new_folder)
        if not os.path.exists(i['circle']):
            os.mkdir('output/' + circle_folder)
        shutil.move(new_folder, 'output/' + circle_folder)


metadata = [parser(rj) for rj in RJ_LIST]
organizer(metadata)
