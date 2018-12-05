# -*- coding: utf-8 -*-
"""Example of walQ running as a Restful API service.

This module runs a very simple flask restful api for running through the
questionnaire. The api responds to GET requests by sending the initial 
question; and to POST requests by saving user input to the context object
and sending the next question.
"""

from flask import Flask, request
from flask_restful import Api, Resource

from walq import Questionnaire, Context
from examples.quest1 import q

app = Flask(__name__)
api = Api(app)


class Conversation(Resource):
    def get(self):
        # First interaction with the app: send the initial message to user
        return q.sendFirstMessage().to_dict()

    def post(self):
        c = Context.from_dict( request.get_json(force=True) )

        # If user input is set, save it to context and send response to user
        if c.isset_user_input():
            q.saveUserInput(c)
            q.sendResponse(c)
            return c.to_dict()

        # If user input was already processed, send next question to user
        elif c.check_flag('send_next_question'):
            c.remove_flag('send_next_question')
            c.set_current_question( c.get_next_question() )
            q.sendQuestion(c)
            return c.to_dict()
            
        # If there is no question next
        else:
            return c.to_dict()


api.add_resource(Conversation, '/')


if __name__ == '__main__':
    app.run(debug=True)
