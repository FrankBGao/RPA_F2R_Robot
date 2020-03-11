from movement.driverCenter import Driver
import pandas as pd
from Translator import deploy_form_action_simply
import time

table = {
    "name": "Final_Grade_list",
    "type": "list",
    "structure": "table",
    "container": "web",
    "address": "https://moodle.rwth-aachen.de/mod/assign/view.php?id=79063&action=grading",
    "structure_address": "html/body[1]/div[1]/div[2]/div[1]/div[1]/section[1]/div[2]/div[2]/div[3]/table[1]",
    "instance_id_col": 4,
    "enter_col": {
        "col": 6,
        "xpath": "/td[6]/a[1]"
    }
}


def read(drive):
    # drive = Driver()
    drive.get(table["address"])  # 'http://localhost:8000/Assignment.html'
    this_table = drive.find_element('xpath', table["structure_address"])
    this_table = this_table.find_elements_by_tag_name('tbody')[0]
    table_rows = this_table.find_elements_by_tag_name('tr')

    this_table_value = []
    for row in table_rows:
        table_col = row.find_elements_by_tag_name('td')
        # This number is different with the Xpath, Xpath starts at 1. this number is for the list
        num = table["instance_id_col"] - 1
        inter = {table["instance_id_col"]: table_col[num].text}
        this_table_value.append(inter)

    drive.set_form_instance_list(table["name"], pd.DataFrame(this_table_value), table["instance_id_col"])
    print(this_table_value)
    return drive


def match_id_into_form_instance(drive, id_is):
    rows = drive.search_form_instance_row_by_id(id_is)

    row_template = "/tbody[1]/tr[%d]"

    for row in rows:
        row_template = row_template % row
        xpath = table["structure_address"] + row_template + table["enter_col"]["xpath"]

        act = {
            "act": "click",
            "element_fetch": {
                "type": "xpath",
                "argument": xpath
            }
        }
        drive.run_activities([act])


def batch_task(drive):
    form_setting = {
        "name": "Final_Grade",
        "type": "form",
        "container": "web",
        "address": "https://moodle.rwth-aachen.de/mod/assign/view.php?id=79063&rownum=0&action=grader&userid=",
        "form_field": [
            {
                "name": "NoticeStudent",
                "type_is": "checkbox",
                "address": "/html/body[1]/div[4]/div[1]/div[1]/div[4]/div[1]/form[1]/label[1]/input[1]"
            },
            {
                "name": "Grade",
                "type_is": "input",
                "address": "//*[@id='id_grade']"
            }
        ],
        "begin_route": {
            "motion_variable": "list",
            # "start_address": "list"
        },
        "finish_route": {
            'motion': [
                {
                    "motion": "click",
                    "address": "/html/body[1]/div[4]/div[1]/div[1]/div[4]/div[1]/form[1]/button[1]",
                    "destination_address": "list"
                }, {
                    "motion": "send_keys",
                    "send_keys": "#ENTER",
                    "address": "/html/body"
                },
                {
                    "motion": "click",
                    "address": "/html/body[1]/div[4]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/a[4]"
                }]
        }
    }

    field_names = [i['name'] for i in form_setting['form_field']]
    data = pd.read_excel('final_grade.xlsx')
    frm = form_setting['name']

    jobs = []
    for i in range(len(data)):
        row = data.iloc[i]
        inter = {}
        for name in field_names:
            inter[name] = str(row['fld:' + name])

        fa = {"fread": {},
              "fwrite": inter,
              "u": "robot", "frm": frm}
        jobs.append({'job': fa, 'form_instance_id': str(row['form_instance:id'])})

    for job in jobs:
        match_id_into_form_instance(drive, job['form_instance_id'])
        deploy_form_action_simply(job['job'], {form_setting['name']: form_setting}, drive)
        time.sleep(1)


if __name__ == '__main__':
    pass
