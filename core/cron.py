from time import sleep
from django.core.exceptions import ObjectDoesNotExist
from core.models import Category, Department, Semester, Subject, Period   
from lxml import html
import requests
import re


def scrap_from_lms(year_semester, limit = True):
    ''' Scrap(Parse) subjects data from lms.
    This function makes a baseline of database.
    Using parsed information of each subject, 
    it searches database and update a matched subject or create a new one.
    If limit is true, this function reads one subject per 0.5 seconds,
    otherwise it reads the lms data as fast as it can.
    '''

    ## input example: '2018s', '2019f'

    ## parsing input
    year = year_semester[0:4]
    semester_input = year_semester[4:5]
    
    ## we change semester 's' to '0' and 'f' to '2' for lms query
    ## semester_code is used for model 'Semester'
    semester_dic = {'s' : '0', 'f' : '2', 'S': '0', 'F' : '2'}
    semester_code = {'0' : 'S', '2': 'F'}
    semester_code_in_Korean = {'0': '년 1학기', '2': '년 2학기'}
    semester = semester_dic[semester_input]

    ## Semester check and if there is no semester, then make it
    try:
        Semester_object = Semester.objects.get(code=year+semester_code[semester])
    except ObjectDoesNotExist:
        Semester_object = Semester(name=year+semester_code_in_Korean[semester], code=year+semester_code[semester])
        Semester_object.save()
        try:
            print("* * * * New semester created! WOW! " + year + semester_code_in_Korean[semester] + " * * * *")
        except:
            print("* * * * New semester created! WOW! " + year + semester_code[semester] + " * * * *")

    ## variables
    lms_url = 'http://lms.postech.ac.kr/'
    
    ## Change department values to use whole departments' information
    department_page = requests.get(lms_url + 'Course.do?cmd=viewCourseAllList')
    department_tree = html.fromstring(department_page.content)
    department_list = department_tree.xpath('//span[@class="selectForm"]')[1]
    department_name = department_list.xpath('.//a[@href]/text()')
    department_code = department_list.xpath('.//a/attribute::href')

    ## save departments variables
    departments = []
    departments_cleared_name = []
    Department_objects = []

    if limit:
        limit_str = '0.5 SEC'
    else:
        limit_str = 'UNLIMITTED!!!'
    print("********************************** PARSING MESSAGE ***************************************")
    print("******* SEMESTER: " + year + " " + semester_code[semester] + "     *************************   SPEED LIMIT: " + limit_str + " *******")
    print("*********************************** PARSING START ****************************************")

    ## for each parsed department information, get 'Department' model object or create new one
    for i in range(len(department_code)):
        departments.append(department_code[i].split(',')[1].split("'")[1])
        departments_cleared_name.append(clear_string(department_name[i]))
        
        try:
            Department_object = Department.objects.get(name=departments_cleared_name[i])
        except ObjectDoesNotExist:
            Department_object = Department(name=departments_cleared_name[i])
            Department_object.save()
            try:
                print("****** New department " + departments_cleared_name[i] + " created ****** This should be done ONCE at the first time")
            except:
                print("****** New department created ****** This should be done ONCE at the first time")

        Department_objects.append(Department_object)
    
    ## current page starts from 1
    cur_page = 1

    ## search. open subject lists by department
    for cur_dept in range(len(departments)):
        # To let you know where you are
        try:
            print("Parsing department: " + departments_cleared_name[cur_dept])
        except:
            print("Parsing department #" + str(cur_dept))

        while True:
            ## get a subject list of one department
            page = requests.get(lms_url + 'Course.do?cmd=viewCourseAllList&courseTermDTO.courseTermId=' + year + '09' + semester 
                    + '&searchCode1=' + departments[cur_dept] + '&curPage=' + str(cur_page))
            if page.status_code != 200:
                cur_page += 1
                continue
            tree = html.fromstring(page.content)

            ## find the href list
            href_list = tree.xpath('//td/a/attribute::href')

            ## if there is no subject it breaks
            if len(href_list) == 0:
                print("No more subjects in this list!")
                break;

            ## start parsing!
            print("Parsing page # " + str(cur_page))

            ## get one subject info and plan data from one subject data
            for cur_subject in href_list:
                info_page = requests.get(lms_url + cur_subject)
                if info_page.status_code != 200:
                    continue
                info_tree = html.fromstring(info_page.content)

                ## get info table
                info_tr = info_tree.xpath('//table/tr')
                ## plan src
                plan_a = info_tree.xpath('//a/attribute::href')[0]
                
                ## EXAMPLE: 1-0-1
                try:
                    credit = clear_string(info_tr[8].xpath('td')[3].text)
                except:
                    continue
                ## EXAMPLE: CSED101
                code = clear_string(info_tr[4].xpath('td')[1].text)

                ## EXAMPLE: 햅틱스 입문
                subject_name = clear_string(info_tr[2].xpath('td')[1].text)
                ## EXAMPLE: 전공선택
                category = clear_string(info_tr[6].xpath('td')[3].text)
            
                ## EXAMPLE: 1
                try:
                    class_number = int(clear_string(info_tr[4].xpath('td')[3].text))
                except ValueError:
                    class_number = 1
                ## EXAMPLE: '200'
                capacity_raw = clear_string(info_tr[10].xpath('td')[1].text)
                ## EXAMPLE: 200
                capacity = int(re.search(r'\d+', capacity_raw).group())

                ## load plan data
                plan_page = requests.get(lms_url + plan_a)
                if plan_page.status_code != 200:
                    continue
                plan_tree = html.fromstring(plan_page.content)

                ## get plan table. sometimes it does not have any plan table (?)
                if len(plan_tree.xpath('//table')) > 0:
                    plan_tr = plan_tree.xpath('//table')

                    ## EXAMPLE: 윤은영
                    prof_name = clear_string(plan_tr[2].xpath('.//td')[0].text)
                    ## EXAMPLE..... is the line below.
                    time_place_raw = plan_tr[1].xpath('.//td')[5].xpath('.//text()')
                    time_place_num = len(time_place_raw)

                    ## time_place lines can be multiple, so we prepare arrays
                    time_place = []
                    place = []
                    start_time = []
                    end_time = []
                    days = []

                    ## This time_place can be several line. So it goes with for loop.
                    for line_number in range(time_place_num):
                        time_place_text = clear_string(time_place_raw[line_number])
                    
                        ## EXAMPLE: 1. 월 수 (09:30~10:45) | 무은재기념관 강의실 [101호]
                        if '.' not in time_place_text:
                            time_place.append(time_place_text)
                        else:
                            time_place.append(time_place_text.split('.')[1])

                        ## EXAMPLE: 월 수 (09:30~10:45) | 무은재기념관 강의실 [101호]

                        ## Actually... I don't know why I wrote like this.
                        ## Maybe there is a historical reason. (e.g. there is no time_place text yet.)
                        if len(time_place[line_number]) < 8:
                            time_place_num = 0
                            break
    
                        ## EXAMPLE:  무은재기념관 강의실 [101호]
                        time_place_or_splitted = time_place[line_number].split('|')
                        place_temp = time_place_or_splitted[1]
                        ## EXAMPLE: ' 무은재기념관 강의실 [101호]' -> '무은재기념관 강의실 [101호]'
                        place.append(place_temp[1:len(place_temp)+1])

                        ## EXAMPLE: 월 수 (09:30~10:45)
                        days_time = time_place_or_splitted[0]
                        ## EXAMPLE: 09:30~10:45
                        time = days_time.split('(')[1].split(')')[0]
                        ## EXAMPLE: 09:30
                        start_time.append(time.split('~')[0])
                        ## EXAMPLE: 10:45
                        end_time_raw = time.split('~')[1]
                        if end_time_raw[0:2] == '24':
                            end_time_raw = '00' + end_time_raw[2:5]
                        end_time.append(end_time_raw)

                        ## EXAMPLE: ['월', '수']
                        days.append(days_time.split('(')[0].split())

                ## if there is no table (I don't know why I wrote this code in RoR lemons)
                ## just pass it. come back later. Don't save anything.
                else:
                    continue

                ## Try to find category of subject. if except occurs, make one.
                try:
                    if category==u"0035":
                        category = u"기초선택"
                    Category_object = Category.objects.get(category=category)
                except ObjectDoesNotExist:
                    Category_object = Category(category=category)
                    Category_object.save()
                    try:
                        print("***** New category: " + category  + " added *****")
                    except:
                        print("***** New category added *****")

                ## Try to find Subject.
                try:
                    ## Find subject by code, class_number, semester and name
                    ## This should be just one 
                    Subject_object = Subject.objects.get(
                            code=code, class_number=class_number, semester=Semester_object, name=subject_name)
                    ## Update it for which is not specified (code, class_number, semester and name)
                    Subject_object.category = Category_object
                    Subject_object.department = Department_objects[cur_dept]
                    Subject_object.plan = plan_a
                    if prof_name != "":
                        Subject_object.professor = prof_name
                    if capacity != 0:
                        Subject_object.capacity = capacity
                    if credit != "":
                        Subject_object.credit = credit
                    Subject_object.save()
                    try:
                        print("Subject " + subject_name + "(" + code + ") is updated")
                    except:
                        print("Updated!")

                except ObjectDoesNotExist:
                    ## There is no matching subject. do once more
                    Subject_object = Subject(
                            name = subject_name,
                            code = code,
                            category = Category_object,
                            department = Department_objects[cur_dept],
                            plan = plan_a,
                            professor = prof_name,
                            class_number = class_number,
                            capacity = capacity,
                            credit = credit,
                            semester = Semester_object)
                    Subject_object.save()
                    try:
                        print("Subject " + subject_name + "(" + code + ") is created")
                    except:
                        print("Created!")
                
                ## Try to find out Period or make it
                ## Update period just in case
                Period_objects = Period.objects.filter(subject=Subject_object)
                    
                ## update for existing time
                if time_place_num - len(Period_objects) >= 0:
                    for period_object_number in range(len(Period_objects)):
                        Period_object = Period_objects[period_object_number]
                        Period_object.place = place[period_object_number]

                        Period_object.start = start_time[period_object_number]
                        Period_object.end = end_time[period_object_number]

                        Period_object.mon = '월' in days[period_object_number]
                        Period_object.tue = '화' in days[period_object_number]
                        Period_object.wed = '수' in days[period_object_number]
                        Period_object.thu = '목' in days[period_object_number]
                        Period_object.fri = '금' in days[period_object_number]
                        Period_object.save()
                    
                    ## Create Period objects for not yet created time
                    for number in range(time_place_num - len(Period_objects)):
                        new_object_number = number + len(Period_objects)
                        #print("Cur # " + str(new_object_number) + " with " + start_hour[new_object_number] + ":" + start_min[new_object_number])
                    
                        Period_object = Period(
                                subject = Subject_object,
                                place = place[new_object_number],
                                start = start_time[new_object_number],
                                end =  end_time[new_object_number],
                                mon = '월' in days[new_object_number],
                                tue = '화' in days[new_object_number],
                                wed = '수' in days[new_object_number],
                                thu = '목' in days[new_object_number],
                                fri = '금' in days[new_object_number])
                        Period_object.save()

                if limit:
                    sleep(0.5)

            cur_page += 1
        cur_page = 1


def clear_string(string):
    ''' Clear any '\r\n' and '\t' characters.
    While parsing too many '\r\n' and '\t' characters appear.
    To wipe out, this function is necessary
    '''
    return string.replace("\r\n", "").replace("\t","")

