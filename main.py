
import sys
import threading

from PyQt5.QtCore import QDateTime, QTimer
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from PyQt5.QtWidgets import QApplication, QMainWindow, QDesktopWidget, QMessageBox
from selenium.webdriver.common.by import By

import my_ui.SeckillUi
from settime import SetTime
import qrainbowstyle



class MainDialog(QMainWindow):
    stop_thread = threading.Event()

    def __init__(self, parent=None):
        super(QMainWindow, self).__init__(parent)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.showTime)
        self.waitflag = 0  # 用于标记是否在等待
        self.buylater = SetTime()
        #self.setStyleSheet(qrainbowstyle.load_stylesheet(style="DarkOrange"))
        self.screen = QDesktopWidget().screenGeometry()
        #size = self.geometry()
        #self.move((self.screen.width() - size.width() - 80), (self.screen.height() - size.height()) / 2)
        option = webdriver.ChromeOptions()
        option.add_experimental_option('excludeSwitches', ['enable-automation'])  # 这里去掉window.navigator.webdriver的特性
        option.add_argument("--disable-blink-features=AutomationControlled")
        self.browser = webdriver.Chrome(options = option)
        #self.browser = webdriver.Chrome()
        self.browser.set_window_size(self.screen.width() / 2, self.screen.height())
        print(sys.path[0])
        #self.manual = "file:///" + sys.path[0] + "/manual/index.html"
        #self.about = "file:///" + sys.path[0] + "/manual/about.html"
        #self.browser.get(self.manual)
        self.ui = my_ui.SeckillUi.SeckillUi()
        self.ui.setupUi(self)
        self.ui.btn_now.clicked.connect(self.buy_it_now)
        self.ui.choose_tao.setChecked(False)
        self.ui.choose_jing.setChecked(False)
        self.ui.choose_tao.clicked.connect(self.toTB)
        self.ui.choose_jing.clicked.connect(self.toJD)
        self.ui.btn_later.clicked.connect(self.gotolater)
        self.ui.help.clicked.connect(self.toHelp)
        self.ui.about.clicked.connect(self.toAbout)
        self.ui.btn_mode.clicked.connect(self.setmode)
        self.ui.btn_quit.setDisabled(True)
        self.ui.textBrowser.setText("准备抢单...")

    def toJD(self):
        if self.ui.choose_jing.isChecked():
            self.ui.choose_tao.setChecked(False)
        else:
            self.ui.choose_tao.setChecked(True)

    def toTB(self):
        if self.ui.choose_tao.isChecked():
            self.ui.choose_jing.setChecked(False)
        else:
            self.ui.choose_jing.setChecked(True)

    def quick_buy2tao(self):
        try:
            self.browser.get("https://www.taobao.com/")
        except:
            self.browser = webdriver.Chrome()
            self.browser.set_window_size(self.screen.width() / 2, self.screen.height())
            self.ui.textBrowser.append("请勿关闭浏览器！抢单失败！")
            return -1
        goods_url = self.ui.lineEdit.text()
        text = self.browser.find_element(By.XPATH, "//*[@id='J_SiteNavLogin']/div[1]/div/a").text
        noLogin = True
        if "亲，请登录" != text:
            noLogin = False
        try:
            text = self.browser.find_element(By.XPATH, "//*[@id='J_SiteNavLogin']/div[1]/div/a").text
            if noLogin:
                loc = (By.LINK_TEXT, "亲，请登录")
                WebDriverWait(self.browser, 30, 10).until(EC.visibility_of_element_located(loc))
                self.browser.find_element(By.LINK_TEXT, "亲，请登录").click()

        except:
            self.ui.textBrowser.append("登录失败！")
            return -1

        try:
            if noLogin:
                # 二维码登录
                loc = (By.XPATH, "//*[@id='login']/div[1]/i")
                WebDriverWait(self.browser, 30, 0.5).until(EC.visibility_of_element_located(loc))
                self.browser.find_element(By.XPATH, "//*[@id='login']/div[1]/i").click()  # 淘宝切换二维码登录按钮
                self.ui.textBrowser.append("请使用手机淘宝扫码登录")
                self.ui.textBrowser.moveCursor(self.ui.textBrowser.textCursor().End)
                WebDriverWait(self.browser, 30, 0.5).until_not(EC.visibility_of_element_located(loc))

                # 短信登录
                # loc = (By.XPATH, "//*[@id='login']/div[2]/div/div[1]/a[2]")
                # WebDriverWait(self.browser, 30, 0.5).until(EC.visibility_of_element_located(loc))
                # self.browser.find_element(By.XPATH, "//*[@id='login']/div[2]/div/div[1]/a[2]").click()  # 淘宝切换短信登录按钮
                # self.ui.textBrowser.append("请使用手机验证码登录")
                # self.ui.textBrowser.moveCursor(self.ui.textBrowser.textCursor().End)
                #
                #
                # #手机号
                # loc = (By.XPATH,"//*[@id='fm-sms-login-id']")
                # WebDriverWait(self.browser, 30, 0.5).until(EC.visibility_of_element_located(loc))
                # phone = "15989306469"
                # self.browser.find_element(By.XPATH, "//*[@id='fm-sms-login-id']").send_keys(phone)
                #
                # #判断滑块是否存在
                # try:
                #     # 找到滑块
                #     slider = self.browser.find_element(By.XPATH,"//span[contains(@class, 'btn_slide')]")
                #     loc = (By.XPATH, "//span[contains(@class, 'btn_slide')]")
                #     # 判断滑块是否可见
                #     if slider.is_displayed():
                #         ActionChains(self.browser)
                #         # 点击并且不松开鼠标
                #         ActionChains(self.browser).click_and_hold(on_element=slider).perform()
                #         # 往右边移动258个位置
                #         ActionChains(self.browser).move_by_offset(xoffset=258, yoffset=0).perform()
                #         # 松开鼠标
                #         ActionChains(self.browser).pause(0.5).release().perform()
                # except:
                #     pass
                # # button = WebDriverWait(self.browser, timeout=30).until(
                # #     EC.presence_of_element_located((By.CLASS_NAME, 'password-login')))
                # # button.click()
                #
                # #获取验证码
                # loc = (By.XPATH, "//*[@id='login-form']/div[2]/div[3]/a")
                # WebDriverWait(self.browser, 30, 0.5).until(EC.visibility_of_element_located(loc))
                # self.browser.find_element(By.XPATH, "//*[@id='login-form']/div[2]/div[3]/a").click()
                # WebDriverWait(self.browser, 30, 0.5).until_not(EC.visibility_of_element_located(loc))


        except:
            self.ui.textBrowser.append("等待扫码时间过长，登陆失败！")
            return -1

        try:
            self.browser.get(goods_url)
            self.ui.textBrowser.append("进入商品页面")
            self.ui.textBrowser.moveCursor(self.ui.textBrowser.textCursor().End)
        except:
            self.ui.textBrowser.append("进入商品页面失败，请检查链接能否正常访问")
            return -1

        # try:
        #     # 鞋码
        #     size = "43"
        #     loc = (By.XPATH, "//span[text()='" + size + "']")
        #     WebDriverWait(self.browser, 30, 0.5).until(EC.visibility_of_element_located(loc))
        #     self.browser.find_element(By.XPATH, "//span[text()='" + size + "']").click()
        #
        #     # 颜色分类
        #     type = "水蓝色/荧光粉绿"
        #     loc = (By.XPATH, "//span[text()='" + type + "']")
        #     WebDriverWait(self.browser, 30, 0.5).until(EC.visibility_of_element_located(loc))
        #     self.browser.find_element(By.XPATH, "//span[text()='" + type + "']").click()
        # except Exception as err:
        #     self.ui.textBrowser.append("选择鞋码和颜色分类失败，请尝试手动选择")

        # 点击购买按钮
        while True:
            try:
                self.ui.textBrowser.append("请选择商品详情，等待开抢...")
                #loc = (By.XPATH, "//*[@id=\"J_juValid\"]/div[1]/a")
                loc = (By.LINK_TEXT, '立即购买')
                WebDriverWait(self.browser, 30, 0.01).until(EC.visibility_of_element_located(loc))
                self.browser.find_element(By.LINK_TEXT, '立即购买').click()
                break
            except:
                self.ui.textBrowser.append("正在等待开抢/抢购中...")
                self.ui.textBrowser.moveCursor(self.ui.textBrowser.textCursor().End)

        # 点击提交订单按钮
        while True:
            try:
                self.ui.textBrowser.append("提交订单中...")
                loc = (By.LINK_TEXT, '提交订单')
                WebDriverWait(self.browser, 30, 0.01).until(EC.visibility_of_element_located(loc))
                self.browser.find_element(By.LINK_TEXT, '提交订单').click()
                self.ui.textBrowser.append("抢购成功，请及时付款")
                self.ui.textBrowser.moveCursor(self.ui.textBrowser.textCursor().End)
                break
            except:
                self.ui.textBrowser.append("再次尝试抢单...")
                self.ui.textBrowser.moveCursor(self.ui.textBrowser.textCursor().End)

    def quick_buy2jing(self):
        goods_url = self.ui.lineEdit.text()
        # 打开Chrome浏览器
        try:
            self.browser.get("https://www.jd.com/")
        except:
            self.browser = webdriver.Chrome()
            self.browser.set_window_size(self.screen.width() / 2, self.screen.height())
            self.ui.textBrowser.append("请勿关闭浏览器！抢单失败！")
            return -1
        try:
            loc = (By.LINK_TEXT, "你好，请登录")
            WebDriverWait(self.browser, 30, 0.5).until(EC.visibility_of_element_located(loc))
            self.browser.find_element(By.LINK_TEXT, "你好，请登录").click()
        except:
            self.ui.textBrowser.append("登录失败！")
            return -1
        try:
            loc = (By.XPATH, "//*[@id=\"content\"]/div[2]/div[1]/div/div[2]/a")
            self.ui.textBrowser.append("请使用手机京东客户端扫码登录")
            self.ui.textBrowser.moveCursor(self.ui.textBrowser.textCursor().End)
            WebDriverWait(self.browser, 30, 0.5).until_not(EC.visibility_of_element_located(loc))
        except:
            self.ui.textBrowser.append("等待扫码时间过长，登陆失败！")
            return -1
        try:
            self.browser.get(goods_url)
            self.ui.textBrowser.append("进入商品页面")
            self.ui.textBrowser.moveCursor(self.ui.textBrowser.textCursor().End)
        except:
            self.ui.textBrowser.append("进入商品页面失败，请检查链接能否正常访问")
            return -1
        # 点击提交订单按钮

        try:
            loc = (By.ID, 'InitCartUrl')
            WebDriverWait(self.browser, 30, 0.01).until(EC.visibility_of_element_located(loc))
            self.browser.find_element(By.ID, 'InitCartUrl').click()
        except:
            self.ui.textBrowser.append("尝试抢单中...")
            self.ui.textBrowser.moveCursor(self.ui.textBrowser.textCursor().End)

        try:
            loc = (By.ID, 'GotoShoppingCart')
            WebDriverWait(self.browser, 30, 0.01).until(EC.visibility_of_element_located(loc))
            self.browser.find_element(By.ID, 'GotoShoppingCart').click()
        except:
            self.ui.textBrowser.append("进入购物车失败，请检查登录状态")
            return -1
        try:
            loc = (By.CSS_SELECTOR, '.common-submit-btn > b')
            WebDriverWait(self.browser, 30, 0.01).until(EC.visibility_of_element_located(loc))
            self.browser.find_element(By.CSS_SELECTOR, '.common-submit-btn > b').click()
            loc = (By.CSS_SELECTOR, '#order-submit > b')
        except:
            self.ui.textBrowser.append("提交订单失败")
            return -1

        try:
            WebDriverWait(self.browser, 30, 0.01).until(EC.visibility_of_element_located(loc))
            self.browser.find_element(By.CSS_SELECTOR, '#order-submit > b').click()
            self.ui.textBrowser.append("抢购成功，请及时付款")
            self.ui.textBrowser.moveCursor(self.ui.textBrowser.textCursor().End)
            return 0
        except:
            self.ui.textBrowser.append("抢单失败...")
            return -1

    def gotolater(self):
        self.buylater.show()
        result = self.buylater.exec_()
        if result:
            self.waitflag = 1
            self.ui.btn_quit.setText("取消抢单")
            self.ui.btn_quit.clicked.connect(self.cancel)
            self.ui.btn_quit.setDisabled(False)
            self.timer.start(1000)
        else:
            self.ui.textBrowser.setText("准备抢单...")

    def buy_it_now(self):
        self.ui.textBrowser.moveCursor(self.ui.textBrowser.textCursor().End)
        if self.ui.choose_tao.isChecked():
            self.ui.textBrowser.setText("开始淘宝抢单...")
            self.ui.btn_now.setDisabled(True)
            sniffer_thread = threading.Thread(target=self.quick_buy2tao)
            #sniffer_thread.setDaemon(True)
            sniffer_thread.daemon = True
            sniffer_thread.start()
        elif self.ui.choose_jing.isChecked():
            self.ui.textBrowser.setText("开始京东抢单...")
            self.ui.btn_now.setDisabled(True)
            sniffer_thread = threading.Thread(target=self.quick_buy2jing)
            sniffer_thread.setDaemon(True)
            sniffer_thread.start()
        else:
            self.ui.textBrowser.append("请选择抢单平台")
            self.ui.textBrowser.moveCursor(self.ui.textBrowser.textCursor().End)
            return
        self.ui.btn_quit.setDisabled(False)
        self.ui.btn_quit.clicked.connect(self.quit)

    def quit(self):
        try:
            self.browser.get(self.manual)
        except:
            self.browser = webdriver.Chrome()
            #self.browser.get(self.manual)
        self.ui.textBrowser.setText("抢单已终止！\n请重新选择抢单...")
        self.stop_thread.set()
        self.ui.btn_now.setDisabled(False)
        self.ui.btn_quit.setDisabled(True)

    def cancel(self):
        self.waitflag = 0
        self.ui.textBrowser.setText("抢单取消\n请重新选择抢单...")

    def toHelp(self):
        if (self.browser):
            self.browser.get(self.manual)
        else:
            try:
                self.browser.get(self.manual)
            except:
                self.browser = webdriver.Chrome()
                self.browser.set_window_size(self.screen.width() / 2, self.screen.height())
                self.browser.get(self.manual)

    def toAbout(self):
        if (self.browser):
            self.browser.get(self.about)
        else:
            try:
                self.browser.get(self.about)
            except:
                self.browser = webdriver.Chrome()
                self.browser.set_window_size(self.screen.width() / 2, self.screen.height())
                self.browser.get(self.about)

    def setmode(self):
        if (self.ui.btn_mode.text() == "深色模式"):
            self.ui.btn_mode.setText("浅色模式")
            self.ui.btn_mode.setStatusTip("切换为深色模式")
            self.setStyleSheet(qrainbowstyle.load_stylesheet(style="QDarkstyle3Light"))
        else:
            self.ui.btn_mode.setStatusTip("切换为浅色模式")
            self.ui.btn_mode.setText("深色模式")
            self.setStyleSheet(qrainbowstyle.load_stylesheet(style="DarkOrange"))

    def showTime(self):
        wait = 0  # 初始化wait变量，记录等待剩余时间
        if self.waitflag == 0:
            self.timer.stop()
            self.ui.btn_quit.setText("结束抢单")
            self.ui.btn_quit.setDisabled(True)
            return
        else:
            date = self.buylater.dateTime()
            now = QDateTime.currentDateTime()
            wait = now.secsTo(date)
            text = "还有" + str(wait) + "秒开始抢购\n请不要关闭Seckill及Chrome窗口！"
            self.ui.textBrowser.setText(text)
        if wait <= 0:
            self.waitflag = 0
            QMessageBox.information(self,"抢单提醒","请点击Yes开始抢单",QMessageBox.Yes,QMessageBox.Yes)
            self.buy_it_now()
            self.timer.stop()


if __name__ == '__main__':
    myapp = QApplication(sys.argv)
    myDlg = MainDialog()
    myDlg.show()
    sys.exit(myapp.exec_())

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
