#!/usr/bin/python
# *-* coding:utf-8 *-*

__appname__ = 'pytacad-client'
__version__ = "0.2"
__author__ = "Benoit Guibert <benoit.guibert@free.fr>"
__licence__ = ""

import os, sys
import unicodedata

server = os.path.dirname(sys.argv[0]) + '/pytacad-server'
cwd = '/var/local/pytacad/'
dirClasses = cwd + 'classes'
os.chdir(cwd)

def find_user():
	back2menu = False
	while back2menu != "m":
		os.system('clear')
		print("\n CHERCHER UN STAGIAIRE")
		print(" ---------------------\n")
		search_str = raw_input('\n Qui cherchez-vous ? : ')
		f = open('liste_stagiaires')
		c = f.readlines()		# c : contenu avec une liste des lignes
		nb = 0
		list_stag = []
		for a in c:
			if unicodedata.normalize("NFKD", unicode(search_str.lower(), 'utf-8')).encode('ascii', 'ignore') in unicodedata.normalize("NFKD", unicode(a.lower(), 'utf-8')).encode('ascii', 'ignore'):
				list_stag.append(a)
				nb +=1

		if nb == 0:
			os.system('clear')
			print("\n Aucune occurence n'a été trouvée, élargissez votre recherche")
		if nb == 1:
			### Afficher le stagiaire trouvé
			os.system('clear')
			print ("\n")
			afficher_stag(list_stag[0])		
		if nb > 1:
			### si plusieurs occurences sont trouvées, choisir une entrée, ou toutes
			os.system('clear')
			print('\n {0} occurences ont été trouvées :\n'.format(nb))
			for i, stag in enumerate(list_stag):
				print(' {0}) {1} {2}'.format(i + 1, stag.split(';')[1], stag.split(';')[0]))
			try:
				choix = input("\n Tapez le chiffre correspondant, ou 'Entrée' pour tous les afficher : ")
			except:
				choix = 0
			### Afficher le ou les stagiaires
			os.system('clear')
			print("\n")
			if choix == 0 :
				for a in list_stag:
					afficher_stag(a.strip())
			else :
				afficher_stag(list_stag[choix - 1])
		back2menu = raw_input("\n Tapez sur la touche 'm' pour revenir au menu... ")

def afficher_stag(stag):
	s = stag.split(';')
	print(' Stagiaire : \t{0} {1} ({2})'.format(s[1], s[0], s[3]))
	print (' Classes : ') ,
	for i,a in enumerate(stag.split(';')[5].split(',')):
		if i == 0: print ('\t{0}'.format(a))
		else : print('\t\t{0}'.format(a))

def infos():
	os.system('clear')
	print("\n INFOS GENERALES\n")
	f = open('liste_stagiaires').readlines()
	print(" Nombre de stagiaires : {0}".format(len(f)))
	classes = os.listdir(dirClasses)
	print(" Nombre de classes : {0}".format(len(classes)))
	c = raw_input("\n Tapez sur une touche pour revenir au menu,\n ou 'c' pour afficher les noms des classes... ")
	if c == "c":
		os.system('clear')
		for a in classes:
			fclasse = open("./classes/" + a)
			print(fclasse.readlines()[1].split(": ")[1].rstrip())
		
		raw_input("\n Tapez sur une touche pour revenir au menu")

def maj_bd():
	os.system('clear')
	print("\n MISE A JOUR DE LA BASE DE DONNEES")
	print(" ---------------------------------\n")
	print(' La base de données est mise à jour 2 fois par jour, à 8H30 et 13H30.')
	print(' Il est cependant possible de forcer une mise à jour ponctuelle en cas de besoin.')
	print(" Celle-ci peut durer plusieurs minutes car il faut télécharger des pages Web sur Internet")
	c = raw_input("\n Voulez-vous mettre la base de donnée à jour (taper 'y' pour accepter) ? ")
	if c == "y":
		print(" Merci de patienter...\n")
		os.system(server)
		print("\n La mise à jour est terminée")
		raw_input("\n Tapez sur une touche pour revenir au menu... ")

def menu():
	while 1:
		os.system('clear')
		print("   | Pour une bonne prise en charge des accents avec putty :  |")
		print("   | Section Windows/Translation, et sélectionner UTF-8.      |")
		print("   | Enregistrer dans 'default-settings' est une bonne idée   |")
		print("   -----------------------------------------------------------")
		print("\n\tGESTION DE CISCO NETACAD")
		print("\t------------------------\n")
		print(' 1) Faire une recherche par mot clé')
		print(" 2) Faire une mise à jour de la base de données")
		print(" 3) Afficher des infos générales")	
		c = raw_input("\n Choisissez un nombre ou tapez 'Entrée' pour quitter : ")	
		if c == '1' : find_user()
		if c == '2' : maj_bd()
		if c == '3' : infos()
		if c == '' : break

if __name__ == "__main__" :
	menu()
