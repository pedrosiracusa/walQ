class Response:
    def __init__(self, response):
        
        if callable(response):
            self.type='function'
            self.response=response
        else:
            self.type='text'
            self.response=response

        
    def getResponse(self, user_input):       
        if self.type=='function':
            return self.response(user_input)
        else:
            return self.response
