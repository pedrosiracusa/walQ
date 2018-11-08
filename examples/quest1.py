from src import Questionnaire


questionnaire = {
    'q1': {
        "prompt": "Hello! I'm walQ, a questionnaire-based chatbot. What is your name?",
        "input_type": "text",
        "next":['q2']
          },
    'q2': {
        "prompt": "Do you want me to demonstrate what I can do?",
        "input_type": "choice",
        "options": [0,1],
        "options_text":["No", "Yes"],
        "next":['q9', 'q3']
    },
    'q3':{
        "prompt": "First, I can ask you questions that expect either a text or numerical input (I've shown the text type when I asked your name).\nTo exemplify the numerical, tell me... how old are you?",
        "input_type": "number",
        "next":['q4']
        },
    'q4': {
        "prompt": "I can also ask you multiple-choice questions and respond accordingly. Do you prever Marvel or DC?",
        "input_type": "choice",
        "options": [0,1],
        "options_text": ["Marvel","DC"],
        "next": ['q5']
    },
    'q5': {
        "prompt": "The flow of the questionnaire can be different based on your answers.\nTo exemplify, do you want me to ask you some personal questions?",
        "input_type": "choice",
        "options": [0,1],
        "options_text": [ "No", "Yes"],
        "next": ['q9','q6']
    },
    'q6': {
        "prompt": "What is your favorite movie?",
        "input_type": "text",
        "next": ['q7']
    },
    'q7': {
        "prompt": "Where would you like to be in 5 years?",
        "input_type": "text",
        "next": ['q8']
    },
    'q8': {
        "prompt": "What are your most remarkable virtues? And in which aspects do you think you should improve?",
        "input_type": "text",
        "next": ['q9']
    },
    'q9': {
        "prompt": "Is there anything else you want to know about me?",
        "input_type": "choice",
        "options": [0,1],
        "options_text": ["No, thanks!", "There actually is"],
        }
}

q = Questionnaire(questionnaire_dict = questionnaire,initial_question_id='q1')

q.attachResponse('q1', response_condition=lambda x: f"Nice to meet you, {x.capitalize()}") 
q.attachResponse('q2', response_message="Ok, then!")

def cond_age(age):
    if age <= 10: return "Wow! Are you a coder already??"
    elif age <=18: return "Now you are fully reponsible for your acts!"
    elif age <20: return "Almost 20!"
    elif age <=27: return "Still a youngster!"
    elif age <30: return "Almost 30!"
    elif age <=37: return "Good age!"
    elif age <40: return "Almost 40!"
    elif age <=47: return "Interesting! a mature person"
    elif age <50: return "Almost 50!"
    else: return "It's never too late to program a chatbot!"

q.attachResponse('q3', response_condition=cond_age)
q.attachResponse('q4', response_condition=lambda x: ["Really??? Me too!", "Nice! But I prever Marvel..."][x])
q.attachResponse('q5', response_message="Sweet!")
q.attachResponse('q7', response_message="hmm.. interesting!")
q.attachResponse('q8', response_message="ok then...")
q.attachResponse('q9', response_condition=lambda x: ["Ok! It was nice talking to you. See you later.", "Ok... I'm not much more than what you have just seen... While I still do not have a formal documentation, take a look at the code at \"examples\". See U!"][x] )

if __name__ =='__main__':
    res = q.run()
    print("Here is the data I recorded from our conversation:")
    print(res)
