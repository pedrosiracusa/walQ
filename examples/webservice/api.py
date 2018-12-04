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
        c = Context.from_json_data( request.get_json(force=True) )

        # If user input is set, save it to context
        if c.get_user_input() != '':
            c = q.saveUserInput(c)
            c = q.sendResponse(c)
            return c.to_dict()

        # If user input was already processed, send next question
        elif c.flags.get('send_next_question') is not None:
            c.flags.pop('send_next_question')
            c.set_current_question( c.get_next_question() )
            c = q.sendQuestion(c)
            return c.to_dict()
            
        else:
            return c


api.add_resource(Conversation, '/')


if __name__ == '__main__':
    app.run(debug=True)
