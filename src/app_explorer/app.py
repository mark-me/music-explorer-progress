import os

import yaml
from flask import Flask, jsonify, redirect, render_template, url_for

from app_explorer.celery_config import celery_app
from app_explorer.tasks import simulate_etl
from log_config import logging

logger = logging.getLogger(__name__)

# Read configuration
with open(r"config/config.yml") as file:
    config = yaml.load(file, Loader=yaml.FullLoader)

app = Flask(
    __name__,
    template_folder=os.getcwd() + "/src/app_explorer/templates",
    static_folder=os.getcwd() + "/src/app_explorer/static",
)

# ETL task id
id_task_etl = None

def celery_tasks_running() -> str:
    """Get task id of active task

    Returns:
        str: Task id
    """
    id_task_etl = None
    i = celery_app.control.inspect()
    dict_tasks = i.active()
    if not dict_tasks:
        logger.error("Could not inspect Celery: it may be down.")
        return []
    lst_tasks = sum(dict_tasks.values(), [])
    for task in lst_tasks:
        if task["name"] in ["tasks.simulator", "tasks.discogs_etl"]:
            id_task_etl = task["id"]
    return id_task_etl


@app.route("/")
@app.route("/home")
def home():
    """Home page"""
    return render_template("home.html")

@app.route("/config")
def config_page():
    dict_config = {
        "credentials_ok": True,
        "url_discogs": f"http:localhost:5000/receive-token"
    }
    return render_template("config.html", config=dict_config)


@app.route("/task_etl_id")
def get_task_ETL_id():
    global id_task_etl
    id_task_etl = celery_tasks_running()
    return jsonify({"success": True, "task_id": id_task_etl})


@app.route("/simulate_etl")
def start_simulate_ETL():
    global id_task_etl
    id_task_etl = celery_tasks_running()
    if not id_task_etl:
        task = simulate_etl.delay()
        id_task_etl = task.id
    return redirect(url_for("config_page"))


@app.route("/check_task/<task_id>", methods=["GET"])
def check_task(task_id):
    task = celery_app.AsyncResult(task_id)
    task_status = {"status": task.state}
    try:
        task_status.update(task.result)
    except TypeError:
        pass
    response = jsonify(task_status)
    return response

if __name__ == "__main__":
    app.run(debug=True, port=5000)
