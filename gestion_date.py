import streamlit as st
import pandas as pd
from datetime import datetime

st.title("🛠️ Convertisseur Date/Heure Excel – Format personnalisé")

st.markdown("**Collez ici colonnes (Date et Heure) copiées depuis Excel :**")

input_text = st.text_area("Entrée (Date et Heure séparées par tabulation)", height=300)

# 🎯 Sélection du format d'entrée
input_date_format = st.selectbox(
    "Format de date d'entrée",
    # options=["MM/DD/YYYY", "DD/MM/YYYY", "YYYY-MM-DD"],
    options=["MM/DD/YYYY"],
    index=0
)

# 🎯 Sélection du format de sortie
output_date_format = st.selectbox(
    "Format de date de sortie",
    options=["DD/MM/YYYY"],
    index=0
)

input_time_format = st.selectbox(
    "Format de heure d'entrée",
    options=["hh:mm:ss AM/PM"],
    index=0
)

input_time_format = st.selectbox(
    "Format de heure de sortie",
    options=["hh:mm:ss 24h"],
    index=0
)

concat_option = st.checkbox("Concaténer la date et l’heure (ex: 29/11/2021 09:30:00)", value=True)


# # Mapping formats personnalisés vers ceux utilisables par `datetime`
# format_mapping = {
#     "MM/DD/YYYY": "%m/%d/%Y",
#     "DD/MM/YYYY": "%d/%m/%Y",
#     "YYYY-MM-DD": "%Y-%m-%d",
#     "YYYY-MM-DD": "%Y-%m-%d",
#     "DD-MM-YYYY": "%d-%m-%Y",
#     "MM-DD-YYYY": "%m-%d-%Y",
# }

def transform(row):
    try:
        date = row[0].strip()
        time = row[1].strip()

        splitted_date = date.split('/')
        day=splitted_date[1]
        month =splitted_date[0]
        year=splitted_date[2]

        if len(day)==1:
            day ="0"+day
        if len(month)==1:
            month="0"+month

        new_date = day+"/"+month+"/"+year
        new_time = datetime.strptime(time, "%I:%M:%S %p").strftime("%H:%M:%S")

        new_value = new_date+" "+new_time


        if concat_option:
            return new_value
        else:
            return new_date, new_time
    except Exception as e:
        return f"Erreur: {e}" if concat_option else ("Erreur", "Erreur")

if st.button("Convertir"):
    lines = input_text.strip().split('\n')
    data = [line.split('\t') for line in lines if '\t' in line]

    if all(len(row) >= 2 for row in data):
        df = pd.DataFrame(data, columns=["Date", "Heure"])

        if concat_option:
            df["Résultat"] = df.apply(transform, axis=1)
            st.success("Conversion réussie ✅")
            st.text_area("Colonne formatée", value="\n".join(df["Résultat"]), height=300)
        else:
            df[["Date formatée", "Heure formatée"]] = pd.DataFrame(df.apply(transform, axis=1).tolist())
            st.success("Conversion réussie ✅")
            st.write("📅 Colonne date :")
            st.text_area("Date", value="\n".join(df["Date formatée"]), height=200)
            st.write("⏰ Colonne heure :")
            st.text_area("Heure", value="\n".join(df["Heure formatée"]), height=200)
    else:
        st.error("⚠️ Veuillez coller deux colonnes (date et heure) séparées par tabulation.")
