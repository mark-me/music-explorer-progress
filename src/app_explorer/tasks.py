import yaml

from app_explorer.celery_config import celery_app
from app_explorer.task_simulator import TaskSimulator

@celery_app.task(name="tasks.simulator", bind=True)
def simulate_etl(self):
    task = TaskSimulator(celery_app=self)
    task.start()
    return {"current": 100, "total": 100, "status": "Task completed!", "result": 42}
