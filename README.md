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

1. 打开bing图片搜索并按F12发开开发者模式![image](https://github.com/kkking789/BingSpyderDataSetCreater/assets/140388891/73e1d741-b5a2-443d-985b-b909f54517bc)


2. 点击网络，筛选Fetch/XHR![image](https://github.com/kkking789/BingSpyderDataSetCreater/assets/140388891/b15ea2db-9c52-4db1-8024-1fe8209379d0)


3. 点击任意一个事件，查看它的标头，并向下翻至请求标头，其中`User-Agent：`即为所需的headers![image](https://github.com/kkking789/BingSpyderDataSetCreater/assets/140388891/2880c71d-d85a-4ddf-b757-bdbfd69c0422)

- Version: 1.0:
  
  这是一个用来爬bing图片做分类数据集的简易爬虫
  
  可以自定义爬的图片的数量，以及爬的种类

- Version: 1.1:

        添加了自动创建数据集的文件夹 在下载图片时随机抽取10张图片

        5张放进测试集，5张放入验证集，其余放入训练集

- Version: 1.2:

        添加了网络连接错误判断，防止在下载中途因网络问题而停止下载

        现在下载的图片均为原始图片，而非之前的缩略图

*Author: kkking789  
Date: 23.11.28 
Version: 1.1  *

*Author: kkking789  
Date: 24.1.29 
Version: 1.2  *
