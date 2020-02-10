import requests
import shutil
import os
from urllib import parse
from bs4 import BeautifulSoup

HEADER = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML,\
          like Gecko) Chrome/79.0.3945.130 Safari/537.36 OPR/66.0.3515.72'}
RJ_LIST = [i for i in os.listdir('.') if 'RJ' in i]
if not os.path.exists('output'):
    os.mkdir('output')


def parser(rj):
    x = rj.find('RJ')
    rj_code = rj[x:x+8]
    print('{} {}'.format(rj_code, rj))
    url = 'https://www.dlsite.com/maniax/work/=/product_id/' + rj_code + '.html'
    try:
        soup = BeautifulSoup(requests.get(url, headers=HEADER).text, "html.parser")
    except:
        print(rj_code + ' not found!')
    try:
        img_url = soup.find('meta', {'name': 'twitter:image:src'})['content'].strip()
    except:
        print(rj_code + ' not found!')
        return None
    return {'title': soup.find('a', {'itemprop': 'url'}).text.strip(),
            'folder': rj,
            'circle': soup.find('span', {'class': 'maker_name'}).text.strip(),
            'rj': rj_code,
            'rg': soup.find('span', {'class': 'maker_name'}).find('a')['href'].split('/')[-1].split('.')[0],
            'img_file': requests.get(img_url, stream=True),
            'img_filename': img_url.split('/')[-1]}


def organizer(le_dictionary):
    for i in le_dictionary:
        if i is None:
            continue
        circle_folder = '{}[{}]'.format(i['circle'], i['rg'])
        new_folder = '{}[{}]'.format(i['title'], i['rj'])
        with open(i['folder']+'/'+i['img_filename'], 'wb') as f:
            shutil.copyfileobj(i['img_file'].raw, f)
        os.rename(i['folder'], new_folder.replace('?', '？'))
        if not os.path.exists('output/'+circle_folder):
            os.mkdir('output/' + circle_folder.replace('/', ' ' ))
        shutil.move(new_folder.replace('?', '？'), 'output/' + circle_folder)

def rj_code_finder():
    blacklist = ['RJ', 'rj', 'output', 'venv', '.py', '.mp4', '.exe', '.idea']
    folder_list = [i for i in os.listdir('.') if not any(j in i for j in blacklist)]
    count = 0
    done = 0
    for title in folder_list:
        count+=1
        counter = '[{}/{}]'.format(count,len(folder_list))
        original_title = title
        if '[' and ']' in title:
            title = [i.strip() for i in title.split(']') if '[' not in i]
            title = title[0].strip()
        if '(' and ')' in title:
            title = [i.strip() for i in title.split(')') if '(' not in i]
            title = title[0].strip()
        if 'ver' in title.lower():
                title = title.lower().split('ver')[0].strip()
        url = 'https://www.dlsite.com/maniax/fsr/=/language/jp/sex_category%5B0%5D/male/keyword/'+ \
               parse.quote(title) + \
               '/ana_flg/off/order%5B0%5D/trend/work_type%5B0%5D/MOV/work_type_name%5B0%5D/動画/'+ \
               'work_type_category%5B0%5D/game/work_type_category_name%5B0%5D/ゲーム'
        soup = BeautifulSoup(requests.get(url, headers=HEADER).text, 'html.parser')
        try:
            result = soup.find('td', {'class': 'page_total'}).findNext('strong')
        except:
            print(title + ' not found!' + counter)
            continue
        if int(result.text) <= 10:
            data = soup.findAll('div', {'class': 'multiline_truncate'})
            for i in data:
                choices = {'Y', 'N'}
                if '！' in title:
                    title = title.replace('！', '!')
                if i.text == title:
                    rj_code = i.find('a')['href'].split('/')[-1].split('.')[0]
                    print('Found {}'.format(i.text) + counter)
                    os.rename(original_title, '{}[{}]'.format(i.text, rj_code))
                    done+=1
                    break
                while True:
                    choice = input('Is this the right one?(Y/N):'+counter+'\nDLSITE:'+i.text+ '\nFOLDER:' +title+'\n')
                    if choice.upper() in choices :
                        break
                if 'Y' in choice.upper():
                    rj_code = i.find('a')['href'].split('/')[-1].split('.')[0]
                    os.rename(original_title, '{}[{}]'.format(i.text.replace('?', '？'), rj_code))
                    done+=1
                    break
                elif 'N' in choice.upper():
                    continue
    print('Found and renamed {} games!'.format(done))

rj_code_finder()
metadata = [parser(rj) for rj in RJ_LIST]
organizer(metadata)
