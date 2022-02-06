#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Source:
- Example: https://www.youtube.com/watch?v=YyIv-y6EXeY
- Code: https://github.com/vadimvvlasov/a-few-simple-python-projects/tree/7ce97b0de5fa73c12a1813899a332e034df87e9f/tkinter-flash-card-project-finished
"""

import os
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import pandas as pd
import random


def next_card():
    global current_card
    current_card = random.choice(to_learn)
    print(current_card["question"])
    canvas.itemconfig(card_title, text="question", fill="black")
    canvas.itemconfig(card_question, text=current_card["question"], fill="black")
    canvas.itemconfig(card_background, image=card_front_img)


def is_known():
    global to_learn
    to_learn.remove(current_card)
    if len(to_learn) == 0:
        restart = messagebox.askokcancel("You rock!!", "Congratulations! You correctly solved all the questions :D\n\nWould you like to keep training?")
        if restart:
            to_learn = select_questions()
            next_card()
        else:
            window.destroy()
    else:
        next_card()


def flip_card(event=None):
    # print('Clicked canvas: ', event.x, event.y, event.widget)
    canvas.itemconfig(card_title, text="answer", fill="white")
    canvas.itemconfig(card_question, text=current_card["answer"], fill="white")
    canvas.itemconfig(card_background, image=card_back_img)


def prepare_questions(selected_files):
    """ Compile all questions from the selected files into a temporary file questions_to_learn.json and read file into
    cariable to_learn.
    """
    questions = []
    for file in selected_files:
        file_questions = pd.read_json(file)
        questions += file_questions.to_dict(orient='records')

    return questions


def select_questions():
    selected_files = filedialog.askopenfilenames(parent=window,
                                                 initialdir=os.getcwd(),
                                                 title="Please select one or more files:",
                                                 filetypes=[('json files', '.json')])
    return prepare_questions(selected_files)


if __name__ == "__main__":

    BACKGROUND_COLOR = "#B1DDC6"
    current_card = {}
    to_learn = {}

    window = tk.Tk()

    to_learn = select_questions()

    window.title("Interview training")
    window.config(padx=25, pady=25, bg=BACKGROUND_COLOR)

    canvas = tk.Canvas(width=800, height=526)
    card_front_img = tk.PhotoImage(file="images/card_front.png")  # Widget which can display images in PGM, PPM, GIF, PNG format."""
    card_back_img = tk.PhotoImage(file="images/card_back.png")
    card_background = canvas.create_image(400, 263, image=card_front_img)
    card_title = canvas.create_text(400, 50, text="Title", font=("Arial", 30, "bold"))
    card_question = canvas.create_text(400, 250, width=750, text="question", font=("Arial", 16, "normal"))

    canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
    canvas.grid(row=0, column=0, columnspan=3)

    canvas.bind('<Button-1>', flip_card)

    cross_image = tk.PhotoImage(file="images/wrong.png")
    unknown_button = tk.Button(image=cross_image, highlightthickness=0, command=next_card)
    unknown_button.grid(row=1, column=0)

    flip_image = tk.PhotoImage(file="images/flip.png")
    known_button = tk.Button(image=flip_image, highlightthickness=0, command=flip_card)
    known_button.grid(row=1, column=1)

    check_image = tk.PhotoImage(file="images/right.png")
    known_button = tk.Button(image=check_image, highlightthickness=0, command=is_known)
    known_button.grid(row=1, column=2)

    next_card()

    window.mainloop()
