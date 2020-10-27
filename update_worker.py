'''
Bibliothèques à importer (les installations nécessaires au projet sont spécifiées dans le fichier texte requirements.txt)
'''

import requests
import time
import json5
from pymongo import MongoClient
import dateutil.parser   # Ce module renvoye un objet datetime même pour les formats de dates ambiguës.

'''
Importation régulière des données des différentes stations vlille. Autrement dit, c'est ici que sont chargées les données
des stations vlille "infiniment". La requête de mises à jour des données s'effectuera environ toutes les 30 secondes
'''

########################################################################################################################
#                         Fonction pour récupérer les différentes données associées aux stations                       #
########################################################################################################################

def get_vlille():
    url = "https://opendata.lillemetropole.fr/api/records/1.0/search/?dataset=vlille-realtime&q=&rows=3000&facet=libelle&facet=nom&facet=commune&facet=etat&facet=type&facet=etatconnexion"
    response = requests.request("GET", url) # récupère l'ensemble des données fournies par l'API associée au lien url
    response_json = json5.loads(response.text.encode('utf8'))     # Transforme notre fichier JSON en liste de dictionnaires
    return response_json.get("records", [])   # On récupére uniquement les données

########################################################################################################################
#                                     Fonction ajoutant les mises à jour des données                                   #
########################################################################################################################

# Connexion à Atlas

def get_station_id(id_ext, database):
    tps = database.velo_lille.find_one({ 'source.id_ext': id_ext }, { '_id': 1 })
    return tps['_id']

def update_vlille():
    atlas = MongoClient(
        'mongodb+srv://delhayedermu:delhayedermu@projectnosql.gtcde.gcp.mongodb.net/velo?retryWrites=true&w=majority')
    # Connexion à la base de données velo
    db = atlas.velo
    """
     Création d'un index en fonction de l'index de la station (increasing) et de la date (decreasing)
    Ceci permettra de trier les données de la plus récente à la plus ancienne
    """
    db.data_velo_lille.create_index([('station_id', 1), ('date', -1)], unique=True)

    while True:
        print("NEW UPDATE !!!")
        vlille = get_vlille()
        newdata = [
            {
                "bike_available": elem.get('fields', {}).get('nbvelosdispo'),
                "stand_available": elem.get('fields', {}).get('nbplacesdispo'),
                "date": dateutil.parser.parse(elem.get('fields', {}).get('datemiseajour')),
                "station_id": get_station_id(elem.get('fields', {}).get('libelle'),db)
            }
            for elem in vlille
        ]
        # On ajoute les données jusqu'à ce qu'on obtienne une date où il n'y a pas eu de nouvelles données
        try:
            db.data_velo_lille.insert_many(newdata, ordered=False)
        except:
            pass
        print("UPDATE DONE !!!")
        time.sleep(30)

update_vlille()