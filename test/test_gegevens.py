import asyncio

DELAY = 0.1  # seconds


async def vul_test_gegevens_in(page):
    print("Kiezen: 2024")
    await select_dropdown(page, "#V1-1_pbt", "2024")
    await asyncio.sleep(DELAY)

    print("Kiezen: zorgtoeslag")
    # await check_checkbox(page, "input#V1-3_pbt_1") # huurtoeslag
    await check_checkbox(page, "input#V1-3_pbt_4")  # zorgtoeslag
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

    print(f"Invoeren: inkomen")
    await fill_field(page, "#V3-10_pbt", "36000", 100)
    await asyncio.sleep(DELAY)

    print("Kiezen: premie")
    await select_radio(page, "label[for='V3-12_pbt_True']")
    await asyncio.sleep(DELAY)

    print("Kiezen: laag vermogen")
    await select_radio(page, "label[for='V11-11_pbt_False']")
    await asyncio.sleep(DELAY)


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
