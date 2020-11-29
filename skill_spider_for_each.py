from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from collections import Counter 
import termtables as tt
import sqlite3
import datetime

def create_database():
    print('Categories:\n', categories, '\n')

    # creating tables if not exists

    cur.execute('''
        CREATE TABLE IF NOT EXISTS language(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(128) UNIQUE,
            last_update varchar(128)
        )
    '''
    )

    cur.execute('''
        CREATE TABLE IF NOT EXISTS skill(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(128) UNIQUE
        )   
    '''
    )

    cur.execute('''
    CREATE TABLE IF NOT EXISTS overtime_jobs(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        language_id INTEGER,
        date_created varchar(128),
        counter INTEGER
    ) 
    '''
    )

    cur.execute('''
        CREATE TABLE IF NOT EXISTS overtime_skills(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            language_id INTEGER,
            skill_id INTEGER,
            date_created varchar(128),
            counter INTEGER
        ) 
    '''
    )

    # inserting categories to language table in the database (only for the first time)
    try:
        for category_name in categories:
            cur.execute('INSERT INTO language (name, last_update) VALUES (?, ?)', (category_name,'NULL'))
        conn.commit()
    except:
        print('')

def live_retrieve():

    print('\n---------------------------------------------')
    print(category)
    print('---------------------------------------------\n')

    browser = webdriver.Firefox()
    url = 'https://justjoin.it/all/' + category
    browser.get(url)
    scroll_element = browser.find_element_by_class_name('css-ic7v2w')
    last_offers = None
    list_of_skills_scraped_from_website = []
    names_list = []
    companies_list = []
    cities_list = []
    now_date = str(datetime.datetime.now()).split(' ')[0]


    # reading divs with offers, to compare with last offers, so if divs_with_offers == last_offers, it means that, we have reached the bottom of the page
    while True:
        time.sleep(1)
        divs_with_offers = browser.find_elements_by_xpath("/html/body/div[1]/div[3]/div[1]/div/div[2]/div[1]/div/div/div")
        divs_with_skills = browser.find_elements_by_class_name('css-1ij7669')
        divs_with_company_names = browser.find_elements_by_class_name('css-ajz12e')
        divs_with_job_names = browser.find_elements_by_class_name('css-1x9zltl')   
        divs_with_city_names = browser.find_elements_by_class_name('css-1ihx907')   

        if divs_with_offers == last_offers:
            break
        else:
            last_offers = divs_with_offers

            # creating lists with company, job and city names
            for div in divs_with_company_names:
                    companies_list.append(div.text)
            for div in divs_with_job_names:
                    names_list.append(div.text)
            for div in divs_with_city_names:
                    cities_list.append(div.text)

            # adding text of anchor tags (as tuple) to a list
            for element in divs_with_skills:
                list_of_skills_scraped_from_website.append(element.text)
            
            # scrolling down, so new divs will be created
            scroll_element.send_keys(Keys.PAGE_DOWN)

    # closing browser
    browser.quit()

    # compounding new list fof touples (job_title, company_name, city_name, (skill1, skill2, skill3))
    # (Python Developer, ChokityPooh, New York, (python, django, sql))
    list_with_company_job_skill_names = []
    for x in range(len(names_list)):
        list_with_company_job_skill_names.append((names_list[x],companies_list[x], cities_list[x], list_of_skills_scraped_from_website[x]))

    # deleting duplicated offers, we are deleting duplicated tuples
    list_with_company_job_skill_names = list(dict.fromkeys(list_with_company_job_skill_names))
    number_of_offers = len(list_with_company_job_skill_names)

    # this is the list of all skills, but without replacing  / \
    list_of_skills_without_duplicates = []

    # this is the list of all skills ['python', 'django', 'sql', 'python', 'flask', 'django']
    # there are duplicates due to the fact, that job offers can have the same required skill set
    list_of_required_skills = []    

    for x in list_with_company_job_skill_names:
        (_, _, _, skill) = x
        list_of_skills_without_duplicates.append(skill)
    
    for x in list_of_skills_without_duplicates:
        x = x.replace(' /','\n').replace('/ ','\n').replace(' / ','\n').replace('/','\n').split('\n')
        x = [sub.strip() for sub in x]
        list_of_required_skills += x

    # we are counting how many duplicates of a single element are in required_skill[] list, and we are getting top number_of_skills entered by user
    most_common_skills = Counter(list_of_required_skills).most_common(1000)

    # adding skills and counter to proper category
    for element in most_common_skills:
        skill_name = element[0]
        skill_counter = element[1]

        # checking if skill name is in the skill table, if not it will insert one
        cur.execute('SELECT id from skill WHERE name like ?', (skill_name, ) )
        row = cur.fetchone()
        if row is None:
            cur.execute('INSERT INTO skill (name) VALUES (?)', (skill_name, ) ) 
        
        # if skill name in skill table, we are retrieving its id
        cur.execute('SELECT id from skill WHERE name like ?', (skill_name, ) )
        row = cur.fetchone()
        skill_id = row[0]

        # getting id of the row from count table, so we can later update its columns
        cur.execute('SELECT id FROM overtime_skills WHERE skill_id like ? AND language_id like ? AND date_created like ?',(skill_id, categories.index(category)+1, now_date))

        row = cur.fetchone()
        if row is None:
            cur.execute('INSERT INTO overtime_skills (language_id, skill_id, counter, date_created) VALUES (?, ?, ?, ?)', (categories.index(category)+1, skill_id, skill_counter, now_date))

        conn.commit()

    # setting last_update to now(), so program knows that there is an exisitng data for this category in the database, so user can decide if he wants to
    # scrape website on live, or just retrieve data for this category from database

    cur.execute('UPDATE language SET last_update = ? WHERE name like ?', (now_date, category) )

    cur.execute('SELECT id FROM overtime_jobs WHERE date_created like ? AND language_id like ?',(now_date, categories.index(category)+1))
    row = cur.fetchone()
    if row is None:
        cur.execute('INSERT INTO overtime_jobs (language_id, counter, date_created) VALUES (?, ?, ?)', (categories.index(category)+1, number_of_offers, now_date))
    else:
        print(category + ' is already in db')
    conn.commit()



if __name__ == '__main__':
    categories = ['all', 'javascript', 'html', 'php', 'ruby', 'python', 'java', 'net', 'scala', 'c', 'mobile', 'testing', 'devops', 'ux', 'pm', 'game', 'analytics', 'security', 'data', 'go', 'sap', 'support', 'other']

    conn = sqlite3.connect('skill_counter.sqlite')
    cur = conn.cursor()

    create_database()

    for category in categories:
        live_retrieve()


    conn.close()