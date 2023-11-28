# BingSpyderDataSetCreater

## 1，简介


这是一个用来爬bing图片做分类数据集的简易爬虫  

可以自定义爬的图片的数量，以及爬的种类  
每次下载图片的time.sleep最好不要低于0.3，不然有被封IP的风险，可以把等待时间调小点，这样下的快   
另外引入了一个额外的库PIL，下载方式直接命令窗输入` pip install Pillow` 即可  

这份爬虫对下载的图片的宽长积存在一定限制，这样防止下载到奇奇怪怪的图标，来污染数据集  

想要自定义一些参量的话可以直接改default的值，也可以在命令窗输入  
`python main.py --你想要修改的参量1=你想要把它改成的值1 --你想要修改的参量2=你想要把它改成的值2`  

并运行  



## 2，headers寻找方法

1. 打开bing图片搜索并按F12发开开发者模式![](C:\Users\ASUS\AppData\Roaming\marktext\images\2023-11-28-23-21-32-image.png)

2. 点击网络，筛选Fetch/XHR![](C:\Users\ASUS\AppData\Roaming\marktext\images\2023-11-28-23-22-41-image.png)

3. 点击任意一个事件，查看它的标头，并向下翻至请求标头，其中`User-Agent：`即为所需的headers![](C:\Users\ASUS\AppData\Roaming\marktext\images\2023-11-28-23-27-03-image.png)
- Version: 1.0:
  
  这是一个用来爬bing图片做分类数据集的简易爬虫
  
  可以自定义爬的图片的数量，以及爬的种类

- Version: 1.1:

        添加了自动创建数据集的文件夹 在下载图片时随机抽取10张图片

        5张放进测试集，5张放入验证集，其余放入训练集

*Author: kkking  
Date: 23.11.28 
Version: 1.1  *

