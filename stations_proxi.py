'''
Bibliothèques à importer (les installations nécessaires au projet sont spécifiées dans le fichier texte requirements.txt)
'''

from pymongo import MongoClient

ATLAS = MongoClient(
        'mongodb+srv://delhayedermu:delhayedermu@projectnosql.gtcde.gcp.mongodb.net/velo?retryWrites=true&w=majority')
DB = ATLAS.velo

class SaisieUtilisateur():
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
    atlas = MongoClient(
        'mongodb+srv://delhayedermu:delhayedermu@projectnosql.gtcde.gcp.mongodb.net/velo?retryWrites=true&w=majority')
    db = atlas.velo
    db.velo_lille.create_index([('geometry', '2dsphere')])
    liste_station = db.velo_lille.aggregate([
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
    return liste_station  # 50.634306 3.048760 : ISEN LILLE

'''
Prépare l'affichage des informations pour l'utilisateur
'''

def infos_stations_proches(listes_stations_proches):
    listes_infos_stations_proches = []
    for doc in listes_stations_proches:
        infos_stations = dict()
        infos_stations['station_id'] = doc.get('_id')
        infos_stations['name'] = doc.get('name')
        infos_stations['distance'] = doc.get('distance')
        listes_infos_stations_proches.append(infos_stations)
    return listes_infos_stations_proches

'''
Demande une nouvelle saisie à l'utilisateur pour qu'il est des informations sur une des stations dans son périmètre
'''

def saisie_infos_stations(infos):
    print("Voici les stations proches de votre position :")
    for i in range(len(infos)):
        print(str(i + 1) + " : " + infos[i].get('name') + " à " + str(round(infos[i].get('distance'))) + " mètres")
    valeur_station = str(input("Pour avoir des informations sur les disponibilités d'une station, veuillez saisir le numéro indiquer "
          "devant le nom de la station. Sinon appuyez sur n'importe quelle autre touche pour quitter la recherche. "))
    liste_valeur_possible = [str(j+1) for j in range (len(infos))]
    if valeur_station in liste_valeur_possible:
        infos_stations = DB.data_velo_lille.find_one({'station_id': infos[int(valeur_station)-1].get('station_id')})
        print("La station " + infos[int(valeur_station)-1].get('name') + " a " + str(infos_stations.get('bike_available'))
              + " vélo(s) de disponibles et " + str(infos_stations.get('stand_available')) + " stand(s) de disponibles.")
    else :
        print("Merci d'avoir consulté ces informations. Passez une bonne journée. A bientôt !")

'''
Exécution code
'''

def main():
    # utilisateur = saisie_coordonnees_utilisateur()
    utilisateur = SaisieUtilisateur(3.048760, 50.634306, 300)
    liste_stations_proches = recherche_station_proche(utilisateur)
    infos = infos_stations_proches(liste_stations_proches)
    saisie_infos_stations(infos)
    return None


main()
