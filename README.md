# skills-requirements-justjoinit-spider
This app counts the number of skills requirements from employees using justjoin.it website.

To use this program you must install chromedriver for Chrome or geckodriver for Firefox.
Then go to terminal and type: python3 skill_spider.py
It will ask you to choose category and number of skills, then it will open your browser, scrape data, close browser, and show you the results.


EXAMPLE: 

Categories:
 ['javascript', 'html', 'php', 'ruby', 'python', 'java', 'net', 'scala', 'c', 'mobile', 'testing', 'devops', 'ux', 'pm', 'game', 'analytics', 'security', 'data', 'go', 'sap', 'support', 'other'] 

Type the category name or press enter to display data for all available jobs: python

Type number of skills to display: 7

---------------------------------------------
LOADING...
---------------------------------------------

+-----------+---------+
| SKILL     | COUNTER |
+===========+=========+
| python    | 63      |
+-----------+---------+
| django    | 24      |
+-----------+---------+
| english   | 10      |
+-----------+---------+
| docker    | 8       |
+-----------+---------+
| git       | 6       |
+-----------+---------+
| databases | 5       |
+-----------+---------+
| rest      | 5       |
+-----------+---------+