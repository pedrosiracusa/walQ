from flask import Flask, request
from flask_restful import Api, Resource

from src import Questionnaire
from quest1 import q

app = Flask(__name__)
api = Api(app)


class Conversation(Resource):
    def get(self):
        # First interaction with the app: send the initial message to user
        return q.sendFirstMessage()

    def post(self):
        c=request.get_json(force=True)

        # If user input is set
        if c.get('user_input','') != '':
            c = q.saveUserInput(c)
            c = q.sendResponse(c)
            return c.data

        # If user input was already processed, send next question
        elif c.get('current_question') in c['responses'].keys():
            c['current_question']=c['next_question']
            c = q.sendQuestion(c)
            return c.data
            
        else:
            return c


api.add_resource(Conversation, '/')


if __name__ == '__main__':
    app.run(debug=True)