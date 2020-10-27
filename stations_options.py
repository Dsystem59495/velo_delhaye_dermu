'''
Bibliothèques à importer (les installations nécessaires au projet sont spécifiées dans le fichier texte requirements.txt)
'''
import json5

import dateutil.parser
import requests
from pymongo import MongoClient

ATLAS = MongoClient(
        'mongodb+srv://delhayedermu:delhayedermu@projectnosql.gtcde.gcp.mongodb.net/velo?retryWrites=true&w=majority')
DB = ATLAS.velo

class SaisieAdmin():
    def __init__(self,name_search):
        self.name_search = name_search
    
'''
Interface administrateur
'''

def saisie_coordonnees_administrateur():
    print("\nBonjour ! Veuillez saisir un nom à chercher :")
    name_search = str(input("Saisissez le nom :"))
    admin = SaisieAdmin(name_search)
    return admin

'''
Chargement des dernières données
'''
def get_vlille():
    url = "https://opendata.lillemetropole.fr/api/records/1.0/search/?dataset=vlille-realtime&q=&rows=3000&facet=libelle&facet=nom&facet=commune&facet=etat&facet=type&facet=etatconnexion"
    response = requests.request("GET", url) # récupère l'ensemble des données fournies par l'API associée au lien url
    response_json = json5.loads(response.text.encode('utf8'))     # Transforme notre fichier JSON en liste de dictionnaires
    return response_json.get("records", [])   # On récupére uniquement les données

def get_station_id(id_ext, database):
    tps = database.velo_lille.find_one({ 'source.id_ext': id_ext }, { '_id': 1 })
    return tps['_id']

def update_vlille():
    DB.data_velo_lille.create_index([('station_id', 1), ('date', -1)], unique=True)
    print("\nMise à jour des données !!!\n")
    vlille = get_vlille()
    newdata = [
        {
            "bike_available": elem.get('fields', {}).get('nbvelosdispo'),
            "stand_available": elem.get('fields', {}).get('nbplacesdispo'),
            "date": dateutil.parser.parse(elem.get('fields', {}).get('datemiseajour')),
            "station_id": get_station_id(elem.get('fields', {}).get('libelle'),DB)
        }
        for elem in vlille
    ]
    try:
        DB.data_velo_lille.insert_many(newdata, ordered=False)
    except:
        pass
    
    
'''
Renvoie l'ensemble des stations dont le nom contient la saisie de l'administrateur
'''

def recherche_nom_station(administrateur):
    """
    """
    pattern = administrateur.name_search
    liste_station = DB.velo_lille.find(
            {
                "name" : {"$regex" : pattern, "$options" : "i"}
            }
    )
        
    return liste_station

'''
Prépare l'affichage des informations pour l'administrateur
'''

def infos_stations_nom(listes_stations):
    listes_infos_stations = []
    for doc in listes_stations:
        infos_stations = dict()
        infos_stations['station_id'] = doc.get('_id')
        infos_stations['name'] = doc.get('name')
        listes_infos_stations.append(infos_stations)
    return listes_infos_stations

'''
Renvoie l'ensemble des informations d'une station dont le nom contient la saisie de l'administrateur
'''

def saisie_infos_stations(listes_infos_stations):
    print("\n Voici les stations contenant votre saisie : \n")

    for i in range(len(listes_infos_stations)):
        infos_stations = DB.data_velo_lille.find_one({'station_id': listes_infos_stations[i].get('station_id')})
        print(str(i + 1) + " : " + listes_infos_stations[i].get('name') + " ( "+
              str(infos_stations.get('bike_available')) + " vélo(s) disponibles et "
              + str(infos_stations.get('stand_available')) + " stand(s) de disponibles le "
              + str(infos_stations.get('date').strftime('%d/%m/%Y')) + " à " + str(infos_stations.get('date').strftime('%T')) + " ).\n")

'''
Exécution code
'''

def main():
    update_vlille()
    admin = saisie_coordonnees_administrateur()
    liste_station = recherche_nom_station(admin)
    liste_infos_stations = infos_stations_nom(liste_station)
    saisie_infos_stations(liste_infos_stations)
    return None

main()