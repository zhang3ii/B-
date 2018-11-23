import time
from io import BytesIO

from PIL import Image
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

EMAIL = '14785137962'
PASSWORD = 'ybdqq1607474154'
BORDER = 10
INIT_LEFT = 60


class CrackGeetest():
    def __init__(self):
        self.url = 'https://passport.bilibili.com/login?gourl=https%3A%2F%2Faccount.bilibili.com%2Faccount%2Fbig'
        self.browser = webdriver.Chrome()
        self.wait = WebDriverWait(self.browser, 20)
        self.email = EMAIL
        self.password = PASSWORD



    # def get_geetest_button(self):
    #     """
    #     获取滑块按钮
    #     :return: button
    #     """
    #     button = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'gt_slider_knob')))
    #     return button

    def get_position(self):
        """
        获取图片验证码在网页中的坐标位置
        :return: 验证码位置元组
        """
        time.sleep(3)
        img = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'gt_box')))
        location = img.location
        size = img.size
        top, bottom, left, right = location['y'], location['y'] + size['height'], location['x'], location['x'] + size[
            'width']
        return (top, bottom, left, right)

    def get_screenshot(self):
        """
        获取网页截图
        :return: 截图对象
        """
        screenshot = self.browser.get_screenshot_as_png()
        screenshot = Image.open(BytesIO(screenshot))
        return screenshot

    def get_slider(self):
        """
        获取滑块
        :return: 滑块对象
        """
        slider = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'gt_slider_knob')))
        return slider

    def get_geetest_image(self, name='captcha.png'):
        """
        获取验证码图片
        :return: 图片对象
        """
        # 掉用方法获得验证码坐标
        top, bottom, left, right = self.get_position()
        print('验证码位置', top, bottom, left, right)
        # 截取整个网页
        screenshot = self.get_screenshot()
        # 根据坐标截取出验证码图片
        captcha = screenshot.crop((left, top, right, bottom))
        print(left, top, right, bottom)
        # 保存验证码图片
        captcha.save(name)

        return captcha

    def open(self):
        """
        打开网页输入用户名密码
        :return: None
        """
        self.browser.get(self.url)
        email = self.wait.until(EC.presence_of_element_located((By.ID, 'login-username')))
        password = self.wait.until(EC.presence_of_element_located((By.ID, 'login-passwd')))
        email.send_keys(self.email)
        password.send_keys(self.password)

    def get_gap(self, image1, image2):
        """
        获取缺口偏移量
        :param image1: 不带缺口图片
        :param image2: 带缺口图片
        :return:
        """
        # 从图片中横坐标位65处开始便利图片像素点
        left = 65
        time.sleep(2)
        for i in range(left, image1.size[0]):
            print(i)
            for j in range(35, image1.size[1] - 35):
                if not self.is_pixel_equal(image1, image2, i, j):
                    print(i, j)
                    left = i
                    return left
        return left

    def is_pixel_equal(self, image1, image2, x, y):
        """
        判断两个像素是否相同
        :param image1: 图片1
        :param image2: 图片2
        :param x: 位置x
        :param y: 位置y
        :return: 像素是否相同
        """
        # 取两个图片的像素点
        pixel1 = image1.load()[x, y]
        pixel2 = image2.load()[x, y]
        threshold = 60
        # 判断像素点之间的RGB值是不是在可接受范围
        if abs(pixel1[0] - pixel2[0]) < threshold and abs(pixel1[1] - pixel2[1]) < threshold and abs(
                pixel1[2] - pixel2[2]) < threshold:
            return True
        else:
            return False

    def get_track(self, distance):
        """
        根据偏移量获取移动轨迹（使用加速度与减速度来模拟，当然并不是每个网站都可以使用加速度来解决的，
        如有妖气使用的顶象验证还会判断是否是存在加速度与加速度，毕竟人手动的速度是有波动的）
        :param distance: 偏移量
        :return: 移动轨迹
        """
        # 移动轨迹
        track = []
        # 当前位移
        current = 0
        # 减速阈值
        mid = distance * 4 / 5
        # 计算间隔
        t = 0.3
        # 初速度
        v = 0
        while current < distance:
            if current < mid:
                # 加速度为正4，实验多次得到的较为准确的速度
                a = 4
            else:
                # 加速度为负5
                a = -5
            # 初速度v0
            v0 = v
            # 当前速度v = v0 + at
            v = v0 + a * t
            # 移动距离x = v0t + 1/2 * a * t^2
            move = v0 * t + 1 / 2 * a * t * t
            # 当前位移
            current += move
            # 加入轨迹
            track.append(round(move))
        return track

    def move_to_gap(self, slider, track):
        """
        拖动滑块到缺口处
        :param slider: 滑块
        :param track: 轨迹
        :return:
        """
        # 点击不放开
        ActionChains(self.browser).click_and_hold(slider).perform()
        # 滑动
        for x in track:
            ActionChains(self.browser).move_by_offset(xoffset=x, yoffset=0).perform()
        time.sleep(0.5)
        # 对齐松开
        ActionChains(self.browser).release().perform()

    def login(self):
        """
        登录
        :return: None
        """
        submit = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'login-btn')))
        submit.click()
        time.sleep(1)
        print('登录成功')

    def crack(self):
        # 输入用户名密码
        self.open()
        # 鼠标移动到验证按钮
        slider = self.get_slider()
        # button = self.get_geetest_button()
        ActionChains(self.browser).move_to_element(slider).perform()
        # 获取验证码图片
        image1 = self.get_geetest_image('captcha1.png')
        # 点按呼出缺口

        slider.click()
        # 获取带缺口的验证码图片
        time.sleep(1)
        image2 = self.get_geetest_image('captcha2.png')
        # 获取缺口位置
        gap = self.get_gap(image1, image2)
        print('缺口位置', gap)
        # 减去缺口位移
        gap -= BORDER
        # 获取移动轨迹
        track = self.get_track(gap)
        print('滑动轨迹', track)
        # 拖动滑块
        self.move_to_gap(slider, track)
        time.sleep(30)


if __name__ == '__main__':
    crack = CrackGeetest()
    crack.crack()