import requests
import json
import time
import os

#存放地址
download_path = r"D:\meiziwang"
#列表页json
main_json = r"D:\meiziwang\mainPic.json"
#详情页json
detail_json = r"D:\meiziwang\detailPic.json"


#ismain判断json是否为列表页json，如果是，下载图片以描述命名；如果否，下载图片以数字命名
def download(f_json, path, ismain) :
    if not os.path.exists(path) :
        os.mkdir(path)
    #图片下载存储子地址
    pic_addr = ""
    # 读取json生成相应文件夹和下载图片
    with open(f_json, 'r', encoding='utf-8') as f :
        #下载总量计数
        x = 1
        total_counts = 100
        #文件夹内下载图片计数
        counts = 1
        # 按行读取json数据
        line = f.readline()
        while line :
            pic_dic = json.loads(line)
            # 新建图片文件夹地址
            if pic_addr != f"{path}\{pic_dic['txt']}" :
                counts = 1
                pic_addr = f"{path}\{pic_dic['txt']}"
            # 判断文件夹是否存在，否就新建
            if not os.path.exists(pic_addr) :
                os.mkdir(pic_addr)
            #没有referer会导致下载失败
            headers = {
                'referer' : 'https://www.mzitu.com/177962/12',
                'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                               'Chrome/69.0.3497.100 Safari/537.36'}
            #获取图片数据并保存到电脑
            try :
                pic = requests.get(pic_dic["src"], headers=headers)
                # print(pic)
                if pic.status_code != 200 :
                    if pic.status_code == 429 :
                        print("访问频繁，休眠10秒")
                        time.sleep(10)
                        pic = requests.get(pic_dic["src"], headers=headers)
                    else :
                        raise Exception("error")
                if ismain :
                    pic_name = pic_addr
                else :
                    pic_name = counts
                #将数据写入电脑
                with open(f"{pic_addr}\{pic_name}.jpg", "wb") as img :
                    img.write(pic.content)
                    print("第", x, "张")
                    x += 1
                    counts += 1
                    #设置下载总张数
                if x > total_counts :
                    break
                line = f.readline()
            except :
                print(f'下载该图片失败：{pic_dic["src"]}')
                break


download(detail_json, download_path, 0)
