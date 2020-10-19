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