
from web_super import Web_Super
from selenium.common import exceptions
import time
from PIL import Image

class web_ins(Web_Super):
    def __init__(self,USER_NAME,PASS_WORD):
        super().__init__()
        self.user=USER_NAME
        self.password=PASS_WORD

    def log_in(self):
        all_cookies=[]
        while(True):
            ###登陆测试
            self.driver.get('http://id.ifeng.com/')
            print(self.driver.title)
            try:
                time.sleep(2)
                self.driver.save_screenshot('index.png')
                self.wait_for_visibility_by_id('nav_safe')
            except exceptions.ElementNotVisibleException:
                print('重新登陆...')
                self.driver.get('https://id.ifeng.com/user/login')
                print(self.driver.title)
                elm_username = self.wait_for_visibility_by_name('userLogin_name')
                elm_password = self.wait_for_visibility_by_name('userLogin_pwd')
                elm_checkbox = self.wait_for_visibility_by_name('userLogin_auto')
                elm_auth_code = self.wait_for_visibility_by_name('userLogin_securityCode')
                elm_login_btn = self.wait_for_visibility_by_id('userLogin_btn')
                code_img = self.wait_for_visibility_by_id('code_img')
                elm_username.clear()
                elm_password.clear()
                elm_username.send_keys(self.user)
                elm_password.send_keys(self.password)
                elm_checkbox.click()
                # login_form.submit()
                # elm=self.wait_for_reload_by_id('SelectVerificationMethodForm_1')
                code_img.screenshot('ifeng_login.png')
                left = code_img.location['x']
                top = code_img.location['y']
                right = code_img.location['x'] + code_img.size['width']
                bottom = code_img.location['y'] + code_img.size['height']
                img = Image.open('ifeng_login.png')
                auth_code_img = img.crop((left, top, right, bottom))
                auth_code_img = auth_code_img.resize((200, 100), Image.ANTIALIAS)
                auth_code_img.save('auth_code.png')
                # auth_code_img.show()
                code_txt = input('验证码--->')
                elm_auth_code.send_keys(code_txt)
                time.sleep(2)
                elm_login_btn.click()
                time.sleep(5)
                self.driver.save_screenshot('after_login.png')
                all_cookies = self.driver.get_cookies()
            else:
                print('cookie获取成功...')
                return all_cookies

    def web_process(self):
        self.driver.get('http://www.ifeng.com/')
        print(self.driver.title)
        try:
            self.wait_for_reload_by_id('logName')
        except exceptions.ElementNotVisibleException :
            print('未登录...')
        self.driver.save_screenshot('index2.png')

