from .question import Question
from .response import Response
from .context import Context


class Questionnaire:
    """
    Stores a graph of questions and runs it; keeps track of interactions using a context dictionary.
    A questionnaire knows how to send questions to user, record user input and respond accordingly.
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

        self.links=[]
            

    def addQuestion(self, id, prompt, input_type="text", is_initial_question=False, options=None, alias=None):
        """
        Adds a new question to the questionnaire.
        """

        # multiple-choice question
        if isinstance(options,list):
            self.questions[id] = Question( id, prompt=prompt, 
                                      input_type='choice',
                                      options=list(range(len(options))),
                                      options_text=options,
                                      alias=alias)

        # text type question
        elif input_type=="text":
            self.questions[id] = Question( id, prompt=prompt, input_type=input_type, alias=alias)


        # Other types (number)
        else:
            self.questions[id] = Question( id, prompt=prompt, input_type=input_type, alias=alias)

        if is_initial_question:
            self.initial_question_id = id

        return self,id
        

    def attachResponse(self, question_id, response):
        """
        Attaches a response to a question from the questionnaire.
        A response can be either a static message (text type) or a condition (function type), in case the response message depends on the user response.

        Parameters:
        ----------
        question_id: The id of the question to which the response must be attached.
        response: string, callable
            The response to be attached to the question.
        """

        question = self.questions.get(question_id)
        if question:
            question.response = Response( response=response)


    def setLink(self, q_src, q_tgt, condition=None):
        """
        Links two questions. If the response attached to the source question is conditional, the link can map to each branch individually. Thus, distinct target questions can be mapped to the same source question, depending on the response given to the user (ultimately, depending on the user input).
        """
        if condition is None:
            self.questions[q_src].next = [q_tgt]

        else:
            if self.questions.get(q_src).next is None: 
                self.questions[q_src].next = [None,None]

            if condition==1:
                self.questions[q_src].next[1]=q_tgt
            else:
                self.questions[q_src].next[0]=q_tgt


    def link(self, q1, q2):
        self.links.append( (q1,q2) )

    def setLinks(self):
        for n_s, n_t in self.links:
            self.questions.get(n_s).next = n_t




    
    def sendQuestion(self, context):
        """
        Sends current question (from context) to user. Changes the context object inplace.
        """
        if not isinstance(context, Context):
            context = Context.from_dict(context)

        questionId = context.get_current_question()
        context.clear_next_question()
        q = self.questions.get(questionId)
        context.set_message( q.promptMessage() )
        context.reset_user_input( '', input_type=q.user_input_type )

        if q.getType()=='choice':
            context.set_input_options(q.options)
            context.set_input_options_text(q.options_text)

        return context
    
    def sendResponse(self, context):
        """
        Sends response to user. Changes the context object inplace.
        """
        if not isinstance(context, Context):
            context = Context.from_dict(context)

        questionId = context.get_current_question()
        user_input = context.read_user_response( questionId )
        q = self.questions.get(questionId)
        response = q.respond(context)
        context.set_message( response )
        if not q.isFinalQuestion():
            context.set_next_question( q.getNextQuestion(user_input) )
        else:
            context.add_flag('last_message')
        return context



    def saveUserInput(self, context):
        """
        Saves user response (input) to the context, using the question to parse it.
        Finally, clears user input
        input type: 'text','number','choice'
        """
        if not isinstance(context, Context):
            context = Context.from_dict(context)

        user_input = context.get_user_input()
        questionId = context.get_current_question()
        q = self.questions.get(questionId)

        context.save_user_response( questionId, q.parseUserInput(user_input) )
        context.clear_user_input()

        return context
    

    
    def sendFirstMessage(self):
        # Sets context initially
        context = Context()
        context.set_current_question(self.initial_question_id)
        return self.sendQuestion(context)


    def getQuestionsAliases(self):
        return { qid: q.alias for qid, q in self.questions.items() if q.alias is not None }


    def run(self):
        # Runs the questionnaire locally, for testing purposes

        # Sets context initially
        context = Context()
        context.set_current_question(self.initial_question_id)
        
        while True:

            # Asks first question
            msg = self.sendQuestion(context).get_message(with_options=True)

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

                




