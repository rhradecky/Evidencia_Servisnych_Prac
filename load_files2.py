import os

def spracuj_nazov_suboru(nazov):
    serial_number = nazov[:10]
    firmware = nazov[11:15]  # Znaky 12 až 15 (indexovanie je 0-based)
    return serial_number, firmware

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
            serial_number, firmware = spracuj_nazov_suboru(subor)
            if serial_number == "999ABC9999":
                continue
            if serial_number not in spracovane_serial_numbers:
                directory.append({'serial_number': serial_number, 'firmware': firmware})
                spracovane_serial_numbers.add(serial_number)

        # Výpis dátovej štruktúry
        print("Dátová štruktúra zo súborov v adresári", adresar)
        for item in directory:
            print(item)
    except FileNotFoundError:
        print("Adresár neexistuje.")
    except PermissionError:
        print("Nemáte povolenie na prístup k tomuto adresáru.")
    except Exception as e:
        print("Vyskytla sa chyba:", e)

# Príklad použitia
adresar = "C:/Users/hrade/PycharmProjects/myproject/Evidencia_Servisnych_Prac/serial_number"
vytvor_datovu_strukturu(adresar)
