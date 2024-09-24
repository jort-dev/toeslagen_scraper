import tkinter as tk
import webbrowser

# Function to open the GitHub link
def open_github():
    webbrowser.open("https://github.com/jort-dev/toeslagen_scraper")

# Main window
root = tk.Tk()
root.title("Toeslagenscraper")
root.geometry("400x300")
root.resizable(False, False)

# Title label
title_label = tk.Label(root, text="Toeslagenscraper", font=("Helvetica", 16, "bold"))
title_label.pack(pady=10)

# GitHub link
link = tk.Label(root, text="https://github.com/jort-dev/toeslagen_scraper", fg="blue", cursor="hand2")
link.pack()
link.bind("<Button-1>", lambda e: open_github())

# Explanation text
explanation_label = tk.Label(root, text="1. Kies de stapgrootte\n2. Klik start\n3. Voer je gegevens in.", justify="left")
explanation_label.pack(pady=10)

# Values display area
values_frame = tk.Frame(root)
values_frame.pack(pady=10)

salaris_label = tk.Label(values_frame, text="Salaris:")
salaris_label.grid(row=0, column=0, padx=5)

huurtoeslag_label = tk.Label(values_frame, text="Huurtoeslag:")
huurtoeslag_label.grid(row=0, column=1, padx=5)

zorgtoeslag_label = tk.Label(values_frame, text="Zorgtoeslag:")
zorgtoeslag_label.grid(row=0, column=2, padx=5)

# Buttons frame
buttons_frame = tk.Frame(root)
buttons_frame.pack(pady=10)

start_button = tk.Button(buttons_frame, text="Start", width=10)
start_button.grid(row=0, column=0, padx=5)

pause_button = tk.Button(buttons_frame, text="Pause", width=10)
pause_button.grid(row=0, column=1, padx=5)

stop_button = tk.Button(buttons_frame, text="Stop", width=10)
stop_button.grid(row=0, column=2, padx=5)

root.mainloop()
