import tkinter as tk
import random
import time
from PIL import Image, ImageTk
from playsound import playsound
import threading

# Difficulty levels
EASY = 10
MEDIUM = 50
HARD = 100

# Mathematical operations
OPERATIONS = ['+', '-', '*', '/']

# Game start time
start_time = time.time()

class MathsGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Maths Game")
        self.score = 0
        self.current_question = 0

        # Load and set background image using PIL
        background_img = Image.open("/Users/amranmuhumad/Desktop/MathsTEST/image.png")
        self.background_photo = ImageTk.PhotoImage(background_img)
        background_lbl = tk.Label(master, image=self.background_photo)
        background_lbl.place(x=0, y=0, relwidth=1, relheight=1)

        self.question_label = tk.Label(master, text="Question:", bg='white')
        self.question_label.pack()

        self.answer_entry = tk.Entry(master)
        self.answer_entry.pack()

        self.submit_button = tk.Button(master, text="Submit", command=self.check_answer)
        self.submit_button.pack()

        self.score_label = tk.Label(master, text="Score: 0", bg='white')
        self.score_label.pack()

        self.result_label = tk.Label(master, text="", bg='white')
        self.result_label.pack()

        self.level_var = tk.StringVar()
        self.level_var.set("Easy")  # default value

        self.level_option = tk.OptionMenu(master, self.level_var, "Easy", "Medium", "Hard")
        self.level_option.pack()

        # Play background music
        self.play_background_music("/Users/amranmuhumad/Desktop/MathsTEST/background_music.mp3")

        self.next_question()

    def next_question(self):
        self.answer_entry.delete(0, 'end')
        if self.current_question < 10 and time.time() - start_time < 600:  # 10 minutes limit
            self.current_question += 1
            self.a = random.randint(1, self.get_max_number())
            self.b = random.randint(1, self.get_max_number())
            self.op = random.choice(OPERATIONS)
            if self.op == '/':
                self.b = random.choice([i for i in range(1, self.get_max_number()+1) if self.a % i == 0])  # Ensure division is exact
            self.question_label['text'] = f"Question {self.current_question}: {self.a} {self.op} {self.b}"
            self.result_label['text'] = ""
        else:
            self.question_label['text'] = "Game Over"
            self.submit_button['state'] = 'disabled'

    def check_answer(self):
        correct = eval(f"{self.a} {self.op} {self.b}")
        try:
            user_answer = float(self.answer_entry.get())
            if user_answer == correct:
                self.score += 1
                self.score_label['text'] = f"Score: {self.score}"
                self.result_label['text'] = "Correct!"
            else:
                self.result_label['text'] = f"Incorrect! The correct answer is {correct}."
        except ValueError:
            pass
        self.next_question()

    def get_max_number(self):
        level = self.level_var.get()
        if level == "Easy":
            return EASY
        elif level == "Medium":
            return MEDIUM
        else:
            return HARD

    def play_background_music(self, music_file):
        def play_sound():
            while True:  # This loop will keep the sound playing indefinitely
                playsound(music_file)

        sound_thread = threading.Thread(target=play_sound)
        sound_thread.start()

root = tk.Tk()
my_game = MathsGame(root)
root.mainloop()
