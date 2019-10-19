from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import random
from retrying import retry
import re

driver = webdriver.Chrome()
@retry
def search_competition_date(competition_name, year):
    driver.implicitly_wait(30)
    driver.get("https://www.swimcloud.com/results/?includeNotSubmitted=true&interval=all&orderBy=latest&region=All&page=1&period=past&searchText={0}".format(competition_name))
    # search_box = driver.find_element_by_xpath("//section/div/div/div/input")
    # search_box.send_keys(competition_name + " " + year)
    # time.sleep(5)
    # search_box.send_keys(Keys.ENTER)
    time.sleep(3)
    driver.implicitly_wait(5)
    no_results = driver.find_elements_by_xpath("//*[contains(text(), 'No results')]")
    if no_results:
        
        return ""
    comp_date = driver.find_elements_by_xpath("//*[contains(text(), '{0}')]".format(year))
    if not comp_date:
        return ""
    return comp_date[0].text



def exists(txt):
    try:
        driver.find_element_by_xpath("//*[contains(text(), '{0}')]".format(txt))
    except Error as e:

        return False
    return True

def parse_row(row, distance, e_type, year):
    split = row.split("\n")
    res = "{0}\t{1}\t{2}\t{3}\t{4}".format(distance, e_type, year, split[len(split) - 2], split[len(split) - 1].split(" ")[0])
    return res

def process_swimmers(distance, e_type, year):
    all_swimmers = []
    driver.implicitly_wait(5)
    next_pages = driver.find_elements_by_xpath("//div[1]/div/div[1]/div/ul/li/button")
    no_times = driver.find_elements_by_xpath("//*[contains(text(), 'No times')]")
    if len(no_times) > 0:
        (False, all_swimmers)

    error = False
    while not error and len(next_pages) > 0 and next_pages[len(next_pages) - 1].is_displayed():
        
        swimmersRows = driver.find_elements_by_xpath("//tbody/tr[td]")
        swimmers =  list(map(lambda x: x.text, swimmersRows))
        swimmers = [parse_row(row, distance, e_type, year) for row in swimmers]
        all_swimmers.extend(swimmers)
        next_pages[len(next_pages) - 1].click()
        # driver.implicitly_wait(5)
        err = driver.find_elements_by_xpath("//*[contains(text(), 'Server Error')]")
        error = len(err) > 0
        next_pages = driver.find_elements_by_xpath("//div[1]/div/div[1]/div/ul/li/button")
        time.sleep(random.randint(3,6))
    swimmersRows = driver.find_elements_by_xpath("//tbody/tr[td]")
    swimmers = list(map(lambda x: x.text, swimmersRows))
    swimmers = [parse_row(row, distance, e_type, year) for row in swimmers]
    all_swimmers.extend(swimmers)
    return (error, all_swimmers)


event_types = {
    "Free":"1",
    "Back":"2",
    "Breast": "3",
    "Fly":"4", 
    "IM": "5" 
    # "Free Relay": "6", 
    # "Medley Relay": "7"
}

event_codes_to_types = {
    "1":"Free",
    "2":"Back",
    "3":"Breast",
    "4":"Fly", 
    "5":"IM" 
    # "Free Relay": "6", 
    # "Medley Relay": "7"
}


event_distance = {
    "1": ["50", "100", "200", "400", "500", "800", "1000", "1500", "1650"],
    "2": ["50", "100", "200"],
    "3": ["50", "100", "200"],
    "4": ["50", "100", "200"],
    "5": ["100", "200", "400"]
    # "6": ["200", "400", "800"],
    # "7": ["50", "100", "200", "400", "500", "800", "1000", "1500", "1650"]
}

events = []
for gender in ["M", "F"]:
    for course in ["L", "S"]:
        for year in range(2009, 2020):
            for k in event_types.keys():
                    type_code = event_types[k]
                    for distance in event_distance[type_code]:
                        events.append((type_code, distance, course, gender, year))

# 
def get_dataset():
    results = []
    progress = ""
    with open("progress.txt", "r", encoding="utf-8") as pin:
        progress = '|'.join(pin.readlines())

    for type_code, distance, course, gender, year in events:
        v = '\t'.join([gender, course, str(year), distance, type_code]) +'\n'
        if v in progress:
            print('\t'.join([gender, course, str(year), distance, type_code]), "Already done", sep="\t")
            continue
        driver.implicitly_wait(60)
        driver.get("https://www.swimcloud.com/times/?dont_group=true&event={0}{1}&event_course={2}&gender={3}&page=1&region&year={4}".format(type_code, distance,course, gender, year))
        time.sleep(3)
        error, swimmer = process_swimmers(distance, event_codes_to_types[type_code], year)
        if error:
            print("Error")
            break
        results = '\n'.join(swimmer) + '\n'
        with open("output_{0}_{1}CM.tsv".format(gender, course), "a+", encoding='utf-8') as out:
            out.write(results)
        with open("progress.txt", "a+", encoding='utf-8') as pout:
            pout.write('\t'.join([gender, course, str(year), distance, type_code])+ '\n') 
        print(gender, course, year, distance, event_codes_to_types[type_code], len(swimmer), sep="\t")

# get_dataset()
# with open("progress.txt", "a+", encoding="utf-8") as prog:
#     for type_code, distance, course, gender, year in events:
#         if gender == "M" and course == "L":
#             if int(year) < 2016 or (type_code == "1" and int(distance) <= 1000):
#                 prog.write()
def get_all_dates():
    prog = None
    with open("dates_progress.tsv", "r", encoding="utf-8") as outf:
        prog = outf.readlines()
    with open("competitions_M_LCM.tsv", "r", encoding="utf-8") as inp:
        for line in inp:
            if line in prog:
                continue
            tokens = line.split("\t")
            comp_date = search_competition_date(re.sub("\d{4}", "", tokens[0]), tokens[1].rstrip())
            if not comp_date:
                with open("not_found.tsv", "a+", encoding="utf-8") as not_found:
                    not_found.write(line)
                continue
            with open("competitions_dates_M_LCM.tsv", "a+", encoding="utf-8") as outf:
                outf.write("{0}\t{1}\t{2}\n".format(tokens[1].rstrip(), tokens[0], comp_date))
            with open("dates_progress.tsv", "a+", encoding="utf-8") as outf:
                outf.write(line)
get_all_dates()






