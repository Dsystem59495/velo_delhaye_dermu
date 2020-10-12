'''
Bibliothèques à importer (les installations nécessaires au projet sont spécifiées dans le fichier texte installation.txt)
'''

import requests
import json
import pymongo
# import dns

'''
Importation des différentes données utilisées au cours du projet. Autrement dit, c'est ici que sont chargées les données
des vélos en libre accès pour les villes de Lille, Lyon, Rennes et Paris
'''

def get_vlille():
    url = "https://opendata.lillemetropole.fr/api/records/1.0/search/?dataset=vlille-realtime&q=&rows=3000&facet=libelle&facet=nom&facet=commune&facet=etat&facet=type&facet=etatconnexion"
    response = requests.request("GET", url)
    response_json = json.loads(response.text.encode('utf8'))     # Transforme notre fichier JSON en liste de dictionnaires
    records = response_json.get("records", [])   # On récupére uniquement les données
    for element in records :
        element['fields'].pop('commune', None)
        element['fields'].pop('adresse', None)
        element['fields'].pop('localisation', None)
        element['fields']['TPE'] = element['fields'].pop('type', None)
    return records

def get_vrennes():
    url = "https://data.rennesmetropole.fr/api/records/1.0/search/?dataset=etat-des-stations-le-velo-star-en-temps-reel&q=&facet=nom&facet=etat&facet=nombreemplacementsactuels&facet=nombreemplacementsdisponibles&facet=nombrevelosdisponibles"
    response = requests.request("GET", url)
    response_json = json.loads(response.text.encode('utf8'))
    return response_json.get("records", [])

def get_vparis():
    url = "https://opendata.paris.fr/api/records/1.0/search/?dataset=velib-disponibilite-en-temps-reel&q=&facet=name&facet=is_installed&facet=is_renting&facet=is_returning&facet=nom_arrondissement_communes"
    response = requests.request("GET", url)
    response_json = json.loads(response.text.encode('utf8'))
    return response_json.get("records", [])

def get_vlyon():
    url = "https://public.opendatasoft.com/api/records/1.0/search/?dataset=station-velov-grand-lyon&q=&rows=2000&facet=last_upd_1"
    response = requests.request("GET", url)
    response_json = json.loads(response.text.encode('utf8'))
    return response_json.get("records", [])

'''
Tests pour vérifier que les nouvelles données sont belles et bien chargées 
'''

###########
#   OK    #
###########

def test_import():
    print("Lille : ")
    print(get_vlille())
    print("\n")
    print("Rennes : ")
    print(get_vrennes())
    print("\n")
    print("Lyon : ")
    print(get_vlyon())
    print("\n")
    print("Paris : ")
    print(get_vparis())
    return None
# test_import()

'''
Affichage plus propre de notre fichier JSON
'''

def affichage(json_file):
    vlille = json.dumps(json_file, indent = 4, separators=(", ", " : ")) # indente les différents éléments pour que le fichier soit plus visible
    print("affichage :")
    print(vlille)
    return None

# affichage(get_vlille())

