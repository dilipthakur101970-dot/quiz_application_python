# Quiz Application with Proper Comments

import tkinter as tk
from tkinter import messagebox
import json
import random

# ---------------- CONFIG ----------------

# Line 8: Total time for the quiz in seconds

QUIZ_TIME = 30

# Line 11: JSON file containing questions

QUESTION_FILE = "questions.json"

# Line 14: Negative marking value

NEGATIVE_MARKS = -1

# ---------------- LOAD QUESTIONS ----------------

# Line 18: Function to load questions from JSON file

def load_questions():
"""Load quiz questions from a JSON file."""
with open(QUESTION_FILE, "r") as f:
return json.load(f)

# Line 24: Store all questions globally

all_questions = load_questions()

# ---------------- APP CLASS ----------------

class QuizApp:
"""Main Quiz Application Class"""

```
# Line 30: Initialize the app window
def __init__(self, root):
    self.root = root
    self.root.title("Quiz Application")
    self.root.geometry("500x450")

    # Store selected category
    self.category = None

    # Store filtered questions
    self.filtered_questions = []

    # Load category selection screen
    self.create_category_screen()

# ---------------- CATEGORY SCREEN ----------------
# Line 43: Display category selection UI
def create_category_screen(self):
    self.clear_screen()

    tk.Label(self.root, text="Select Category", font=("Arial", 16)).pack(pady=20)

    # Extract unique categories from questions
    categories = list(set(q["category"] for q in all_questions))

    # Create button for each category
    for cat in categories:
        tk.Button(self.root, text=cat, width=20,
                  command=lambda c=cat: self.start_quiz(c)).pack(pady=5)

# ---------------- START QUIZ ----------------
# Line 57: Start quiz based on selected category
def start_quiz(self, category):
    self.category = category

    # Filter questions by category
    self.filtered_questions = [q for q in all_questions if q["category"] == category]

    # Shuffle questions randomly
    random.shuffle(self.filtered_questions)

    # Initialize quiz variables
    self.q_index = 0
    self.score = 0
    self.time_left = QUIZ_TIME

    # Load quiz UI and first question
    self.create_quiz_screen()
    self.load_question()
    self.update_timer()

# ---------------- QUIZ UI ----------------
# Line 76: Create quiz interface
def create_quiz_screen(self):
    self.clear_screen()

    # Display question text
    self.question_label = tk.Label(self.root, text="", font=("Arial", 14), wraplength=400)
    self.question_label.pack(pady=20)

    # Variable to store selected option
    self.var = tk.StringVar()

    # Create radio buttons for options
    self.options = []
    for i in range(4):
        rb = tk.Radiobutton(self.root, text="", variable=self.var, value="", font=("Arial", 12))
        rb.pack(anchor="w")
        self.options.append(rb)

    # Timer label
    self.timer_label = tk.Label(self.root, text=f"Time: {self.time_left}", fg="red")
    self.timer_label.pack(pady=10)

    # Score label
    self.score_label = tk.Label(self.root, text=f"Score: {self.score}")
    self.score_label.pack()

    # Next button
    self.next_btn = tk.Button(self.root, text="Next", command=self.next_question)
    self.next_btn.pack(pady=10)

# ---------------- LOAD QUESTION ----------------
# Line 103: Load current question and options
def load_question(self):
    if self.q_index < len(self.filtered_questions):
        q = self.filtered_questions[self.q_index]

        # Set question text
        self.question_label.config(text=q["question"])

        # Reset selected option
        self.var.set("")

        # Load options into radio buttons
        for i, opt in enumerate(q["options"]):
            self.options[i].config(text=opt, value=opt)
    else:
        # If no questions left, show result
        self.show_result()

# ---------------- NEXT QUESTION ----------------
# Line 121: Handle answer selection and scoring
def next_question(self):
    selected = self.var.get()
    correct = self.filtered_questions[self.q_index]["answer"]

    # Check answer correctness
    if selected == correct:
        self.score += 1
    elif selected != "":
        self.score -= NEGATIVE_MARKS

    # Update score display
    self.score_label.config(text=f"Score: {round(self.score, 2)}")

    # Move to next question
    self.q_index += 1
    self.load_question()

# ---------------- TIMER ----------------
# Line 139: Countdown timer function
def update_timer(self):
    if self.time_left > 0:
        self.time_left -= 1

        # Update timer label
        self.timer_label.config(text=f"Time: {self.time_left}")

        # Call function again after 1 second
        self.root.after(1000, self.update_timer)
    else:
        # Time over condition
        messagebox.showinfo("Time Up", "Time's up!")
        self.show_result()

# ---------------- RESULT ----------------
# Line 154: Display final score
def show_result(self):
    messagebox.showinfo("Result", f"Final Score: {round(self.score, 2)}")
    self.root.destroy()

# ---------------- CLEAR SCREEN ----------------
# Line 160: Remove all widgets from window
def clear_screen(self):
    for widget in self.root.winfo_children():
        widget.destroy()
```

# ---------------- RUN APP ----------------

# Line 166: Entry point of the program

if **name** == "**main**":
root = tk.Tk()
app = QuizApp(root)
root.mainloop()

