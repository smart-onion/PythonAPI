import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from dotenv import load_dotenv
from selenium.webdriver.support.ui import Select
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary

load_dotenv()


def load_page(driver, condition: str, second_condition='', value=''):
    assert type(condition) is str
    assert type(second_condition) is str
    assert type(value) is str

    while True:
        try:
            if driver.find_element(By.ID, condition):
                return True

        except Exception:
            if second_condition != '':
                if driver.find_element(By.ID, second_condition).text == value:
                    return False
            time.sleep(0.1)


class WebDriver:
    options = Options()
    hosts = []
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')

    def __init__(self, hostname: str):
        assert type(hostname) is str
        assert hostname not in self.hosts

        self.hostname = hostname
        self.driver = webdriver.Firefox(options=self.options)
        self.hosts.append(self.hostname)

    def change_password(self, folio_id: str):
        assert type(folio_id) is str, 'should be string'

        # LOG IN TO ICSMANAGER
        self.driver.get('https://managers.mtnsat.io/Login.aspx')
        if load_page(self.driver, 'txtUserName', 'ctl00_ContentPlaceHolder1_Tabs_pInfo_User1_txtUN'):
            load_page(self.driver, 'txtUserName')
            self.driver.find_element(By.ID, 'txtUserName').send_keys(os.environ.get('ICS_USER'))
            self.driver.find_element(By.ID, 'txtPassword').send_keys(os.environ.get('ICS_PASSWORD'))
            self.driver.find_element(By.ID, 'btnGo').click()
            load_page(self.driver, 'ctl00_Menu1_dlTabs_ctl00_AMenu')

        # MANAGE USERS TUB
        self.driver.get('https://managers.mtnsat.io/Forms/Manager/Default.aspx?Tab=Users')
        load_page(self.driver, 'ctl00_ContentPlaceHolder1_Tabs_pInfo_User1_txtUN')
        self.driver.find_element(By.ID, 'ctl00_ContentPlaceHolder1_Tabs_pInfo_User1_txtUN').send_keys(folio_id)
        Select(
            self.driver.find_element(By.ID, 'ctl00_ContentPlaceHolder1_Tabs_pInfo_User1_drpSearchBy')).select_by_value(
            '1')
        self.driver.find_element(By.ID, 'ctl00_ContentPlaceHolder1_Tabs_pInfo_User1_btnGo').click()

        try:
            load_page(self.driver, 'ctl00_ContentPlaceHolder1_Tabs_pInfo_User1_dlUser_ctl00_btnSave',
                      'ctl00_ContentPlaceHolder1_Tabs_pInfo_User1_lbMsg', 'User not found in the current voyage')
            print('load')
            if self.driver.find_element(By.ID, 'ctl00_ContentPlaceHolder1_Tabs_pInfo_User1_dlUser_ctl00_btnSave'):
                # Change password here
                return "PASSWORD_CHANGED"
        except Exception:
            return 'NOT_FOUND'

    def __del__(self):
        self.driver.close()
        self.driver.quit()
