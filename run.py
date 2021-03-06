'''
Typekwondo
Typing game with different themes of answers.
User can set different difficulties which have an
effect on their score. Scores are compiled in a
google sheets database and a sorted version
can be accessed for highscores
'''

import random
import os
import time
import string
import gspread
from prettytable import PrettyTable
from google.oauth2.service_account import Credentials
import answers


SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('leaderboard')
leaderboard = SHEET.worksheet('Sheet1')
ordered_leaderboard = SHEET.worksheet("highscore")

print("  _______               _                            _       ")
print(" |__   __|             | |                          | |      ")
print("    | |_   _ _ __   ___| | ___      _____  _ __   __| | ___  ")
print("    | | | | | '_ \ / _ \ |/ | \ /\ / / _ \| '_ \ / _` |/ _ \ ")
print("    | | |_| | |_) |  __/   < \ V  V / (_) | | | | (_| | (_) |")
print("    |_|\__, | .__/ \___|_|\_\ \_/\_/ \___/|_| |_|\__,_|\___/ ")
print("        __/ | |                                              ")
print("       |___/|_|                                              ")
print("\n")


class User:
    '''
    Creates an instance of User. A user object has 3 attributes which
    are name, score and difficulty. These correspond to the data required
    in the database.
    '''
    def __init__(self):

        while True:
            name = input("What is your name? \n")
            print(f"You have entered {name}")
            print("Is this correct?")
            correct_name = name_check()
            if correct_name == 1:
                self.name = name
                break
        self.score = 0
        self.difficulty = ""
        clear_screen()
        print(f"Hi {self.name}")


class Quiz:
    '''
    Creates an instance of Quiz. A quiz class has two methods
    which are used to select the quiz theme and the difficulty.
    The results of these methods for the attributes.
    '''

    def __init__(self):
        self.answers = self.select_theme()
        self.lives = self.select_difficulty()

    def select_theme(self):
        '''
        Function enabling user to select the theme of the typing challenge.
        '''
        while True:
            print("Typing themes:")
            print("1 - Star Wars")
            print("2 - Harry Potter")
            print("3 - Periodic table of elements")
            print("4 - Popular Cheeses")
            print("5 - Populous Countries")
            theme_selection = input(
                                "Please enter the number of your choice: \n")
            if theme_selection == "1":
                answer_set = random.sample(
                                answers.STAR_WARS, len(answers.STAR_WARS))
                return answer_set
            elif theme_selection == "2":
                answer_set = random.sample(
                                answers.HARRY_POTTER, len(
                                    answers.HARRY_POTTER))
                return answer_set
            elif theme_selection == "3":
                answer_set = random.sample(
                                answers.ELEMENTS, len(answers.ELEMENTS))
                return answer_set
            elif theme_selection == "4":
                answer_set = random.sample(
                                answers.CHEESE, len(answers.CHEESE))
                return answer_set
            elif theme_selection == "5":
                answer_set = random.sample(
                                answers.COUNTRIES, len(answers.COUNTRIES))
                return answer_set
            else:
                clear_screen()
                print(f"You have entered {theme_selection}")
                print("Please enter the number of one of the options provided")

    def select_difficulty(self):
        '''
        Function enabling user to select the difficulty of the game.
        Selecting the difficulty changes the number of lives
        a user has to play the game.
        '''
        while True:
            print("What difficulty would you like to play?")
            print("1 - Easy - 3 lives - Score *1")
            print("2 - Normal - 2 lives - Score *1.5")
            print("3 - Hard - 1 life - Score *2")
            difficulty_selection = input(
                                "Please enter the number of your choice: \n")
            if difficulty_selection == "1":
                lives = 3
                return lives
            elif difficulty_selection == "2":
                lives = 2
                return lives
            elif difficulty_selection == "3":
                lives = 1
                return lives
            else:
                clear_screen()
                print(f"You have entered {difficulty_selection}")
                print("Please enter the number of one of the options provided")
                print("\n")


class Timer:
    '''
    Creates an instance of Timer. This calculates the time in 60 seconds.
    '''

    def __init__(self):
        self.game_over = time.time() + 60


