
import re
from abc import ABCMeta, abstractmethod
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
from selenium.common import exceptions
import weakref

BUSY_TIME=5

class Web_Super (metaclass=ABCMeta):
    """A headless PhantomJS page running the formular page"""
    instances = weakref.WeakSet()
    def __init__(self):
        Web_Super.instances.add(self)
        self.driver = webdriver.PhantomJS()
        self.driver.set_window_size(1280, 720)
        # self.home_dir = '/home/ubuntu/zbw_scraper/'
        self.home_dir = ''

    def wait_for_reload_by_id(self,id,timeout_seconds=5):

        retries = timeout_seconds
        pause_interval = 1
        while retries:
            # print("tries left: {}".format(retries))
            try:
                element = WebDriverWait(self.driver, timeout_seconds).until(EC.presence_of_element_located((By.ID,id)))
                if element.is_displayed():
                    return element
                elif "visible" in element.value_of_css_property("visibility"):
                    print("trying to focus on element")
                    self.driver.execute_script("$(\"" + id + "\").focus()")
            except (exceptions.NoSuchElementException,
                    exceptions.StaleElementReferenceException):
                if retries <= 0:
                    print('重试多次退出')
                    raise
                else:
                    pass

            retries = retries - 1
            time.sleep(pause_interval)
        raise exceptions.ElementNotVisibleException(
            "Element {} not visible despite waiting for {} seconds".format(
                id, timeout_seconds * pause_interval)
        )

    def wait_for_visibility(self, selector, timeout_seconds=5):
        retries = timeout_seconds
        pause_interval = 2
        while retries:
            # print("tries left: {}".format(retries))
            try:
                element = self.driver.find_element_by_css_selector(selector)
                if element.is_displayed():
                    return element
                elif "visible" in element.value_of_css_property("visibility"):
                    print("trying to focus on element")
                    self.driver.execute_script("$(\"" + selector + "\").focus()")
            except (exceptions.NoSuchElementException,
                    exceptions.StaleElementReferenceException):
                if retries <= 0:
                    print('重试多次退出')
                    raise
                else:
                    pass

            retries = retries - 1
            time.sleep(pause_interval)
        raise exceptions.ElementNotVisibleException(
            "Element {} not visible despite waiting for {} seconds".format(
                selector, timeout_seconds * pause_interval)
        )

    def wait_for_visibility_by_text(self, text, timeout_seconds=5):
        retries = timeout_seconds
        pause_interval = 2
        while retries:
            # print("tries left: {}".format(retries))
            try:
                element = self.driver.find_element_by_link_text(text)
                if element.is_displayed():
                    return element
                elif "visible" in element.value_of_css_property("visibility"):
                    print("trying to focus on element")
                    self.driver.execute_script("$(\"" + text + "\").focus()")
            except (exceptions.NoSuchElementException,
                    exceptions.StaleElementReferenceException):
                if retries <= 0:
                    print('重试多次退出')
                    raise
                else:
                    time.sleep(2)
                    pass

            retries = retries - 1
            time.sleep(pause_interval)
        raise exceptions.ElementNotVisibleException(
            "Element {} not visible despite waiting for {} seconds".format(
                text, timeout_seconds * pause_interval)
        )
    def wait_for_visibility_by_id(self, id, timeout_seconds=5):
        retries = timeout_seconds
        pause_interval = 2
        while retries:
            # print("tries left: {}".format(retries))
            try:
                element = self.driver.find_element_by_id(id)
                if element.is_displayed():
                    return element
                elif "visible" in element.value_of_css_property("visibility"):
                    print("trying to focus on element")
                    self.driver.execute_script("$(\"" + id + "\").focus()")
            except (exceptions.NoSuchElementException,
                    exceptions.StaleElementReferenceException):
                if retries <= 0:
                    print('重试多次退出')
                    raise
                else:
                    time.sleep(2)
                    pass

            retries = retries - 1
            time.sleep(pause_interval)
        raise exceptions.ElementNotVisibleException(
            "Element {} not visible despite waiting for {} seconds".format(
                id, timeout_seconds * pause_interval)
        )


    def wait_for_visibility_by_name(self, name, timeout_seconds=5):
        retries = timeout_seconds
        pause_interval = 2
        while retries:
            # print("tries left: {}".format(retries))
            try:
                element = self.driver.find_element_by_name(name)
                if element.is_displayed():
                    return element
                elif "visible" in element.value_of_css_property("visibility"):
                    print("trying to focus on element")
                    self.driver.execute_script("$(\"" + name + "\").focus()")
            except (exceptions.NoSuchElementException,
                    exceptions.StaleElementReferenceException):
                if retries <= 0:
                    print('重试多次退出')
                    raise
                else:
                    time.sleep(2)
                    pass

            retries = retries - 1
            time.sleep(pause_interval)
        raise exceptions.ElementNotVisibleException(
            "Element {} not visible despite waiting for {} seconds".format(
                name, timeout_seconds * pause_interval)
        )

    def print_title(self):
        print("Page title:")
        print(self.driver.title)

    def quit(self):
        print("closing page...")
        self.driver.quit()

    @abstractmethod
    def log_in(self):
        pass

    @abstractmethod
    def web_process(self):
        pass


