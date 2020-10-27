'''
Bibliothèques à importer (les installations nécessaires au projet sont spécifiées dans le fichier texte requirements.txt)
'''
import json5

import dateutil.parser
import requests
from pymongo import MongoClient

# Connexion au serveur MongoDB

ATLAS = MongoClient(
        'mongodb+srv://delhayedermu:delhayedermu@projectnosql.gtcde.gcp.mongodb.net/velo?retryWrites=true&w=majority')
DB = ATLAS.velo

class SaisieUtilisateur():
    def __init__(self, long, lat, rayon):
        self.long = long
        self.lat = lat
        self.rayon = rayon

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
            "station_id": get_station_id(elem.get('fields', {}).get('libelle'), DB)
        }
        for elem in vlille
    ]
    try:
        DB.data_velo_lille.insert_many(newdata, ordered=False)
    except:
        pass

'''
Interface utilisateur
'''

def saisie_coordonnees_utilisateur():
    print("\nBonjour ! Veuillez saisir vos coordonnées :")
    longitude = float(input("Saissisez la longitude (Ouest-Est) : "))
    latitude = float(input("Saissisez la latitude (Nord-Sud) : "))
    distance_max = float(input("Saissisez le rayon de recherche en mètres : "))
    utilisateur = SaisieUtilisateur(longitude, latitude, distance_max)
    return utilisateur

'''
Renvoie l'ensemble des stations les plus proches de l'utilisateur en fonction de sa saisie
'''

def recherche_station_proche(utilisateur):
    """
    Pour l'Isen (3.048760,50.634306), voici un exemple d'une des stations proches située à moins de 200 mètres :
    {'_id': ObjectId('5f85755d5b69f0e31f96930c'), 'name': 'Palais Rameau',
    'geometry': {'type': 'Point', 'coordinates': [3.048344, 50.634686]},
    'size': 40, 'source': {'dataset': 'Lille', 'id_ext': 28}, 'tpe': True, 'distance': 51.498544325095466}
    """
    DB.velo_lille.create_index([('geometry', '2dsphere')])
    liste_station = DB.velo_lille.aggregate([
        {"$geoNear": {
            "near": {
                "type": "Point",
                "coordinates": [utilisateur.long, utilisateur.lat]
            },
            "maxDistance": utilisateur.rayon,
            "spherical": True,
            "distanceField": "distance"
        }}
    ])
    return liste_station

'''
Prépare l'affichage des informations pour l'utilisateur
'''

def infos_stations_proches(listes_stations):
    listes_infos_stations = []
    for station in listes_stations:
        infos_stations = dict()
        infos_stations['station_id'] = station.get('_id')
        infos_stations['name'] = station.get('name')
        infos_stations['distance'] = station.get('distance')
        listes_infos_stations.append(infos_stations)
    return listes_infos_stations

'''
Renvoie l'ensemble des informations d'une station située dans son périmètre
'''

def saisie_infos_stations(listes_infos_stations):
    print("\n Voici les stations proches de votre position : \n")

    for i in range(len(listes_infos_stations)):
        infos_stations = DB.data_velo_lille.find_one({'station_id': listes_infos_stations[i].get('station_id')})
        print(str(i + 1) + " : " + listes_infos_stations[i].get('name') + " à " + str(
            round(listes_infos_stations[i].get('distance'))) + " mètres ( "+
              str(infos_stations.get('bike_available')) + " vélo(s) disponibles et "
              + str(infos_stations.get('stand_available')) + " stand(s) de disponibles le "
              + str(infos_stations.get('date').strftime('%d/%m/%Y')) + " à " + str(infos_stations.get('date').strftime('%T')) + " ).\n")

'''
Exécution code
'''

def main():
    update_vlille()
    # 50.634306 3.048760 : ISEN LILLE
    # utilisateur = SaisieUtilisateur(3.048760, 50.634306, 300)
    # 50.61915 3.126501 : Boulevard De Valmy
    # utilisateur = SaisieUtilisateur(3.126501, 50.61915, 1000)
    utilisateur = saisie_coordonnees_utilisateur()
    listes_stations = recherche_station_proche(utilisateur)
    listes_infos_stations = infos_stations_proches(listes_stations)
    saisie_infos_stations(listes_infos_stations)
    return None

main()
