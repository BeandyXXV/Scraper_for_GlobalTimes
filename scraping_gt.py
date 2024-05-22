from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


class ScrapingTool:
    def __init__(self, keyword, ):
        self.news_links = []
        self.browser = webdriver.Edge()
        self.keyword = keyword

    def scrap_from_global_times(self):
        # open the advanced search url
        self.browser.get('https://search.globaltimes.cn/SearchCtrl')

        # Find the input box for Title contains
        title_set_element = self.browser.find_element(By.NAME, 'title')
        title_set_element.send_keys(self.keyword)
