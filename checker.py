import logging
import time
import sys

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.keys import Keys

import config
import credentials


logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logger = logging.getLogger(__name__)


class InternetChecker(object):

    logged_in = False
    webdriver_open = False
    browser_kinds = ["chrome", "firefox"]
    def __init__(self, browser="chrome", headless=True, slowdown=0):

        # Used so I can see steps taken
        self.slowdown = slowdown

        if (browser == "chrome"):
            self.capabilities = DesiredCapabilities().CHROME

            options = Options()
            if (headless):
                options.add_argument('--headless')
                options.add_argument('--disable-gpu') 

            self.driver = webdriver.Chrome("webdrivers/chromedriver_linux64", 
                                            chrome_options=options)

        elif (browser == "firefox"):
            self.capabilities = DesiredCapabilities().FIREFOX
            # self.capabilities["pageLoadStrategy"] = "eager"
            # self.capabilities["pageLoadStrategy"] = "normal"
            
            self.driver = webdriver.Firefox(desired_capabilities=self.capabilities)

        else:
            logger.error("browser should be either chrome or firefox")
            raise Exception("Invalid browser kind supplied to "
                            "InternetChecker: {} not in {}".format(browser, self.browser_kinds))
            
        self.webdriver_open = True
        logger.debug("Returning from InternetChecker init")
        return

    def _login(self):
        logger.info("Logging in...")

        # Get the base router url
        self.driver.get(config.ROUTER_URL)

        # Give it time to load
        time.sleep(1)

        # Get elements and clear contents
        username_element = self.driver.find_element_by_name("admin_user_name")
        password_element = self.driver.find_element_by_name("admin_password")
        username_element.clear()
        password_element.clear()

        # Set field username and password
        username_element.send_keys(credentials.USERNAME)
        password_element.send_keys(credentials.PASSWORD)

        # Press RETURN on password field
        password_element.send_keys(Keys.RETURN)

        # This assertion doesnt work how you think
        try:
            assert "Login Failed" not in self.driver.page_source
            self.logged_in = True
            logger.info("Login success!")
        except AssertionError:
            raise CouldNotLoginException("Could not login, check username and password")

        time.sleep(1)
        return self.logged_in

    def reboot(self):
        logger.info("Rebooting")

        # Go to the utilities section and click the reboot button
        self._goto_utilities()
        reboot_button = self.driver.find_element_by_class_name("btn.reboot_btn")
        reboot_button.send_keys(Keys.RETURN)

        time.sleep(1)

        # Click ok on the popup
        ok_button = self.driver.find_element_by_class_name("dialog-ok_new")
        ok_button.send_keys(Keys.RETURN)

        return 

    def get_connection_status(self):
        logger.info("Getting connection status")

        if (not self._goto_modem_status()):
            raise CouldNotLoginException("Could not log in, check username and password")

        century_link_dsl = self.driver.find_element_by_id("ISP_status1")
        internet = self.driver.find_element_by_id("ISP_status2")

        connection_status = {"dsl": century_link_dsl.text,
                            "internet": internet.text}

        modem_status_broadband_table = self.driver.find_element_by_id("broadband_table")
        table_elements = modem_status_broadband_table.find_elements_by_tag_name("tr")
        for row in table_elements:

            columns = row.find_elements_by_tag_name("td")

            # If there are columns add them as long as they're not empty
            if (len(columns) > 0 and (columns[0].text != "" or columns[1].text != "")):
                connection_status[columns[0].text.replace(" ", "_").lower()] = columns[1].text

        logger.debug(connection_status)
        return connection_status
    
    def connect(self):
        logger.info("Connecting")

        self._goto_modem_status()

        # Get the bottons on the modem status page
        buttons = self.driver.find_elements_by_class_name("btn")

        # Look for the connect button and click it
        for button in buttons:
            if (button.text == "Connect"):
                button.send_keys(Keys.RETURN)
                logger.info("Clicked Connect")
                return

        return

    def _goto_modem_status(self):
        logger.info("Going to modem status")

        # Check if logged in 
        # if (not self.__check_login()):
        #     return self.logged_in
        
        if (not self.logged_in):
            logger.info("Not logged in, attempting to login")

            self._login()

        # Have the driver get the modem status page
        self.driver.get(config.ROUTER_URL + config.MODEM_STATUS_LINK_HREF)

        return self.logged_in


    def _goto_quick_setup(self):
        logger.info("Going to quick setup")
        pass

    def _goto_wireless_setup(self):
        logger.info("Going to wireless setup")
        pass

    def _goto_utilities(self):
        logger.info("Going to utilities")

        # Check if logged in 
        # if (not self.__check_login()):
        #     return self.logged_in
        
        if (not self.logged_in):
            logger.info("Not logged in, attempting to login")
            return self.logged_in

        self.driver.get(config.ROUTER_URL + config.UTILITIES_LINK_HREF)
        # print(self.driver.page_source)

        return self.logged_in

    def _goto_advanced_setup(self):
        logger.info("Going to advanced setup")
        pass


    def tear_down(self):
        logger.info("Tearing down InternetChecker")
        self.driver.close()
        self.webdriver_open = False


class CouldNotLoginException(Exception):
    pass