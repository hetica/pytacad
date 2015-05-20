# Pytacad

Ce script à été créé pour retrouver **rapidement** des informations sur un ou plusieurs étudiants du site netacad.com.  
Cisco ne fournit pas de champs de recherche, si bien qu'il est plus que fastidieux de retrouver un stagiaires dans la base.  
Et il est encore plus compliqué de retrouver ses classes.

Pytacad est divisé en 2 parties : 

## pytacad-server  

Son rôle est d'aller parser toutes les classes d'une académie Cisco sur le site netacad.com, et d'en extraire des informations :

* chaque classe est sotckée dans un fichier texte
* un fichier contient l'ensemble des stagiaires, et les classes auxquels ils appartiennent  

On pourra exécuter le serveur une ou plusieurs fois par jour à l'aide de la crontab

## pytacad-client  

Permet d'afficher des informations extraire par pytacad-server :  

* chercher un ou des stagiaires ou classes  
* mettre à jour la base de données (exécute pytacad-server)  
* afficher des infos générales (nombre de classes/stagiaires)  
