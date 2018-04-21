from lxml import html
import requests

def scrap_from_lms(year_semester):
    ## parsing input
    year = year_semester[0:4]
    semester_input = year_semester[4:5]
    
    semester_dic = {'s' : '0', 'f' : '2'}
    semester = semester_dic[semester_input]

    ## strings
    lms_url = 'http://lms.postech.ac.kr/'
    
    ## TODO: change department values to use whole departments
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
            subject_info_page = requests.get(lms_url + cur_subject)
            subject_info_tree = html.fromstring(subject_info_page.content)

            info_tr = subject_info_tree.xpath('//table/tr')

            credit = clear_string(info_tr[8].xpath('td')[3].text)
            code = clear_string(info_tr[4].xpath('td')[1].text)

            subject_name = clear_string(info_tr[2].xpath('td')[1].text)

            test_str = subject_name + ": " + code + " // " + credit

            print(test_str)


def clear_string(string):
    return string.replace("\r\n", "").replace("\t","")
