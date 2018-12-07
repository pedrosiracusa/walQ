from walq import Questionnaire

q = Questionnaire()

# Question 1
q.addQuestion('q1', "Hello! I'm walQ, a questionnaire-based chatbot. What is your name?", is_initial_question=True)
q.attachResponse('q1', lambda x: f"Nice to meet you, {x.capitalize()}") 
q.link('q1','q2')


# Question 2
q.addQuestion('q2', "Do you want me to demonstrate what I can do?", options=["No", "Yes"])
q.attachResponse('q2', "Ok, then!")
q.link('q2', lambda x: {1:'q3',0:'q9'}[x])


# Question 3
q.addQuestion('q3',"First, I can ask you questions that expect either a text or numerical input (I've shown the text type when I asked your name).\nTo exemplify the numerical, tell me... how old are you?", input_type="number")
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
q.attachResponse('q3', cond_age)
q.link('q3','q4')


# Question 4
q.addQuestion('q4', "I can also ask you multiple-choice questions and respond accordingly. Do you prever Marvel or DC?", options=["Marvel", "DC"])
q.attachResponse('q4', lambda x: ["Really??? Me too!", "Nice! But I prever Marvel..."][x])
q.link('q4','q5')


# Question 5
q.addQuestion('q5',"The flow of the questionnaire can be different based on your answers.\nTo exemplify, do you want me to ask you some personal questions?", options=["No", "Yes"])
q.attachResponse('q5', "Sweet!")
q.link('q5', lambda x: ['q9','q6'][x])


# Question 6
q.addQuestion('q6', "What is your favorite movie?")
q.link('q6','q7')



# Question 7
q.addQuestion('q7', "Where would you like to be in 5 years?")
q.attachResponse('q7', "hmm.. interesting!")
q.link('q7','q8')



# Question 8

q.addQuestion('q8', "What are your most remarkable virtues? And in which aspects do you think you should improve?")
q.attachResponse('q8', "ok then...")
q.link('q8','q9')



# Question 9
q.addQuestion('q9',"Is there anything else you want to know about me?", input_type="choice", options=["No, thanks!", "There actually is"])
q.attachResponse('q9', lambda x: ["Ok! It was nice talking to you. See you later.", "Ok... I'm not much more than what you have just seen... While I still do not have a formal documentation, take a look at the code at \"examples\". See U!"][x] )




# Set links
q.setLinks()




# Run the questionnaire
if __name__ == '__main__':
    res = q.run()
    print("Here is the data I've recorded from our conversation:")
    print(res)