def new_game():
    '''
    Function which builds the game and questions. It calls the classes to be
    constructed and runs another function which runs through the questions
    '''
    new_user = User()
    new_quiz = Quiz()
    if new_quiz.lives == 3:
        new_user.difficulty = "Easy"
        print(new_user.difficulty)
    elif new_quiz.lives == 2:
        new_user.difficulty = "Normal"
    elif new_quiz.lives == 1:
        new_user.difficulty = "Hard"
    clear_screen()
    print("You will be shown a word. Type the word into the terminal")
    print("as fast as possible and hit enter\n")
    input("The game will start when you hit enter")
    clear_screen()
    new_timer = Timer()
    x = 0
    print(f"Correct: {new_user.score}     Lives: {new_quiz.lives}\n")
    while new_timer.game_over > time.time() and new_quiz.lives != 0:
        print("       "+new_quiz.answers[x]+"\n")
        answer = string.capwords(input("Enter answer: \n").lower())
        if answer == new_quiz.answers[x]:
            new_user.score += 1
        else:
            new_quiz.lives -= 1
        x += 1
        clear_screen()
        print(f"Correct: {new_user.score}     Lives: {new_quiz.lives}\n")
    new_user.score = difficulty_bonus(new_user.score, new_user.difficulty)
    user_result = [new_user.name, new_user.score, new_user.difficulty]
    leaderboard.append_row(user_result)
    print("Gameover!\n")
    print(
        f"{new_user.name} scored {new_user.score} \
on difficulty {new_user.difficulty.lower()}\n")


def menu():
    '''
    Function which is called to play the game. It gives the user a choice
    as to whether they want to start. If they select yes then the game starts
    else they are given the option again.
    '''
    while True:
        print("Please select an option: ")
        print("1 - Start new game")
        print("2 - View leaderboard")
        print("3 - How to play")
        print("4 - Exit game")
        menu_selection = input("Please enter the number of your choice: \n")
        if menu_selection == "1":
            clear_screen()
            new_game()
        elif menu_selection == "2":
            view_highscore()
        elif menu_selection == "3":
            show_rules()
        elif menu_selection == "4":
            clear_screen()
            print("Thanks for playing!")
            print("Goodbye")
            return False
        else:
            clear_screen()
            print(f"You have entered {menu_selection}")
            print("Please enter the number of one of the options provided\n")


def view_highscore():
    '''
    Function retrieves data from an numerically ordered
    spreadsheet and splices the top 5 scores. These
    are then printed in formatted way.
    '''
    clear_screen()
    scores = SHEET.worksheet("highscore").get_all_values()
    highscores = scores[slice(1, 6, 1)]
    table = PrettyTable(scores[0])
    [table.add_row(highscore) for highscore in highscores]
    print(table)
    print("\n")


def name_check():
    '''
    Function to check the validity of input of a yes/no
    question. Contains validation internally which
    calls the function recursively if not met.
    '''
    input_check = input("Press Y for yes and N for no: \n").lower()
    if input_check == "y":
        return 1
    elif input_check == "n":
        clear_screen()
        return 2
    else:
        clear_screen()
        print("You did not enter Y or N")
        print("Please try again")
        return name_check()


def difficulty_bonus(player_score, player_difficulty):
    '''
    Function to add difficulty multipier to score
    '''
    if player_difficulty == "Easy":
        return player_score
    elif player_difficulty == "Normal":
        return player_score * 1.5
    elif player_difficulty == "Hard":
        return player_score * 2


def show_rules():
    '''
    Function which displays how to play the game
    '''
    clear_screen()
    print("Welcome to Typekwondo!\n")
    print("Take a typing challenge and see how you compare to others")
    print("Rules:")
    print("- You have 60 seconds to type as many answers as possible")
    print("- Difficulty affects score and lives.")
    print("- Easy - You have 3 lives and a 1* score multiplier")
    print("- Normal - You have 2 lives and a 1.5* score multiplier")
    print("- Hard - You have 1 lives and a 2* score multiplier")
    print("- If you run out of time or life, the quiz ends")
    print("- You can view the leaderboard of the top 5 typers")
    print("- ! The quiz is not case sensitive !\n")
    print("Good luck!\n")


def clear_screen():
    '''
    Function which clears the terminal
    '''
    os.system('cls' if os.name == 'nt' else 'clear')


menu()
