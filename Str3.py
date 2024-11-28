import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go

# Titel van de applicatie
st.title("Relatie Begintijd laadsessie, Oplaadtijd en Aangesloten tijd")

# Toon tekst
st.write("De tijd van de dag waarop een laadsessie wordt gestard heeft een sterke invloed op de gemiddelde duur \
         en de gemiddelde aangesloten tijd van de sessie. In de onderstaande visualistie, gebaseerd op data \
         van ruim 10.000 laadsessies, zijn de uren van de dag (starttijd van de sessie) weergegeven\
         gerelateerd hun gemiddelde oplaadtijd en verbonden tijd aan de laadpaal. ")

st.write("De laadsessies die diep in de nacht worden gestart duren relatief kort, maar hebben vaak een lange aangesloten tijd.\
         Deze trent houdt aan tot in de ochtend, de uren dat de werkdagen beginnen. Werknemers die tijdens het werk de auto aan de lader leggen \
         zorgen voor zowel een langere laadtijd als aangesloten tijd. Overdag is een standaard trent te zien, hoewel de aangesloten blijft stijgen \
         naarmate het later wordt. Vanaf 17.00/18.00, wanneer de werkdag is afgelopen, worden veel auto's langer aan de lader gelegd en is er een \
         stijgende trent te zien in oplaadtijd. De aangesloten tijd van meer dan 10 uur in de avonduren is natuurlijk te verklaren door de vele auto's\
         die de gehele nacht aan de laadpaal blijven staan.")

df = pd.read_csv('/Users/christianrombouts/Downloads/Minor Data Science/Cases/Case 3/laadpaaldata.csv')
#df.isna().sum()
df['Started'] = pd.to_datetime(df['Started'],format="%Y-%m-%d %H:%M:%S", errors='coerce')
df['Startuur'] = df['Started'].dt.hour #Nieuwe kolom met startuur

df = df[(df['ChargeTime'] >= 0.1) & (df['ConnectedTime'] >= 0.1)]
Gemiddelden = df.groupby('Startuur')[['ChargeTime','ConnectedTime']].mean()
df_new = pd.DataFrame(Gemiddelden)
df_new.loc[df_new['ConnectedTime'] >= 10, 'ConnectedTime'] = 10

dropdown = st.selectbox('Kies een variabele:', ['Oplaadtijd', 'Aangesloten Tijd','Gecombineerd'])

fig = go.Figure()

if dropdown == 'Oplaadtijd':
    fig.add_trace(go.Bar(x=df_new.index, y=df_new['ChargeTime'], name='Oplaadtijd', opacity=1))
elif dropdown == 'Aangesloten Tijd':
    fig.add_trace(go.Scatter(x=df_new.index, y=df_new['ConnectedTime'], name='Aangesloten Tijd', mode='lines+markers'))
elif dropdown == 'Gecombineerd':
    fig.add_trace(go.Bar(x=df_new.index, y=df_new['ChargeTime'], name='Oplaadtijd', opacity=1))
    fig.add_trace(go.Scatter(x=df_new.index, y=df_new['ConnectedTime'], name='Aangesloten Tijd', mode='lines+markers'))

fig.update_xaxes(tickmode = 'linear', range = [-0.5, 23.5])
fig.update_yaxes(tickvals=[0, 2, 4, 6, 8, 10], ticktext=['0', '2', '4', '6', '8', '10+'])
fig.update_layout(title = 'Verband tussen beginuur laadsessie en variabelen', xaxis_title = 'Beginuur laadsessie', 
                  yaxis_title = 'Gemiddelde tijd (uren)')
st.plotly_chart(fig)

# Voeg een knop toe
#if st.button('Klik hier'):
#    st.write("De knop is geklikt!")
