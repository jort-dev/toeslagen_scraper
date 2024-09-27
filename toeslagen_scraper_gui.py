import asyncio
import os
import re
import tkinter as tk
import webbrowser
from datetime import datetime
from idlelib.tooltip import Hovertip
from threading import Thread
from tkinter import filedialog

from playwright.async_api import async_playwright, expect

from test.test_gegevens import vul_test_gegevens_in

is_paused = False
is_stopped = False

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
csv_bestand_folder = os.path.join(os.getcwd(), 'resultaten')
csv_bestand = os.path.join(csv_bestand_folder, f"toeslagen_{timestamp}.csv")
os.makedirs(csv_bestand_folder, exist_ok=True)  # maak resultaat folder aan als het nog niet bestaat


def get_toeslag(results, tag):
    for str in results:
        if tag not in str:
            continue
        pattern = r"€\s*(\d+)"
        match = re.search(pattern, str)
        if not match:
            continue
        extracted_number = match.group(1)
        return extracted_number
    return "0"


async def get_toeslagen(page):
    locator = page.locator("#divE3_pbt")
    strong_locators = locator.locator("strong")
    strong_locators = await strong_locators.all()
    results = []
    for strong_locator in strong_locators:
        txt = await strong_locator.inner_text()
        txt = txt.strip()
        results.append(txt)
    return results


async def get_inkomen(page):
    locator = page.locator("#V3-10_pbt")
    inkomen = await locator.input_value()
    inkomen = inkomen.replace(".", "")
    return int(inkomen)


def schrijf_resultaten(filename, inkomen, huurtoeslag, zorgtoeslag, kinderopvangtoeslag, kindergevonden_budget):
    with open(filename, "a") as file:
        line = f"{inkomen},{huurtoeslag},{zorgtoeslag},{kinderopvangtoeslag},{kindergevonden_budget}"
        file.write(line + "\n")
    inkomen_var.set(str(inkomen))
    zorgtoeslag_var.set(str(zorgtoeslag))
    huurtoeslag_var.set(str(huurtoeslag))
    kinderopvangtoeslag_var.set(str(kinderopvangtoeslag))
    kindergebonden_budget_var.set(str(kindergevonden_budget))


def plot_resultaten(from_path, to_path):
    pass


def plot_huidige_resultaten():
    print(f"Plot huidige resultaten")


def vraag_csv_bestand():
    print(f"Bestand vragen met file picker...")
    global csv_bestand
    initial_dir = os.path.join(os.getcwd(), 'resultaten')
    picked_path = filedialog.askopenfilename(initialdir=initial_dir, filetypes=[("CSV files", "*.csv"), ("All files", "*.*")])
    if picked_path:
        csv_bestand = picked_path
        relative_path = os.path.relpath(csv_bestand, os.getcwd())
        plot_source.set(value=f"Plotten: {relative_path}")
        plot_new_button.config(state=tk.NORMAL)
        print(f"Gekozen: {relative_path}")
    else:
        print(f"Niks gekozen")


def validate_input(new_value):
    if new_value == '':
        return True  # allow empty string for easier editing
    try:
        value = int(new_value)
        if 1 <= value <= 1000:
            return True
        else:
            return False
    except ValueError:
        return False


async def run_playwright():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()
        page.set_default_timeout(0)  # Disable timeout

        print("Website laden")
        await page.goto('https://www.belastingdienst.nl/wps/wcm/connect/nl/toeslagen/content/hulpmiddel-proefberekening-toeslagen')

        if str(demo_checkbox_var.get()) == "1":
            await vul_test_gegevens_in(page)  # TEST

        button = page.locator("#butResults_pbt")
        print(f"Wachten tot de 'Toon resultaten' knop tevoorschijn komt. Vul je gegevens in")
        await button.wait_for(timeout=0)
        print(f"Het script start wanneer je op 'Toon resultaten' drukt")
        await expect(button).to_be_hidden(timeout=0)

        schrijf_resultaten(csv_bestand, "inkomen", "huurtoeslag", "zorgtoeslag", "kinderopvangtoeslag",
                           "kindergevonden_budget")
        relative_path = os.path.relpath(csv_bestand, os.getcwd())
        print(f"Gestart! Resultaten worden geschreven naar {relative_path}")

        while True:
            if is_paused:
                await asyncio.sleep(0.1)
                continue

            if is_stopped:
                print(f"Gestopt")
                break

            # haal toeslag resultaten op
            inkomen = await get_inkomen(page)
            toeslagen_text = await get_toeslagen(page)
            zorgtoeslag = get_toeslag(toeslagen_text, "zorgtoeslag")
            huurtoeslag = get_toeslag(toeslagen_text, "huurtoeslag")
            kinderopvangtoeslag = get_toeslag(toeslagen_text, "kinderopvangtoeslag")
            kindergebonden_budget = get_toeslag(toeslagen_text, "kindgebonden budget")

            plot_source.set(value=f"Plotten: {relative_path}")
            plot_new_button.config(state=tk.NORMAL)

            # schrijf resultaten weg
            print(f"{inkomen=}: {zorgtoeslag=}, {huurtoeslag=}, {kinderopvangtoeslag=}, {kindergebonden_budget=}")
            schrijf_resultaten(csv_bestand, inkomen, zorgtoeslag, huurtoeslag, kinderopvangtoeslag, kindergebonden_budget)

            if zorgtoeslag == '0' and huurtoeslag == '0' and kinderopvangtoeslag == '0' and kindergebonden_budget == '0' and auto_stop_var.get() == 1:
                print(f"Auto stop triggered!")
                stop_process()

            # klik 'Wijzig invoer'
            locator = page.locator("#butWijzig_pbt")
            await locator.click()

            # voer een verhoogd inkomen in
            stapgrootte = stapgrootte_spinbox.get()
            if not stapgrootte:
                stapgrootte = "1"
            print(f"Stapgrootte {stapgrootte}")
            inkomen += int(stapgrootte)
            locator = page.locator("#V3-10_pbt")
            inkomen = str(inkomen)
            await locator.fill(inkomen[:-1])
            # als we het laatste cijfer niet 'handmatig' typen, heeft de berekening de nieuwe waarde niet door
            await locator.type(inkomen[-1], delay=33)

            # klik 'Toon resultaten'
            locator = page.locator("#butResults_pbt")
            await locator.click()

        await browser.close()


