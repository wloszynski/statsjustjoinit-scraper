from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from collections import Counter 
import termtables as tt
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

categories = ['javascript', 'html', 'php', 'ruby', 'python', 'java', 'net', 'scala', 'c', 'mobile', 'testing', 'devops', 'ux', 'pm', 'game', 'analytics', 'security', 'data', 'go', 'sap', 'support', 'other']

print('Categories:\n', categories, '\n')

while True:
    category = input('Type the category name or press enter to display data for all available jobs: ')

    if category in categories:
        break
    elif category == '':
        break
    print('Wrong input, type again!\n')

while True:
    try:
        number_of_skills = int(input('\nType number of skills to display: '))
    except ValueError:
        print('Not an integer! Try again!')
        continue
    else:
        break

    
print('\n---------------------------------------------')
print('LOADING...')
print('---------------------------------------------\n')

browser = webdriver.Firefox()
url = 'https://justjoin.it/all/' + category
browser.get(url)
scroll_element = browser.find_element_by_class_name('css-ic7v2w')
last_offers = None
required_skills = []

while True:
    time.sleep(1)
    divs_with_offers = browser.find_elements_by_xpath("/html/body/div[1]/div[3]/div[1]/div/div[2]/div[1]/div/div/div")
    divs_with_skills = browser.find_elements_by_class_name('css-1ij7669')
    # divs_with_skills = [my_elem.text for my_elem in WebDriverWait(browser, 10).until(EC.visibility_of_all_elements_located((By.CLASS_NAME, "css-1ij7669")))]

    if divs_with_offers == last_offers:
        break
    else:
        last_offers = divs_with_offers

        for element in divs_with_skills:
            required_skills.append(element.text)

        scroll_element.send_keys(Keys.PAGE_DOWN)

browser.quit()

requirements_list = []

required_skills = list(dict.fromkeys(required_skills))

for x in required_skills:
    x = x.replace(' /','\n').replace('/ ','\n').replace(' / ','\n').replace('/','\n').split('\n')
    x = [sub.strip() for sub in x]
    requirements_list = requirements_list + x
    
most_common_skills = Counter(requirements_list).most_common(number_of_skills)

formatted_table_with_data = tt.to_string(
    most_common_skills,
    header = ['SKILL', 'COUNTER'],
    style = tt.styles.ascii_thin_double
)
print(formatted_table_with_data)