import os
import requests
import json
from flask import Flask, request, session, render_template


app = Flask(__name__)
app.secret_key = os.urandom(24)

api_endpoint = 'http://localhost:5000'

@app.route('/', methods=['GET','POST'])
def initialize():
    if request.method=='GET':
        context_data = requests.get(api_endpoint).json()
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

        except:
            message='End'

        # update session data (context)
        session.clear()
        session['context_data']=context_data
        
        return render_template('form.html',message=message, answer=answer)
    


if __name__ == '__main__':
    app.run(debug=True, port=5001)