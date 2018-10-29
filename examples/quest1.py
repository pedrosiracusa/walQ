from src import Questionnaire  

questionnaire = {
    'q1': {
        "prompt": "Olá! Me chamo Lando! Sou um assistente de terras. Qual seu nome?",
        "input_type": "text",
        "next":['q2']
          },
    'q2': {
        "prompt": "E sua idade?",
        "input_type": "number",
        "next":['q3']
    },
    'q3': {
        "prompt": "Primeiro preciso saber sobre a situação do seu solo. Ele está degradado?",
        "input_type": "choice",
        "options": [0,1],
        "options_text": ["não","sim"],
        "next": ['q4']
    },
    'q4': {
        "prompt": "E pecuária? Tem pecuária na vizinhança?",
        "input_type": "choice",
        "options": [0,1],
        "options_text": [ "não", "sim"],
        "next": ['q5']
    },
    'q5': {
        "prompt": "Tem risco de incêndio?",
        "input_type": "choice",
        "options": [0,1],
        "options_text": [ "não", "sim"],
        "next": ['q6']
    },
    'q6': {
        "prompt": "Qual o potencial de regeneração natural?",
        "input_type": "choice",
        "options": [0,1],
        "options_text": [ "baixo potencial", "alto potencial"],
        "next": ['q7','q8']
    },
    'q7':{
        "prompt": "Prefere plantar mudas ou semear?",
        "input_type": "choice",
        "options": [0,1],
        "options_text": ["plantar mudas", "semear"],
        "next": ['q9', 'q10']
    },
    'q8':{
        "prompt": "Prefere manejar a regeneração natural ou não?",
        "input_type": "choice",
        "options": [0,1],
        "options_text": ["não manejar", "manejar"]
    },
    'q9':{
        "prompt": "Que tipo de muda?",
        "input_type": "text"
    },
    'q10':{
        "prompt": "Que sementes?",
        "input_type": "text"
    }
}

def setup_questionnaire():
    """
    Returns the questionnaire and the context
    """
    q = Questionnaire(questionnaire, initial_question_id='q1')

    # Response to q1
    q.attachResponse( 'q1', response_condition=lambda x: f"Prazer em conhecê-lo, {x}" )

    # Response to q2
    def cond(x):
        if x>=50:
            return "Nunca é tarde para começar!"
        elif x>=30:
            return "Boa idade!"
        elif x>=18:
            return "É ótimo começar cedo!"
        else:
            return "Você tem certeza que deveria estar usando este app?"
    q.attachResponse( 'q2', response_condition=cond )

    # Response to q3
    q.attachResponse( 'q3', response_condition=lambda x: 'Certo... antes você precisará recuperar seu solo.' if x==1 else 'Ótimo!' )

    # Response to q4
    q.attachResponse( 'q4',  response_condition=lambda x: 'Entendo... é importante que vc cerque a área, ok?' if x==1 else 'Bom!')

    # Response to q5
    q.attachResponse( 'q5',  response_condition=lambda x: 'Que tal construir um aceiro?' if x==1 else 'Bom!' )


    # Reponses to q8,q9,q10
    q.attachResponse( 'q8', response_message="Obrigado pela conversa!")
    q.attachResponse( 'q9', response_message="Obrigado pela conversa!")
    q.attachResponse( 'q10', response_message="Obrigado pela conversa!")
            

    return q

if __name__=='__main__':
    q = setup_questionnaire()
    q.run()
