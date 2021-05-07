from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
import os
import argparse
import sys
import pandas as pd


def get_soup(url, header):
    return BeautifulSoup(urlopen(Request(url, headers=header)), 'html.parser')


def main(query, max_images, save_directory, save_name):
    query = query.split()
    query = '+'.join(query)
    url = "https://www.google.com/search?q=" + query + "&source=lnms&tbm=isch"
    header = {
        'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"}
    soup = get_soup(url, header)
    ActualImages = []  # contains the link for Large original images, type of  image
    for a in soup.find_all("div", {"class": "svla5d"}):
        link = a.find_all('img')[0].attrs['src']
        ActualImages.append(link)
    for i, img in enumerate(ActualImages[0:max_images]):
        try:
            req = Request(img, headers=header)
            raw_img = urlopen(req)
            file_type = ""
            try:
                file_type = raw_img.headers['Content-Type'].split(';')[0].lower().split('/')[1]
            except Exception as e:
                pass
            if len(file_type) == 0:
                f = open(os.path.join(save_directory, save_name + ".jpg"), 'wb')
            else:
                f = open(os.path.join(save_directory, save_name + "." + file_type), 'wb')
            f.write(raw_img.read())
            f.close()
        except Exception as e:
            print("could not load : " + img)
            print(e)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Scrape Google images')
    parser.add_argument('-d', '--directory', default='/home/user/Downloads/', type=str, help='save directory')
    parser.add_argument('-f', '--file', default='./file_to_download.csv', type=str, help='file to read')
    parser.add_argument('-n', '--maxnum', default=3, type=int, help='number of file to download')
    argv = parser.parse_args()

    save_directory = argv.directory
    file = argv.file
    n = argv.maxnum
    df = pd.read_csv(file)
    print(f"num of rows ==>  {len(df)}")
    for index, row in df.iterrows():
        name_to_save = row['name']
        query = row['query']
        try:
            main(query, n, save_directory, name_to_save)
        except KeyboardInterrupt:
            pass
        print(f"row {index + 1} from {len(df)} is complete")

    sys.exit()
