from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from collections import Counter 
import termtables as tt

categories = ['javascript', 'html', 'php', 'ruby', 'python', 'java', 'net', 'scala', 'c', 'mobile', 'testing', 'devops', 'ux', 'pm', 'game', 'analytics', 'security', 'data', 'go', 'sap', 'support', 'other']

my_list = []
cities = ['Warszawa', 'Kraków', 'Wrocław', 'Poznań', 'Trójmiasto', 'Śląsk', 'Białystok', 'Bielsko-Biała', 'Bydgoszcz', 'Częstochowa', 'Kielce', 'Lublin', 'Łódź', 'Olsztyn', 'Opole', 'Toruń', 'Rzeszów', 'Szczecin', 'Zielona Góra', 'Katowice', 'Gdynia']
types = ['interview', 'Online', 'Remote', '/', 'ago', 'Poland']
numbers = ['1','2','3','4','5','6','7','8','9']
forbidden_words = cities + types + numbers


print('Categories:\n',categories, '\n')

category = ''
number_of_skills = 5

while True:
    category = input('Type the category name or press enter to display data for all available jobs: ')

    if category in categories:
        break
    elif category == '':
        break
    print('Wrong input, type again!\n')

while True:
    number_of_skills = input('\nType number of skills to display: ')

    if number_of_skills in numbers:
        break
    else:
        number_of_skills = 5
        break

print('\n---------------------------------------------')
print('LOADING...')
print('---------------------------------------------\n')

browser = webdriver.Firefox()
url = 'https://justjoin.it/all/' + category
browser.get(url)
html = browser.find_element_by_class_name('css-ic7v2w')
last_offers = None

while True:
    time.sleep(0.4)
    offer_divs = browser.find_elements_by_xpath("/html/body/div[1]/div[3]/div[1]/div/div[2]/div[1]/div/div/div")

    if offer_divs == last_offers:
        break

    last_offers = offer_divs

    for offer in offer_divs:
        my_list.append(offer.text)
        
    html.send_keys(Keys.PAGE_DOWN)
    html.send_keys(Keys.PAGE_DOWN)
    html.send_keys(Keys.PAGE_DOWN)


my_list = list(dict.fromkeys(my_list))
# print(len(my_list))

requirements_list = []

for x in my_list:
    x = x.split()
    requirements_list = requirements_list + x[-6:]

for word in list(requirements_list):
    if word in forbidden_words:
            requirements_list.remove(word)


Counter = Counter(requirements_list)

most_occur = Counter.most_common(int(number_of_skills))
# print(most_occur)

# print('Keywords list: ',most_occur)

formatted_table_with_data = tt.to_string(
    most_occur,
    header = ['SKILL', 'COUNTER'],
    style = tt.styles.ascii_thin_double
)
print(formatted_table_with_data)