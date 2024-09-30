import asyncio

DELAY = 0.1  # seconds


async def vul_uitgebreide_test_gegevens_in(page):
    print("Kiezen: 2024")
    await select_dropdown(page, "#V1-1_pbt", "2024")
    await asyncio.sleep(DELAY)

    print("Kiezen: alle toeslagen")
    # await check_checkbox(page, "input#V1-3_pbt_1") # huurtoeslag
    await check_checkbox(page, "input#V1-3_pbt_0")  # zorgtoeslag
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

    print(f"Kiezen: ik werk")
    await select_radio(page, "label[for='V3-2_pbt_True']")
    await asyncio.sleep(DELAY)

    print(f"Invoeren: inkomen")
    await fill_field(page, "#V3-10_pbt", "20000", 100)
    await asyncio.sleep(DELAY)

    print("Kiezen: premie")
    await select_radio(page, "label[for='V3-12_pbt_True']")
    await asyncio.sleep(DELAY)

    print(f"Kiezen: thuiswonende kinderen")
    await select_radio(page, "label[for='V6-1_pbt_True']")
    await asyncio.sleep(DELAY)

    print(f"Kiezen: geen co-ouder")
    await select_radio(page, "label[for='V6-3_pbt_False']")
    await asyncio.sleep(DELAY)

    print(f"Kiezen: 1 kind")
    await select_dropdown(page, "#V6-4_pbt", "1")
    await asyncio.sleep(DELAY)

    print(f"Invoeren: geboortedatum kind")
    await fill_field(page, "#V6-5-1_pbt-1", "2")
    await asyncio.sleep(DELAY)
    await fill_field(page, "#V6-5-1_pbt-2", "2")
    await asyncio.sleep(DELAY)
    await fill_field(page, "#V6-5-1_pbt-3", "2020", 100)
    await asyncio.sleep(DELAY)

    print(f"Kiezen: kind thuiswonend")
    await select_radio(page, "label[for='V6-24-1_pbt_True']")
    await asyncio.sleep(DELAY)

    print(f"Kiezen: kind gaat kinderopvang")
    await select_radio(page, "label[for='V6-9-1_pbt_True']")
    await asyncio.sleep(DELAY)


    print(f"Kiezen: buitenschoolse opvang")
    await select_radio(page, "label[for='V7-1-1_pbt_1']")
    await asyncio.sleep(DELAY)

    print(f"Kiezen: kindercentrum")
    await select_dropdown(page, "#V7-2-a-1-1_pbt", "Kindercentrum")
    await asyncio.sleep(DELAY)

    print(f"Invoeren: opvanguren per maand")
    await fill_field(page, "#V7-2-b-1-1_pbt", "40")

    print(f"Invoeren: uurtarief")
    await fill_field(page, "#V7-2-c-1-1_pbt", "11,00")

    print(f"Kiezen: kinderbijslag")
    await select_radio(page, "label[for='V8-1-1_pbt_True']")
    await asyncio.sleep(DELAY)

    print(f"Kiezen: kind inkomen")
    await select_radio(page, "label[for='V6-14-1_pbt_False']")
    await asyncio.sleep(DELAY)

    print(f"Kiezen: geen huisgenoten")
    await select_radio(page, "label[for='V9-1_pbt_False']")
    await asyncio.sleep(DELAY)

    print(f"Kiezen: geen kamers")
    await select_radio(page, "label[for='V10-1_pbt_False']")
    await asyncio.sleep(DELAY)

    print(f"Kiezen: geen groepswoning")
    await select_radio(page, "label[for='V10-2_pbt_False']")
    await asyncio.sleep(DELAY)

    print(f"Kiezen: geen aanpassing huurhuis")
    await select_radio(page, "label[for='V10-5_pbt_False']")
    await asyncio.sleep(DELAY)

    print(f"Invullen: kale huur")
    await fill_field(page, "#V10-10_pbt", "500,00", 100)
    await asyncio.sleep(DELAY)

    print(f"Kiezen: geen servicekosten")
    await select_radio(page, "label[for='V10-11_pbt_False']")
    await asyncio.sleep(DELAY)

    print("Kiezen: laag vermogen")
    await select_radio(page, "label[for='V11-3_pbt_False']")
    await asyncio.sleep(DELAY)

    print("Kiezen: laag vermogen kind")
    await select_radio(page, "label[for='V11-6_pbt_False']")
    await asyncio.sleep(DELAY)


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
