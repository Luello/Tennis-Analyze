import streamlit as st
import pandas as pd
import numpy as np



df=pd.read_csv("B:\\prog\\p3\\ATP_MASTER_tennis_single_concat.csv")
df=df.iloc[87553:]

def ace_analyze(nom_joueur): # La liste contient dans l'ordre: nombre moyen global d'ace, moyenne par Clay, Grass, Hard , Carpet
    surfaces = ['Clay', 'Grass', 'Hard', 'Carpet']
    liste=[]
    dw=df[(df['winner_name'] == nom_joueur)]
    ace_winning= round(dw['w_ace'].mean(),1)
    #st.write(f"Nombre moyen d'ace quand {nom_joueur} gagne: {ace_winning}")
    
    dl= df[df['loser_name'] == nom_joueur]
    ace_losing= round(dl['l_ace'].mean(),1)
    #st.write(f"Nombre moyen d'ace quand {nom_joueur} perd: {ace_losing}\n")
    moyenne= (ace_winning+ace_losing)/2
    liste.append(moyenne)
    for surface in surfaces:
        dw=df[(df['winner_name'] == nom_joueur)]
        dw=dw[dw['surface']==surface]
        ace_winning= round(dw['w_ace'].mean(),1)
        #st.write(f"Nombre moyen d'ace sur {surface} quand {nom_joueur} gagne: {ace_winning}")

        dl= df[df['loser_name'] == nom_joueur]
        dl=dl[dl['surface']==surface]
        ace_losing= round(dl['l_ace'].mean(),1)
        #st.write(f"Nombre moyen d'ace sur {surface} quand {nom_joueur} perd: {ace_losing}")
        moyenne_surf= (ace_winning+ace_losing)/2
        liste.append(moyenne_surf)
    return liste

def tx_vic_surface(nom_joueur, surface):
    #surfaces : 'Clay', 'Grass', 'Hard', 'Carpet'

    dj=df[(df['winner_name'] == nom_joueur)]
    dj= dj[dj['surface'] == surface]
    vic_surface= len(dj)  #Nombre de win sur la surface

    dj=df[(df['loser_name']== nom_joueur)]
    dj= dj[dj['surface']== surface]
    lose_surface= len(dj)  #Nombre de lose sur la surface

    try:
        taux_victoire_surface =  round(vic_surface/(vic_surface+lose_surface)*100,2)   # Cela renvoie un pourcentage de Victoire sur la surface 
    except:
        taux_victoire_surface=0
    return taux_victoire_surface


def best_surface_joueur(nom_joueur):
    surfaces = ['Clay', 'Grass', 'Hard', 'Carpet']
    top_surface= "indéfini"
    top_winrate=0

    for surface in surfaces:
        taux_victoire= tx_vic_surface(nom_joueur, surface)
        if taux_victoire > top_winrate:
            top_winrate= taux_victoire
            top_surface=surface

    st.write(f"La meilleure surface pour {nom_joueur} est {top_surface} avec un taux de Victoire de {top_winrate}%")
    

def player_hand(nom_joueur):
    df_player = df.loc[df['winner_name'] == nom_joueur]
    main_joueur= df_player['winner_hand'].values[0]
    if main_joueur=="L":
        return "Gaucher"
    elif main_joueur=="R":
        return "Droitier"
    elif main_joueur=="U":
        return "Latéralité inconnue"

def dernier_classement(nom_joueur):    #CETTE FONCTION RENVOIE LE DERNIER CLASSEMENT CONNU. NE PAS L'UTILISER POUR AVOIR LE CLASSEMENT ACTUEL CAR CERTAINS JOUEURS SONT A LA RETRAITES
    df_joueur = df[(df['winner_name'] == nom_joueur) | (df['loser_name'] == nom_joueur)]
    df_joueur = df_joueur.sort_values('tourney_date', ascending=False)
    classement= df_joueur.iloc[0]
    if classement['winner_name'] == nom_joueur:
        return df_joueur.iloc[0]['winner_rank']
    else:
        return df_joueur.iloc[0]['loser_rank']



