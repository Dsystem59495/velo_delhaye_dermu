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
Modification ou suppression d'une station
'''

def update_station(liste_infos_stations, num_station):
    num = 0
    while num <= 0 or num > num_station :
        num = eval(input("\n Quel est le numéro de la station que vous souhaitez sélectionner ? "))
    print("\n Vous avez choisi la station : ")
    station = liste_infos_stations[num-1]
    print(station.get('name'))
    
    choice = 0
    while choice != 1 and choice != 2:
        choice = eval(input("\n Souhaitez-vous modifier (1) ou supprimer la station sélectionnée (2) ? "))    
    if choice == 1:
        modifie_station(station)
    else:
        supprime_station(station)
        
    

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
Saisie des coordonnées pour la désactivation
'''

def saisie_coordonnees_desactivation():
    print("\n Veuillez saisir vos coordonnées :")
    while True:
        try:
            longitude = float(input("Saissisez la longitude (Ouest-Est) : "))
            break
        except ValueError:
            print("Erreur de saisie : Veuillez recommencer la saisie de la longitude (Ouest-Est). ")
    while True:
        try:
            latitude = float(input("Saissisez la latitude (Nord-Sud) : "))
            break
        except ValueError:
            print("Erreur de saisie : Veuillez recommencer la saisie de la latitude (Nord-Sud). ")
    while True:
        try:
            distance_max = float(input("Saissisez le rayon maximal pour la désactivation en mètres : "))
            break
        except ValueError:
            print("Erreur de saisie : Veuillez recommencer la saisie de la distance. ")
    
    return longitude, latitude, distance_max


'''
Désactivation de la zone autour de la station
'''

def desactive_zone_station():
    longitude, latitude, distance_max = saisie_coordonnees_desactivation()
    
    DB.velo_lille.create_index([('geometry', '2dsphere')])
    
    liste_station = DB.velo_lille.aggregate([
        {"$geoNear": {
            "near": {
                "type": "Point",
                "coordinates": [longitude, latitude]
            },
            "maxDistance": distance_max,
            "spherical": True,
            "distanceField": "distance"
        }}
    ])
    
    for i in liste_station :
        DB.velo_lille.update_many({"_id" : i.get('_id')}, {"$set": {"etat": False}})
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
    print("\n Bienvenue dans la section administrateur \n")
    choice = 0
    while choice != 1 and choice != 2:
        choice = eval(input("\n Souhaitez vous rechercher une station (1) ou désactiver des stations autour d'un point défini (2) ? "))    
    
    if choice == 2:
        desactive_zone_station()
    else :
        admin = saisie_coordonnees_administrateur()
        liste_station = recherche_nom_station(admin)
        liste_infos_stations = infos_stations_nom(liste_station)
        num_station = saisie_infos_stations(liste_infos_stations)
        update_station(liste_infos_stations, num_station)