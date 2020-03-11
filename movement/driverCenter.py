from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys

import time

#
chrome_options = Options()
chrome_options.add_extension("movement/driver/IO_log_collector.crx")  # .crx file


class Driver:
    def __init__(self):
        self.driver = webdriver.Chrome(executable_path="movement/driver/chromedriver.exe",
                                       chrome_options=chrome_options)
        self.method_list = {
            "id": self.driver.find_element_by_id,
            "name": self.driver.find_element_by_name,
            "xpath": self._xpath_find,
            "partial_link_text": self.driver.find_element_by_partial_link_text,
            "link_text": self.driver.find_element_by_link_text,
        }
        self.try_times = 0
        self.form_instance_list = {}

    def get(self, url):
        self.driver.get(url)

    def click_sequence(self, clicks):
        for i in clicks:
            self.driver.find_element_by_partial_link_text(i).click()

    def fill_in_sequence_name(self, info):
        for i in info:
            self.driver.find_element_by_name(i).send_keys(info[i])

    def fill_in_sequence_id(self, info):
        for i in info:
            self.driver.find_element_by_id(i).send_keys(info[i])

    def _xpath_find(self, argument):
        return self.driver.find_element(By.XPATH, argument)

    def find_element(self, type_is, argument):
        """
        :param type_is:
        :param argument:
        :return: element
        """
        try:
            return self.method_list[type_is](argument)
        except Exception as arg:  # try 5s times to wait page
            if type(arg) == NoSuchElementException and self.try_times < 5:
                time.sleep(1)
                self.try_times += 1
                return self.find_element(type_is, argument)
            else:
                raise Exception(arg)

    def set_form_instance_list(self, instance_name, list_is, id_col=None):
        """

        :param instance_name: a string value
        :param list_is: a pd.DataFrame
        :param id_col: the col in DataFrame is the id
        :return:
        """
        self.form_instance_list["instance_name"] = instance_name
        self.form_instance_list["table"] = list_is
        self.form_instance_list["id_col"] = id_col

        self.form_instance_list["table"]['row_number'] = [i + 1 for i in range(len(list_is))]

    def search_form_instance_row_by_id(self, id_is):
        """
        searching the row number for instance id.
        in the same row, we expect a button could step in the form
        :param id_is: instance id
        :return: row number, maybe is a sequence of row number
        """
        id_col = self.form_instance_list["id_col"]

        # inter = self.form_instance_list["table"][id_col] == id_is
        # inter = self.form_instance_list["table"][inter]
        # inter = inter["row_number"]

        # be shorter
        inter = self.form_instance_list["table"][self.form_instance_list["table"][id_col] == id_is]["row_number"]
        return list(inter)

    def run_activities(self, activities):
        """
        :param activities: a sequence of activities
        {
            "act": "click, send_keys",
            "send_keys": "demo",
            "element_fetch":{
                "type":"method_list's type is",
                "argument":"argument"
            }
            "sleep":seconds
        }
        send_keys, #RETURN means send "enter" key to the page
        :return:
        """
        for i in activities:
            self.try_times = 0
            element = self.find_element(i["element_fetch"]["type"], i["element_fetch"]["argument"])
            if i["act"] == "click":
                element.click()
            elif i["act"] == "send_keys":
                if type(i["send_keys"]) == tuple:
                    if i["send_keys"][0] == "checkbox":
                        if element.is_selected() and i["send_keys"][1] == "F":
                            element.click()

                        if element.is_selected() and i["send_keys"][1] == "T":
                            element.click()

                elif "#" in i["send_keys"]:
                    inter = {
                        "#RETURN": Keys.RETURN,
                        "#ENTER": Keys.ENTER,
                    }
                    element.send_keys(inter[i["send_keys"]])
                else:
                    element.clear()
                    element.send_keys(i["send_keys"])

            if "sleep" in i.keys():
                time.sleep(i['sleep'])


if __name__ == '__main__':
    drive = Driver()
    drive.get('http://localhost:8080/camunda/app/tasklist/default/#/login')
    activities = [{
        "act": "send_keys",
        "send_keys": "demo",
        "element_fetch": {
            "type": "xpath",
            "argument": "//input[@placeholder='Username']"
        }
    },
        {
            "act": "send_keys",
            "send_keys": "demo",
            "element_fetch": {
                "type": "xpath",
                "argument": "//input[@placeholder='Password']"
            }
        },
        {
            "act": "click",
            "element_fetch": {
                "type": "xpath",
                "argument": "//button[@type='submit']"
            }
        }]
    drive.run_activities(activities)
