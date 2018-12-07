# -*- coding: utf-8 -*-
"""Example of an application using walQ Restful API.

This module runs a very simple application which interacts with the walQ
restful api. Notice that none of the modules which implement walQ need to
be loaded by the client application.
"""

import os
import requests
import json
import re
from flask import Flask, request, session, render_template


app = Flask(__name__)
app.secret_key = os.urandom(24)

api_endpoint = 'http://localhost:5000'


def updateMessages(session,context_data):
    usrinput=context_data.get('usrinput')
    if usrinput['data']=='':
        if context_data['message'] is None:
            return session
        else:
            session['messages_history'].append(context_data['message'])
    elif usrinput['type']=='choice':
        session['messages_history'].append(usrinput.get('options_text')[ int(usrinput['data']) ])
    else:
        session['messages_history'].append(usrinput.get('data'))
    return session

@app.route('/', methods=['GET','POST'])
def initialize():

    if request.method=='GET':
        session.clear()
        context_data = requests.get(api_endpoint).json()
        session['walq_context_data'] = context_data
        session['messages_history'] = list()
        message = context_data.get('message')
        updateMessages(session,context_data)
        return render_template('form.html',send_input=True, messages=session['messages_history']) 
        

    elif request.method=='POST':

        # Get user input from the form and save it to context
        context_data = session['walq_context_data'] 
        usr_input = request.form.get('input')
        context_data['usrinput'].update({'data':usr_input})
        updateMessages(session,context_data)

        # Post the context object (with user input set) and receive new context containing the api response
        context_data = requests.post(api_endpoint, data=json.dumps(context_data)).json()
        answer = context_data.get('message')
        updateMessages(session,context_data)


        # If this is the last message (no more questions from the api)
        if 'last_message' in context_data.get('flags'):
            return render_template('form.html', 
                    messages=session['messages_history'],
                    send_input=False, 
                    conv_data=context_data.get('usrdata'))

        # If this is not the last message (there are next questions), ask for the next question
        else:
            context_data = requests.post(api_endpoint, data=json.dumps(context_data)).json()

            # Update session data (context)
            session['walq_context_data']=context_data
            updateMessages(session,context_data)

            if context_data.get('usrinput').get('type')=='choice':
                return render_template('form.html', send_input=True,
                        messages=session['messages_history'],
                        input_type=context_data.get('usrinput').get('type'), 
                        input_vals=[ list(i) for i in zip(context_data.get('usrinput').get('options'), context_data.get('usrinput').get('options_text')) ])
            else:
                return render_template('form.html',send_input=True, answer=answer, messages=session['messages_history'])



    


if __name__ == '__main__':
    app.run(debug=True, port=5001)
