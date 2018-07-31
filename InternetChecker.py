import config
import passwordConfig

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.keys import Keys
import time

class InternetChecker(object):

    logged_in = False
    webdriver_open = False
    def __init__(self):

        self.capabilities = DesiredCapabilities().FIREFOX
        # self.capabilities = DesiredCapabilities().CHROME
        # self.capabilities = DesiredCapabilities().HTMLUNITWITHJS
        self.capabilities["pageLoadStrategy"] = "eager"
        # self.capabilities["pageLoadStrategy"] = "normal"
        
        self.driver = webdriver.Firefox(desired_capabilities=self.capabilities)
        # self.driver = webdriver.Chrome(desired_capabilities=self.capabilities)
        # self.driver = webdriver.PhantomJS(desired_capabilities=self.capabilities)
        self.webdriver_open = True

        return

        
    def __login(self):

        # Get the base router url
        self.driver.get(config.ROUTER_URL)

        time.sleep(5)

        # Get elements and clear contents
        usernameElem = self.driver.find_element_by_name("admin_user_name")
        passwordElem = self.driver.find_element_by_name("admin_password")
        usernameElem.clear()
        passwordElem.clear()

        # Set field username and password
        usernameElem.send_keys(passwordConfig.USERNAME)
        passwordElem.send_keys(passwordConfig.PASSWORD)

        # Press RETURN on password field
        passwordElem.send_keys(Keys.RETURN)

        # This assertion doesnt work how you think
        try:
            assert "Login Failed" not in self.driver.page_source
            success = True
            self.logged_in = True
        except AssertionError as ae:
            print("Could not login: {}".format(ae))
            success = False

        time.sleep(5)
        return success

    def reboot(self):

        # Go to the utilities section and click the reboot button
        self.__goto_utilities()
        reboot_button = self.driver.find_element_by_class_name("btn.reboot_btn")
        reboot_button.send_keys(Keys.RETURN)

        time.sleep(1)

        # Click ok on the popup
        ok_button = self.driver.find_element_by_class_name("dialog-ok_new")
        ok_button.send_keys(Keys.RETURN)

        return 

    def get_connection_status(self):

        self.__goto_modem_status()

        CenturyLink_DSL = self.driver.find_element_by_id("ISP_status1")
        internet = self.driver.find_element_by_id("ISP_status2")

        connection_staus = {"dsl": CenturyLink_DSL.text,
                            "internet": internet.text}

        modem_status_broadband_table = self.driver.find_element_by_id("broadband_table")
        table_elements = modem_status_broadband_table.find_elements_by_tag_name("tr")
        for row in table_elements:

            columns = row.find_elements_by_tag_name("td")

            # If there are columns add them as long as they're not empty
            if (len(columns) > 0 and (columns[0].text != "" or columns[1].text != "")):
                connection_staus[columns[0].text.replace(" ", "_").lower()] = columns[1].text

        return connection_staus
    
    def connect(self):

        self.__goto_modem_status()

        # Get the bottons on the modem status page
        buttons = self.driver.find_elements_by_class_name("btn")

        # Look for the connect button and click it
        for button in buttons:
            if (button.text == "Connect"):
                button.send_keys(Keys.RETURN)
                return

        return

    def __check_login(self):

        # Check if logged in. If not try to log in
        print("Logged in: {}".format(self.logged_in))
        if (not self.logged_in):
            self.__login()

            if (not self.logged_in):
                print("Could not login.")
                return self.logged_in
            else:
                print("Log in success: {}".format(self.logged_in))

        return self.logged_in


    def __goto_modem_status(self):

        # Check if logged in 
        if (not self.__check_login()):
            return self.logged_in

        # Have the driver get the modem status page
        self.driver.get(config.ROUTER_URL + config.MODEM_STATUS_LINK_HREF)

        return self.logged_in


    def __goto_quick_setup(self):
        pass


    def __goto_wireless_setup(self):
        pass


    def __goto_utilities(self):

        # Check if logged in 
        if (not self.__check_login()):
            return self.logged_in

        self.driver.get(config.ROUTER_URL + config.UTILITIES_LINK_HREF)
        # print(self.driver.page_source)

        return self.logged_in


    def __goto_advanced_setup(self):
        pass


    def tear_down(self):
        self.driver.close()
        self.webdriver_open = False