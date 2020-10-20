import requests
import re
import uuid
from bs4 import BeautifulSoup

url = "https://illustrain.com/?cat=%s"
# cat_dic = {'114':1, '174':5, '252':2, '99':2, '169':5, '95':17, '52':1, '192':5, '217':9, '75':2, '168':10, '190':3, '11':4, '167':18, '80':7, '150':1}
cat_dic = {'252':1}

for key, page in cat_dic.items():
    cat_urls = []
    cat_urls.append(url%key)
    if page>=1:
        for p in range(1, page):
            p = str(p+1)
            cat_urls.append(url%key + "&paged=%s"%p)

    for u in cat_urls:
        print(u)
        r = requests.get(u)
        soup = BeautifulSoup(r.content, 'lxml')
        img_links = soup.find_all('a', title=True, href=re.compile('^https://illustrain\.com/\?p='))
        print(len(img_links))

        for link in img_links:
            print(link['href'])
            r = requests.get(link['href'])
            soup = BeautifulSoup(r.text, 'lxml')
            img = soup.find('img',src=re.compile('http://illustrain\.com/img/work.+\.png'))
            if not img is None:
                print(img['src'])
                r = requests.get(img['src'])
                with open(str('./dataset/')+str(uuid.uuid4())+str('.png'),'wb') as file:
                    file.write(r.content)
