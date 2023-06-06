import os  # 创建文件夹, 文件是否存在
import time,datetime # time 计时
import pickle  # 保存和读取cookie实现免登陆的一个工具
from time import sleep
from selenium import webdriver  # 操作浏览器的工具
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options# 手机模式



mobile_emulation = {
            "deviceName": "Apple iPhone 3GS",
            "deviceName": "Apple iPhone 4",
            "deviceName": "Apple iPhone 5",
            "deviceName": "Apple iPhone 6",
            "deviceName": "Apple iPhone 6 Plus",
            "deviceName": "BlackBerry Z10",
            "deviceName": "BlackBerry Z30",
            "deviceName": "Google Nexus 4",
            "deviceName": "Google Nexus 5",
            "deviceName": "Google Nexus S",
            "deviceName": "HTC Evo, Touch HD, Desire HD, Desire",
            "deviceName": "HTC One X, EVO LTE",
            "deviceName": "HTC Sensation, Evo 3D",
            "deviceName": "LG Optimus 2X, Optimus 3D, Optimus Black",
            "deviceName": "LG Optimus G",
            "deviceName": "LG Optimus LTE, Optimus 4X HD" ,
            "deviceName": "LG Optimus One",
            "deviceName": "Motorola Defy, Droid, Droid X, Milestone",
            "deviceName": "Motorola Droid 3, Droid 4, Droid Razr, Atrix 4G, Atrix 2",
            "deviceName": "Motorola Droid Razr HD",
            "deviceName": "Nokia C5, C6, C7, N97, N8, X7",
            "deviceName": "Nokia Lumia 7X0, Lumia 8XX, Lumia 900, N800, N810, N900",
            "deviceName": "Samsung Galaxy Note 3",
            "deviceName": "Samsung Galaxy Note II",
            "deviceName": "Samsung Galaxy Note",
            "deviceName": "Samsung Galaxy S III, Galaxy Nexus",
            "deviceName": "Samsung Galaxy S, S II, W",
            "deviceName": "Samsung Galaxy S4",
            "deviceName": "Sony Xperia S, Ion",
            "deviceName": "Sony Xperia Sola, U",
            "deviceName": "Sony Xperia Z, Z1",
            "deviceName": "Amazon Kindle Fire HDX 7″",
            "deviceName": "Amazon Kindle Fire HDX 8.9″",
            "deviceName": "Amazon Kindle Fire (First Generation)",
            "deviceName": "Apple iPad 1 / 2 / iPad Mini",
            "deviceName": "Apple iPad 3 / 4",
            "deviceName": "BlackBerry PlayBook",
            "deviceName": "Google Nexus 10",
            "deviceName": "Google Nexus 7 2",
            "deviceName": "Google Nexus 7",
            "deviceName": "Motorola Xoom, Xyboard",
            "deviceName": "Samsung Galaxy Tab 7.7, 8.9, 10.1",
            "deviceName": "Samsung Galaxy Tab",
            "deviceName": "Notebook with touch",
            "deviceName": "iPhone 6"
}

"""
一. 实现免登陆
二. 抢票并且下单
"""
# 大麦网主页
damai_url = 'https://www.damai.cn/'
# 登录
login_url = 'https://passport.damai.cn/login?ru=https%3A%2F%2Fwww.damai.cn%2F'
# 抢票目标页
target_url = 'https://m.damai.cn/damai/detail/item.html?itemId='+'720545258599'
#抢票的价位
price = "580"
#抢票的数量
personcount = "2"
#抢票的场次
shownumber = 1
#如果写0，说明不需要等待，需要等待抢票的可以写抢票时间，最好提前几秒钟
specified_time = '2023-06-06 21:12:00'

