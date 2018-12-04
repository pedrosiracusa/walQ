#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Future: json context could look like { 'persistent_items': {...}, 'volatile_items': {...} }
persistent_items: should be passed back and forth in all interactions. ex: user_responses
volatile_items: Only make sense for a given, particular interaction. ex: current_question, next_question, message, input_type, input
"""


class Context:
    # TODO: After receiving user input, should send next question in the response
    def __init__(self):
        self.usrinput={}
        self.message=None
        self.usrdata={}
        self.flags={}
        self.from_dict = self.from_json_data # TO REMOVE


    @classmethod
    def from_json_data(cls, datadict):
        ctx = cls()
        ctx.usrinput=datadict.get('usrinput')
        ctx.message=datadict.get('message')
        ctx.usrdata=datadict.get('usrdata',{})
        ctx.flags=datadict.get('flags',{})

        return ctx 

    def to_dict(self):
        return { 'usrinput': self.usrinput,
                'message': self.message,
                'usrdata': self.usrdata,
                'flags': self.flags }
    



    def get_current_question(self):
        return self.flags.get('current_question')

    def set_current_question(self, current_question):
        self.flags['current_question']=current_question



    def get_user_input(self):
        return self.usrinput.get('data','')

    def set_user_input(self, user_input):
        self.usrinput['data']=user_input

    def set_input_options(self, options):
        self.usrinput['options'] = options

    def set_input_options_text(self, text):
        self.usrinput['options_text'] = text

    def set_input_type(self, input_type):
        self.usrinput['type']=input_type
        
    def reset_user_input(self, new_input, input_type):
        self.set_user_input('')
        self.set_input_type(input_type)

    def clear_user_input(self):
        # TO REMOVE
        self.set_user_input('')



    def get_user_data(self):
        return self.usrdata
    
    def set_user_data(self, data_dict):
        self.usrdata = data_dict



    def set_message(self,message):
        self.message = message

    def get_message(self):
        return self.message

    def set_next_question(self, question_id):
        self.flags['next_question'] = question_id
        self.flags['send_next_question'] = True

    def get_next_question(self):
        return self.flags['next_question']

    def save_user_response(self, question_id, response):
        self.usrdata[question_id] = response

    def read_user_response(self,question_id):
        return self.usrdata.get(question_id)
