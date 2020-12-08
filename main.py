import utils
import get_news
import get_urls
from tqdm import tqdm

config = utils.readjson("config.json")

url_crawler = get_urls.Url_crawler(config)
news_crawler = get_news.News_crawler()

url_crawler.get_urls_recursively(depth=1)
url_crawler.save_urls()
'''
urls = utils.readtxt(config["url_save_path"], limits=None)
news = {
    "title": [],
    "text": []
}
for url in tqdm(urls):
    try:
        p = news_crawler.get_w_artical(url)
        news["title"].append(p[0])
        news["text"].append(p[1])
    except:
        pass
    try:
        p = news_crawler.get_l_artical(url)
        news["title"].append(p[0])
        news["text"].append(p[1])
    except:
        pass

for i in tqdm(range(len(news["title"]))):
    try:
        utils.save_news(news["title"][i], news["text"]
                        [i], config["news_save_path"])
    except:
        print("pass")
        pass
'''
print("done")
