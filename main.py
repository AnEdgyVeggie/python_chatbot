from create_chatbot_model import ask_chatbot


def talk_to_chatbot():
    #SAVE INPUTS AND OUTPUTS TO TEXT FILE FOR ANALYSIS

    asking_questions = True
    while asking_questions:
        prompt = input(">  ")
        response = ask_chatbot(prompt)
        if response is None:
            continue
        print(response[0])

        if response[0][1] == "ending":
            asking_questions = False


talk_to_chatbot()