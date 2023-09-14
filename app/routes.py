from flask import (
    Flask,
    request,
    render_template
)

import requests # Not to be consufed with "request" above!
from requests.exceptions import ConnectionError

app = Flask(__name__)

BACKEND_URL = "http://127.0.0.1:5000/tasks"

#Quick test/example:
@app.get("/")
def index():
    return render_template("index.html")

@app.get("/about")
def about_me():

    me = {
        "first_name" : "Adrian",
        "last_name" : "Adame",
        "hobbies" : "Coding, Listening to Music",
        "bio" : "Adrian Adame is a Computer Engineer with experience in embbedded systems and IoT, also ..."
    }

    return render_template("about.html", user = me)

@app.get("/tasks")
def task_list():
    try:
        response = requests.get(BACKEND_URL)

        if response.status_code == 200:
            task_l = response.json().get('tasks')
            return render_template("list.html", tasks = task_l)
        
        return (
            render_template("error.html", err = response.status_code), 
            response.status_code
        )
    except ConnectionError:
        return (
        render_template("error.html", err = 500), 
        500
    )


@app.get("/tasks/create")
def create_task():
    return render_template("create.html")

@app.post("/tasks/create")
def create_task_req():

    task_data = request.form

    try:
        response = requests.post(BACKEND_URL, json = task_data)

        if response.status_code == 204:
            return render_template("success.html")
        
        return (
            render_template("error.html", err = response.status_code), 
            response.status_code
        )

    except ConnectionError:
        return (
        render_template("error.html", err = 500), 
        500
    )

@app.get("/tasks/edit/<int:pk>")
def edit_task(pk):
    url = "%s/%s" % (BACKEND_URL, pk)

    try:
        response = requests.get(url)

        if response.status_code == 200:
            task_l = response.json().get('task')
            return render_template("edit.html", task = task_l)
        
        return (
            render_template("error.html", err = response.status_code), 
            response.status_code
        )
    except ConnectionError:
        return (
        render_template("error.html", err = 500), 
        500
    )

@app.post("/tasks/edit/<int:pk>")
def edit_task_req(pk):
    url = "%s/%s" % (BACKEND_URL, pk)

    task_data = request.form

    try:
        response = requests.put(url, json = task_data)

        if response.status_code == 204:
            return render_template("success.html")
        
        return (
            render_template("error.html", err = response.status_code), 
            response.status_code
        )
    except ConnectionError:
        return (
        render_template("error.html", err = 500), 
        500
    )

@app.get("/tasks/delete/<int:pk>")
def delete_task_req(pk):
    url = "%s/%s" % (BACKEND_URL, pk)

    try:
        response = requests.delete(url)

        if response.status_code == 204:
            return render_template("success.html")
        
        return (
            render_template("error.html", err = response.status_code), 
            response.status_code
        )
    except ConnectionError:
        return (
        render_template("error.html", err = 500), 
        500
    )