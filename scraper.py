#!/usr/bin/env python3

from decouple import config
from requests import get
from bs4 import BeautifulSoup as bs

# get the BASE_URL defined in the .env file
BASE_URL = config('BASE_URL')

# build the list of urls to scrape
url_list = [BASE_URL + str(i) for i in range(0,4)]

def get_page_soup(url):
    """Returns a BeautifulSoup object for a given url"""
    response = get(url)
    return bs(response.text, 'html.parser')

# build a list of all the soup objects for each page in url_list
pages_soup = []
for url in url_list:
    pages_soup.append(get_page_soup(url))

# parse out relevant student html from soups
student_soup = []
for page in pages_soup:
    student_soup.append(page.find_all(class_='student'))

# flattened list of students
student_list = [student for students in student_soup for student in students]

# parse student details (name, email, primary advisor) from student list
for student in student_list:
    full_name = student.find(class_='field-content').text
    full_name = [i for i in full_name.split(" ") if i]
    first_name, last_name = full_name[0], " ".join(full_name[1:])
    try:
        email = student.find(
            class_='views-field-field-contact-email').text.strip()
    except:
        email = "n/a"
    try:
        advisor = student.find(class_='views-field-field-affiliation').find(
            class_='odd').text.split(':')[1].lstrip()
    except:
        advisor = 'n/a'
    print(f"{first_name} {last_name}, {email}, {advisor}")