def start_playwright():
    global is_paused
    global is_stopped
    is_paused = False
    is_stopped = False
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(run_playwright())


def start_process():
    start_button.config(state=tk.DISABLED)
    pause_button.config(state=tk.ACTIVE)
    stop_button.config(state=tk.ACTIVE)
    demo_checkbox.config(state=tk.DISABLED)
    Thread(target=start_playwright).start()


def toggle_pause():
    global is_paused
    if is_paused:
        pause_button.config(text="Pauzeren", command=toggle_pause)
        is_paused = False
    else:
        pause_button.config(text="Hervatten", command=toggle_pause)
        is_paused = True


def stop_process():
    global is_stopped
    global is_paused
    is_stopped = True
    if is_paused:
        toggle_pause()
    stop_button.config(state=tk.DISABLED)
    pause_button.config(state=tk.DISABLED)


def on_escape(event):
    stop_process()
    root.destroy()


def open_github():
    webbrowser.open("https://github.com/jort-dev/toeslagen_scraper")


# Main window
root = tk.Tk()
root.title("Toeslagen scraper")
window_width = 500
window_height = 650
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width // 2) - (window_width // 2)
y = (screen_height // 2) - (window_height // 2)
root.geometry(f"{window_width}x{window_height}+{x}+{y}")
# root.resizable(False, False)
root.bind("<Escape>", on_escape)
tooltip_delay = 200
validate_cmd = root.register(validate_input)

# Title label
title_label = tk.Label(root, text="Toeslagenscraper", font=("Helvetica", 16, "bold"))
# title_label.pack(pady=10)
title_label.pack(pady=1)

# GitHub link
link = tk.Label(root, text="https://github.com/jort-dev/toeslagen_scraper", fg="blue", cursor="hand2")
link.pack()
link.bind("<Button-1>", lambda e: open_github())

# Explanation text
explanation_label = tk.Label(root, text="1. Kies de stapgrootte\n2. Klik 'Start' om de calculator te openen\n3. Vul de calculator in\n4. Klik in de calculator op 'Toon resultaten' om het proces te starten!\n5. Klik 'Plot resultaten'", justify="left")
explanation_label.pack(pady=10)

# settings frame
settings_frame = tk.Frame(root)
settings_frame.pack(anchor="center")

# Stapgrootte input
stapgrootte_frame = tk.Frame(settings_frame)
stapgrootte_frame.pack(pady=5)

stapgrootte_label = tk.Label(stapgrootte_frame, text="Stapgrootte: ")
stapgrootte_label.grid(row=0, column=0)

stapgrootte_var = tk.StringVar(value="50")
stapgrootte_spinbox = tk.Spinbox(stapgrootte_frame, from_=1, to=1000, increment=1, textvariable=stapgrootte_var, validate='key', validatecommand=(validate_cmd, '%P'))
stapgrootte_spinbox.grid(row=0, column=1)
Hovertip(stapgrootte_spinbox, "Het script verhoogt steeds het inkomen met dit bedrag (Kies een waarde tussen 1-1000, tussentijds aanpasbaar)", hover_delay=tooltip_delay)

# auto stop mode
auto_stop_var = tk.IntVar()
auto_stop_checkbox = tk.Checkbutton(settings_frame, text="Stop automatisch", variable=auto_stop_var, anchor="w")
auto_stop_checkbox.pack(anchor="w")
Hovertip(auto_stop_checkbox, "Stop met het ophalen van toeslagen wanneer elke toeslag 0 is", hover_delay=tooltip_delay)

# demo mode
demo_checkbox_var = tk.IntVar(value=1)
demo_checkbox = tk.Checkbutton(settings_frame, text="Demo", variable=demo_checkbox_var, anchor="w")
demo_checkbox.pack(anchor="w")
Hovertip(demo_checkbox, "Vul automatisch test gegevens in voor demonstratie van deze tool", hover_delay=tooltip_delay)

# Buttons frame
control_buttons_frame = tk.Frame(root)
control_buttons_frame.pack(pady=10)
width = 10

# Start button
start_button = tk.Button(control_buttons_frame, text="Start", command=start_process, width=width)
start_button.grid(row=0, column=0, padx=5)
Hovertip(start_button, "Open de browser om het proces te starten", hover_delay=tooltip_delay)

# Pause button
pause_button = tk.Button(control_buttons_frame, text="Pauzeren", command=toggle_pause, width=width)
pause_button.grid(row=0, column=1, padx=5)
pause_button.config(state=tk.DISABLED)
Hovertip(pause_button, "Pauzeer het ophalen van toeslagen", hover_delay=tooltip_delay)

# Stop button
stop_button = tk.Button(control_buttons_frame, text="Stop", command=stop_process, width=width)
stop_button.grid(row=0, column=2, padx=5)
stop_button.config(state=tk.DISABLED)
Hovertip(stop_button, "Sluit de browser af", hover_delay=tooltip_delay)

# resultaten titel
line_frame = tk.Frame(root, height=2, bd=1, relief="sunken")
line_frame.pack(fill="x", padx=20, pady=(10, 5))
header_label = tk.Label(root, text="Resultaten", font=("Helvetica", 12, "bold"))
header_label.pack(pady=(5, 0))  # Padding above and below the header
relative_path = os.path.relpath(csv_bestand, os.getcwd())
Hovertip(header_label, f"Onderstaande waardes worden weggeschreven naar {relative_path}", hover_delay=tooltip_delay)

# write_path_var = tk.StringVar(value=f"Onderstaande waardes worden weggeschreven naar {relative_path}")
# subtitle_label = tk.Label(root, textvariable=write_path_var, font=("Helvetica", 10, "italic"))
# subtitle_label.pack(pady=(0, 10))  # Adjust padding as needed

# tussentijdse waardes tabel
table_frame = tk.Frame(root)
table_frame.pack(pady=10)
inkomen_var = tk.StringVar(value="0")
zorgtoeslag_var = tk.StringVar(value=f"0")
huurtoeslag_var = tk.StringVar(value=f"0")
kinderopvangtoeslag_var = tk.StringVar(value=f"0")
kindergebonden_budget_var = tk.StringVar(value=f"0")
labels = [
    ("Inkomen", inkomen_var),
    ("Zorgtoeslag", zorgtoeslag_var),
    ("Huurtoeslag", huurtoeslag_var),
    ("Kinderopvangtoeslag", kinderopvangtoeslag_var),
    ("Kindergebonden budget", kindergebonden_budget_var),
]
for i, (text, var) in enumerate(labels):  # chatgpt bro
    tk.Label(table_frame, text=text).grid(row=i, column=0, padx=10, pady=5, sticky="w")
    tk.Entry(table_frame, textvariable=var, state="readonly").grid(row=i, column=1, padx=10, pady=5)

# # resultaten titel
# line_frame = tk.Frame(root, height=2, bd=1, relief="sunken")
# line_frame.pack(fill="x", padx=20, pady=(10, 5))
# header_label = tk.Label(root, text="Visualisatie", font=("Helvetica", 12, "bold"))
# header_label.pack(pady=(5, 0))

relative_path = os.path.relpath(csv_bestand, os.getcwd())
plot_source = tk.StringVar(value=f"")
subtitle_label = tk.Label(root, text="Alle getoonde waardes worden weggeschreven naar resultaten.csv", textvariable=plot_source, font=("Helvetica", 10, "italic"))
subtitle_label.pack(pady=(0, 5))

# result buttons
result_buttons_frame = tk.Frame(root)
result_buttons_frame.pack(pady=10)
result_button_width = 15

# plot new button
plot_new_button = tk.Button(result_buttons_frame, text="Visualiseer", command=plot_huidige_resultaten, width=result_button_width)
plot_new_button.grid(row=0, column=0, padx=5)
plot_new_button.config(state=tk.DISABLED)
Hovertip(plot_new_button, "Sla een visualisatie van de toeslag resultaten op", hover_delay=tooltip_delay)

# plot existing button
plot_existing_button = tk.Button(result_buttons_frame, text="Kies ander bestand", command=vraag_csv_bestand, width=result_button_width)
plot_existing_button.grid(row=0, column=1, padx=5)
Hovertip(plot_existing_button, "Kies een ander bestand, bijvoorbeeld van een vorige run, om te visualiseren", hover_delay=tooltip_delay)

root.mainloop()
