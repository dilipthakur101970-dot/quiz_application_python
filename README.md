# quiz_application_python
import tkinter as tk
from tkinter import messagebox
import json
import random

# ---------------- CONFIG ----------------
QUIZ_TIME = 30  # seconds
QUESTION_FILE = "questions.json"

# ---------------- LOAD QUESTIONS ----------------
def load_questions():
    with open(QUESTION_FILE, "r") as f:
        return json.load(f)

questions = load_questions()
random.shuffle(questions)

# ---------------- APP CLASS ----------------
class QuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Quiz Application")
        self.root.geometry("500x400")

  self.q_index = 0
  self.score = 0
  self.time_left = QUIZ_TIME

   self.question_label = tk.Label(root, text="", font=("Arial", 14), wraplength=400)
   self.question_label.pack(pady=20)

   self.var = tk.StringVar()

   self.options = []
        for i in range(4):
            rb = tk.Radiobutton(root, text="", variable=self.var, value="", font=("Arial", 12))
            rb.pack(anchor="w")
            self.options.append(rb)

  self.timer_label = tk.Label(root, text=f"Time: {self.time_left}", fg="red")
        self.timer_label.pack(pady=10)

  self.next_btn = tk.Button(root, text="Next", command=self.next_question)
        self.next_btn.pack(pady=10)

   self.load_question()
   self.update_timer()

   # ---------------- LOAD QUESTION ----------------
  def load_question(self):
        if self.q_index < len(questions):
            q = questions[self.q_index]
            self.question_label.config(text=q["question"])

   self.var.set(None)
       for i, opt in enumerate(q["options"]):
        self.options[i].config(text=opt, value=opt[0])  # A/B/C/D

  else:
            self.show_result()

   # ---------------- NEXT QUESTION ----------------
   def next_question(self):
        selected = self.var.get()
        correct = questions[self.q_index]["answer"]

  if selected == correct:
            self.score += 1
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
        messagebox.showinfo("Result", f"Your Score: {self.score}")
        self.root.destroy()

# ---------------- RUN APP ----------------
root = tk.Tk()
app = QuizApp(root)
root.mainloop()
