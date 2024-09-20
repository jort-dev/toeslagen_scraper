import nodriver as uc
import csv
import time

TIMEOUT = 9999


def schrijf_toeslagen_weg(salaris, huurtoeslag, zorgtoeslag):
    with open('toeslagen.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([salaris, huurtoeslag, zorgtoeslag])


async def main():
    driver = await uc.start()
    tab = await driver.get("https://www.belastingdienst.nl/wps/wcm/connect/nl/toeslagen/content/hulpmiddel-proefberekening-toeslagen")
    print(f"Voer je gegevens in, en klik op 'Invoeren'")

    salaris_veld = await tab.select("#V3-10_pbt", timeout=TIMEOUT)
    print(f"Voer het salaris in vanaf waar je wilt gaan rekenen")
    wijzig_invoer_knop = await tab.select("#butWijzig_pbt", timeout=TIMEOUT)
    salaris = salaris_veld.text_all
    print(salaris_veld)
    print(f"Start salaris: {salaris}")
    while True:
        print(f"Wachten op wijzig invoer")
        wijzig_invoer_knop = await tab.select("#butWijzig_pbt", timeout=TIMEOUT)
        await wijzig_invoer_knop.click()
        print(f"Wachten op salaris veld")
        salaris_veld = await tab.select("#V3-10_pbt", timeout=TIMEOUT)
        await salaris_veld.clear_input()
        await salaris_veld.send_keys("1234")
        print(f"Salaris is {salaris_veld.value}")
        print(f"Wachten tot invoer knop")
        toon_resultaten_knop = await tab.select("butResults_pbt", timeout=TIMEOUT)
        await toon_resultaten_knop.click()
        print(f"Goedzo")

    salaris_veld = await tab.select("#V3-10_pbt", timeout=TIMEOUT)
    await salaris_veld.send_keys("123")
    time.sleep(TIMEOUT)


if __name__ == '__main__':
    # since asyncio.run never worked (for me)
    uc.loop().run_until_complete(main())
