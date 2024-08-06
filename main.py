from create_chatbot_model import ask_chatbot, classes
import os.path as op

def talk_to_chatbot():
    expected_tag = ""

    asking_questions = True
    while asking_questions:
        prompt = input(">  ")
        response = ask_chatbot(prompt)
        if response is None:
            continue
        print(response[0])

        if response[0][1] == "ending":
            asking_questions = False

def gather_training_data():
    class_list = ""
    for index, c in enumerate(classes):
        class_list += f"[{index}]: {c}  |  "

    asking_questions = True
    while asking_questions:
        prompt = input(">  ")
        response = ask_chatbot(prompt)
        if response is None:
            continue
        print(response[0])

        print(f"The tag for this response was: {response[1]}")
        correct_tag = input("1 if this is correct, 2 if this is incorrect: ")

        correct_flag = False
        while not correct_flag:
            if correct_tag == "1":
                file_path = f"{response[1]}.txt"
                file = open(file_path, "a")
                file.write(f"{prompt}\n")
                correct_flag = True

            elif correct_tag == "2":
                print("Please add the expected tag from the list: " + class_list)
                correct_tag = input()
                correct_flag = True
                file_path = f"{classes[int(correct_tag)]}.txt"
                file = open(file_path, "a")
                file.write(f", \"{prompt}\"")
                file.close()


# talk_to_chatbot()
gather_training_data()
