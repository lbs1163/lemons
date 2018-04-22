from core.models import Category, Department, Semester, Subject, Period   
from lxml import html
import requests
import re

def scrap_from_lms(year_semester):
    ## parsing input
    year = year_semester[0:4]
    semester_input = year_semester[4:5]
    
    semester_dic = {'s' : '0', 'f' : '2', 'S': '0', 'F' : '2'}
    semester = semester_dic[semester_input]

    ## TODO: SEMESTER CODE CHECK AND DECIDE MAKE OR NOT

    ## variables
    lms_url = 'http://lms.postech.ac.kr/'
    days_dict = {'월' :  '1', '화' : '2', '수': '3', '목': '4', '금': '5'}
    
    ## TODO: change department values to use whole departments
    department_page = requests.get(lms_url + 'Course.do?cmd=viewCourseAllList')
    department_tree = html.fromstring(department_page.content)
    department_list = department_tree.xpath('//span[@class="selectForm"]')[1]
    department_name = department_list.xpath('.//a[@href]/text()')
    department_code = department_list.xpath('.//a/attribute::href')

    departments = ['00031000']

    ## current page starts from 1
    cur_page = 1

    for department in departments:
        ## get a subject list of one department
        page = requests.get(lms_url + 'Course.do?cmd=viewCourseAllList&courseTermDTO.courseTermId=' + year + '09' + semester + '&searchCode1=' + department + '&curPage=' + str(cur_page))
        tree = html.fromstring(page.content)

        ## find the href list
        href_list = tree.xpath('//td/a/attribute::href')

        ## if ther is no subject it breaks
        if len(href_list) == 0:
            print("there is no subject")
            break

        ## start parsing!
        print("Parsing page #" + str(cur_page))

        ## get one subject info and plan data from one subject data
        for cur_subject in href_list:
            info_page = requests.get(lms_url + cur_subject)
            info_tree = html.fromstring(info_page.content)

            ## get info table
            info_tr = info_tree.xpath('//table/tr')
            ## plan src
            plan_a = info_tree.xpath('//a/attribute::href')[0]

            credit = clear_string(info_tr[8].xpath('td')[3].text)
            code = clear_string(info_tr[4].xpath('td')[1].text)

            subject_name = clear_string(info_tr[2].xpath('td')[1].text)
            subject_category = clear_string(info_tr[6].xpath('td')[3].text)
            ## TODO: category find
            ## DO WE NEED? subject_department = ...
            
            class_number = int(clear_string(info_tr[4].xpath('td')[3].text))
            capacity_raw = clear_string(info_tr[10].xpath('td')[1].text)
            capacity = int(re.search(r'\d+', capacity_raw).group())

            ## load plan only if it needs
            plan_page = requests.get(lms_url + plan_a)
            plan_tree = html.fromstring(plan_page.content)

            ## get plan table
            if len(plan_tree.xpath('//table')) > 0:
                plan_tr = plan_tree.xpath('//table')

                prof_name = clear_string(plan_tr[2].xpath('.//td')[0].text)
                time_place_raw = plan_tr[1].xpath('.//td')[5].xpath('.//text()')

                for text in time_place_raw:
                    time_place_text = clear_string(text)
                    
                    if '.' not in time_place_text:
                        time_place = time_place_text
                    else:
                        time_place = time_place_text.split('.')[1]

                    ## Actually... I don't know why I wrote like this.
                    ## Maybe there is a historical reason. (e.g. there is no time_place text yet.)
                    if len(time_place) < 8:
                        break

                    days_time = time_place.split('|')[0]
                    place = time_place.split('|')[1]
                    place = place[1:len(place)+1]

                    time = days_time.split('(')[1].split(')')[0]
                    start = time.split('~')[0]
                    end = time.split('~')[1]

                    ## TODO: DAY DAY DAY
                    days = days_time.split('(')[0].split()



def clear_string(string):
    return string.replace("\r\n", "").replace("\t","")
