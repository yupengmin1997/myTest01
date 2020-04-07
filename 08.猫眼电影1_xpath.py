from fake_useragent import UserAgent
import requests
from lxml import etree
import time

def get_html(url):
    '''
    :param url: 要爬取的地址
    :return: 返回html
    '''
    headers = {
        'User-Agent':UserAgent().chrome
    }
    res = requests.get(url,headers=headers)
    time.sleep(2)
    if res.status_code == 200:
        res.encoding = 'utf-8'
        return res.text
    else:
        return None

def parse_list(html):
    '''
    :param html: 传递进来一个有电影列表的html
    :return: 返回一个电影列表的url地址
    '''
    e = etree.HTML(html)
    list_url = ['http://maoyan.com{}'.format(url )for url in e.xpath('//div[@class="movie-item film-channel"]/a/@href')]
    return list_url


def parse_index(html):
    '''
    :param html: 传递一个电影信息的列表
    :return: 返回有个提取好的电影信息
    '''
    e = etree.HTML(html)
    name = e.xpath('//h1[@class="name"]/text()')
    type = e.xpath('//li[@class="ellipsis"][1]/a[1]/text()')
    actor_list = e.xpath('//ul[@class="celebrity-list clearfix"]/li[@class="celebrity actor"]/div[@class="info"]/a/text()')
    actors = format_data(actor_list)
    return {"name":name,"type":type,"actors":actors}

# 演员信息去重
def format_data(actor_list):
    actors_set = set()
    for actor in actor_list:
        actors_set.add(actor.strip())
    return actors_set


def main():
    for page in range(4):
        url = "https://maoyan.com/films?showType=2&offset={}".format(page*30)
        # 获得即将上映的电影页面
        list_html = get_html(url)
        # 获取一个页面
        list_url= parse_list(list_html)
        # 获取每部电影详情的url
        for url_page in list_url:
            info_html = get_html(url_page)
            movies = parse_index(info_html)
            # 打印每个电影的名字，类型，演员
            print(movies)

if __name__ == '__main__':
    main()