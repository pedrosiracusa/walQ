from .question import Question
from .response import Response
from .context import Context


class Questionnaire:
    """
    Stores a graph of questions and runs it; keeps track of interactions using a context dictionary.
    """
    
    def __init__(self, questionnaire_dict=None, initial_question_id=None):
        """
        Questionnaire dict to be used to build the instance
        """
        self.initial_question_id = initial_question_id
        
        if questionnaire_dict:
            self.questions = { qname: Question(qname,**qattrs) for qname, qattrs in questionnaire_dict.items() }
            

    def attachResponse(self, question_id, response_message=None, response_condition=None):
        """
        Attaches a response to a question.
        A response can be either a static message (a string) or a condition (a function), in case the response message depends on the user response.
        In case both a message and a condition are passed, the condition is evaluated.

        Parameters:
            question_id: The id of the question to which the response must be attached.
            response_message: The response to be attached to the question, as a static string.
            response_condition: The response to be attached to the question, as a condition that is evaluated using the user input.
        """
        question = self.questions.get(question_id)
        if question:
            question.response = Response(message=response_message, condition=response_condition)

    
    def sendQuestion(self, context):
        """
        Sends current question (from context) to user
        """
        questionId = context.data['current_question']
        q = self.questions.get(questionId)
        context.data['message']=q.promptMessage()
        context.data['user_input']=''
        context.data['input_type']=q.user_input_type
        
        input_options = q.options
        if input_options:
            context.data['input_options']=input_options
            
        input_options_text = q.options_text
        if input_options_text:
            context.data['input_options_text']=input_options_text

        return context
    
    def saveUserInput(self, context):
        """
        Saves user response (input) to the context, using the question to parse it.
        Finally, clears user input
        input type: 'text','number','choice'
        """
        user_input = context.data.get('user_input','')
        questionId = context.data.get('current_question')
        q = self.questions.get(questionId)
        
        context.data['responses'][questionId] = q.parseUserInput(user_input)

        context.clear_user_input()
        return context
    
    def sendResponse(self, context):
        questionId = context.data.get('current_question')
        user_input = context.data['responses'].get(questionId)
        q = self.questions.get(questionId)
        response = q.respond(context)
        context.data['message'] = response
        context.data['next_question'] = q.getNextQuestionName(user_input)
        return context

    def run(self):
        # Runs the questionnaire locally, for testing purposes

        # Sets context initially
        self.context = Context()
        self.context.set_current_question(self.initial_question_id)
        
        while True:

            # Asks first question
            data = self.sendQuestion(self.context).data

            # Saves user input
            usr_input = input( data.get('message') )
            self.context.set_user_input(usr_input)
            self.saveUserInput(self.context)

            # Sends response
            data = self.sendResponse(self.context).data
            print(data.get('message'))

            # Get next question
            next_question_id = data.get('next_question')
            self.context.set_current_question(next_question_id)

            if not next_question_id:
                return

                




