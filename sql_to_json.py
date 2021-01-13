import sqlite3
import datetime
import json

conn = sqlite3.connect('skill_counter.sqlite')
cur = conn.cursor()

cur.execute('''
        SELECT skill.name, overtime_skills.counter
        FROM overtime_skills
        INNER JOIN skill ON skill.id=overtime_skills.skill_id
        WHERE overtime_skills.language_id like 2 AND date_created like "2021-01-09"
    ''')

rows = cur.fetchall()

# https://jsonbin.io/5fff1cb668f9f835a3dec1a1

id = 1

with open("javascript.json", "w") as fp:
    fp.write('{"js": [')
    for row in rows:
        (skill, counter) = row
        print(skill, counter)
        item = f'\"id\":\"{id}\", \"skill\":\"{skill}\", \"counter\" :\"{counter}\"'
        item = '{' + item + '},'

        fp.write(item)
        id += 1
    fp.write(']}')


# {
#     "jokes": [
#     {
#         "id": 1,
#         "question": "Jaki jest ulubiony horror frontendowców?",
#         "answer": "Freddy kontra JSON"
#     },
#     ]
# }



# for row in rows:
#     print(row)
# with open("javascript.txt", "r") as fp:
#     lines = fp.readlines()
#     for line in lines:
#         jokes.append(such)
#         # print(such)
#         id = id + 1