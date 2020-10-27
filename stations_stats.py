'''
Bibliothèques à importer (les installations nécessaires au projet sont spécifiées dans le fichier texte requirements.txt)
'''

from pymongo import MongoClient

# Connexion au serveur MongoDB

ATLAS = MongoClient(
        'mongodb+srv://delhayedermu:delhayedermu@projectnosql.gtcde.gcp.mongodb.net/velo?retryWrites=true&w=majority')
DB = ATLAS.velo


# Recherche des données sur une station pour un intervalle d'heure données

def recherche_données_ratio(ratio):
    stations_sous_ratio = DB.data_velo_lille.aggregate([{
        "$project": {
            "_id": 0,
            "date": 1,
            "station_id": 1,
            "size": { "$sum": ["$bike_available", "$stand_available"]},
            "status": {
                "bikes": "$bike_available",
                "stands": "$stand_available"
            },
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
        print(str(infos_stations.get("name")) + " ( ratio : " + str(station.get("station_ratio")) + " )")
    return None


def group():  # pour vérifier le nombre de stations
    liste = DB.data_velo_lille.aggregate([{
        "$project": {
            "_id": 0,
            "date": 1,
            "station_id": 1,
            "size": {"$sum": ["$bike_available", "$stand_available"]},
            "status": {
                "bikes": "$bike_available",
                "stands": "$stand_available"
            }
        }
    },
        {
            "$group": {  # On regroupe les stations par leur identifiant
            "_id": "$station_id"
            }
        }
    ])
    i = 0
    for doc in liste:
        i = i+1
    print(i)




def main():
    group()
    stations_sous_ratio = recherche_données_ratio(0.2)
    affiche_nom_stations(stations_sous_ratio)

main()
