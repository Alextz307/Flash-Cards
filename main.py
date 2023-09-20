from tkinter import *
import pandas
import random


BACKGROUND_COLOR = "#B1DDC6"
SECOND_TO_MS = 1000

try:
    card_data = pandas.read_csv('data/words_to_learn.csv')
except FileNotFoundError:
    to_learn = pandas.read_csv('data/french_words.csv').to_dict(orient='records')
else:
    to_learn = card_data.to_dict(orient='records')

random_card = {}


def generate_card():
    global random_card, flip_timer

    random_card = random.choice(to_learn)

    canvas.itemconfig(canvas_image, image=card_front_image)
    canvas.itemconfig(title_id, text='French', fill='black')
    canvas.itemconfig(word_id, text=random_card['French'], fill='black')

    window.after_cancel(flip_timer)
    flip_timer = window.after(3 * SECOND_TO_MS, flip_card)


def flip_card():
    canvas.itemconfig(canvas_image, image=card_back_image)
    canvas.itemconfig(title_id, text='English', fill='white')
    canvas.itemconfig(word_id, text=random_card['English'], fill='white')


def known_card():
    to_learn.remove(random_card)

    to_learn_data_frame = pandas.DataFrame(to_learn)
    to_learn_data_frame.to_csv('data/words_to_learn.csv', index=False)

    generate_card()


window = Tk()
window.title('Flashy')
window.config(bg=BACKGROUND_COLOR, padx=50, pady=50)

canvas = Canvas(width=800, height=526)
card_front_image = PhotoImage(file='images/card_front.png')
card_back_image = PhotoImage(file='images/card_back.png')
canvas_image = canvas.create_image(400, 263, image=card_front_image)
canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
title_id = canvas.create_text(400, 150, text='Title', font=('Ariel', 40, 'italic'), fill='black')
word_id = canvas.create_text(400, 263, text='Word', font=('Ariel', 60, 'bold'), fill='black')
canvas.grid(row=0, column=0, columnspan=2)

wrong_image = PhotoImage(file='images/wrong.png')
wrong_button = Button(image=wrong_image)
wrong_button.config(borderwidth=0, bd=0, padx=0, pady=0, highlightthickness=0, command=generate_card)
wrong_button.grid(row=1, column=0)

right_image = PhotoImage(file='images/right.png')
right_button = Button(image=right_image)
right_button.config(borderwidth=0, bd=0, padx=0, pady=0, highlightthickness=0, command=known_card)
right_button.grid(row=1, column=1)

flip_timer = window.after(1, generate_card)

window.mainloop()
