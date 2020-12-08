import requests
from bs4 import BeautifulSoup


class News_crawler():
    def __init__(self):
        pass

    def get_w_artical(self, url):  # 获取方法1（适用于国际新闻）
        strhtml = requests.get(url)
        strhtml.encoding = 'utf-8'
        soup = BeautifulSoup(strhtml.text,
                             'html.parser'
                             )
        articles = soup.find('div', id='article').find_all('p')
        title = str(soup.title).replace("<title>", "").replace("</title>", "")
        full_artical = ""
        for artical in articles:
            full_artical += artical.get_text()
        return title, full_artical

    def get_l_artical(self, url):  # 获取方法2（适用于大部分国内新闻）
        strhtml = requests.get(url)
        strhtml.encoding = 'utf-8'
        soup = BeautifulSoup(strhtml.text,
                             'html.parser'
                             )
        title = str(soup.title).replace("<title>", "").replace("</title>", "")
        articles = soup.find('div', id='artibody').find_all('p')
        full_artical = ""
        for artical in articles:
            full_artical += artical.get_text()
        return title, full_artical


if __name__ == "__main__":
    Crawler = News_crawler()
    url = 'http://hb.sina.com.cn/news/w/2020-11-28/detail-iiznctke3717091.shtml'
    print(Crawler.get_l_artical(url))
