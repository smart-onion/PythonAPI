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
    """
    Function to wait for a page to load based on certain conditions.

    Args:
        driver (WebDriver): The Selenium WebDriver instance.
        condition (str): The first condition to wait for (HTML element ID).
        second_condition (str): The second condition to wait for (optional, HTML element ID).
        value (str): The value to compare for the second condition.

    Returns:
        bool: True if the first condition is met, False otherwise.
    """
    assert type(condition) is str
    assert type(second_condition) is str
    assert type(value) is str

    while True:
        try:
            # Check if the first condition is met
            if driver.find_element(By.ID, condition):
                return True

        except Exception:
            # If an exception occurs, check for the second condition (if provided)
            if second_condition != '':
                # If the second condition is met, return False
                if driver.find_element(By.ID, second_condition).text == value:
                    return False
            # Wait for a short interval before checking again
            time.sleep(0.1)


class WebDriver:
    options = Options()
    hosts = []
    # options.add_argument('--headless')
    # options.add_argument('--disable-gpu')

    def __init__(self, hostname: str):
        """
        Initialize a WebDriver instance for a specific hostname.

        Args:
            hostname (str): The hostname to initialize the WebDriver for.

        Raises:
            AssertionError: If hostname is not a string or already exists in hosts.
        """
        assert type(hostname) is str
        assert hostname not in self.hosts

        # Initialize WebDriver with headless options
        self.hostname = hostname
        self.driver = webdriver.Firefox(options=self.options)
        self.hosts.append(self.hostname)

    def change_password(self, folio_id: str, username: str):
        """
        Change password for a user identified by folio ID.

        Args:
            folio_id (str): The folio ID of the user.

        Returns:
            str: "PASSWORD_CHANGED" if password change is successful, "NOT_FOUND" otherwise.
        """
        assert type(folio_id) is str, 'should be a string'
        assert type(username) is str, "should be a string"
        # LOG IN TO ICSMANAGER
        self.driver.get('https://managers.mtnsat.io/Login.aspx')
        if load_page(self.driver, 'txtUserName', 'ctl00_ContentPlaceHolder1_Tabs_pInfo_User1_txtUN'):
            load_page(self.driver, 'txtUserName')
            # Fill in username and password
            self.driver.find_element(By.ID, 'txtUserName').send_keys(os.environ.get('ICS_USER'))
            self.driver.find_element(By.ID, 'txtPassword').send_keys(os.environ.get('ICS_PASSWORD'))
            self.driver.find_element(By.ID, 'btnGo').click()
            load_page(self.driver, 'ctl00_Menu1_dlTabs_ctl00_AMenu')

        # MANAGE USERS TAB
        self.driver.get('https://managers.mtnsat.io/Forms/Manager/Default.aspx?Tab=Users')
        load_page(self.driver, 'ctl00_ContentPlaceHolder1_Tabs_pInfo_User1_txtUN')
        self.driver.find_element(By.ID, 'ctl00_ContentPlaceHolder1_Tabs_pInfo_User1_txtUN').send_keys(folio_id)
        # Select search option
        Select(
            self.driver.find_element(By.ID, 'ctl00_ContentPlaceHolder1_Tabs_pInfo_User1_drpSearchBy')).select_by_value(
            '1')
        # Click search button
        self.driver.find_element(By.ID, 'ctl00_ContentPlaceHolder1_Tabs_pInfo_User1_btnGo').click()

        try:
            # Check if user not found message is displayed
            load_page(self.driver, 'ctl00_ContentPlaceHolder1_Tabs_pInfo_User1_dlUser_ctl00_btnSave',
                      'ctl00_ContentPlaceHolder1_Tabs_pInfo_User1_lbMsg', 'User not found in the current voyage')
            print('load')
            if self.driver.find_element(By.ID, 'ctl00_ContentPlaceHolder1_Tabs_pInfo_User1_dlUser_ctl00_btnSave'):
                # Change password
                self.driver.find_element(By.ID, "ctl00_ContentPlaceHolder1_Tabs_pInfo_User1_txtUserName").clear()
                self.driver.find_element(By.ID, "ctl00_ContentPlaceHolder1_Tabs_pInfo_User1_txtUserName").send_keys(username)
                Select(self.driver.find_element(By.ID, "ctl00_ContentPlaceHolder1_Tabs_pInfo_User1_dlUser_ctl00_ddlStatus")).select_by_value('121')
                self.driver.find_element(By.ID, "ctl00_ContentPlaceHolder1_Tabs_pInfo_User1_dlUser_ctl00_txtPass").clear()
                self.driver.find_element(By.ID, "ctl00_ContentPlaceHolder1_Tabs_pInfo_User1_dlUser_ctl00_txtPass").send_keys("11")
                self.driver.find_element(By.ID, "ctl00_ContentPlaceHolder1_Tabs_pInfo_User1_dlUser_ctl00_btnSave").click()
                return "PASSWORD_CHANGED"
        except Exception:
            return 'NOT_FOUND'

    def __del__(self):
        """
        Destructor to close and quit the WebDriver instance.
        """
        # Close the WebDriver instance
        self.driver.close()
        self.driver.quit()
