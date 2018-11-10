# -*- coding: utf-8 -*-
"""Example of an application using walQ Restful API.

This module runs a very simple application which interacts with the walQ
restful api. 
"""

import os
import requests
import json
import re
from flask import Flask, request, session, render_template


app = Flask(__name__)
app.secret_key = os.urandom(24)

api_endpoint = 'http://localhost:5000'

@app.route('/', methods=['GET','POST'])
def initialize():
    if request.method=='GET':
        context_data = requests.get(api_endpoint).json()
        session.clear()
        session['context_data'] = context_data
        message = context_data.get('message')
        return render_template('form.html',message=message) 
        

    elif request.method=='POST':
        usr_input = request.form.get('input')
        context_data = session['context_data'] 
        context_data['user_input']=usr_input

        # Get the response
        context_data = requests.post(api_endpoint, data=json.dumps(context_data)).json()
        answer = context_data.get('message')

        # Get next question if it exists
        try:
            context_data = requests.post(api_endpoint, data=json.dumps(context_data)).json()
            message = context_data.get('message')
            message = re.sub("\s*{.*}\s*", "", message)

        except:
            session.clear()
            return render_template('form.html', answer=answer)

        # update session data (context)
        session.clear()
        session['context_data']=context_data
        
        if context_data.get('input_type')=='choice':
            return render_template('form.html',message=message, answer=answer,
                                    input_type=context_data.get('input_type'), 
                                    input_vals=[ list(i) for i in zip(context_data.get('input_options'),context_data.get('input_options_text')) ]
            )
        else:
            return render_template('form.html',message=message, answer=answer)
    


if __name__ == '__main__':
    app.run(debug=True, port=5001)
