from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask
import requests
from config import hosts

app = Flask(__name__)

WEB_SEEVICES = hosts
BAD_SERVICES = []

def off_service():
    service = WEB_SEEVICES[0]
    WEB_SEEVICES.remove(service)
    BAD_SERVICES.append(service)
def on_service():
    service = BAD_SERVICES[0]
    WEB_SEEVICES.append(service)
    BAD_SERVICES.remove(service)

scheduler = BackgroundScheduler()
scheduler.add_job(off_service, "interval", seconds=100)
scheduler.add_job(on_service, "interval", seconds=200)
scheduler.start()

@app.route('/')
def catch_all():
    for service in WEB_SEEVICES:
        try:
            response = requests.get(service)

            WEB_SEEVICES.remove(service)
            WEB_SEEVICES.append(service)
            break
        except requests.exceptions.ReadTimeout:
            WEB_SEEVICES.remove(service)
            BAD_SERVICES.append(service)
    return response


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
