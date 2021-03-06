'''
Bibliothèques à importer (les installations nécessaires au projet sont spécifiées dans le fichier texte requirements.txt)
'''

from pymongo import MongoClient

# Connexion au serveur MongoDB

ATLAS = MongoClient(
        'mongodb+srv://delhayedermu:delhayedermu@projectnosql.gtcde.gcp.mongodb.net/velo?retryWrites=true&w=majority')
DB = ATLAS.velo


# Recherche des données sur une station pour un intervalle d'heure données

def recherche_données_ratio(ratio, heure_debut, heure_fin):
    stations_sous_ratio = DB.data_velo_lille.aggregate([{
        "$project": {
            "station_id": 1,
            "date complète": "$date",
            "heure": {"$hour": "$date"},
            "jour de la semaine": {"$dayOfWeek": "$date"},
            "ratio":    # Calcul du ratio pour l'ensemble des données
                {"$cond":
                    [
                        {'$ne':       # Si la taille n'est pas égale à 0
                            [
                                {"$sum":
                                     ["$bike_available", "$stand_available"]
                                 },
                                0.0
                            ]},
                        {"$divide":        # Alors on effectue le calcul du ratio
                            ["$bike_available",
                            {"$sum": ["$bike_available", "$stand_available"]}
                            ]
                                 },
                                0.0           # Sinon on met 0
                        ]}
                }
            },
            {"$match":
                 {"heure": {'$gte': heure_debut,'$lte': heure_fin, '$ne': heure_fin}}
             },
            {"$match":
                 {"jour de la semaine": {'$gte': 7}}
             },
            {
                "$group": {     # On regroupe les stations par leur identifiant
                "_id": "$station_id",
                "station_ratio": {"$avg": "$ratio"}
                }
            },
            {"$match":
                {"station_ratio": {'$lte': ratio}}
            }
    ])
    return stations_sous_ratio

def affiche_nom_stations(stations_sous_ratio):
    for station in stations_sous_ratio:
        infos_stations = DB.velo_lille.find_one({'_id': station.get('_id')})
        if infos_stations != None:
            print(str(infos_stations.get("name")) + " ( ratio : " + str(station.get("station_ratio")) + " )")
    return None

if __name__ == '__main__':
    heure_debut = 17
    heure_fin = 18   # Les heures de notre sauvegarde sont basées selon le méridien de Greenwich
    ratio = 0.2
    print("\n Affichage des stations ayant un ratio inférieur ou égal à " + str(ratio) + " entre 18h et 19h le samedi : ")
    stations_sous_ratio = recherche_données_ratio(ratio, heure_debut, heure_fin)
    affiche_nom_stations(stations_sous_ratio)

