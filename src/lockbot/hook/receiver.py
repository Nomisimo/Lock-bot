# -*- coding: utf-8 -*-
"""
Created on Sun Feb  2 20:28:10 2025

@author: kolja
"""

from flask import Flask, request

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    if request.method == 'POST':
        print("Data received from Webhook is: ", request.json)
        return "Webhook received!"

app.run(host='0.0.0.0', port=8000)