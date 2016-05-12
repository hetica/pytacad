#!/usr/bin/python
# *-* coding:utf-8 *-*

"""
Docs diverses
	http://stockrt.github.io/p/handling-html-forms-with-python-mechanize-and-BeautifulSoup/
	http://stockrt.github.io/p/emulating-a-browser-in-python-with-mechanize/
	http://domeu.blogspot.fr/2011/03/beautifulsoup-comment-extraire-ou.html
Docs de mechanize
	http://www.pythonforbeginners.com/python-on-the-web/browsing-in-python-with-mechanize/
	PB de select
		http://stackoverflow.com/questions/8590172/setting-a-select-control-in-a-form-with-mechanize-using-python
Doc de BeautifulSoup : 
	http://www.daniweb.com/software-development/python/threads/405662/beautifulsoup-to-extract-multiple-td-tags-within-tr
	http://www.crummy.com/software/BeautifulSoup/bs3/documentation.html
Suivi de liens :
	http://www.pythonforbeginners.com/cheatsheet/python-mechanize-cheat-sheet/
	http://www.pythonforbeginners.com/python-on-the-web/browsing-in-python-with-mechanize/
HTTP Error 406 Not acceptable
	http://www.checkupdown.com/status/E406.html
"""
__appname__ = 'pytacad'
__version__ = "0.5"
__author__ = "Benoit Guibert <benoit.guibert@free.fr>"
__licence__ = "LGPL"


import os
import mechanize, urllib
import cookielib
# from bs4 import BeautifulSoup
from BeautifulSoup import BeautifulSoup
from _credentials import *

"""
Un fichier _credentials doit être créé à la racine du projet
Il contient les entrées : 
user = "login netacad"
mdp = "mot de passe"
"""

def manageFiles():
	"""
	Définit l'emplacement des fichiers générés
	Crée les répertoires s'ils ne sont pas présents
	"""
	cwd = '/var/local/pytacad/'
	dirClasses = cwd + 'classes'
	if not os.path.isdir(cwd):
		os.mkdir(cwd)
	if not os.path.isdir(dirClasses):
		os.mkdir(cwd + 'classes')
	os.chdir(cwd)
	
def createInstance():
	"""
	Se connecter au site Netacad de Cisco
	"""
	
	## CREER UNE INSTANCE DE BROWSER

	# Browser
	br = mechanize.Browser()

	# Cookie Jar
	cj = cookielib.LWPCookieJar()
	br.set_cookiejar(cj)

	# Browser options
	br.set_handle_equiv(True)
	# br.set_handle_gzip(True)
	br.set_handle_redirect(True)
	br.set_handle_referer(True)
	br.set_handle_robots(False)

	# Follows refresh 0 but not hangs on refresh > 0
	br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

	# Want debugging messages?
	#br.set_debug_http(True)
	#br.set_debug_redirects(True)
	#br.set_debug_responses(True)

	# User-Agent (this is cheating, ok?)
	br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; fr-FR; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

	return br

	## L'INSTANCE CRÉÉE, IL EST MAINTENANT POSSIBLE D'OUVRIR UNE PAGE OU D'INTERRAGIR

def connect2netacad(br):

	## The site we will navigate into, handling it's session
	r = br.open('https://www.netacad.com')
	# html = r.read()

	## Afficher les formulaires
	#for f in br.forms():
	#	print f
	
	## show the source
	# print r.info()
	## or
	# print br.response().info()

	## Show the html title
	print br.title()

	## Select the first (index zero) form
	br.select_form(nr=1)

	## User credentials
	br.form['_58_INSTANCE_fm_login'] = user
	br.form['_58_INSTANCE_fm_password'] = mdp
	## Login
	br.submit()

	## L'AUTHENTIFICATION ET LA CONNEXION SONT MAINTENANT RÉALISÉÉS
	## Vérifier si l'in est bien sur la page d'accueil du compte
	# print br.response().read()
	# print br.response().info()
	# print br.response().code
	print br.title()
	# response

	return br

