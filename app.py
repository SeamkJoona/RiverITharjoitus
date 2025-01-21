import requests
from collections import Counter
import re
import json

def hae_data(): #haetaan data
    url = "https://jsonplaceholder.typicode.com/posts"
    vastaus = requests.get(url)
    postaukset = json.loads(vastaus.text)
    return postaukset

# Käsitellään dataa ja lasketaan käyttäjäkohtaisia tilastoja
def kasittele_data(data):
    kayttajat = {}

    # Käydään läpi data
    for postaus in data:
        kayttaja_id = postaus['userId']
        body_sanat = len(postaus['body'].split())

        # Jos käyttäjä ei ole vielä listassa, lisätään ja alustetaan tilastot
        if kayttaja_id not in kayttajat:
            kayttajat[kayttaja_id] = {'postaukset': 0, 'sanat': 0}

        # Päivitä käyttäjän tilastot
        kayttajat[kayttaja_id]['postaukset'] += 1
        kayttajat[kayttaja_id]['sanat'] += body_sanat

    # Lasketaan keskimääräinen sanamäärä per postaus ja tallennetaan se
    for kayttaja_id, tilastot in kayttajat.items():
        keskiarvo = tilastot['sanat'] / tilastot['postaukset']
        tilastot['keskiarvo_sanoja'] = keskiarvo  # Tallennetaan keskiarvo

        # Tulostetaan käyttäjäkohtaiset tilastot
        print(f"Käyttäjä {kayttaja_id}:")
        print(f"  Postauksia: {tilastot['postaukset']}")
        print(f"  Sanoja yhteensä: {tilastot['sanat']}")
        print(f"  Keskiarvo sanoja per postaus: {keskiarvo:.2f}")

    return kayttajat

# Lasketaan viisi yleisintä sanaa
def viisi_yleisinta(data):
    bodyt = " ".join([postaus['body'] for postaus in data]) # Yhdistetään kaikki postaukset yhdeksi merkkijonoksi
    sanat = bodyt.split()  # Erotetaan sanat listaksi

    # Lasketaan sanojen yleisyyksiä
    sana_laskuri = Counter(sanat)

    # Tulostetaan viisi yleisintä sanaa
    top_5 = sana_laskuri.most_common(5)
    print("\nViisi yleisintä sanaa:")
    for sana, maara in top_5:
        print(f"'{sana}': {maara} kertaa")

    return top_5

def tallenna_tiedot(kayttajat, yleisimmat):
    # Rakennetaan JSON-muotoinen data
    data = {
        "kayttajat": [
            {
                "kayttaja_id": kayttaja_id,
                "postaukset": tilastot['postaukset'],
                "sanat": tilastot['sanat'],
                "keskiarvo_sanoja": tilastot['keskiarvo_sanoja']
            }
            for kayttaja_id, tilastot in kayttajat.items()
        ],
        "top_sanat": [
            {"sana": sana, "maara": maara} for sana, maara in yleisimmat
        ]
    }

    # Tallennetaan tiedot JSON-tiedostoon
    with open("kayttaja_tiedot.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def main():
    data = hae_data()
    kayttajat = kasittele_data(data)  # Korjattu muuttujan nimi
    yleisimmat = viisi_yleisinta(data)
    tallenna_tiedot(kayttajat, yleisimmat)  # Korjattu muuttujan nimi
    print("Data tallennettu tiedostoon 'kayttaja_tiedot.json'")

if __name__ == '__main__':
    main()
