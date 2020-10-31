# velo_delhaye_dermu

Ce projet est fait dans un cadre scolaire (cours de NoSQL). Les collaborateurs de ce projet sont : DELHAYE François et DERMU Romain. 

Le but de ce projet est d'écrire 4 codes python et mongo.

Le premier doit récupérer des données de stations de vélo en libre-service (géolocalisation, taille, nom, ...) dans 4 villes différentes (Lille, Lyon, Paris et
Rennes).
Le second doit effectuer des mises à jour de ces différentes données et les stocker.
Le troisième doit donner les stations disponibles à proximité d'un utilisateur (en fonction de sa position : longtitude et latitude) en utilisant les données mises à jour. 
Enfin, effectuer les dernières instructions suivantes :
	- trouver une station grâce à son nom (enfin quelques lettres de celui-ci)
	- mettre à jour une station
	- supprimer une station et ses données
	- désactiver toutes les stations dans un espace donné
	- donner toutes les stations avec un ratio vélo/total emplacement inférieur à 20% entre 18h et 19h (entre lundi et vendredi).

--------------------------------------------------------------------------------------------------------------------------------------------------------------
Le fichier importation_data.py charge l'ensemble des informations générales des stations pour les villes de Lille, Lyon, Paris et Rennes. /!\ Ne pas exécuter 
pour ne pas avoir l'ensemble des stations en double

Le fichier update_worker effectue la mise à jour régulière et temporelle des informations d'une station (nombre de vélos et de stations disponibles).

Le fichier stations_proxi agit comme une interface utlisateur. L'utilisateur a la possibilité de saisir ses coordonnées ainsi qu'un rayon de recherche et reçoit l'ensemble des stations 
qui se situe à proximité (le nom, le nombre de vélos et de stands disponibles, l'heure et la date des informations). Une mise à jour des données est faite avant la saisie de l'utilisateur.

Les fichiers stations_options et stations_stats agissent comme des interfaces administrateurs. Le premier propose à l'administrateur de chercher une station ou 
de désactiver les stations dans un périmètre qu'on lui demande de définir par la suite. S'il effectue une recherche, il doit saisir le nom de la station qu'il cherche ou une partie de celui-ci.
Une fois la recherche effectuée, il peut choisir une station pour soit la modifier (dans l'exemple, on modifie l'option tpe mais il est possible pour le futur de développer cette partie pour que l'administrateur
modifie les informations qu'il désire) soit la supprimer ( la station est supprimée défénitivement et ses futures données ne seront plus chargées). Enfin, le fichier stations_stats renvoie le nom des stations (et
leurs ratios) qui ont un ratio inférieur à 0.2 le samedi entre 18H et 19H (il est possible d'améliorer cela afin que l'on obtienne les informations des stations sur n'importe quelle période).
  