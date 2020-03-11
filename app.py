from flask import Flask, request, render_template
from movement.driverCenter import Driver
import util.pymo_interface as mo_inface
import readTable as RT

import time
import json
import pymongo as pymo

app = Flask(__name__)
driver = Driver()
client = pymo.MongoClient('mongodb://localhost:27017/')
db = client['ioLog_arl_robot']


# driver = ""


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/get_url')
def get_url():
    """
    /get_url?url=https://moodle.rwth-aachen.de/mod/assign/view.php?id=79063&action=grading
    :return:
    """
    url = request.args.get("url")
    driver.get(url)
    return "finish"


@app.route('/Commander', methods=["GET", "POST"])
def commander():
    if request.method == "GET":
        com_list = mo_inface.get_data(db["command"].find())
        for i in com_list:
            i["command"] = json.dumps(i["command"])
        return render_template("commander.html", com_list=com_list)
    else:
        command = request.form["Command"]
        command = json.loads(command)
        try:
            driver.run_activities(command)
            return "success"
        except Exception as arg:
            return str(arg)


@app.route('/Save', methods=["POST"])
def save():
    try:
        command = request.form["Command"]
        command = json.loads(command)
        db['command'].insert_one({"command": command, "name": request.form["Name"]})
        return "success"
    except Exception as arg:
        return str(arg)


# developing test
@app.route('/try_form_instance_table')
def try_form_instance_table():
    RT.read(driver)
    return "finish"


@app.route('/try_form_instance_enter')
def try_form_instance_enter():
    """
    /try_form_instance_enter?id_is=30291
    :return:
    """
    id_is = request.args.get("id_is")
    RT.match_id_into_form_instance(driver, id_is)
    return "finish"


@app.route('/try_batch_task')
def try_batch_task():
    """
    /try_batch_task
    :return:
    """
    RT.read(driver)
    time.sleep(1)
    RT.batch_task(driver)
    return "finish"


if __name__ == '__main__':
    app.run()
