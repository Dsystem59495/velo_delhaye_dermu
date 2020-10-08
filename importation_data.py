'''
Bibliothèques à importer (les installations nécessaires au projet sont spécifiées dans le fichier texte installation.txt)
'''

import requests
import json

'''
Importation des différentes données utilisées au cours du projet. Autrement dit, c'est ici que sont chargées les données
des vélos en libre accès pour les villes de Lille, Lyon, Rennes et Paris
'''

def get_vlille():
    url = "https://opendata.lillemetropole.fr/api/records/1.0/search/?dataset=vlille-realtime&q=&rows=3000&facet=libelle&facet=nom&facet=commune&facet=etat&facet=type&facet=etatconnexion"
    response = requests.request("GET", url)
    response_json = json.loads(response.text.encode('utf8'))
    return response_json.get("records", [])

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
    url = "https://download.data.grandlyon.com/ws/rdata/jcd_jcdecaux.jcdvelov/all.json?maxfeatures=100&start=1"
    response = requests.request("GET", url)
    response_json = json.loads(response.text.encode('utf8'))
    return response_json.get("records", [])

'''
Tests pour vérifier que les nouvelles données sont belles et bien chargées

NB : Il semblerait que les données ne se chargent pas. En effet, lorsque l'on cherche à afficher les données qui 
viennent d'être chargées, l'affichage nous renvoie : []
'''

def test_import():
    print("Lille : /n")
    print(get_vlille())
    print("\n")
    print("Rennes : /n")
    print(get_vrennes())
    #print("\n")
    #print("Lyon : /n")
    #print(get_vlyon())
    print("\n")
    print("Paris : /n")
    print(get_vparis())
    print("\n")

test_import()

