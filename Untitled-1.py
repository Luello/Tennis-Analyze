import pandas as pd 
import streamlit as st



df=pd.read_csv("B:\\prog\\p3\\ATP_MASTER_tennis_single_concat.csv")
df=df.iloc[87553:]


#fonction qui visera à regrouper les différentes infos sur un joueur 
# def info_joueur(name_joueur):
#     dj=df[(df['winner_name']== name_joueur) | (df['loser_name']== name_joueur)]
#     hand= dj[dj['winner_name']== name_joueur]['winner_hand'].head(1).values[0]  #recupère la main du joueur sur un seul match. Pour l'instant je pars du fait qu'elle ne change jamais 
#     return
# infos= info_joueur('Roger Federer')


#Fonction pour calculer un taux de Victoire par type de Terrain
nom_joueur= 'Roger Federer'

#ace moyen / terrain



df_grouped = df.groupby('winner_name')['loser_ht'].value_counts()
