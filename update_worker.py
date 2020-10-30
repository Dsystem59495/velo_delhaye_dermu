'''
Bibliothèques à importer (les installations nécessaires au projet sont spécifiées dans le fichier texte requirements.txt)
'''

import time
from pymongo import MongoClient
import dateutil.parser  # Ce module renvoye un objet datetime même pour les formats de dates ambiguës.

'''
Importation régulière des données des différentes stations vlille. Autrement dit, c'est ici que sont chargées les données
des stations vlille "infiniment". La requête de mises à jour des données s'effectuera environ toutes les 30 secondes
'''

########################################################################################################################
#                         Fonction pour récupérer les différentes données associées aux stations                       #
########################################################################################################################

from importation_data import get_vlille

########################################################################################################################
#                                     Fonction ajoutant les mises à jour des données                                   #
########################################################################################################################

# Connexion à Atlas
ATLAS = MongoClient(
    'mongodb+srv://delhayedermu:delhayedermu@projectnosql.gtcde.gcp.mongodb.net/velo?retryWrites=true&w=majority')
# Connexion à la base de données velo
DB = ATLAS.velo


def get_station_id(id_ext, database):
    tps = database.velo_lille.find_one({'source.id_ext': id_ext}, {'_id': 1})
    return tps['_id']


def update_one_vlille():
    """
     Création d'un index en fonction de l'index de la station (increasing) et de la date (decreasing)
    Ceci permettra de trier les données de la plus récente à la plus ancienne
    """
    DB.data_velo_lille.create_index([('station_id', 1), ('date', -1)], unique=True)
    vlille = get_vlille()
    newdata = [
        {
            "bike_available": elem.get('fields', {}).get('nbvelosdispo'),
            "stand_available": elem.get('fields', {}).get('nbplacesdispo'),
            "date": dateutil.parser.parse(elem.get('fields', {}).get('datemiseajour')),   # les dates sont enregistrés selon l'heure de Londres (méridien de Greenwich)
            "station_id": get_station_id(elem.get('fields', {}).get('libelle'), DB)
        }
        for elem in vlille
    ]
    # On ajoute les données jusqu'à ce qu'on obtienne une date où il n'y a pas eu de nouvelles données
    try:
        DB.data_velo_lille.insert_many(newdata, ordered=False)
    except:
        pass


def update_vlille():
    while True:
        print("NEW UPDATE !!!")
        update_one_vlille()
        print("UPDATE DONE !!!")
        time.sleep(30)

if __name__ == '__main__':
    update_vlille()