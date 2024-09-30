import asyncio
import re
import os
from datetime import datetime


from playwright.async_api import async_playwright, expect

from test.test_gegevens import vul_test_gegevens_in

EURO_STAP_GROOTTE = 50


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


async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()

        page = await context.new_page()

        print("Website laden")
        await page.goto('https://www.belastingdienst.nl/wps/wcm/connect/nl/toeslagen/content/hulpmiddel-proefberekening-toeslagen')

        await vul_test_gegevens_in(page)  # TEST

        print(f"Het script start wanneer je op 'Toon resultaten' drukt")
        button = page.locator("#butResults_pbt")
        await expect(button).to_be_hidden()

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        resultaat_bestand_path = f"resultaten/toeslagen_{timestamp}.csv"
        os.makedirs("../resultaten", exist_ok=True)  # maak resultaat folder aan als het nog niet bestaat
        schrijf_resultaten(timestamp, "inkomen", "huurtoeslag", "zorgtoeslag", "kinderopvangtoeslag", "kindergevonden_budget")
        print(f"Gestart! Resultaten worden geschreven naar {resultaat_bestand_path}")

        while True:
            # haal toeslag resultaten op
            inkomen = await get_inkomen(page)
            toeslagen_text = await get_toeslagen(page)
            zorgtoeslag = get_toeslag(toeslagen_text, "zorgtoeslag")
            huurtoeslag = get_toeslag(toeslagen_text, "huurtoeslag")
            kinderopvangtoeslag = get_toeslag(toeslagen_text, "kinderopvangtoeslag")
            kindergebonden_budget = get_toeslag(toeslagen_text, "kindgebonden budget")

            # schrijf resultaten weg
            print(f"{inkomen=}: {zorgtoeslag=}, {huurtoeslag=}, {kinderopvangtoeslag=}, {kindergebonden_budget=}")
            schrijf_resultaten(timestamp, inkomen, zorgtoeslag, huurtoeslag, kinderopvangtoeslag, kindergebonden_budget)

            # klik 'Wijzig invoer'
            locator = page.locator("#butWijzig_pbt")
            await locator.click()

            # voer een verhoogd inkomen in
            inkomen += EURO_STAP_GROOTTE
            locator = page.locator("#V3-10_pbt")
            inkomen = str(inkomen)
            await locator.fill(inkomen[:-1])
            # als we het laatste cijfer niet 'handmatig' typen, heeft de berekening de nieuwe waarde niet door
            await locator.type(inkomen[-1], delay=33)

            # klik 'Toon resultaten'
            locator = page.locator("#butResults_pbt")
            await locator.click()

            # await asyncio.sleep()

        print(f"Klaar")
        while True:
            await asyncio.sleep(0.1)


asyncio.run(main())
