from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select


class ScrapingTool:
    def __init__(self, input_dict):
        self.news_links = []
        self.browser = webdriver.Edge()
        self.input_dict = input_dict

    def setting_info(self):
        # open the advanced search url
        self.browser.get('https://search.globaltimes.cn/SearchCtrl')

        # set title keyword
        if self.input_dict['title_keyword']:
            title_set_element = self.browser.find_element(By.NAME, 'title')
            title_set_element.send_keys(self.input_dict['title_keyword'])

        # set section
        if self.input_dict['section']:
            section_element = self.browser.find_element(By.NAME, 'column')
            select = Select(section_element)
            select.select_by_visible_text(self.input_dict['section'])

        # set section
        if self.input_dict['sub_section']:
            sub_section_element = self.browser.find_element(By.NAME, 'sub_column')
            select = Select(sub_section_element)
            select.select_by_visible_text(self.input_dict['sub_section'])

        # set author
        if self.input_dict['author']:
            author_element = self.browser.find_element(By.NAME, 'author')
            author_element.send_keys(self.input_dict['author'])

        # set source
        if self.input_dict['source']:
            source_element = self.browser.find_element(By.NAME, 'source')
            source_element.send_keys(self.input_dict['source'])

        # set text keyword
        if self.input_dict['text_keyword']:
            text_set_element = self.browser.find_element(By.NAME, 'textPage')
            text_set_element.send_keys(self.input_dict['text_keyword'])

        # set begin date
        begin_date_element = self.browser.find_element(By.NAME, 'begin_date')
        self.browser.execute_script("arguments[0].value = '{}';".format(self.input_dict['start_date']),
                                    begin_date_element)
        # # set end date
        end_date_element = self.browser.find_element(By.NAME, 'end_date')
        self.browser.execute_script("arguments[0].value = '{}';".format(self.input_dict['end_date']),
                                    end_date_element)

        # set order
        # Find the checkbox element
        checkbox_element = self.browser.find_element(By.NAME, 'orderByTime')
        # Check the current state of the checkbox
        is_checked = checkbox_element.is_selected()
        # If the current state of the checkbox is not the same as self.input_record['order_by_time'], click the checkbox
        if is_checked != self.input_dict['order_by_time']:
            checkbox_element.click()



