# Toeslagen scraper

Berekent voor elk inkomen je toeslagen.  

Hoeveel toeslag krijg je precies voor jouw specifieke situatie?  
Met deze tool vul je de [toeslagen calculator](https://www.belastingdienst.nl/wps/wcm/connect/nl/toeslagen/content/hulpmiddel-proefberekening-toeslagen) van de belastingdienst in zoals je gewend bent.  
Vervolgens gaat de tool automatisch jouw specifieke toeslag ophalen voor elk inkomen.  
Deze informatie wordt in een grafiek gezet, zodat je overzichtelijk kunt zien 

## Opzetten
[//]: # (1. `python -m venv venv`)

[//]: # (2. `.\venv\Scripts\activate`)
1. Open de command line in deze folder
1. `pip install -r requirements.txt`
2. `playwright install`  
Optineel maak je eerst 

## Uitvoeren
`python toeslagen_scraper.py`

## Bronnen
Deze tool maakt gebruik van de toeslagen calculator:  
https://www.belastingdienst.nl/wps/wcm/connect/nl/toeslagen/content/hulpmiddel-proefberekening-toeslagen

Sommige toeslagen uit de calculator zijn ook zelf makkelijk te begrijpen:
* Kinderopvangtoeslag:  
https://www.rijksoverheid.nl/onderwerpen/kinderopvangtoeslag/bedragen-kinderopvangtoeslag-2023
* Zorgtoeslag:  
https://www.belastingdienst.nl/wps/wcm/connect/nl/zorgtoeslag/content/hoeveel-zorgtoeslag


## TODO
* Duidelijk maken dat je inkomen invoert waarvanaf je geintereseerd bent.
* Alternatief: een range invoeren waarvan je inkomen wilt weten
* Opties verwijderen onder menu, prevent overwhelm
* Hide results until running
* Breng GUI in front wanneer het begint te draaien