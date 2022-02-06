#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import random
import pandas as pd
import tkinter as tk
from tkinter import filedialog


if __name__ == "__main__":

    root = tk.Tk()
    root.withdraw()

    selected_files = filedialog.askopenfilenames(parent=root,
                                                 initialdir=os.getcwd(),
                                                 title="Please select one or more files:",
                                                 filetypes=[('json files', '.json')])
    questions = []
    for file in selected_files:
        file_questions = pd.read_json(file)
        questions += file_questions.to_dict(orient='records')

    tags = set([q["tag"] for q in questions])

    selected_categories = input(f"Select one or more categories, comma separated: {tags}\n>>> ")
    num_questions = int(input(f"How many questions would you like to answer?\n>>> "))

    filtered_questions = [q for q in questions if q['tag'] in selected_categories]
    random.shuffle(filtered_questions)

    for question in filtered_questions[:num_questions]:
        input(f"\n\n================================================\n{question['question']}\n================================================\n")
        print(f"\n{question['answer']}\n")
