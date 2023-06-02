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

# Authenticates the user with the provided username and password
def authenticate(username, password):
    with open("users.json", "r") as file:
        users = json.load(file)
        if username in users and users[username] == password:
            return True
    return False

data = load_data("./data.json")
infos = load_data("./Zellinformationen.json")

st.title('CellCounter')  # Titel hinzufügen

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

 # ...

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
    
        # Define login form
        login_form = st.form(key='login_form')
        username_input = login_form.text_input("Benutzername")
        password_input = login_form.text_input("Passwort", type="password")
        login_button = login_form.form_submit_button("Anmelden")
    
        save_button_visible = False
        if login_button:
            if authenticate(username_input, password_input):
                st.success("Erfolgreich angemeldet!")
                # Hier können Sie den Inhalt anzeigen, den angemeldete Benutzer sehen sollen
                save_button_visible = True

            else:
                st.error("Ungültige Anmeldedaten")
    
        # Speichern-Button hinzufügen
        if save_button_visible and st.button('Speichern'):
            st.write("hi")
            
            if auswahl not in data:
                data[auswahl] = {}  # Create a new entry for the selected cell type if it doesn't exist
    
                anz_zaehlungen = len(data[auswahl])
                count = anz_zaehlungen + 1  # Start counting from 1
                date_str = datetime.datetime.now().strftime("%d.%m.%y %H:%M:%S")  # Format: dd.mm.yy HH:MM:SS
                if anz_zaehlungen == 0:  # First measurement of the day
                    label = date_str
                else:
                    label = f"Zählung {count}"
        
                data[auswahl][label] = {
                    "Zellzahlen": values,
                    "Ergebnis": result
                }
        
                save_data(data, f"data_{auswahl}.json")  # Save data in a separate file for each cell type
        
                st.write('Daten wurden gespeichert.')
        
                x = []
                y = []
                for key, value in data[auswahl].items():
                    x.append(key)
                    y.append(value["Ergebnis"])
        
                fig, ax = plt.subplots()
                ax.plot(x, y)
                ax.set(xlabel='Datum + Zählung', ylabel='Zellkonzentration [Zellen / ml]', title='Ergebnisse der Zählungen')
                ax.grid()
        
                # Remove or modify the line below
                ax.xaxis.set_major_locator(plt.MaxNLocator(len(x)))
        
                # Optionally, modify the line below to adjust the font size of tick labels
                ax.set_xticklabels(x, rotation=45, ha='right', fontsize=8)
        
                st.pyplot(fig)
    
