import asyncio
import os
import re
import sys
import tkinter as tk
import webbrowser
from datetime import datetime
from idlelib.tooltip import Hovertip
from threading import Thread, Event
from tkinter import messagebox

from playwright.async_api import async_playwright, expect

from test.test_gegevens import vul_test_gegevens_in

stapgrootte = 50

# Global variable to control the loop
pause_event = Event()
stop_event = Event()


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


# Function to validate and update stapgrootte
def update_stapgrootte(event):
    global stapgrootte
    try:
        value = int(stapgrootte_entry.get())
        if 1 <= value <= 1000:
            stapgrootte = value
        else:
            messagebox.showwarning("Ongeldige waarde", "De stapgrootte moet tussen 1 en 1000 zijn")
            stapgrootte_entry.delete(0, tk.END)
    except ValueError:
        messagebox.showwarning("Invalid Input", "Voer een geldig nummer in")
        stapgrootte_entry.delete(0, tk.END)

    stapgrootte_entry.insert(0, str(stapgrootte))


async def run_playwright():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()
        page.set_default_timeout(0)  # Disable timeout

        print("Website laden")
        await page.goto(
            'https://www.belastingdienst.nl/wps/wcm/connect/nl/toeslagen/content/hulpmiddel-proefberekening-toeslagen')

        await vul_test_gegevens_in(page)  # TEST

        print(f"Het script start wanneer je op 'Toon resultaten' drukt")
        button = page.locator("#butResults_pbt")
        await expect(button).to_be_hidden(timeout=0)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        resultaat_bestand_path = f"resultaten/toeslagen_{timestamp}.csv"
        os.makedirs("resultaten", exist_ok=True)  # maak resultaat folder aan als het nog niet bestaat
        schrijf_resultaten(resultaat_bestand_path, "inkomen", "huurtoeslag", "zorgtoeslag", "kinderopvangtoeslag",
                           "kindergevonden_budget")
        print(f"Gestart! Resultaten worden geschreven naar {resultaat_bestand_path}")

        while True:
            pause_event.wait()  # Wait if the pause event is not set
            if stop_event.is_set():
                print(f"Gestopt")
                break

            # haal toeslag resultaten op
            inkomen = await get_inkomen(page)
            toeslagen_text = await get_toeslagen(page)
            zorgtoeslag = get_toeslag(toeslagen_text, "zorgtoeslag")
            huurtoeslag = get_toeslag(toeslagen_text, "huurtoeslag")
            kinderopvangtoeslag = get_toeslag(toeslagen_text, "kinderopvangtoeslag")
            kindergebonden_budget = get_toeslag(toeslagen_text, "kindgebonden budget")

            # schrijf resultaten weg
            print(
                f"{inkomen=}: {zorgtoeslag=}, {huurtoeslag=}, {kinderopvangtoeslag=}, {kindergebonden_budget=}")
            schrijf_resultaten(resultaat_bestand_path, inkomen, zorgtoeslag, huurtoeslag, kinderopvangtoeslag,
                               kindergebonden_budget)

            # klik 'Wijzig invoer'
            locator = page.locator("#butWijzig_pbt")
            await locator.click()

            # voer een verhoogd inkomen in
            inkomen += stapgrootte
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
    # Set the event to resume execution
    pause_event.set()
    # Create a new asyncio event loop and run the Playwright coroutine
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(run_playwright())


def start_process():
    start_button.config(state=tk.DISABLED)
    pause_button.config(state=tk.ACTIVE)
    stop_button.config(state=tk.ACTIVE)
    if not pause_event.is_set():
        pause_event.set()
        Thread(target=start_playwright).start()


def toggle_pause():
    if pause_event.is_set():
        pause_event.clear()
        pause_button.config(text="Pauzeren", command=toggle_pause)
    else:
        pause_event.set()
        pause_button.config(text="Hervatten", command=toggle_pause)


def stop_process():
    stop_event.set()
    if pause_event.is_set():
        pause_event.clear()


def on_escape(event):
    stop_process()
    root.destroy()


def open_github():
    webbrowser.open("https://github.com/jort-dev/toeslagen_scraper")


# Main window
root = tk.Tk()
root.title("Toeslagen scraper")
root.geometry("400x300")
root.resizable(False, False)
root.bind("<Escape>", on_escape)
tooltip_delay = 200

# Title label
title_label = tk.Label(root, text="Toeslagenscraper", font=("Helvetica", 16, "bold"))
# title_label.pack(pady=10)
title_label.pack(pady=1)

# GitHub link
link = tk.Label(root, text="https://github.com/jort-dev/toeslagen_scraper", fg="blue", cursor="hand2")
link.pack()
link.bind("<Button-1>", lambda e: open_github())

# Explanation text
explanation_label = tk.Label(root, text="1. Kies de stapgrootte\n2. Klik start\n3. Voer je gegevens in.\n4. Klik op 'Toon resultaten' om het proces te starten!", justify="left")
explanation_label.pack(pady=10)

# Stapgrootte input
stapgrootte_frame = tk.Frame(root)
stapgrootte_frame.pack(pady=5)

stapgrootte_label = tk.Label(stapgrootte_frame, text="Stapgrootte: ")
stapgrootte_label.grid(row=0, column=0)

stapgrootte_entry = tk.Entry(stapgrootte_frame, width=10)
stapgrootte_entry.grid(row=0, column=1)
stapgrootte_entry.insert(0, "50")
# stapgrootte_entry.bind("<FocusOut>", update_stapgrootte)
stapgrootte_entry.bind("<KeyRelease>", update_stapgrootte)

tooltip = "Het script verhoogt steeds het inkomen met dit bedrag"
Hovertip(stapgrootte_entry, tooltip, hover_delay=tooltip_delay)

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
width = 10

# Start button
start_button = tk.Button(buttons_frame, text="Start", command=start_process, width=width)
start_button.grid(row=0, column=0, padx=5)
Hovertip(start_button, "Open de browser om het proces te starten", hover_delay=tooltip_delay)

# Pause button
pause_button = tk.Button(buttons_frame, text="Pauzeren", command=toggle_pause, width=width)
pause_button.grid(row=0, column=1, padx=5)
pause_button.config(state=tk.DISABLED)
Hovertip(pause_button, "Pauzeer het ophalen van toeslagen", hover_delay=tooltip_delay)

# Stop button
stop_button = tk.Button(buttons_frame, text="Stop", command=stop_process, width=width)
stop_button.grid(row=0, column=2, padx=5)
stop_button.config(state=tk.DISABLED)
Hovertip(stop_button, "Sluit de browser af", hover_delay=tooltip_delay)

root.mainloop()
