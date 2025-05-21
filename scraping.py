import requests
from bs4 import BeautifulSoup
import re
import json
import os

def foldering(urlinput):
    hasil = re.sub(r'[^\w\s-]', '_', urlinput) #hapus karakter aneh
    hasil = re.sub(r'\s+', '_', hasil) #ganti spasi dengan _
    return hasil


def dumy(url):
    response = requests.get(format(url))

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        
        body_content = soup.body
        judul = soup.title.get_text().split("|")

        if body_content:

            ####################################
            albums = body_content.find_all('div', "album-box grid_14")

            for album in albums:
                img_tag = album.find("img")
                img_src = img_tag['src']
                #print(img_src)

                h4_tag = album.find("h4")
                a_tag = h4_tag.find("a")

                #title_vocaloid = foldering(a_tag['href'])
                title_vocaloid = a_tag['href'].split("mikudb.moe/album/")
                title_vocaloid = title_vocaloid[1]
                print(title_vocaloid)


    else:
        print(f'Error: {response.status_code}')



def get_page(url, page):
    response = requests.get(format(url))

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        body_content = soup.body
        title = soup.title.get_text()

        print(f"[+] process: {title}")

        os.system(f"mkdir -p {page}")

        with open(f"{page}/index.html", "w") as file:
            file.write(response.text)


        if body_content:
            ####################################
            ####################################
            albums = body_content.find_all('div', "album-box grid_14")

            for album in albums:
                img_tag = album.find("img")
                img_src = img_tag['src']
                #print(img_src)

                h4_tag = album.find("h4")
                a_tag = h4_tag.find("a")

                #title_vocaloid = foldering(a_tag['href'])
                title_vocaloid = a_tag['href'].split("mikudb.moe/album/")
                title_vocaloid = title_vocaloid[1]
                #print(title_vocaloid)

                print(f"[.]   {title_vocaloid}")
                os.system(f"mkdir -p {page}/{title_vocaloid}")

                print("[.]       download img...")
                imgrespon = requests.get(img_src)
                with open(f"{page}/{title_vocaloid}/cover.jpg", "wb") as f:
                    f.write(imgrespon.content)

                print("[.]       download html album...")
                albumrespon = requests.get(a_tag['href'])
                with open(f"{page}/{title_vocaloid}/index.html", "w") as f:
                    f.write(albumrespon.text)


    else:
        print(f'Not found: {response.status_code}')



#dumy("https://mikudb.moe/type/vocaloid")
#exit()

for i in range(1, 400):
    with open(f"count", "w") as f:
        f.write(f"page_{i}")

    if i == 1:
        get_page(f"https://mikudb.moe/type/vocaloid", f"page_{i}")
    else:
        get_page(f"https://mikudb.moe/type/vocaloid/page/{i}/", f"page_{i}")

