"""
这是一个用来爬bing图片做分类数据集的简易爬虫

可以自定义爬的图片的数量，以及爬的种类
每次下载图片的time.sleep最好不要低于0.3，不然有被封IP的风险，可以把等待时间调小点，这样下的快
headers最好改成自己的，现在这份代码里的是我的headers，这玩意可以在浏览器的开发者模式下找到，具体从网上查怎么找
另外引入了一个额外的库PIL，下载方式直接命令窗输入 pip install Pillow 即可

这份爬虫对下载的图片的宽长积存在一定限制，这样防止下载到奇奇怪怪的图标，来污染数据集

想要自定义一些参量的话可以直接改default的值，也可以在命令窗输入
python main.py --你想要修改的参量1=你想要把它改成的值1 --你想要修改的参量2=你想要把它改成的值2
并运行

另外，为什么整个世界上有FPGA这么恶心的东西啊，服了

Author: kkking
Date: 23.11.27
Version: 1.0

Author: kkking
Date: 24.1.30
Version: 1.2

"""
import PIL
import requests
import re
import os
import time
import argparse
import random

import urllib3
from PIL import Image
from urllib import parse
from urllib.parse import unquote
from requests.adapters import HTTPAdapter



def print_progress_bar(current_value, total_value, bar_length=50):
    progress = int(bar_length * current_value / total_value)
    bar = "[" + "#" * progress + " " * (bar_length - progress) + "]"
    percentage = int(current_value * 100 / total_value)
    print(f"\r{bar} {percentage}%", end=" ", flush=True)
    print(f"{current_value}/{total_value}", end="\n")


class SpiderClass:
    def __init__(self, opt):
        self.search = opt.search
        self.headers = {'User-Agent': opt.headers}
        self.savePath = opt.savePath
        self.urlEmpty = opt.url
        self.getNum = opt.getNum
        self.outputDir = opt.savePath + opt.search
        self.trainDir = None
        self.testDir = None
        self.validDir = None
        self.urlSearch = None
        self.html = None

    def find_src_strings(self):  # 获取返回的图片的src
        pattern = re.compile(r'mediaurl=(.*?)&amp;exph=')
        matches = re.findall(pattern, self.html)
        matches = matches[::3]
        return matches

    def get_img_link(self):  # 获取网页的feedback的图片的链接
        searchName_parse = parse.quote(self.search)
        self.urlSearch = self.urlEmpty.format(searchName_parse)
        s = requests.session()
        s.keep_alive = False
        s.mount('http://', HTTPAdapter(max_retries=3))
        s.mount('https://', HTTPAdapter(max_retries=3))
        try:
            strhtml = s.get(self.urlSearch, headers=self.headers, timeout=10)
        except requests.exceptions.ConnectionError:
            return None
        except requests.exceptions.ChunkedEncodingError:
            return None
            print("网络错误")
        self.html = strhtml.text
        img_link = self.find_src_strings()
        return img_link

    def make_output_dir(self):  # 设置输出文件
        self.trainDir = self.savePath+'dataset/train/'+self.search
        self.validDir = self.savePath+'dataset/valid/'+self.search
        self.testDir = self.savePath+'dataset/test/'+self.search

        if not os.path.exists(self.trainDir):
            os.makedirs(self.trainDir)
        if not os.path.exists(self.validDir):
            os.makedirs(self.validDir)
        if not os.path.exists(self.testDir):
            os.makedirs(self.testDir)

    def get_img(self, img_links, num):  # 获取一组图片
        cnt = 0
        random_numbers = random.sample(range(1,31), 10)
        test_numbers = random_numbers[0:4]
        valid_numbers = random_numbers[5:9]
        for img_link in img_links:
            img_link = unquote(img_link)
            s = requests.session()
            s.keep_alive = False
            s.mount('http://', HTTPAdapter(max_retries=3))
            s.mount('https://', HTTPAdapter(max_retries=3))
            try:
                res = s.get(img_link, headers=self.headers, timeout=10)
            except requests.exceptions.ConnectionError :
                print("连接错误")
                return
            except requests.exceptions.ChunkedEncodingError:
                print("网络错误")
                return
            if res.status_code == 404:
                print(f"图片{img_link}下载出错")
            else:
                cnt += 1
                if cnt in test_numbers:
                    filename = f"{self.testDir}/{self.search}_{num}_{cnt}.jpg"
                elif cnt in valid_numbers:
                    filename = f"{self.validDir}/{self.search}_{num}_{cnt}.jpg"
                else:
                    filename = f"{self.trainDir}/{self.search}_{num}_{cnt}.jpg"
                with open(filename, "wb") as f:
                    f.write(res.content)
                    f.close()
                    try:
                        img = Image.open(filename)
                        width, height = img.size
                        img.close()
                        if width * height < 2500:  # 宽高积低于2500则视为垃圾图片，将其删去
                            print("图片长宽积过低，已删去")
                            os.remove(filename)
                    except PIL.UnidentifiedImageError as e:
                        print("图片异常，已删去")
                        os.remove(filename)
                    print_progress_bar((num - 1) * 30 + cnt, self.getNum * 30)
                    time.sleep(0.4)  # 每次休眠一段时间，防止封IP
                if cnt == 30:
                    return
            res.close()

def url_change(url, cnt):
    index = url.find("first=")
    start_str = "first=" + str(cnt*30)
    return url[:index]+start_str+url[len("first=" + str(cnt-1))+index:]


def parse_opt():
    parser = argparse.ArgumentParser()
    parser.add_argument('--search', type=str, default='water')
    parser.add_argument('--headers', type=str, default='')
    parser.add_argument('--savePath', type=str, default='./')
    parser.add_argument('--url', type=str, default='https://cn.bing.com/images/async?q={'
                                                   '}&first=5&count=29&cw=1280&ch=780&relp=32&apc=0&datsrc=I&layout'
                                                   '=RowBased_Landscape&mmasync=1&dgState=x*0_y*0_h*0_c*4_i*126_r*31'
                                                   '&IG=FA7FC853DC934344BA0C794E0E318FAB&SFX=5&iid=images.5571')
    parser.add_argument('--getNum', type=int, default=4)
    return parser.parse_known_args()[0]


def main(opt):
    Spider = SpiderClass(opt)
    Spider.make_output_dir()
    for currentNum in range(1, opt.getNum + 1):
        Spider.urlEmpty = url_change(Spider.urlEmpty, currentNum)
        img_links = Spider.get_img_link()
        Spider.get_img(img_links, currentNum)
    print("批量图片下载完成")


if __name__ == '__main__':
    opt = parse_opt()
    main(opt)
