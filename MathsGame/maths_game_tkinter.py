import random
import tkinter as tk
from tkinter import messagebox

def generate_question():
    operators = ['+', '-', '*', '/']
    num1 = random.randint(1, 10)
    num2 = random.randint(1, 10)
    operation = random.choice(operators)

    if operation == '/':
        num1 *= num2

    question_text.set(f"{num1} {operation} {num2} = ")
    return eval(f"{num1} {operation} {num2}")

def check_answer():
    try:
        answer = float(entry_answer.get())
    except ValueError:
        result_text.set("Invalid input. Please enter a number.")
        return

    if round(answer, 2) == round(correct_answer.get(), 2):
        result_text.set("Correct!")
        score.set(score.get() + 1)
    else:
        result_text.set(f"Sorry, the correct answer is {correct_answer.get()}.")

    if questions.get() < 10:
        questions.set(questions.get() + 1)
        correct_answer.set(generate_question())
    else:
        result_text.set(f"Game over! Your final score is {score.get()} out of 10!")
        root.after_cancel(timer)
        messagebox.showinfo("Game Over", f"Your final score is {score.get()} out of 10!")

def start_game():
    questions.set(1)
    score.set(0)
    correct_answer.set(generate_question())
    countdown(600)  # 600 seconds = 10 minutes

def countdown(time_left):
    if time_left > 0:
        time_text.set(f"Time remaining: {time_left} seconds")
        global timer
        timer = root.after(1000, countdown, time_left - 1)
    else:
        result_text.set("Time's up!")
        messagebox.showinfo("Time's Up", "10 minutes have passed. The game is over!")

root = tk.Tk()
root.title("Math Game")

questions = tk.IntVar()
score = tk.IntVar()
question_text = tk.StringVar()
result_text = tk.StringVar()
time_text = tk.StringVar()
correct_answer = tk.DoubleVar()

label_time = tk.Label(root, textvariable=time_text)
label_time.pack()

label_question = tk.Label(root, textvariable=question_text)
label_question.pack()

entry_answer = tk.Entry(root)
entry_answer.pack()

button_submit = tk.Button(root, text="Submit", command=check_answer)
button_submit.pack()

label_result = tk.Label(root, textvariable=result_text)
label_result.pack()

button_start = tk.Button(root, text="Start Game", command=start_game)
button_start.pack()

root.mainloop()
