import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import re


class ScrapingTool:
    def __init__(self, input_dict):
        self.total_pages = None
        self.total_records = None
        self.news_links = []
        self.browser = webdriver.Edge()
        # open the advanced search url
        self.browser.get('https://search.globaltimes.cn/SearchCtrl')
        self.input_dict = input_dict

    def setting_info(self):
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

    def start_scraping(self, max_records):
        # Click on search to start
        self.browser.find_element(By.CLASS_NAME, "search_btn").click()
        # Find the element
        page_element = self.browser.find_element(By.XPATH, "/html/body/div[4]/div[1]/div[12]/a[9]")
        # Get the text of the element and convert it to an integer
        self.total_pages = int(page_element.get_attribute("text"))
        # total records
        records_num_element = self.browser.find_element(By.XPATH, "/html/body/div[4]/div[1]/div[12]/font")
        # Get the text of the element
        records_text = records_num_element.text
        # Use regular expression to find the number in the text
        self.total_records = int(re.search(r'\d+', records_text).group())
        # setting the max pages will be obtained.
        if max_records > self.total_records:
            max_records = self.total_records
        # Calculate max_pages based on max_records
        max_pages = max_records // 10 + 1 if max_records % 10 != 0 else max_records // 10

        current_page = 1
        while current_page < max_pages:
            current_page = int(self.browser.find_element(By.CLASS_NAME, "btn.btn-inverse").get_attribute("text"))
            self.get_news_links()
            time.sleep(5)
            if current_page >= self.total_pages - 5:
                self.browser.find_element(By.XPATH, "/html/body/div[4]/div[1]/div[12]/a[11]").click()
            else:
                self.browser.find_element(By.XPATH, "/html/body/div[4]/div[1]/div[12]/a[10]").click()
        print(self.news_links)

    def get_news_links(self):
        # Get element with class name = row-fluid
        search_result = self.browser.find_element(By.CLASS_NAME, 'row-fluid')
        # Get all the elements available with tag name 'a' and save the element link
        link_elements = search_result.find_elements(By.TAG_NAME, 'a')
        # iterate the link elements
        for link in link_elements:
            news_url = link.get_attribute('href')
            if news_url.startswith('https://www.globaltimes.cn/page/'):
                if news_url not in self.news_links:
                    self.news_links.append(news_url)
