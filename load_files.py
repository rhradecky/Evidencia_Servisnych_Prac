import os


def vypis_orezane_unikatne_subory(adresar):
    try:
        # Získanie zoznamu súborov a podadresárov v zadanom adresári
        zoznam_suborov = os.listdir(adresar)

        # Filtrovanie len súborov (bez podadresárov)
        len_subory = [subor for subor in zoznam_suborov if os.path.isfile(os.path.join(adresar, subor))]

        # Orezanie názvov súborov na prvých 10 znakov a získanie jedinečných názvov
        orezane_subory = {subor[:10] for subor in len_subory}

        # Výpis jedinečných orezaných názvov súborov
        print("Zoznam jedinečných súborov v adresári", adresar)
        for subor in orezane_subory:
            print(subor)
    except FileNotFoundError:
        print("Adresár neexistuje.")
    except PermissionError:
        print("Nemáte povolenie na prístup k tomuto adresáru.")
    except Exception as e:
        print("Vyskytla sa chyba:", e)


# Príklad použitia
adresar = "C:/Users/hrade/PycharmProjects/myproject/Evidencia_Servisnych_Prac/serial_number"
vypis_orezane_unikatne_subory(adresar)