class Concert:
    # 初始化加载
    def __init__(self):
        self.status = 0  # 状态, 表示当前操作执行到了哪个步骤
        self.login_method = 1  # {0:模拟登录, 1:cookie登录}自行选择登录的方式
        option = webdriver.ChromeOptions()  # 默认Chrome浏览器
        # 关闭开发者模式, window.navigator.webdriver 控件检测到你是selenium进入，若关闭会导致出现滑块并无法进入。
        option.add_experimental_option('excludeSwitches', ['enable-automation'])
        option.add_argument('--disable-blink-features=AutomationControlled')
        # 设置手机型号，这设置为iPhone 6
        mobile_emulation = {"deviceName": "iPhone 6"}
        option.add_experimental_option("mobileEmulation", mobile_emulation)
        # 开发者模式
        option.add_argument("--auto-open-devtools-for-tabs")
        self.driver = webdriver.Chrome(executable_path='D:\Program Files\Google\Chrome\Application\chromedriver.exe',options=option)  # 当前浏览器驱动对象
        self.driver.maximize_window()





    """""""""""""""""""""""""""""""登录"""""""""""""""""""""""""""""""""""""""""""""""""
    # cookies: 登录网站时出现的 记录用户信息用的
    def set_cookies(self):
        """cookies: 登录网站时出现的 记录用户信息用的"""
        self.driver.get(damai_url)
        print('###请点击登录###')
        # 我没有点击登录,就会一直延时在首页, 不会进行跳转
        while self.driver.title.find('大麦网-全球演出赛事官方购票平台') != -1:
            sleep(1)
        print('###请扫码登录###')
        # 没有登录成功
        while self.driver.title != '大麦网-全球演出赛事官方购票平台-100%正品、先付先抢、在线选座！':
            sleep(1)
        print('###扫码成功###')
        # get_cookies: driver里面的方法
        pickle.dump(self.driver.get_cookies(), open('cookies.pkl', 'wb'))
        print('###cookie保存成功###')
        self.driver.get(target_url)

    # 假如说我现在本地有 cookies.pkl 那么 直接获取
    def get_cookie(self):
        """假如说我现在本地有 cookies.pkl 那么 直接获取"""
        cookies = pickle.load(open('cookies.pkl', 'rb'))
        for cookie in cookies:
            cookie_dict = {
                'domain': '.damai.cn',  # 必须要有的, 否则就是假登录
                'name': cookie.get('name'),
                'value': cookie.get('value')
            }
            self.driver.add_cookie(cookie_dict)
        print('###载入cookie###')

    def login(self):
        """登录"""
        if self.login_method == 0:
            self.driver.get(login_url)
            print('###开始登录###')
        elif self.login_method == 1:
            print(os.path)
            # 创建文件夹, 文件是否存在
            if not os.path.exists('cookies.pkl'):
                self.set_cookies()  # 没有文件的情况下, 登录一下
            else:
                self.driver.get(target_url)  # 跳转到抢票页
                self.get_cookie()  # 并且登录

    def enter_concert(self):
        """打开浏览器"""
        print('###打开浏览器,进入大麦网###')
        # 调用登录
        self.login()  # 先登录再说
        self.status = 2  # 登录成功标识
        print('###登录成功###')

    """""""""""""""""""""""""""""""登录"""""""""""""""""""""""""""""""""""""""""""""""""

    # 二. 抢票并且下单
    def choose_ticket(self):
        print('###开始进行日期及票价选择###')
        title = self.driver.title
        if title == '商品详情':
            # 选座购买的逻辑
            self.choice_seats()
        while True:
            # 如果标题为确认订单
            print('正在加载.......')
            # 如果当前购票人信息存在 就点击
            WebDriverWait(self.driver,20,0.1).until(EC.element_to_be_clickable((By().XPATH,'//*[@class="viewer"]/div/div')))
            bugperson = self.driver.find_elements(By().XPATH,'//*[@class="viewer"]/div/div')

            #滚轮将元素展示出来，否则会报找不到元素的错
            locationelement = self.driver.find_element(By().XPATH,'//*[@class="viewer"]/div/div')
            self.driver.execute_script("window.scrollTo(0, arguments[0].getBoundingClientRect().top);", locationelement)

            print(len(bugperson))
            for person in bugperson:
                person.click();
            
            # 下单操作
            self.check_order()
            break
    """""""""""""""""""""""""""""""选择座位"""""""""""""""""""""""""""""""""""""""""""""""""
    def choice_seats(self):
        #有几率出现报错页面
        if self.isElementExist('empty-page'):
            self.driver.find_element(By.CLASS_NAME, 'empty-page').find_element(By().CLASS_NAME,"btn").click();

        if specified_time!="0":
            time_tuple = time.strptime(specified_time, '%Y-%m-%d %H:%M:%S')
            specified_time_seconds = time.mktime(time_tuple)
            #获取当前时间
            now = time.strptime(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S')
            now_time =  time.mktime(now)
            while now_time<specified_time_seconds:
                now = time.strptime(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S')
                now_time =  time.mktime(now)
        #判断票是否开始售卖
        while self.isElementExist("count-down"):
            print("-----------即将开始抢票-------该元素可能会消失，未进行过测试-------------")

        #当有该元素时候再去点击立即购买WebDriverWait，driver：浏览器驱动，timeout：最长超时时间，默认以秒为单位，poll_frequency：检测的间隔步长，默认为0.5s
        #所以下面这个如果在0.1s找不到元素就会报错,另外里面不应该使用self.driver.find_element
        #WebDriverWait(self.driver, 0.1).until(EC.element_to_be_clickable(self.driver.find_element(By.CLASS_NAME, 'buy__button')))
        WebDriverWait(self.driver, 20,0.1).until(EC.element_to_be_clickable((By.CLASS_NAME, 'detail-button')))
        self.driver.find_element(By.CLASS_NAME, 'detail-button').click()

        #选场次
        WebDriverWait(self.driver,2,0.1).until(EC.element_to_be_clickable((By.CLASS_NAME, 'sku-times-card')))
        #获取所有场次
        showElements = self.driver.find_element(By.CLASS_NAME, 'sku-times-card').find_elements(By.CLASS_NAME,"item-content");
        i=0;
        for temp in showElements:
           i=i+1
           if(i==shownumber):
                temp.click();
                break

        #选票价
        WebDriverWait(self.driver,20,0.1).until(EC.element_to_be_clickable((By.CLASS_NAME, 'sku-tickets-card')))
        #直接滚动到底部,这块不知道怎么给滚动下来，直接设置全屏,
        #用另一种方式解决，使用手机模式打开浏览器
        # tempprocie = self.driver.find_element(By.XPATH, '//*[@class="bui-dm-sku-card-title"]')
        # self.driver.execute_script("arguments[0].scrollIntoView();", tempprocie) 
        #获取所有的票
        ticketElements = self.driver.find_element(By.CLASS_NAME, 'sku-tickets-card').find_elements(By.CLASS_NAME,"item-content");

        for temp in ticketElements:
            #判断票是否卖完
            outer = temp.find_elements(By().CLASS_NAME,"item-tag-outer");
            #获取价位
            tempprice = temp.find_element(By().CLASS_NAME,"item-text").text
            if len(outer)>0:
                continue;
            #如果有该价位的票直接选中
            elif tempprice.find(price)!=-1:
                temp.click();
        #遍历完成后如果没有选择数量的元素，说明没票了
        if self.isElementExist("number-tips"):
            ticketcount = self.driver.find_element(By.CLASS_NAME,"total").text
            while ticketcount.find(personcount)==-1:
                self.driver.find_element(By().CLASS_NAME,"plus-enable").click()
                ticketcount = self.driver.find_element(By.CLASS_NAME,"total").text
        else:
            print("没有票了-----------------")
        #点击确定按钮
        self.driver.find_element(By().CLASS_NAME,"sku-footer-buy-button").click()
        self.status=5;

    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""下单操作"""""""""""""""""""""""""""""""""""""""""""""""""""
    def check_order(self):
        if self.status in [3, 4, 5]:
            print('###开始确认订单###')
            temp = self.driver.find_element(By.XPATH, '//*[@id="dmOrderSubmitBlock_DmOrderSubmitBlock"]/div[@class="tpl-wrapper"]/div/div[2]/div[@view-name="FrameLayout"]')
            print("下单成功了-------------")
            #temp.click()

            sleep(200)

    def isElementExist(self, element):
        """判断元素是否存在"""
        flag = True
        browser = self.driver
        try:
            browser.find_element(By.CLASS_NAME, element)
            return flag
        except:
            flag = False
            return flag


if __name__ == '__main__':
    con = Concert()
    con.enter_concert()  # 打开浏览器
    con.choose_ticket()  # 选择座位