def getListeClasses(br):
	"""
	Obtenir les Informations concernant toutes les classes
	- Nom de la classe
	- ID de la classe (un nombre)
	- URL (pour s'y connecter)
	- le nombre de cours actuels
	"""
	
	html = br.response().read()
	soup = BeautifulSoup(html)
	# print soup
	listeClasses = []
	for a in soup.findAll('ul', attrs={ 'class' : "course-list" } ):
		for b in a.findAll('a', title=True, href=True):
			nomCours = b['title']
			idCours = b['href'].split('/')[-1]
			# urlCours =  "https://www.netacad.com" + b['href']
			urlCours = b['href'].split('=')[1]
			urlCours = 'https://' + urlCours.split('/')[2] + r'/' + b['href'].split('=/')[-1]
			listeClasses = listeClasses + [[nomCours , idCours , urlCours ]]
	
	for a in listeClasses:
		print a
	
	return listeClasses		

def getInfosClasse(br):
	"""
	Récuperer les infos d'une classe : 
	- nom de la classe
	- type de cours (CCNA2, CCNA3)
	- date de début
	- date de fin
	- liste des stagiaires de la classe :
		nom;prénom;login;adresse mail;dernière connexion
	A étudier :
		réinitialiser le mot de passe d'un stagiaire
		demander une attestation
		demander une lettre
	"""
	urls = []
	for link in br.links():
		## Lister les URLs des pages à ouvrir
		if "courseId=" in link.url:
		#if "courseId=256623" in link.url:														# A COMMENTER
			## Ajouter le delta pour afficher 50 stagiaires par page
			delta = "&_omni_WAR_omniportlet_delta=50"
			link.url = link.url + delta
			urls.append(link.url)
		
	for a in urls:
		## Ouvrir la page de gestion de la classe
		resp = br.open(a)
		## Récupérer le contenu de la page
		content = resp.get_data()
		## Soup permet d'organiser les recherches par balise
		soup = BeautifulSoup(content)
		#print(content)																			# A COMMENTER
		#print(soup)																			# A COMMENTER
		### RECUPERER LA PARTIE INTERRESSANTE DE LA PAGE
		for cadre in soup.findAll('div', attrs={ 'class': "portlet-borderless-container" }):
			# print cadre.get_text().encode('utf-8')
			nb = 0
			for table in cadre.findAll('table'):
				#for td in table.find('td'):
				#print table																	# A COMMENTER
				### RECUPERER LES INFOS GENERALES
				if nb == 0:
					nb_infos = 0
					infos = []
					for a in table.findAll('td'):
						if nb_infos == 0:
							infos.append(a.getText().strip().encode('utf-8'))
						if nb_infos == 1:
							infos.append(a.getText().strip().encode('utf-8'))
						if nb_infos == 3:
							infos.append(a.getText().strip().encode('utf-8'))	
						if nb_infos == 4:
							infos.append(a.getText().strip().encode('utf-8'))
						if nb_infos == 7:
							infos.append(a.getText().strip().encode('utf-8'))
						if nb_infos == 8:
							infos.append(a.getText().strip().encode('utf-8'))
						if nb_infos == 10:
							infos.append(a.getText().strip().encode('utf-8'))
						if nb_infos == 11:
							infos.append(a.getText().strip().encode('utf-8'))
						nb_infos +=1
						
					print infos[0], infos[2]
					print infos[1], infos[3]
					print infos[4], infos[6]
					print infos[5], infos[7]
						
				### RECUPERER LES INFOS DU CURSUS
				if nb == 1:
					print 'table 2 : infos sur le cursus et la langue'
					for a,b in enumerate(table.findAll('tr')):
						if a == 1:
							cours = b.text.strip().split(':')[0]
							print(cours)
						
				### RECUPERER LES INFOS SUR LES FORMATEURS
				# A FAIRE
				if nb == 2:
					print 'table 3 : Infos sur les formateurs'
						
				nb +=1
		
		### Récupérer les infos sur les stagiaires
		print 'Infos sur les stagiaires'

		# Sélectionner uniquement le tableau des stagiaires
		stagTab = soup.find(id="_omni_WAR_omniportlet_studentsSearchContainer")

		# initialiser un dictionnaire qui contiendra les stagiaires
		stag = {}
		num_line = 0
		num_cell = 0
		# Sélectionner les cellules utilisant les 'class' css : "table-cell" et "course-view"
		for cellule in stagTab.findAll('td', attrs={'class' : "table-cell course-view"}):
			col = num_cell % 6
			# La première colonne par ligne est utilisée pour créer un item du dictionnaire
			if col == 0:
				stag[num_line] = [cellule.text.encode('utf-8')]
			# on ajoute les items des colonnes 1 à 4 
			elif col <= 4:	
				stag[num_line].append(cellule.text.encode('utf-8'))
			# la sixième colonne, inutile, permet d'incrémenter le numéro de ligne...
			elif col == 5:
				num_line +=1
			# Pour chaque cellule, on incrémente de 1
			num_cell+=1

		
		### CREER LE FICHIER
		file = 'classe_' + infos[2].replace(' ','_') + '.txt'
		f = open( './classes/' + file, 'w')		
		### AJOUTER LES INFOS D'ENTETE
		f.write('Cursus : ' + cours + '\n')
		f.write('Nom de la classe : ' + infos[2] + '\n')
		f.write('ID de la classe : ' + infos[3] + '\n')
		f.write('Date de début : ' + infos[6] + '\n')
		f.write('Date de fin : ' + infos[7] + '\n')
		f.write('\nNom;Prénom;login;mail;last login\n')
		### AJOUTER LES STAGIAIRES
		# print(stag)
		for a in stag.values():
			f.write("{};{};{};{};{};\n".format(a[1], a[0], a[2], a[3], a[4]))
		### FERMER LE FICHIER
		f.close()

