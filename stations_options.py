'''
Bibliothèques à importer (les installations nécessaires au projet sont spécifiées dans le fichier texte requirements.txt)
'''

from pymongo import MongoClient

'''
Chargement des dernières données
'''
from update_worker import update_one_vlille

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
    name_search = str(input("Saisissez le nom : "))
    admin = SaisieAdmin(name_search)
    return admin

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

if __name__ == '__main__':
    print("\n Mise à jour des données \n")
    update_one_vlille()
    admin = saisie_coordonnees_administrateur()
    liste_station = recherche_nom_station(admin)
    liste_infos_stations = infos_stations_nom(liste_station)
    saisie_infos_stations(liste_infos_stations)