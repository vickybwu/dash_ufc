from selenium import webdriver
from selenium.webdriver.common.keys import Keys


browser = webdriver.Chrome("/Users/VickyWu/Desktop/datavizufc/chromedriver")
base_url = ('http://www.ufcstats.com/statistics/fighters?char=a&page=1')

browser.get(base_url)

fighter_stats = []
stats_table = browser.find_elements_by_css_selector('b-statistics__table')
print(stats_table)

# for row in stats_table:
#     fighter = {
#         'FN' : listing.find_element_by_css_selector('.details-title a').text,
#         'LN' :  listing.find_element_by_css_selector('.price').text,
#         'HT' : [d.text.strip() for d in listing.find_elements_by_css_selector('ul.details_info li, li.details_info')],
#         'WT' : listing.find_element_by_css_selector('.details-title a').get_attribute('href')}