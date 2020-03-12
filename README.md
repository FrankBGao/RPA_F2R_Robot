# RPA_F2R_Robot
This project is a part of the RWTH-Aachen PADS group's RPA research.
This project is a further POC for [the F2R approach](https://github.com/FrankBGao/F2R_approach_RPA).
In this project, we try to build a robot for transferring data from a excel file to a webpage form.

For example, in our group, we should upload students' grade for a course to the Moodle system.
![alt text](https://raw.githubusercontent.com/FrankBGao/RPA_F2R_Robot/master/pic/form_base.png "the idea of this robot")

In our F2R approach, we say any constant data structure can be defined as a form.
In this example, the webpage for filling the students' grade could be seen as a form.
![alt text](https://raw.githubusercontent.com/FrankBGao/RPA_F2R_Robot/master/pic/form.png  "a form")

In robot, we define this form as a key-value object.
```json
{
    "name": "Final_Grade",
    "type": "form",
    "container":"web",
    "address": "https://moodle.rwth-aachen.de/mod/assign/view.php?id=79063&rownum=0&action=grader&userid=",
    "form_field": [
      {
        "name": "NoticeStudent",
        "address": "/html/body[1]/div[4]/div[1]/div[1]/div[4]/div[1]/form[1]/label[1]/input[1]"
      },
      {
        "name": "Grade",
        "address": "//*[@id='id_grade']"
      }
    ],
    "begin_route": {
      "motion": "list",
      "start_address": "list"
    },
    "finish_route": [{
      "motion": "click",
      "address": "/html/body[1]/div[4]/div[1]/div[1]/div[4]/div[1]/form[1]/button[1]",
      "destination_address": "list"
    },{
      "motion": "click",
      "address":"/html/body[1]/div[4]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/a[4]"
    },{
      "motion": "click",
      "address":"/html/body[1]/div[4]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/a[4]"
    }
```

Except the keys we defined in the F2R, we also define the "begin_route" and "finish_route" in this project.
The robot will follow this two key's information for entering and leaving the form.

In this project, we also define anther data object, "Table". A "Table" contains a set of filled form (form instance).
In this example, a list of students's grade in the Moodle is a "Table".
![alt text](https://raw.githubusercontent.com/FrankBGao/RPA_F2R_Robot/master/pic/table.png "a form")

In robot, we define this table as a key-value object.
```json
  {
    "name": "Final_Grade_list",
    "type": "list",
    "structure":"table",
    "container":"web",
    "address": "https://moodle.rwth-aachen.de/mod/assign/view.php?id=79063&action=grading",
    "structure_address":"html/body[1]/div[1]/div[2]/div[1]/div[1]/section[1]/div[2]/div[2]/div[3]/table[1]",
    "instance_id_class":"/td[4]/a[1]",
    "enter_class":"/td[6]/a[1]"
  }
```

We assume any filed form has an instance ID.
In a "table", the robot could search a certain filled form based on an instance ID.
 