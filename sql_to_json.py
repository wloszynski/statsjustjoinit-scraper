import sqlite3
import datetime
import json

categories = ['all', 'javascript', 'html', 'php', 'ruby',  'python','java', 'net', 'scala', 'c', 'mobile','testing', 'devops', 'ux','pm', 'game', 'analytics', 'security', 'data', 'go', 'sap', 'support','other']
# categories = ['all', 'javascript']


conn = sqlite3.connect('skill_counter.sqlite')
cur = conn.cursor()




with open("skills.json", "w") as fp:
    fp.write('{"skills":{ ')

    for category in categories:
        fp.write('\n"'+category+'":[')
        id = 1

        cur.execute('''
        SELECT skill.name, overtime_skills.counter
        FROM overtime_skills
        INNER JOIN skill ON skill.id=overtime_skills.skill_id
        WHERE overtime_skills.language_id like ? AND date_created like "2021-01-09" AND overtime_skills.counter > 1 LIMIT 30''',(categories.index(category)+1,))
        rows = cur.fetchall()


        for row in rows:
            (skill, counter) = row
            item = f'\"name\":\"{skill}\",\"id\":\"{id}\", \"counter\" :\"{counter}\"'
            if(len(rows) != id):
                item = '{' + item + '}'
            else:
                item = '{' + item + '}'

            fp.write(item)
            if(len(rows) != id):
                fp.write(',')
            else:
                fp.write('')

            id += 1
        if(len(categories) != categories.index(category)+1):
            fp.write('],\n')
        else:
            fp.write(']\n')

    fp.write('}}')


# https://jsonbin.io/5fff1cb668f9f835a3dec1a1

# id = 1

# with open("javascript.json", "w") as fp:
#     fp.write('{"js": [')
#     for row in rows:
#         (skill, counter) = row
#         print(skill, counter)
#         item = f'\"id\":\"{id}\", \"skill\":\"{skill}\", \"counter\" :\"{counter}\"'
#         item = '{' + item + '},'

#         fp.write(item)
#         id += 1
#     fp.write(']}')


# {
    # "skills": []
#     "javascript": [
#     {
#         "id": 1,
#         "question": "Jaki jest ulubiony horror frontendowców?",
#         "answer": "Freddy kontra JSON"
#     },
#     ],
# }



# for row in rows:
#     print(row)
# with open("javascript.txt", "r") as fp:
#     lines = fp.readlines()
#     for line in lines:
#         jokes.append(such)
#         # print(such)
#         id = id + 1