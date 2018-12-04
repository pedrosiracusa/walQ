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

        else:
            self.questions = dict()
            

    def addQuestion(self, id, prompt, input_type="text", is_initial_question=False, options=None):

        # text type question
        if input_type=="text":
            self.questions[id] = Question( id, prompt=prompt, input_type=input_type)

        # multiple-choice question
        elif input_type=="choice":
            self.questions[id] = Question( id, prompt=prompt, 
                                      input_type=input_type,
                                      options=list(range(len(options))),
                                      options_text=options)

        # Other types (number)
        else:
            self.questions[id] = Question( id, prompt=prompt, input_type=input_type)

        if is_initial_question:
            self.initial_question_id = id
        

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

    def setLink(self, q_src, q_tgt, condition=None):
        if condition is None:
            self.questions[q_src].next = [q_tgt]

        else:
            if self.questions.get(q_src).next is None: 
                self.questions[q_src].next = [None,None]

            if condition==1:
                self.questions[q_src].next[1]=q_tgt
            else:
                self.questions[q_src].next[0]=q_tgt



    
    def sendQuestion(self, context):
        """
        Sends current question (from context) to user
        """
        if not isinstance(context, Context):
            context = Context.from_json_data(context)

        questionId = context.get_current_question()
        q = self.questions.get(questionId)
        context.set_message( q.promptMessage() )
        context.reset_user_input( '', input_type=q.user_input_type )
        
        input_options = q.options
        if input_options:
            context.set_input_options(input_options)
            
        input_options_text = q.options_text
        if input_options_text:
            context.set_input_options_text(input_options_text)


        return context
    
    def saveUserInput(self, context):
        """
        Saves user response (input) to the context, using the question to parse it.
        Finally, clears user input
        input type: 'text','number','choice'
        """
        if not isinstance(context, Context):
            context = Context.from_json_data(context)

        user_input = context.get_user_input()
        questionId = context.get_current_question()
        q = self.questions.get(questionId)
        
        context.save_user_response( questionId, q.parseUserInput(user_input) )
        context.clear_user_input()

        return context
    
    def sendResponse(self, context):
        if not isinstance(context, Context):
            context = Context.from_json_data(context)

        questionId = context.get_current_question()
        user_input = context.read_user_response( questionId )
        q = self.questions.get(questionId)
        response = q.respond(context)
        context.set_message( response )
        context.set_next_question( q.getNextQuestionName(user_input) )
        return context

    
    def sendFirstMessage(self):
        # Sets context initially
        context = Context()
        context.set_current_question(self.initial_question_id)
        return self.sendQuestion(context)



    def run(self):
        # Runs the questionnaire locally, for testing purposes

        # Sets context initially
        context = Context()
        context.set_current_question(self.initial_question_id)
        
        while True:

            # Asks first question
            msg = self.sendQuestion(context).get_message()

            # Saves user input
            usr_input = input( msg )
            context.set_user_input(usr_input)
            self.saveUserInput(context)

            # Sends response
            respMsg = self.sendResponse(context).get_message()
            print(respMsg)

            # Get next question
            next_question_id = context.get_next_question()
            context.set_current_question(next_question_id)

            if not next_question_id:
                return context.usrdata

                




