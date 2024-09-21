import asyncio
import re

from playwright.async_api import async_playwright

DELAY = 0.1  # seconds


async def fill_field(page, selector, value, delay=10):
    locator = page.locator(selector)
    await locator.scroll_into_view_if_needed()
    await locator.type(value, delay=delay)


async def check_checkbox(page, input_selector):
    locator = page.locator(input_selector)
    await locator.scroll_into_view_if_needed()
    await locator.click()


async def select_radio(page, label_selector):
    locator = page.locator(label_selector)
    await locator.scroll_into_view_if_needed()
    await locator.click()


async def select_dropdown(page, selector, value):
    # locator = page.locator("label[for='V2-1_pbt_False']")
    locator = page.locator(selector)
    await locator.scroll_into_view_if_needed()
    await locator.select_option(value)


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
        await page.goto(
            'https://www.belastingdienst.nl/wps/wcm/connect/nl/toeslagen/content/hulpmiddel-proefberekening-toeslagen')
        await asyncio.sleep(DELAY)

        print("Kiezen: 2024")
        await select_dropdown(page, "#V1-1_pbt", "2024")
        await asyncio.sleep(DELAY)

        print("Kiezen: zorgtoeslag")
        await check_checkbox(page, "input#V1-3_pbt_4")
        await asyncio.sleep(DELAY)

        print("Kiezen: geen toeslagpartner")
        await select_radio(page, "label[for='V2-1_pbt_False']")
        await asyncio.sleep(DELAY)

        print(f"Invoeren: geboortedatum")
        await fill_field(page, "#V2-3_pbt-1", "1")
        await asyncio.sleep(DELAY)
        await fill_field(page, "#V2-3_pbt-2", "1")
        await asyncio.sleep(DELAY)
        await fill_field(page, "#V2-3_pbt-3", "2000", 100)
        await asyncio.sleep(DELAY)

        print(f"Invoeren: salaris 543")
        await fill_field(page, "#V3-10_pbt", "543", 100)
        await asyncio.sleep(DELAY)

        print("Kiezen: premie")
        await select_radio(page, "label[for='V3-12_pbt_True']")
        await asyncio.sleep(DELAY)

        print("Kiezen: laag vermogen")
        await select_radio(page, "label[for='V11-11_pbt_False']")
        await asyncio.sleep(DELAY)

        print("Klikken: Toon resultaten")
        locator = page.locator("#butResults_pbt")
        await locator.click()

        print(f"Resultaten ophalen")
        results = await get_results(page)
        print(results)

        zorgtoeslag = get_result(results, "zorgtoeslag")
        huurtoeslag = get_result(results, "huurtoeslag")
        kinderopvangtoeslag = get_result(results, "kinderopvangtoeslag")
        kindergebonden_budget = get_result(results, "kindgebonden budget")
        print(f"{zorgtoeslag=}, {huurtoeslag=}, {kinderopvangtoeslag=}, {kindergebonden_budget=}")

        print(f"Klaar")
        while True:
            await asyncio.sleep(0.1)


asyncio.run(main())
