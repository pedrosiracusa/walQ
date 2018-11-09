from walq import Questionnaire

q = Questionnaire()

# Question 1
q.addQuestion('q1', "Hello! I'm walQ, a questionnaire-based chatbot. What is your name?", is_initial_question=True)
q.attachResponse('q1', response_condition=lambda x: f"Nice to meet you, {x.capitalize()}") 


# Question 2
q.addQuestion('q2', "Do you want me to demonstrate what I can do?", input_type="choice", options=["No", "Yes"])
q.attachResponse('q2', response_message="Ok, then!")


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
q.attachResponse('q3', response_condition=cond_age)


# Question 4
q.addQuestion('q4', "I can also ask you multiple-choice questions and respond accordingly. Do you prever Marvel or DC?", input_type="choice", options=["Marvel", "DC"])
q.attachResponse('q4', response_condition=lambda x: ["Really??? Me too!", "Nice! But I prever Marvel..."][x])


# Question 5
q.addQuestion('q5',"The flow of the questionnaire can be different based on your answers.\nTo exemplify, do you want me to ask you some personal questions?", input_type="choice", options=["No", "Yes"])
q.attachResponse('q5', response_message="Sweet!")


# Question 6
q.addQuestion('q6', "What is your favorite movie?")



# Question 7
q.addQuestion('q7', "Where would you like to be in 5 years?")
q.attachResponse('q7', response_message="hmm.. interesting!")



# Question 8

q.addQuestion('q8', "What are your most remarkable virtues? And in which aspects do you think you should improve?")
q.attachResponse('q8', response_message="ok then...")



# Question 9
q.addQuestion('q9',"Is there anything else you want to know about me?", input_type="choice", options=["No, thanks!", "There actually is"])
q.attachResponse('q9', response_condition=lambda x: ["Ok! It was nice talking to you. See you later.", "Ok... I'm not much more than what you have just seen... While I still do not have a formal documentation, take a look at the code at \"examples\". See U!"][x] )




# Set links

q.setLink('q1','q2')
q.setLink('q2','q3', condition=1)
q.setLink('q2','q9', condition=0)
q.setLink('q3','q4')
q.setLink('q4','q5')
q.setLink('q5','q6', condition=1)
q.setLink('q5','q9', condition=0)
q.setLink('q6','q7')
q.setLink('q7','q8')
q.setLink('q8','q9')




# Run the questionnaire
res = q.run()
print("Here is the data I've recorded from our conversation:")
print(res)
