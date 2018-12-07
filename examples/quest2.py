from walq import Questionnaire
import sys


"""
In the end, we call Questionnaire.validate() to validate for inconsistencies
"""



movies = [  {'name':'Jurassic Park', 'gender': 'dinosaur', 'age':13},
            {'name':'Titanic','gender':'drama', 'age':13},
            {'name':'The Lion King','gender':'disney', 'age':0},
            {'name':'The Grinch','gender':'comedy', 'age':0},
            {'name':'Home Alone','gender':'comedy', 'age':0},
            {'name':'Pokemon','gender':'anime', 'age':0},
            {'name':'Dragon Ball Z','gender':'anime', 'age':13},
            {'name':'Star Wars: Episode IV','gender':'fantasy', 'age':13},
            {'name':'The Exorcist', 'gender':'horror','age':18}  ]

q = Questionnaire()



# Question 1
q.addQuestion('q1', "Hello! I'm walQ, a questionnaire-based chatbot. What is your name?", alias='name', is_initial_question=True)
q.attachResponse('q1', lambda x: f"Nice to meet you, {x.capitalize()}. In this chat I'll help you chosing a movie.")
q.link('q1','q2')



# Question 2
q.addQuestion('q2', "First, I must ask: how old are you?", input_type='number', alias='age') 
def res(x):
    if x < 12: return "You're a kid!"
    elif x < 18: return "Hmm.. a teenager!"
    elif x < 50: return "A young adult"
    else: return "I bet you're old school!'"
def lnk(x):
    if x < 13: return 'q3'
    elif x < 18: return 'q4'
    else: return 'q5'
q.attachResponse('q2',res)
q.link('q2',lnk)



# Question 3
q.addQuestion('q3', "Do you prefer Disney movies, Anime or comedy?", input_type='choice', options=["Disney","Anime", "Comedy"])
def res(x):
    if x==0: movlist = [ m for m in movies if m['gender']=='disney' and m['age']<13 ]
    elif x==1: movlist = [ m for m in movies if m['gender']=='anime' and m['age']<13 ]
    elif x==2: movlist = [ m for m in movies if m['gender']=='comedy' and m['age']<13 ]
    else: movlist=[]
    return f"Here are some movies I found for you: {', '.join([m['name'] for m in movlist])}" if len(movlist)>0 else "Sorry, I didn't find any movies for you =/'"
q.attachResponse('q3',res)



# Question 4
q.addQuestion('q4', "Do you prefer dinosaur movies, fantasy, comedy or drama?", options=['I love dinosaurs','Fantasy, please!','I\'d like to watch a Comedy', 'I prefer Drama'])
def res(x):
    if x==0: movlist = [ m for m in movies if m['gender']=='dinosaur' and m['age']<18 ]
    elif x==1: movlist = [ m for m in movies if m['gender']=='fantasy' and m['age']<18 ]
    elif x==2: movlist = [ m for m in movies if m['gender']=='comedy' and m['age']<18 ]
    elif x==3: movlist = [ m for m in movies if m['gender']=='drama' and m['age']<18 ]
    return f"Here are some movies I found for you: {', '.join([m['name'] for m in movlist])}" if len(movlist)>0 else "Sorry, I didn't find any movies for you =/'"
q.attachResponse('q4',res)



# Question 5
q.addQuestion('q5', "Do you prefer drama, fantasy or horror?",options=['I love Drama','I\'m a Fantasy person','Anime','Horror is great!'])
def res(x):
    movlist =  { 0:[m for m in movies if m['gender']=='drama'],
                 1:[m for m in movies if m['gender']=='fantasy'],
                 2:[m for m in movies if m['gender']=='anime'],
                 3:[m for m in movies if m['gender']=='horror'] }[x]
    return f"Here are some movies I found for you: {', '.join([m['name'] for m in movlist])}" if len(movlist)>0 else "Sorry, I didn't find any movies for you =/'"
q.attachResponse('q5',res)


# Set links
q.setLinks()



# Run the questionnaire
if __name__=='__main__':
    res = q.run()
    print("Here is the data I've recorded from our conversation:")
print(res)
