from flask import Flask
from apscheduler.schedulers.background import BackgroundScheduler
import logging

app = Flask(__name__)
requests_count = 0

Log_Format = "%(levelname)s %(asctime)s - %(message)s"

logging.basicConfig(filename="logfile.log",
                    filemode="w",
                    format=Log_Format,
                    level=logging.INFO)

logger = logging.getLogger()



def logging_func():
    global requests_count
    print(requests_count)
    logger.info("requests_count: " + str(requests_count))
    requests_count = 0


scheduler = BackgroundScheduler()
scheduler.add_job(logging_func, "interval", seconds=10)
scheduler.start()


def check_requests_count(func):
    def wrapper(*args, **kwargs):
        global requests_count
        requests_count += 1
        outer = func(*args, **kwargs)
        return outer

    return wrapper


@app.route("/")
@check_requests_count
def hello_world():
    return "<p>Hello, World!</p>"


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001)
    # scheduler.shutdown()
