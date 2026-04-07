import tkinter as tk
from tkinter import messagebox
import json
import random

# ---------------- CONFIG ----------------

QUIZ_TIME = 30  # seconds
QUESTION_FILE = "questions.json"
NEGATIVE_MARKS = -1  # marks deducted for wrong answer

# ---------------- LOAD QUESTIONS ----------------

def load_questions():
    with open(QUESTION_FILE, "r") as f:
        return json.load(f)

all_questions = load_questions()

# ---------------- APP CLASS ----------------

class QuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Quiz Application")
        self.root.geometry("500x450")

        self.category = None
        self.filtered_questions = []

        self.create_category_screen()

    # ---------------- CATEGORY SCREEN ----------------
    def create_category_screen(self):
        self.clear_screen()

        tk.Label(self.root, text="Select Category", font=("Arial", 16)).pack(pady=20)

        categories = list(set(q["category"] for q in all_questions))

        for cat in categories:
            tk.Button(self.root, text=cat, width=20,
                      command=lambda c=cat: self.start_quiz(c)).pack(pady=5)

    # ---------------- START QUIZ ----------------
    def start_quiz(self, category):
        self.category = category
        self.filtered_questions = [q for q in all_questions if q["category"] == category]
        random.shuffle(self.filtered_questions)

        self.q_index = 0
        self.score = 0
        self.time_left = QUIZ_TIME

        self.create_quiz_screen()
        self.load_question()
        self.update_timer()

    # ---------------- QUIZ UI ----------------
    def create_quiz_screen(self):
        self.clear_screen()

        self.question_label = tk.Label(self.root, text="", font=("Arial", 14), wraplength=400)
        self.question_label.pack(pady=20)

        self.var = tk.StringVar()

        self.options = []
        for i in range(4):
            rb = tk.Radiobutton(self.root, text="", variable=self.var, value="", font=("Arial", 12))
            rb.pack(anchor="w")
            self.options.append(rb)

        self.timer_label = tk.Label(self.root, text=f"Time: {self.time_left}", fg="red")
        self.timer_label.pack(pady=10)

        self.score_label = tk.Label(self.root, text=f"Score: {self.score}")
        self.score_label.pack()

        self.next_btn = tk.Button(self.root, text="Next", command=self.next_question)
        self.next_btn.pack(pady=10)

    # ---------------- LOAD QUESTION ----------------
    def load_question(self):
        if self.q_index < len(self.filtered_questions):
            q = self.filtered_questions[self.q_index]
            self.question_label.config(text=q["question"])

            self.var.set("")  # reset selection
            for i, opt in enumerate(q["options"]):
                self.options[i].config(text=opt, value=opt)
        else:
            self.show_result()

    # ---------------- NEXT QUESTION ----------------
    def next_question(self):
        selected = self.var.get()
        correct = self.filtered_questions[self.q_index]["answer"]

        if selected == correct:
            self.score += 1
        elif selected != "":
            self.score -= NEGATIVE_MARKS

        self.score_label.config(text=f"Score: {round(self.score, 2)}")

        self.q_index += 1
        self.load_question()

    # ---------------- TIMER ----------------
    def update_timer(self):
        if self.time_left > 0:
            self.time_left -= 1
            self.timer_label.config(text=f"Time: {self.time_left}")
            self.root.after(1000, self.update_timer)
        else:
            messagebox.showinfo("Time Up", "Time's up!")
            self.show_result()

    # ---------------- RESULT ----------------
    def show_result(self):
        messagebox.showinfo("Result", f"Final Score: {round(self.score, 2)}")
        self.root.destroy()

    # ---------------- CLEAR SCREEN ----------------
    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

# ---------------- RUN APP ----------------

if __name__ == "__main__":
    root = tk.Tk()
    app = QuizApp(root)
    root.mainloop()