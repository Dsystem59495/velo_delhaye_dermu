'''
Bibliothèques à importer (les installations nécessaires au projet sont spécifiées dans le fichier texte requirements.txt)
'''

import requests
import json5
from pymongo import MongoClient

'''
Importation des différentes données utilisées au cours du projet. Autrement dit, c'est ici que sont chargées les données
des vélos en libre accès pour les villes de Lille, Lyon, Rennes et Paris
'''

########################################################################################################################
#                                                   Pour Lille :                                                       #
########################################################################################################################

def get_vlille():
    url = "https://opendata.lillemetropole.fr/api/records/1.0/search/?dataset=vlille-realtime&q=&rows=3000&facet=libelle&facet=nom&facet=commune&facet=etat&facet=type&facet=etatconnexion"
    response = requests.request("GET", url) # récupère l'ensemble des données fournies par l'API associée au lien url
    response_json = json5.loads(response.text.encode('utf8'))     # Transforme notre fichier JSON en liste de dictionnaires
    return response_json.get("records", [])   # On récupére uniquement les données

velo_lille = get_vlille()

# print(json5.dumps(velo_lille[0], indent=4, separators=(", ", " : ")))  # indente les différents éléments pour que le fichier soit plus visible et affiche le premier élément chargé

"""
Voici à quoi ressemble une donnée associée à une station velo de Lille :
{
    "datasetid" : "vlille-realtime", 
    "recordid" : "e76138729b09a25cec4020ec405ca46807ef3d1d", 
    "fields" : {
        "etat" : "EN SERVICE", 
        "etatconnexion" : "CONNECTED", 
        "nbvelosdispo" : 9, 
        "nbplacesdispo" : 3, 
        "commune" : "LILLE", 
        "type" : "SANS TPE", 
        "libelle" : 172, 
        "datemiseajour" : "2020-10-12T13:28:05+00:00", 
        "localisation" : [
            50.612635, 
            3.059261
        ], 
        "nom" : "PLACE DE LA GARONNE", 
        "adresse" : "Rue de la Seine", 
        "geo" : [
            50.612635, 
            3.059261
        ]
    }, 
    "geometry" : {
        "type" : "Point", 
        "coordinates" : [
            3.059261, 
            50.612635
        ]
    }, 
    "record_timestamp" : "2020-10-12T13:30:23.748000+00:00"
}
"""

def vlille_insert(data):
    vlille_to_insert = [
        {
            'name': elem.get('fields', {}).get('nom', '').title(),
            'geometry': elem.get('geometry'),
            'size': elem.get('fields', {}).get('nbvelosdispo') + elem.get('fields', {}).get('nbplacesdispo'),
            'source': {
                'dataset': 'Lille',
                'id_ext': elem.get('fields', {}).get('libelle')
            },
            'tpe': elem.get('fields', {}).get('type', '') == 'AVEC TPE',
            'etat': elem.get('fields', {}).get('etat', '') == 'EN SERVICE'
        }
        for elem in data
    ]
    atlas = MongoClient(
        'mongodb+srv://delhayedermu:delhayedermu@projectnosql.gtcde.gcp.mongodb.net/velo?retryWrites=true&w=majority')
    atlas.velo.velo_lille.insert_many(vlille_to_insert)
    print("!!!!!!!!!! IMPORTATION Lille DONE !!!!!!!!!!")
    return None

########################################################################################################################
#                                                   Pour Rennes:                                                       #
########################################################################################################################

def get_vrennes():
    url = "https://data.rennesmetropole.fr/api/records/1.0/search/?dataset=etat-des-stations-le-velo-star-en-temps-reel&q=&rows=55&facet=nom&facet=etat&facet=nombreemplacementsactuels&facet=nombreemplacementsdisponibles&facet=nombrevelosdisponibles"
    response = requests.request("GET", url)
    response_json = json5.loads(response.text.encode('utf8'))
    return response_json.get("records", [])

velo_rennes = get_vrennes()

# print(json5.dumps(velo_rennes[0], indent=4, separators=(", ", " : ")))

"""
Voici à quoi ressemble une donnée associée à une station velo de Rennes :
{
    "datasetid" : "etat-des-stations-le-velo-star-en-temps-reel", 
    "recordid" : "88a8871cd455b991aae541e2d60ebdab34840e3e", 
    "fields" : {
        "etat" : "En fonctionnement", 
        "lastupdate" : "2020-10-12T14:24:10+00:00", 
        "nombrevelosdisponibles" : 12, 
        "nombreemplacementsactuels" : 16, 
        "nom" : "Musée Beaux-Arts", 
        "nombreemplacementsdisponibles" : 4, 
        "idstation" : "5510", 
        "coordonnees" : [
            48.109601, 
            -1.67408
        ]
    }, 
    "geometry" : {
        "type" : "Point", 
        "coordinates" : [
            -1.67408, 
            48.109601
        ]
    }, 
    "record_timestamp" : "2020-10-12T14:24:00+00:00"
}
"""

def vrennes_insert(data):
    vrennes_to_insert = [
        {
            'name': elem.get('fields', {}).get('nom', '').title(),
            'geometry': elem.get('geometry'),
            'size': elem.get('fields', {}).get('nombreemplacementsactuels'),
            'source': {
                'dataset': 'Rennes',
                'id_ext': elem.get('fields', {}).get('idstation')
            },
        }
        for elem in data
    ]
    atlas = MongoClient(
        'mongodb+srv://delhayedermu:delhayedermu@projectnosql.gtcde.gcp.mongodb.net/velo?retryWrites=true&w=majority')
    atlas.velo.velo_rennes.insert_many(vrennes_to_insert)
    print("!!!!!!!!!! IMPORTATION Rennes DONE !!!!!!!!!!")
    return None

