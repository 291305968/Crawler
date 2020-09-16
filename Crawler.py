import requests
from bs4 import BeautifulSoup
import time
import json
import os


#获取详情页页码总数
def get_detail_pagenum(url) :
    try :
        r = requests.get(url, headers=headers)
        if r.status_code != 200 :
            if r.status_code == 429 :
                print("访问频繁，休眠10秒")
                time.sleep(10)
                r = requests.get(url, headers=headers)
            else :
                raise Exception("error")
        bs = BeautifulSoup(r.text, 'html.parser')
        pageNum: str =\
            bs.find("div", class_="pagenavi").find_all("span")[-2].get_text()
        print(f"网址：{url}，页码:{pageNum}")
        return pageNum
    except :
        print(f'下载该网页失败：{url}')


#获取指定链接和需下载页码总数的html
def download_htmls(weburl, maxtrynum) :
    htmls = []
    for page in range(maxtrynum) :
        try :
            url = f'{weburl}/{page + 1}'
            r = requests.get(url, headers=headers)
            if r.status_code != 200 :
                if r.status_code == 429 :
                    print("访问频繁，休眠10秒")
                    time.sleep(10)
                    r = requests.get(url, headers=headers)
                    htmls.append(r.text)
                    print(f"网址：{url}:状态码：{r.status_code}")
                    print(f'已下载网页：{page + 1}/{maxtrynum}')
                    continue
                else :
                    print(f'下载该网页失败：{url}，状态码:{r.status_code}')
                    raise Exception("error")
            print(f'已下载网页：{page + 1}/{maxtrynum}')
            htmls.append(r.text)
        except :
            if page < (maxtrynum - 1) :
                continue
            else :
                print("access failed!")
                break
    return htmls


#解析下载的html获取列表页图片下载链接、描述、时间和详情页链接
def parse_main_html(html) :
    soup = BeautifulSoup(html, 'html.parser')
    pic_list = soup.find(id="pins")
    lis = pic_list.find_all("li")
    pic_data = []
    for li in lis :
        detail_src = li.find("a")["href"]
        pic_src = li.find("img")["data-original"]
        pic_txt = li.find("img")["alt"]
        pic_time = li.find("span", class_="time").get_text()
        pic_data.append({"detail" : detail_src, "src" : pic_src, "txt" : pic_txt, "time" : pic_time})
    return pic_data


#解析获取详情页图片下载链接和描述
def parse_child_html(html) :
    soup = BeautifulSoup(html, 'html.parser')
    pic_src = soup.find("div", class_="main-image").find("img")["src"]
    pic_txt = soup.find("div", class_="main-image").find("img")["alt"]
    pic_url = {"src" : pic_src, "txt": pic_txt}
    return pic_url

# 提取数据
def disposal_data() :
    #提取主页图片链接和详情页网页链接
    for html in pic_main_htmls :
        pic_data = parse_main_html(html)
        pic_main_list.extend(pic_data)
        for detail_url in pic_main_list :
            detail_url_lists.append(detail_url["detail"])
    #提取详情页图片链接
    for detailUrl in detail_url_lists :
        pageNum = int(get_detail_pagenum(detailUrl))
        pic_detail_htmls = download_htmls(detailUrl, pageNum)
        for detailHtml in pic_detail_htmls :
            detail_download_url = parse_child_html(detailHtml)
            detail_download_lists.append(detail_download_url)


#将解析后的数据保存为json
def save_json() :
    json_path = r"D:\meiziwang"
    if not os.path.exists(json_path) :
        os.mkdir(json_path)
    with open(r"D:\meiziwang\mainPic.json", "w", encoding='utf-8') as mainPic :
        for data in pic_main_list :
            mainPic.write(json.dumps(data, ensure_ascii=False) + "\n")
    with open(r"D:\meiziwang\detailPic.json", "w", encoding='utf-8') as detailPic :
        for data in detail_download_lists :
            detailPic.write(json.dumps(data, ensure_ascii=False) + "\n")

if __name__ == "__main__":
    # 网站地址
    webUrl = r"https://www.mzitu.com/page"
    # 随机浏览器User-Agent
    my_headers = [
        'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 '
        'Safari/537.36',
        "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 "
        "Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:30.0) Gecko/20100101 Firefox/30.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 "
        "Safari/537.75.14",
        "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Win64; x64; Trident/6.0)",
        'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11',
        'Opera/9.25 (Windows NT 5.1; U; en)',
        'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
        'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu)',
        'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.0.12) Gecko/20070731 Ubuntu/dapper-security Firefox/1.5.0.12',
        'Lynx/2.8.5rel.1 libwww-FM/2.14 SSL-MM/1.4.1 GNUTLS/1.2.9',
        "Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.7 (KHTML, like Gecko) Ubuntu/11.04 Chromium/16.0.912.77 "
        "Chrome/16.0.912.77 Safari/535.7",
        "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:10.0) Gecko/20100101 Firefox/10.0 "
    ]
    # 请求头部，没有referer会影响访问网页和图片下载
    headers = {'referer': 'https://www.mzitu.com/', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) '
                                                                  'AppleWebKit/537.36 (KHTML, like Gecko) '
                                                                  'Chrome/69.0.3497.100 Safari/537.36'}
    # 主页下载列表页总数
    mainPageNum = 1
    # 下载列表页html
    pic_main_htmls = download_htmls(webUrl, mainPageNum)
    # 每个主页解析后图片数据列表
    pic_main_list = []
    # 详情页图片链接列表
    detail_url_lists = []
    # 详情页图片下载链接列表
    detail_download_lists = []

    disposal_data()
    save_json()
