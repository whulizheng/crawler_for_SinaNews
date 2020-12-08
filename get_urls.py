from selenium import webdriver
from tqdm import tqdm
import time
import re
import utils


class Url_crawler():
    def __init__(self, config):
        self.target_url = config["target_url"]
        self.target_url_s = config["target_url_s"]
        self.browser = webdriver.PhantomJS(config["phantomjs_path"])
        self.url_save_path = config["url_save_path"]
        self.news_link_list = []
        self.visited = []
        self.depth_count = 1
        self.block_list = [self.target_url]
        self.supported_news_features = config["supported_news_features"]
        self.data = time.strftime("%Y_%m_%d")

    def save_urls(self):
        sep = '\n'
        save_name = self.url_save_path + "urls_" + self.data
        fl = open(save_name, 'w')
        fl.write(sep.join(self.news_link_list))
        fl.close()
        print("爬取结果保存在："+save_name)

    def load_page(self, url=None, save_screenshot=0):
        self.visited.append(url)
        if url is None:
            self.browser.get(self.target_url)
            # 截图
            if save_screenshot:
                print("生成网页截图中...")
                title = str(self.browser.title)
                if not self.browser.save_screenshot('tmp\\img\\'+title+".png"):
                    print("io error，截图生成失败，请检查路径")
        else:
            self.browser.get(self.target_url)
            # 截图
            if save_screenshot:
                print("生成网页截图中...")
                if not self.browser.save_screenshot('tmp\\img\\index.png'):
                    print("io error，截图生成失败，请检查路径")

    def get_urls(self):
        self.load_page()
        source = self.browser.page_source
        linklist = re.findall(
            r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', source, re.I)  # 匹配所有的a节点
        for link in tqdm(linklist):
            if "video" in link or "photo" in link:
                continue  # 跳过图片视频板块或链接
            elif ".sina.com.cn" in link and link[-4:] == ".cn/":
                self.block_list.append(link)  # 疑似子模块链接
            else:
                for f in self.supported_news_features:
                    if f in link:  # 疑似新闻链接
                        self.news_link_list.append(link)
                        continue
        self.news_link_list = list(set(self.news_link_list))  # 去重
        self.block_list = list(set(self.block_list))  # 去重

        print("疑似新闻链接数 : %d" % len(self.news_link_list))  # 疑似新闻链接数
        print("疑似子模块链接数 : %d" % len(self.block_list))  # 疑似子模块链接数

    def get_urls_recursively(self, depth=2):
        if depth == 0:
            return
        else:
            print("开始第"+str(self.depth_count)+"层爬取")
            self.depth_count += 1
            tmp = self.block_list
            new_block_list = []
            for link in tqdm(tmp):
                self.load_page(url=link)
                source = self.browser.page_source
                linklist = re.findall(
                    r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', source, re.I)  # 匹配所有的a节点的http(s)链接
                for li in linklist:
                    if "video" in li or "photo" in li:
                        continue  # 跳过图片视频板块或链接
                    elif ".sina.com.cn" in li and li[-4:] == ".cn/":
                        if li in self.visited:
                            continue
                        else:
                            new_block_list.append(li)  # 疑似子模块链接
                    else:
                        for f in self.supported_news_features:
                            if f in li:  # 疑似新闻链接
                                self.news_link_list.append(li)
                                continue
                self.news_link_list = list(set(self.news_link_list))  # 去重
            self.block_list = list(set(new_block_list))  # 去重
            print("疑似新闻链接数 : %d" % len(self.news_link_list))  # 疑似新闻链接数
            print("疑似子模块链接数 : %d" % len(self.block_list))  # 疑似子模块链接数
            self.get_urls_recursively(depth=depth-1)


if __name__ == "__main__":
    config = utils.readjson("config.json")
    crawler = Url_crawler(config)
    crawler.get_urls_recursively(depth=1)
    crawler.save_urls()
    print("down")