def getManageClasse(br):
	"""
	Aller sur la page d'administration d'une classe
	"""
	resp = br.open('https://1336773.netacad.com/courses/30329/')
	print br.title()
	#print br.response().read()
	#br.retrieve('https://1336773.netacad.com/courses/30329/gradebook.csv','fic.csv')[0]
	"""
	url = 'https://1336773.netacad.com/courses/34582'
	br.follow_link('Link(url=url)')
	print br.response().read()
	"""
	"""
	for link in br.links():
		if r"35800" in link.url:
			print link
	"""
			#resp = br.follow_link(link)
			#print br.response().read()
	
			#print link.base_url
			#print link.url
			# resp = br.follow_link(link)
			# print br.title()

	# br.open('https://www.netacad.com/c/portal/saml/sso?entityId=http://1336773.netacad.com/saml2&RelayState=/courses/36308')
	# print br.title()
	
	## voir http://www.pythonforbeginners.com/cheatsheet/python-mechanize-cheat-sheet/
	
	## MAIS COMMENT OUVRIR UNE BETE PAGE ????
	"""
	r = br.open('https://1336773.netacad.com/courses/35800')
	print br.response().read()
	print br.response().info()
	print br.geturl()
	#br.retrieve('https://1336773.netacad.com/courses/35800/gradebook.csv', 'gradeboock.csv')[-1]
	"""

def createUsersList():
	### CREER LA LISTE DE TOUS LES STAGIAIRES
	### A FAIRE : UNE BLACKLIST
	f = 'listeUsers.txt'
	liste_stags = []
	for a in os.listdir('./classes'): 
		f = open('./classes/' + a)
		for a in f.readlines():
			if 'Nom de la classe' in a:
				classe = a.split(':')[1].strip()
			if '@' in a:
				stag = a.strip()
				liste_stags.append(stag)
		f.close()
	## Supprimer les doublons de ligne
	l = list(set(liste_stags))
	# l.sort()

	### AJOUTER LEURS CLASSES AUX STAGIAIRES
	## Pour chacune des classes
	listeStags = []
	for a in os.listdir('./classes'):
		## a : liste des fichiers de classe
		f = open('./classes/' + a)
		file = f.read()
		fic = file.split('\n')[1].split(': ')[1]
		## A chaque fois que l'email d'un stagiaire est trouvée dans
		## un fichier, on ajoute le nom de la classe pour le stagiaire
		for i,stag in enumerate(l):
			mail =  stag.split(';')[3]
			if mail in file:
				l[i] = stag + fic + ','
		f.close()
	
	## Trier la liste des stagiaires
	l.sort()
	## Créer le fichier de la liste des stagiaires
	f = open('liste_stagiaires', 'w')
	## Ecrire chaque entrée de stagiaire
	for a in l:
		f.write(a + '\n')
	f.close

	print 'Nombre de stagiaires : ',len(l)
	

if __name__ == "__main__" :
	# gérer les répertoires de destination
	manageFiles()
	# créer une instance de navigateur web
	br = createInstance()
	# se connecter à Netacad
	connect2netacad(br)
	## listeClasses = getListeClasses(br)	# ne pas activer
	# récupérer les infos sur les stagiaires et classes
	getInfosClasse(br)		# A ACTIVER
	## getManageClasse(br)
	br.close()
	# créer la liste des students
	createUsersList()			# A ACTIVER
