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
Modification, suppression ou désactivation d'une zone
'''

def update_station(liste_infos_stations, num_station):
    num = 0
    while num <= 0 or num > num_station :
        num = eval(input("\n Quel est le numéro de la station que vous souhaitez sélectionner ?" ))
    print("\n Vous avez choisi la station : ")
    station = liste_infos_stations[num-1]
    print(station.get('name'))
    
    choice = 0
    while choice != 1 and choice != 2 and choice != 3:
        choice = eval(input("\n Souhaitez vous modifier(1), supprimer la station(2) ou désactiver toutes les stations alentour (3) ?"))
        
    if choice == 1:
        modifie_station(station)
    elif choice == 2:
        supprime_station(station)
    else :
        desactive_zone_station(station)
        
    

'''
Modifier la station
'''

def modifie_station(station):
    DB.velo_lille.update_one({"name" : station.get('name')}, {"$set":{"tpe":False}})
    return None

'''
Supprimer la station
'''

def supprime_station(station):
    DB.velo_lille.delete_one({"name" : station.get("name")})
    DB.data_velo_lille.delete_many({"id_station" : station.get('id_station')})
    return None

'''
Désactivation de la zone autour de la station
'''

def desactive_zone_station(station):
    return None

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
              + str(infos_stations.get('date').strftime('%d/%m/%Y')) + " à "
              + str(int(infos_stations.get('date').strftime('%H'))+1)
              + infos_stations.get('date').strftime(':%M:%S'))
        
    return len(listes_infos_stations)

'''
Exécution code
'''

if __name__ == '__main__':
    print("\n Mise à jour des données \n")
    update_one_vlille()
    admin = saisie_coordonnees_administrateur()
    liste_station = recherche_nom_station(admin)
    liste_infos_stations = infos_stations_nom(liste_station)
    num_station = saisie_infos_stations(liste_infos_stations)
    update_station(liste_infos_stations, num_station)