def taille_age_natio(nom_joueur):
    df_player = df.loc[df['winner_name'] == nom_joueur]
    taille= df_player['winner_ht'].values[0]
    age= df_player['winner_age'].max()
    natio= df_player['winner_ioc'].values[0]
    
    return [taille,age,natio]

def nb_win_lose(nom_joueur):
    df_win = df.loc[df['winner_name'] == nom_joueur]
    df_win=len(df_win)

    df_lose = df.loc[df['loser_name'] == nom_joueur]
    df_lose=len(df_lose)

    return [df_win,df_lose]


#####################################################################################################################
df_unique = df.groupby('winner_name').first()
df_unique = df.groupby('winner_name')['winner_name'].first()
liste_joueur= df_unique.values



col1, col2 = st.columns(2)

joueur= col1.selectbox("Choisissez un joueur",options= liste_joueur, key= 'A')
joueur2= col2.selectbox("Choisissez un joueur",options= liste_joueur,key="B")

col1.title(f"{joueur}")
col1.write(player_hand(joueur))

info=taille_age_natio(joueur)

col1.write(f"Taille: {info[0]} cm ")
col1.write(f"Âge: {info[1]} ans")
col1.write(f"Nationalité: {info[2]}")

col2.title(f"{joueur2}")
col2.write(player_hand(joueur2))

info=taille_age_natio(joueur2)

col2.write(f"Taille: {info[0]} cm ")
col2.write(f"Âge: {info[1]} ans")
col2.write(f"Nationalité: {info[2]}")



#############################   COMPARAISON    #####################################################################################################
st.markdown("<h1 style='text-align: center;'> Victoires / Défaites </h1>", unsafe_allow_html=True)
col1, col2 = st.columns(2)

result_j1= nb_win_lose(joueur)
result_j2= nb_win_lose(joueur2)

col1.metric(label="VICTOIRES", value= result_j1[0])
col1.metric(label="DEFAITES", value= result_j1[1])

col2.metric(label="VICTOIRES", value= result_j2[0])
col2.metric(label="DEFAITES", value= result_j2[1])





st.markdown("<h1 style='text-align: center;'> ACES/MATCH </h1>", unsafe_allow_html=True)
col1, col2 = st.columns(2)
ace1= ace_analyze(joueur)
ace2= ace_analyze(joueur2)

deltaAce1 = ace1[0]-ace2[0]
col1.metric(label="Moyenne d'ace/Match", value= ace1[0], delta=deltaAce1)

deltaAce2 = ace2[0]-ace1[0]
col2.metric(label="Moyenne d'ace/Match", value= ace2[0], delta=deltaAce2)



st.markdown("<h1 style='text-align: center;'> WINRATE PAR SURFACE </h1>", unsafe_allow_html=True)
col1, col2 = st.columns(2)

surfaces = ['Clay', 'Grass', 'Hard', 'Carpet']

taux_victoire_joueur1 = []#sert pour le graph après
taux_victoire_joueur2 = [] 

for surface in surfaces:
    txj1= tx_vic_surface(joueur, surface)
    txj2= tx_vic_surface(joueur2, surface)

    deltaTx = round(txj1-txj2,1)
    col1.metric(label= f"Winrate sur {surface}", value= f"{txj1}%", delta=f"{deltaTx}%")
    deltaTx2= round(txj2-txj1,1)
    col2.metric(label=f"Winrate sur {surface}", value= f"{txj2}%", delta=f"{deltaTx2}%")

    taux_victoire_joueur1.append(txj1)
    taux_victoire_joueur2.append(txj2) 
##################################################################################################################################################


import plotly.graph_objects as go


surfaces = ['Clay', 'Grass', 'Hard', 'Carpet']


fig = go.Figure()
fig.add_trace(go.Scatterpolar(r=taux_victoire_joueur1,
    theta=surfaces,
    fill='toself',
    name=f'Taux de victoire {joueur}',))


fig.add_trace(go.Scatterpolar(r=taux_victoire_joueur2,
    theta=surfaces,
    fill='toself',
    name=F'Taux de victoire {joueur2}', line=dict(color='rgba(255, 0, 0, 0.5)')))

fig.update_layout(
  polar=dict(
    radialaxis=dict(
      visible=True,
      range=[0, 100]
    )),
  showlegend=True
)

st.plotly_chart(fig)






