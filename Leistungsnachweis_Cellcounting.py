import os
import json 
import streamlit as st
import matplotlib.pyplot as plt
import datetime


# JSON-Datei wird geöffnet und der Inhalt in eine Python-Datenstruktur geladen, inklusive Funktionsagument
def load_data(filename):
    if os.path.isfile(filename):
        with open(filename, "r", encoding="utf-8") as file:
            data = json.load(file)
    else:
        data = []
    return data

# Speicherung des Python-Dictionary als JSON-Datei. (2 argumente, 1. die eingegebenen daten, 2. den filenamen unter dem gespeichet wird)
def save_data(data, filename):
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=2, ensure_ascii=False)

data = load_data("./data.json")
infos = load_data("./Zellinformationen.json")

# Dropdown-Menü mit den Auswahlmöglichkeiten
    
auswahl = st.selectbox('Zelltyp auswählen', list(infos.keys()))

# Wenn der Benutzer eine Auswahl trifft, wird eine neue Seite angezeigt
if auswahl:
    st.write(f'Du hast {auswahl} ausgewählt!')
    option = st.radio('Was möchtest du tun?', ('Informationen anzeigen', 'Zellen zählen'))

    if option == 'Informationen anzeigen':
        st.markdown(
            # in markdown machen **text** den text dick, *text* macht es kursiv
            f"""
            - **Name**: {infos[auswahl]["Name"]}
            - **Art**: {infos[auswahl]["Art"]}
            - **Medium**: {infos[auswahl]["Medium"]}
            - **Zellgrösse**: {infos[auswahl]["Zellgrösse"]}
            - **Inkubationsbedingungen**: {infos[auswahl]["Inkubationsbedingungen"]}
              """
            )

    elif option == 'Zellen zählen':
        # Bild mit Neubauer Zählkammer anzeigen
        st.image(infos[auswahl]["Pfad_zum_Bild"])

        # Vorverdünnung eingeben
        vitalitaet = st.number_input('Gib die verwendete Vorverdünnung an', min_value=1, max_value=1000, value=1, step=1)

        # Fünf Zahlen eingeben
        values = []
        for i in range(infos[auswahl]["Eingabefelder"]):
            number = st.number_input(f'Gib Zellzahl für Quadrat {i+1} ein', min_value=1, max_value=10000, value=1, step=1)
            values.append(number)

        # Durchschnitt berechnen und Wert multiplizieren (inklusive der vitalitaet)
        mean_value = sum(values) / len(values)
        result = mean_value * 5 * 10 ** 4 * vitalitaet

        # Ergebnis ausgeben
        st.write('Der Durchschnitt der eingegebenen Werte ist:', mean_value, 'Zellen')
        st.write('Das Ergebnis der Berechnung ist:', result, 'Zellen pro ml')

# Speichern-Button hinzufügen
if st.button('Speichern'):
    anz_zaehlungen = len(data[auswahl])
    date_str = datetime.datetime.now().strftime("%d.%m.%y")  # Get current date as "dd.mm.yy" string
    data[auswahl][date_str] = {
        "Zellzahlen": values,
        "Ergebnis": result
    }
# Gespeicherte Daten als plot wiedergeben und mit Datum versehen    
    save_data(data, "data.json")
    st.write('Daten wurden gespeichert.')
    x = []
    y = []
    for key, value in data["MF"].items():
        x.append(key)
        y.append(value["Ergebnis"])

    fig, ax = plt.subplots()
    ax.plot(x, y)
    ax.set(xlabel='Datum + Zählung', ylabel='Zellkonzentration [Zellen / ml]', title='Ergebnisse der Zählungen')
    ax.grid()

    st.pyplot(fig)

            
            
            


