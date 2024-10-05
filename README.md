# Toeslagen scraper

Berekent voor elk inkomen je toeslagen.  

## Opzetten
1. `python -m venv venv`
2. `.\venv\Scripts\activate`
3. `pip install -r requirements.txt`
4. `playwright install`

## Uitvoeren
1. `python toeslagen_scraper.py`
2. Voer je gegevens in
3. Bij inkomen: het salaris vanaf waar je wilt gaan berekenen
4. Stop het script wanneer je hoog genoeg zit
5. `python -m toeslagen_plotter.py`


## TODO
* Duidelijk maken dat je inkomen invoert waarvanaf je geintereseerd bent.
* Alternatief: een range invoeren waarvan je inkomen wilt weten
* Opties verwijderen onder menu, prevent overwhelm
* Hide results until running
* Breng GUI in front wanneer het begint te draaien