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

    now_time = datetime.datetime.now()
    cur.execute('UPDATE language SET last_update = ? WHERE name like ?', (now_time, category) )

    for element in most_common_skills:
        cur.execute('SELECT id from skill WHERE name like ?', (element[0], ) )
        print(element[0], element[1])

        row = cur.fetchone()
        if row is None:
            cur.execute('INSERT INTO skill (name) VALUES (?)', (element[0],))
        
        cur.execute('SELECT id from skill WHERE name like ?', (element[0], ) )
        row = cur.fetchone()
        skill_id = row[0]

        cur.execute('SELECT skill_id FROM count WHERE skill_id like ?',(skill_id,))

        row = cur.fetchone()
        if row is None:
            cur.execute('INSERT INTO count (language_id, skill_id, counter) VALUES (?, ?, ?)', (categories.index(category)+1, skill_id, element[1]))
        else:
            cur.execute('UPDATE count SET counter = ? WHERE language_id = ? AND skill_id = ?', ( element[1],categories.index(category)+1, skill_id))

        conn.commit()


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

    formatted_table_with_data = tt.to_string(
        rows,
        header = ['SKILL', 'COUNTER'],
        style = tt.styles.ascii_thin_double
    )
    print(formatted_table_with_data)






categories = ['all', 'javascript', 'html', 'php', 'ruby', 'python', 'java', 'net', 'scala', 'c', 'mobile', 'testing', 'devops', 'ux', 'pm', 'game', 'analytics', 'security', 'data', 'go', 'sap', 'support', 'other']

print('Categories:\n', categories, '\n')

conn = sqlite3.connect('skill_counter.sqlite')

cur = conn.cursor()

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
        language_id INTEGER,
        skill_id INTEGER,
        counter INTEGER
    ) 
'''
)

try:
    for category_name in categories:
        cur.execute('INSERT INTO language (name, last_update) VALUES (?, ?)', (category_name,'NULL'))
    conn.commit()
except:
    print('')

   

while True:
    category = input('Type the category name or press enter to display data for all available jobs: ')

    if category in categories:
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


cur.execute('SELECT last_update FROM language WHERE id like ?',(categories.index(category)+1, ))    
row = cur.fetchone()

if(row[0] != 'NULL'):
    print('Last update:',row[0])
    while True:
        from_db = input('Do you want to retrieve data from db? (yes/no)\n')

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

def main():
    conn = sqlite3.connect('skill_counter.sqlite')

    #create tables
    #insert base data
    #ask for input
    #display

    conn.close()