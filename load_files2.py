import os
import csv
from datetime import datetime

def spracuj_nazov_suboru(nazov):
    serial_number = nazov[:10]
    fw = nazov[11:15]  # Znaky 12 až 15 (indexovanie je 0-based)
    return serial_number, fw

def vytvor_datovu_strukturu(adresar):
    try:
        # Získanie zoznamu súborov a podadresárov v zadanom adresári
        zoznam_suborov = os.listdir(adresar)

        # Filtrovanie len súborov (bez podadresárov)
        len_subory = [subor for subor in zoznam_suborov if os.path.isfile(os.path.join(adresar, subor))]

        # Vytvorenie dátovej štruktúry
        directory = []
        spracovane_serial_numbers = set()
        for subor in len_subory:
            serial_number, fw = spracuj_nazov_suboru(subor)
            if serial_number == "999ABC9999":
                continue
            if serial_number not in spracovane_serial_numbers:
                directory.append({
                    'serial_number': serial_number,
                    'fw': fw,
                    'uroven': 'L1',
                    'faktura': '20240011',
                    'datum': datetime.now().strftime('%Y-%m-%d')
                })
                spracovane_serial_numbers.add(serial_number)

        # Uloženie dátovej štruktúry do CSV súboru
        csv_soubor = 'vysledky.csv'
        with open(csv_soubor, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=['serial_number', 'fw', 'uroven', 'faktura', 'datum'])
            writer.writeheader()
            for item in directory:
                writer.writerow(item)

        # Výpis dátovej štruktúry
        print(f"Dátová štruktúra zo súborov v adresári {adresar} bola uložená do súboru {csv_soubor}.")
        for item in directory:
            print(item)
    except FileNotFoundError:
        print("Adresár neexistuje.")
    except PermissionError:
        print("Nemáte povolenie na prístup k tomuto adresáru.")
    except Exception as e:
        print("Vyskytla sa chyba:", e)

# Príklad použitia
adresar = "C:\Radiopol_3"
vytvor_datovu_strukturu(adresar)
