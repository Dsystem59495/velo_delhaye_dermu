'''
Bibliothèques à importer (les installations nécessaires au projet sont spécifiées dans le fichier texte requirements.txt)
'''

import requests
import json
from pymongo import MongoClient

'''
Chargement des données 
'''
def get_vlille():
    url = "https://opendata.lillemetropole.fr/api/records/1.0/search/?dataset=vlille-realtime&q=&rows=3000&facet=libelle&facet=nom&facet=commune&facet=etat&facet=type&facet=etatconnexion"
    response = requests.request("GET", url) # récupère l'ensemble des données fournies par l'API associée au lien url
    response_json = json.loads(response.text.encode('utf8'))     # Transforme notre fichier JSON en liste de dictionnaires
    return response_json.get("records", [])   # On récupére uniquement les données

'''
Création de la classe Saisie_utilisateur  
'''

class Saisie_utilisateur():
    def __init__(self, long, lat, rayon):
        self.long = long
        self.lat = lat
        self.rayon = rayon

'''
Interface utilisateur
'''

def saisie_coordonnees_utilisateur():
    print("Bonjour ! Veuillez saisir vos coordonnées :")
    longitude = float(input("Saissisez la longitude (Ouest-Est) : "))
    latitude = float(input("Saissisez la latitude (Nord-Sud) : "))
    distance_max = float(input("Saissisez le rayon de recherche en mètres : "))
    utilisateur = Saisie_utilisateur(longitude, latitude, distance_max)
    return utilisateur

def recherche_station_proche(utilisateur):
    atlas = MongoClient(
        'mongodb+srv://delhayedermu:delhayedermu@projectnosql.gtcde.gcp.mongodb.net/velo?retryWrites=true&w=majority')
    db = atlas.velo
    db.velo_lille.create_index([('geometry', '2dsphere')])
    liste_station = db.velo_lille.find({"geometry":
                                            { "$near":
                                                {"$geometry":
                                                     { "type" : "Point",
                                                       "coordinates": [utilisateur.long, utilisateur.lat]
                                                       },
                                                 "$maxDistance": utilisateur.rayon
                                                 }
                                              }
                                        })
    for doc in liste_station:
        print("coucou")
        print(doc)
    return liste_station     # 50.634306 3.048760 : ISEN LILLE


'''
Exécution code
'''

def main():
    utilisateur = saisie_coordonnees_utilisateur()
    liste_stations_proches = recherche_station_proche(utilisateur)
    print(liste_stations_proches)
    return None

main()