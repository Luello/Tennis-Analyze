import streamlit as st
import pandas as pd
import numpy as np

df=pd.read_csv("B:\\prog\\p3\\ATP_MASTER_tennis_single_concat.csv")
df=df.iloc[87553:]

def ace_analyze(nom_joueur):
    surfaces = ['Clay', 'Grass', 'Hard', 'Carpet']

    dw=df[(df['winner_name'] == nom_joueur)]
    ace_winning= round(dw['w_ace'].mean(),1)
    st.write(f"Nombre moyen d'ace quand {nom_joueur} gagne: {ace_winning}")
    
    dl= df[df['loser_name'] == nom_joueur]
    ace_losing= round(dl['l_ace'].mean(),1)
    st.write(f"Nombre moyen d'ace quand {nom_joueur} perd: {ace_losing}\n")

    for surface in surfaces:
        dw=df[(df['winner_name'] == nom_joueur)]
        dw=dw[dw['surface']==surface]
        ace_winning= round(dw['w_ace'].mean(),1)
        #st.write(f"Nombre moyen d'ace sur {surface} quand {nom_joueur} gagne: {ace_winning}")

        dl= df[df['loser_name'] == nom_joueur]
        dl=dl[dl['surface']==surface]
        ace_losing= round(dl['l_ace'].mean(),1)
        #st.write(f"Nombre moyen d'ace sur {surface} quand {nom_joueur} perd: {ace_losing}")

        st.write(f"En Moyenne, ce joueur fait {(ace_winning+ace_losing)/2} aces sur {surface}\n")


def tx_vic_surface(nom_joueur, surface):
    #surfaces : 'Clay', 'Grass', 'Hard', 'Carpet'

    dj=df[(df['winner_name'] == nom_joueur)]
    dj= dj[dj['surface'] == surface]
    vic_surface= len(dj)  #Nombre de win sur la surface

    dj=df[(df['loser_name']== nom_joueur)]
    dj= dj[dj['surface']== surface]
    lose_surface= len(dj)  #Nombre de lose sur la surface

    try:
        taux_victoire_surface =  round(100-((lose_surface/vic_surface)*100),2)   # Cela renvoie un pourcentage de Victoire sur la surface 
    except:
        taux_victoire_surface=0

    st.write(f"{nom_joueur}- {surface} : Nombre de Victoire: {vic_surface}, Nombre de Défaites: {lose_surface}, Taux de Victoire: {taux_victoire_surface} % ")
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
##################################################################################################################################



df_unique = df.groupby('winner_name').first()
df_unique = df.groupby('winner_name')['winner_name'].first()
liste_joueur= df_unique.values


joueur= st.selectbox("Choisissez un joueur",options= liste_joueur)


ok = st.button("Analyze")

if ok :
    st.title(f"This is  {joueur}")
    st.write(player_hand(joueur))

    info=taille_age_natio(joueur)
    
    st.write(f"Taille: {info[0]} cm ")
    st.write(f"Âge: {info[1]} ans")
    st.write(f"Nationalité: {info[2]}")

    st.header("ANALYSE DES ACES")
    ace_analyze(joueur)

    st.header("ANALYSE DES SURFACES")
    best_surface_joueur(joueur)