########################################################################################################################
#                                                   Pour Paris :                                                       #
########################################################################################################################

def get_vparis():
    url = "https://opendata.paris.fr/api/records/1.0/search/?dataset=velib-disponibilite-en-temps-reel&q=&rows=1398&facet=name&facet=is_installed&facet=is_renting&facet=is_returning&facet=nom_arrondissement_communes"
    response = requests.request("GET", url)
    response_json = json5.loads(response.text.encode('utf8'))
    return response_json.get("records", [])

velo_paris = get_vparis()

# print(json5.dumps(velo_paris[0], indent=4, separators=(", ", " : ")))

"""
Voici à quoi ressemble une donnée associée à une station velo de Paris :
{
    "datasetid" : "velib-disponibilite-en-temps-reel", 
    "recordid" : "a595840b0e46d40168ed12d2145a93e720e1b146", 
    "fields" : {
        "ebike" : 4, 
        "capacity" : 21, 
        "name" : "Toudouze - Clauzel", 
        "nom_arrondissement_communes" : "Paris", 
        "numbikesavailable" : 7, 
        "is_installed" : "OUI", 
        "is_renting" : "OUI", 
        "mechanical" : 3, 
        "stationcode" : "9020", 
        "coordonnees_geo" : [
            48.8792959173, 
            2.33736008406
        ], 
        "numdocksavailable" : 12, 
        "duedate" : "2020-10-12T14:09:02+00:00", 
        "is_returning" : "OUI"
    }, 
    "geometry" : {
        "type" : "Point", 
        "coordinates" : [
            2.33736008406, 
            48.8792959173
        ]
    }, 
    "record_timestamp" : "2020-10-12T14:39:08.655000+00:00"
}
"""

def vparis_insert(data):
    vparis_to_insert = [
        {
            'name': elem.get('fields', {}).get('name', '').title(),
            'geometry': elem.get('geometry'),
            'size': elem.get('fields', {}).get('capacity'),
            'source': {
                'dataset': 'Paris',
                'id_ext': elem.get('fields', {}).get('stationcode')
            },
        }
        for elem in data
    ]
    atlas = MongoClient(
        'mongodb+srv://delhayedermu:delhayedermu@projectnosql.gtcde.gcp.mongodb.net/velo?retryWrites=true&w=majority')
    atlas.velo.velo_paris.insert_many(vparis_to_insert)
    print("!!!!!!!!!! IMPORTATION Paris DONE !!!!!!!!!!")
    return None

########################################################################################################################
#                                                   Pour Lyon :                                                       #
########################################################################################################################

def get_vlyon():
    url = "https://public.opendatasoft.com/api/records/1.0/search/?dataset=station-velov-grand-lyon&q=&rows=2000&facet=last_upd_1"
    response = requests.request("GET", url)
    response_json = json5.loads(response.text.encode('utf8'))
    return response_json.get("records", [])

velo_lyon = get_vlyon()

# print(json5.dumps(velo_lyon[0], indent=4, separators=(", ", " : ")))

"""
Voici à quoi ressemble une donnée associée à une station velo de Lyon :
{
    "datasetid" : "station-velov-grand-lyon", 
    "recordid" : "35a35fa3d3108e1305d37c7f7218897842a2a7ab", 
    "fields" : {
        "available" : "23", 
        "status" : "OPEN", 
        "availabl_1" : "12", 
        "name" : "ZAC de la Buire", 
        "commune" : "Lyon 3 \u00e8me", 
        "bonus" : "Non", 
        "last_updat" : "2015-07-01 16:08:47", 
        "address" : "Face au 106 avenue F\u00e9lix Faure", 
        "bike_stand" : "35", 
        "geo_point_2d" : [
            45.75379945822723, 
            4.859863339774901
        ], 
        "availabili" : "1", 
        "number" : "3036", 
        "banking" : "t", 
        "gid" : "952", 
        "nmarrond" : "36", 
        "lat" : "45.7537994582273000", 
        "geo_shape" : {
            "type" : "Point", 
            "coordinates" : [
                4.859863339774901, 
                45.75379945822723
            ]
        }, 
        "lng" : "4.8598633397749000", 
        "availabi_1" : "Vert", 
        "last_upd_1" : "2015-07-01 16:11:00"
    }, 
    "geometry" : {
        "type" : "Point", 
        "coordinates" : [
            4.859863339774901, 
            45.75379945822723
        ]
    }, 
    "record_timestamp" : "2019-03-12T10:20:50.428000+00:00"
}
"""

def vlyon_insert(data):
    vlyon_to_insert = [
        {
            'name': elem.get('fields', {}).get('name', '').title(),
            'geometry': elem.get('geometry'),
            'size': elem.get('fields', {}).get('bike_stand'),
            'source': {
                'dataset': 'Lyon',
                'id_ext': elem.get('fields', {}).get('number')
            },
        }
        for elem in data
    ]
    atlas = MongoClient(
        'mongodb+srv://delhayedermu:delhayedermu@projectnosql.gtcde.gcp.mongodb.net/velo?retryWrites=true&w=majority')
    atlas.velo.velo_lyon.insert_many(vlyon_to_insert)
    print("!!!!!!!!!! IMPORTATION Lyon DONE !!!!!!!!!!")
    return None

'''
Chargement des différentes données utilisées au cours du projet dans MongoDB Atlas
'''

if __name__ == '__main__':
    vlille_insert(velo_lille)
    vrennes_insert(velo_rennes)
    vparis_insert(velo_paris)
    vlyon_insert(velo_lyon)
    print("ALL IMPORTATION DONE")

