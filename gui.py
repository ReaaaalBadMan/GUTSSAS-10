
import tkinter as tk
from tkinter import *
from scraper import get_event_scrape
import random
import webbrowser

root = tk.Tk()

root.geometry("800x600")
root.title("Night Out Planner")


label = tk.Label(root, text="Plan your ideal night out!", font=("Helvetica", 24))
label.pack(padx=20, pady=20)


def surp_click():
    events = get_event_scrape()
    print(events)

    if events: 
        
        event_list = list(events.items())
        
        random_event = random.choice(event_list)

        event_name = random_event[0]
        event_url = random_event[1]

        print(f"Surprise Event Selected: {event_name} - {event_url}")

        surprise_label.config(text=f"How about: {event_name}?", fg="black")
        webbrowser.open_new_tab(event_url)

def con_click():
    mood = opt1.get()
    group_size = groupsize_entry.get()
    budget = budget_entry.get()

    mood_inval = mood == "Mood"
    gs_inval = not group_size.isdigit() or int(group_size) <= 0
    budget_inval = not budget.isdigit() or int(budget) <=0

    if mood_inval or gs_inval or budget_inval:
        confirmation_label.config(text="Please enter valid inputs for all fields.", fg="red")
    else:
        confirmation_label.config(text=f"Your night out plan: Mood - {mood}, Group Size - {group_size}, Budget - £{budget}", fg="green")

        print(f"Mood: {mood}")
        print(f"Group Size: {group_size}")
        print(f"Budget: £{budget}")


surprise_button = tk.Button(root, text="Surprise Me!", command = surp_click, font = ("Helvetica", 16))
surprise_button.pack(pady=20)

Mood_options = ["Happy", "Adventurous", "Underground", "Chill"]


optionframe = tk.Frame(root)

optionframe.columnconfigure(0, weight=2, minsize=100)
optionframe.columnconfigure(1, weight=1, minsize=100)
optionframe.columnconfigure(2, weight=2, minsize=100)
optionframe.columnconfigure(3, weight=1, minsize=100)
optionframe.columnconfigure(4, weight=2, minsize=100)

optionframe.pack(fill="x", padx=20, pady=20) 


opt1 = StringVar(optionframe)
opt1.set("Mood")
dropdown1 = OptionMenu(optionframe, opt1, *Mood_options)
dropdown1.config(font=("Helvetica", 14), width=12)
dropdown1.grid(row=0, column=0, padx=2, pady=10)


gs_label = tk.Label(optionframe, text="Group size", font=("Helvetica", 14))
gs_label.grid(row=0, column=1, padx=2, sticky="e") 


groupsize_entry = tk.Entry(optionframe, font=("Helvetica", 14), justify="center")
groupsize_entry.grid(row=0, column=2, sticky="ew", padx=5)
groupsize_entry.insert(0,"")


budget_label = tk.Label(optionframe, text="Budget(£)", font=("Helvetica", 14))
budget_label.grid(row=0, column=3, padx=5, sticky="w") 

budget_entry = tk.Entry(optionframe, font=("Helvetica", 14), justify="center")
budget_entry.grid(row=0, column=4, sticky="ew", padx=5)
budget_entry.insert(0, "")

confirm_button = tk.Button(root, text="Confirm", command = con_click, font=("Helvetica", 16))
confirm_button.pack(pady=20)

confirmation_label = tk.Label(root, text="", font=("Helvetica", 14))
confirmation_label.pack(pady=10)

surprise_label = tk.Label(root, text="", font=("Helvetica", 12))
surprise_label.pack(pady=10)

root.mainloop()