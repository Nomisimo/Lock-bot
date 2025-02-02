# -*- coding: utf-8 -*-
"""
Created on Sun Feb  2 20:47:36 2025

@author: kolja
"""
import requests
import json
import logging
import time
import textwrap

from lockbot import config
from lockbot.tool import testdata

logger = logging.getLogger(__name__)

# WEBHOOK_RECEIVER_URL = 'http://localhost:5001/consumetasks'

def send_webhook(msg):
    """
    Send a webhook to a specified URL
    :param msg: task details
    :return:
    """
    URL_RECEIVE = config.get("hook", "URL_RECEIVE")
    try:
        # Post a webhook message
        # default is a function applied to objects that are not serializable = it converts them to str
        resp = requests.post(URL_RECEIVE, data=json.dumps(
            msg, sort_keys=True, default=str), headers={'Content-Type': 'application/json'}, timeout=1.0)
        # Returns an HTTPError if an error has occurred during the process (used for debugging).
        resp.raise_for_status()
    except requests.exceptions.HTTPError as err:
        # logger.error("An HTTP Error occurred: " + repr(err))
        pass
    except requests.exceptions.ConnectionError as err:
        # logger.error("An Error Connecting to the API occurred: " + repr(err))
        pass
    except requests.exceptions.Timeout as err:
        # logger.error("A Timeout Error occurred: " + repr(err))
        pass
    except requests.exceptions.RequestException as err:
        # logger.error("An Unknown Error occurred: " + repr(err))
        pass
    else:
        return resp.status_code
    
    
def generate_test_logs(n: int=10, timeout: int=1):
    """
    Generate a Bunch of Fake Tasks
    """
    data = testdata.load_logfile()
    for i in range(n):
        msg = data[i]
        resp = send_webhook(msg)
        time.sleep(timeout)
        logger.debug(f"Task {i:03}/{n:03} -- Status {str(resp):<8}\n"+ textwrap.indent(str(msg), "\t"))
        yield resp, n, msg


def _test():
    config.load_config()
    logger.setLevel(logging.DEBUG)
    for resp, total, msg in generate_test_logs():
        pass


if __name__ == "__main__":
    _test()
    

# from flask import Flask,  Response, render_template
# from testhook import tasks

# app = Flask(__name__)
# app.config.from_object("testhook.config")


# def stream_template(template_name, **context):
#     app.update_template_context(context)
#     t = app.jinja_env.get_template(template_name)
#     rv = t.stream(context)
#     rv.enable_buffering(5)
#     return rv

# @app.route("/", methods=['GET'])
# def index():
#     return render_template('producer.html')

# @app.route('/producetasks', methods=['POST'])
# def producetasks():
#     print("producetasks")
#     return Response(stream_template('producer.html', data= tasks.produce_bunch_tasks() ))

