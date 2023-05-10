import tkinter as tk
import random
import time

class MathsGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Maths Game")

        self.question_count = 0
        self.start_time = time.time()
        self.score = 0
        self.level = "Easy"
        self.create_widgets()

    def create_widgets(self):
        self.level_label = tk.Label(self.master, text="Select Level:")
        self.level_label.grid(row=0, column=0, padx=10, pady=10)

        self.level_var = tk.StringVar(self.master)
        self.level_var.set("Easy")

        self.level_option = tk.OptionMenu(self.master, self.level_var, "Easy", "Medium", "Hard")
        self.level_option.grid(row=0, column=1, padx=10, pady=10)

        self.problem_label = tk.Label(self.master, text="Problem: ")
        self.problem_label.grid(row=1, column=0, padx=10, pady=10)

        self.entry = tk.Entry(self.master)
        self.entry.grid(row=1, column=1, padx=10, pady=10)

        self.submit_button = tk.Button(self.master, text="Submit", command=self.check_answer)
        self.submit_button.grid(row=1, column=2, padx=10, pady=10)

        self.status_label = tk.Label(self.master, text="")
        self.status_label.grid(row=2, columnspan=3, padx=10, pady=10)

        self.update_problem()

    def generate_problem(self):
        num_range = {"Easy": (1, 10), "Medium": (10, 100), "Hard": (100, 1000)}
        self.level = self.level_var.get()
        a, b = random.randint(*num_range[self.level]), random.randint(*num_range[self.level])
        operation = random.choice(["+", "-", "*", "/"])

        if operation == "+":
            result = a + b
        elif operation == "-":
            result = a - b
        elif operation == "*":
            result = a * b
        elif operation == "/":
            b = random.choice([i for i in range(1, a+1) if a % i == 0])
            result = a // b
        return f"{a} {operation} {b}", result

    def update_problem(self):
        if self.question_count < 10 and time.time() - self.start_time < 600:
            problem, self.correct_answer = self.generate_problem()
            self.problem_label["text"] = f"Problem: {problem}"
            self.entry.delete(0, tk.END)
        else:
            self.end_game()

    def check_answer(self):
        try:
            answer = int(self.entry.get())
        except ValueError:
            self.status_label["text"] = "Invalid input. Please enter a number."
            return

        if answer == self.correct_answer:
            self.score += 1
            self.status_label["text"] = "Correct!"
        else:
            self.status_label["text"] = f"Incorrect. The correct answer was {self.correct_answer}."

        self.question_count += 1
        self.update_problem()

    def end_game(self):
        self.problem_label["text"] = f"Game Over! Your score: {self.score}"
        self.entry.grid_forget()
        self.submit_button.grid_forget()

if __name__ == "__main__":
    root = tk.Tk()
    app = MathsGame(root)
    root.mainloop()
