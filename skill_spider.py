from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from collections import Counter 
import termtables as tt
import sqlite3
import datetime

def liveRetrieve():

    print('\n---------------------------------------------')
    print('LOADING...')
    print('---------------------------------------------\n')

    browser = webdriver.Firefox()
    url = 'https://justjoin.it/all/' + category
    browser.get(url)
    scroll_element = browser.find_element_by_class_name('css-ic7v2w')
    last_offers = None
    requirements_list = []
    names_list = []
    companies_list = []

    # reading divs with offers, to compare with last offers, so if divs_with_offers == last_offers, it means that, we have reached the bottom of the page
    while True:
        time.sleep(1)
        divs_with_offers = browser.find_elements_by_xpath("/html/body/div[1]/div[3]/div[1]/div/div[2]/div[1]/div/div/div")
        divs_with_skills = browser.find_elements_by_class_name('css-1ij7669')
        divs_with_company_names = browser.find_elements_by_class_name('css-ajz12e')
        divs_with_job_names = browser.find_elements_by_class_name('css-1x9zltl')    

        if divs_with_offers == last_offers:
            break
        else:
            last_offers = divs_with_offers

            for div in divs_with_company_names:
                    companies_list.append(div.text)
            for div in divs_with_job_names:
                    names_list.append(div.text)
            # adding text of anchor tags (as tuple) to a list
            for element in divs_with_skills:
                requirements_list.append(element.text)
            
            # scrolling down, so new divs will be created
            scroll_element.send_keys(Keys.PAGE_DOWN)

    # closing browser
    browser.quit()

    list_compound_elements = []
    for x in range(len(names_list)):
        list_compound_elements.append((names_list[x],companies_list[x], requirements_list[x]))

    # deleting duplicated offers, we are deleting duplicated tuples 
    list_compound_elements = list(dict.fromkeys(list_compound_elements))

    # this list will contain every single anchor tag (so when we have tuple like (python, machine learning, go), they will be added to the list as single elements
    # ('python', 'machine learning', 'go'), and in this list will be a lot of duplicates
    required_skills = []    

    for x in list_compound_elements:
        (job_title, company_name, skill) = x
        requirements_list.append(skill)
    
    print(len(list_compound_elements))
    for x in requirements_list:
        x = x.replace(' /','\n').replace('/ ','\n').replace(' / ','\n').replace('/','\n').split('\n')
        x = [sub.strip() for sub in x]
        required_skills += x

    # we are counting how many duplicates of a single element are in required_skill[] list, and we are getting top number_of_skills entered by user
    most_common_skills = Counter(required_skills).most_common(1000)


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
        cur.execute('SELECT id FROM count WHERE skill_id like ? AND language_id like ?',(skill_id, categories.index(category)+1) )

        row = cur.fetchone()
        if row is None:
            cur.execute('INSERT INTO count (language_id, skill_id, counter) VALUES (?, ?, ?)', (categories.index(category)+1, skill_id, skill_counter))
        else:
            cur.execute('UPDATE count SET counter = ? WHERE id = ? AND skill_id = ?', (skill_counter, row[0], skill_id))

        conn.commit()

    # setting last_update to now(), so program knows that there is an exisitng data for this category in the database, so user can decide if he wants to
    # scrape website on live, or just retrieve data for this category from database
    now_time = datetime.datetime.now()
    cur.execute('UPDATE language SET last_update = ? WHERE name like ?', (now_time, category) )
    conn.commit()


#displaying data function - retrieving data from db, and printing it as table
def displayData():
    cur.execute('''
        SELECT skill.name, counter
        FROM count
        INNER JOIN language ON language.id = count.language_id
        INNER JOIN skill on skill.id = count.skill_id
        WHERE language.id = ?
        ORDER BY counter DESC
        LIMIT ?
    ''', (categories.index(category)+1, number_of_skills))

    rows = cur.fetchall()

    print('\nDisplaying data for: ', category.upper())
    # formating data into tables
    formatted_table_with_data = tt.to_string(
        rows,
        header = ['SKILL', 'COUNTER'],
        style = tt.styles.ascii_thin_double
    )
    print(formatted_table_with_data)


# --------------------------------------------
# MAIN PROGRAM
# --------------------------------------------

# list of available categories from justjoin.it website
categories = ['all', 'javascript', 'html', 'php', 'ruby', 'python', 'java', 'net', 'scala', 'c', 'mobile', 'testing', 'devops', 'ux', 'pm', 'game', 'analytics', 'security', 'data', 'go', 'sap', 'support', 'other']

print('Categories:\n', categories, '\n')

conn = sqlite3.connect('skill_counter.sqlite')

cur = conn.cursor()

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
    CREATE TABLE IF NOT EXISTS count(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        language_id INTEGER,
        skill_id INTEGER,
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

# choosing category to scrape data for
while True:
    category = input('Type the category name or press enter to display data for all available jobs: ').lower()

    if category in categories:
        break
    print('Wrong input, type again!\n')

# choosing the number of skills to display in the table, it must be an integer
while True:
    try:
        number_of_skills = int(input('\nType number of skills to display: '))
    except ValueError:
        print('Not an integer! Try again!')
        continue
    else:
        break

# getting information if data for chose category is in our database if not it will immediately go to scrape a web
# otherwise it will ask user whether to display data from database or scrape web to display live data
# at the begining every category has last_update set to NULL
cur.execute('SELECT last_update FROM language WHERE id like ?',(categories.index(category)+1, ))    
row = cur.fetchone()

if(row[0] != 'NULL'):
    print('Last update:',row[0])
    while True:
        from_db = input('Do you want to retrieve data from db? (yes/no) ').strip().lower()

        if from_db == 'yes':
            print('Displaying from db')
            displayData()
            break
        elif from_db == 'no':
            print('Displaying live data')
            liveRetrieve()
            displayData()
            break
        else:
            print('Wrong input, type again!\n')
else:
    liveRetrieve()
    displayData()

conn.close()

