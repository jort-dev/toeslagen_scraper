import asyncio
import re
import tkinter as tk

from playwright.async_api import async_playwright

from test.test_gegevens import vul_test_gegevens_in

STEP = 50  # euros


def get_result(results, tag):
    for str in results:
        if tag not in str:
            continue
        pattern = r"€\s*(\d+)"
        match = re.search(pattern, str)
        if not match:
            continue
        extracted_number = match.group(1)
        return extracted_number


async def get_results(page):
    locator = page.locator("#divE3_pbt")
    strong_locators = locator.locator("strong")
    strong_locators = await strong_locators.all()
    results = []
    for strong_locator in strong_locators:
        txt = await strong_locator.inner_text()
        txt = txt.strip()
        results.append(txt)
    return results


def write_results(huurtoeslag, zorgtoeslag, kinderopvangtoeslag, kindergevonden_budget):
    pass


async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()

        page = await context.new_page()

        print("Website laden")
        await page.goto('https://www.belastingdienst.nl/wps/wcm/connect/nl/toeslagen/content/hulpmiddel-proefberekening-toeslagen')

        await vul_test_gegevens_in(page)  # TEST

        print(f"Resultaten ophalen")
        results = await get_results(page)
        print(results)

        zorgtoeslag = get_result(results, "zorgtoeslag")
        huurtoeslag = get_result(results, "huurtoeslag")
        kinderopvangtoeslag = get_result(results, "kinderopvangtoeslag")
        kindergebonden_budget = get_result(results, "kindgebonden budget")
        print(f"{zorgtoeslag=}, {huurtoeslag=}, {kinderopvangtoeslag=}, {kindergebonden_budget=}")

        print(f"Start berekening vanaf: {inkomen}")
        while True:
            inkomen += STEP

            # wijzig invoer
            await page.evaluate("window.scrollTo(0, 0)")
            locator = page.locator("#butWijzig_pbt")
            await locator.click()

            await instant_fill_field(page, "#V3-10_pbt", str(inkomen))

            await page.evaluate("window.scrollTo(0, 0)")
            locator = page.locator("#butResults_pbt")
            await locator.click()

            results = await get_results(page)
            zorgtoeslag = get_result(results, "zorgtoeslag")
            huurtoeslag = get_result(results, "huurtoeslag")
            kinderopvangtoeslag = get_result(results, "kinderopvangtoeslag")
            kindergebonden_budget = get_result(results, "kindgebonden budget")
            print(f"{inkomen=}: {zorgtoeslag=}, {huurtoeslag=}, {kinderopvangtoeslag=}, {kindergebonden_budget=}")
            await asyncio.sleep(2)

        print(f"Klaar")
        while True:
            await asyncio.sleep(0.1)


asyncio.run(main())
