#!/usr/bin/python
# coding: utf-8

###############################################################
####################################################### MODULES
###############################################################

import argparse
import os
import sys
import urllib.request

###############################################################
############################################# AIDE ET ARGUMENTS
###############################################################

parser = argparse.ArgumentParser(
					prog='dico_tad',
					description='Création de wordlists à partir de pages web ou de fichiers avec suppression des doublons.\nVous aurez la possibilité de mettre les mots en minuscules, en majuscules ou tel quel, et de les filtrer en fonction de leur taille.\nSi vous ne précisez pas de fichier de sortie (-s), la liste sera affichée dans la sortie standard.',
					epilog='Ce programme a été créé par hackoys.')

parser.add_argument('chemin', help='Chemins des fichiers, dossiers ou URL des pages web (séparés par des virgules si plusieurs, - récupèrera l\'entrée standard).')
parser.add_argument('-s', '--sortie', help='Chemin du fichier dans lequel écrire la liste de mots.', required=False)
parser.add_argument('-t', '--taille', help='Taille des mots acceptés. Ex: 2-4 = de 2 caractères à 4 caractères inclus. 0=infini. (Par défaut 2-0)', required=False)
parser.add_argument('-r', '--recursif', help='Rechercher aussi dans les sous-dossiers. (uniquement pour un chemin local. Par défaut: non)', required=False)
parser.add_argument('--maj', help='Ajouter les mots convertis en majuscules dans la liste. (Par défaut: non)', action='store_true')
parser.add_argument('--min', help='Ajouter les mots convertis en minuscules dans la liste. (Par défaut: non)', action='store_true')
parser.add_argument('--tel', help='Ajouter les mots dans la liste tels qu\'ils ont été trouvés. (Par défaut: oui)', action='store_true')
parser.add_argument('--acc', help='Remplacer les voyelles avec des accents par leur lettre normale. (Par défaut: non)', action='store_true')

args = parser.parse_args()

###############################################################
################################################ INITIALISATION
###############################################################

autorises = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZâôûîêéèà-_.@/\\"
speciaux = [ "\\", "/", "@", ".", "_", "-" ]
tchemins = []
tmots = []
sortie = False
fichier = False
ttaille = [ 2, 0 ]
majuscule = False
minuscule = False
tel_que = True
accents = False
recursif = False

###############################################################
##################################################### FONCTIONS
###############################################################

# Suivant les types de conversions autorises j'ajoute le mot à la liste 
# et l'affiche en gardant ou pas les accents
def ajouter_mot(par_mot):
	if ttaille[1] > 0 and len(par_mot) > ttaille[1]: return
	mot = par_mot
	
	# Gestion des accents si nécéssaire
	if accents:
		mot = mot.replace("ê", "e").replace("é", "e").replace("è", "e").replace("ë", "e")
		mot = mot.replace("î", "i").replace("ì", "i").replace("ï", "i").replace("â", "a").replace("à", "a").replace("ä", "a")
		mot = mot.replace("ô", "o").replace("ò", "o").replace("ö", "o").replace("û", "u").replace("ù", "u").replace("ù", "u").replace("ü", "u")
		
	# Gestion de la casse
	if sortie != False:
		if tel_que:
			if not mot in tmots:
				tmots.append(mot)
				fichier.write(mot + "\n")
		if minuscule:
			mot = par_mot.lower()
			if not mot in tmots:
				tmots.append(mot)
				fichier.write(mot + "\n")
		if majuscule:
			mot = par_mot.upper()
			if not mot in tmots:
				tmots.append(mot)
				fichier.write(mot + "\n")
	else:
		if tel_que:
			if not mot in tmots:
				tmots.append(mot)
				print(mot)
		if minuscule:
			mot = par_mot.lower()
			if not mot in tmots:
				tmots.append(mot)
				print(mot)
		if majuscule:
			mot = par_mot.upper()
			if not mot in tmots:
				tmots.append(mot)
				print(mot)

# Analyse un mot ou suite de mot puis essaye de le scinder si 
# il contient des symboles autorisés pour récupérer les "sous-mots"
def analyser_mot(par_mot):
	# Vérification taille
	if len(par_mot) < ttaille[0]: return
	ajouter_mot(par_mot)
	for s in speciaux:
		if s in par_mot:
			for m in par_mot.split(s): analyser_mot(m)
			return

# Analyse une chaine en remplaçant tous les caractères interdits par 
# des espaces puis récupération et analyse des "mots" qui en retournent
def analyser_chaine(par_str):
	str = par_str
	for j in range(1, 256):
		if autorises.find(chr(j)) < 0:
			str = str.replace(chr(j), " ")
	while str.find("  ") >= 0:
		str = str.replace("  ", " ")
	for m in str.split(" "):
		analyser_mot(m)

# Lire un fichier et analyser la chaine qui en retourne
def analyser_fichier(par_chem):
	try:
		with open(par_chem, "r") as f:
			analyser_chaine(f.read())
	except IOError as e:
		print("# " + str(e))
		pass
		
# Lit le contenu d'un dossier et des sous-dossiers si on est en mode récursif
def analyser_dossier(par_chem):
	for el in os.listdir(par_chem):
		if os.path.isfile(par_chem + "/" + tchemins[i]):
			analyser_fichier(tchemins[i])
		elif os.path.isdir(par_chem + "/" + tchemins[i]) and recursif:
			analyser_dossier(tchemins[i])
			
# Lit le contenu d'une page web et l'analyse
def analyser_url(par_url):
	tmpstr = ""
	try:
		with urllib.request.urlopen(par_url) as f:
			tmpstr = str(f.read())
		analyser_chaine(tmpstr)
	except urllib.error.URLError as e:
		print("# " + str(e))
		pass
		
#################################################################
####################################################### EXECUTION
#################################################################

# Gestion de la casse
if args.maj or args.min or args.tel:
	if args.maj: majuscule = True
	else: majuscule = False
	if args.min: minuscule = True
	else: minuscule = False
	if args.tel: tel_que = True
	else: tel_que = False
if args.acc: accents = True
else: accents = False
if args.recursif: recursif = True
else: recursif = False

# Récupération des tailles maxi et mini
if args.taille:
	tmptab = args.taille.split("-")
	if len(tmptab) == 2:
		ttaille[0] = int(tmptab[0])
		ttaille[1] = int(tmptab[1])
	else:
		print("Erreur: La taille n'a pas été écrite correctement (voir aide).")
		print("Pour accéder à l'aide: dico_tad -h")
		print("				   ou: dico_tad --help")
		exit(1)
		
# Redirection de la sortie vers un fichier si nécéssaire
if args.sortie:
	sortie = args.sortie
	try: fichier = open(sortie, "w")
	except IOError as e:
		print("# " + str(e))
		exit(2)
		
# Lecture du ou des chemins et analyse (dossier, fichier ou url)
if args.chemin.find(',') >= 0:
	tchemins = args.chemin.split(',')
else:
	tchemins.append(args.chemin)

for i in range(0, len(tchemins)):
	if tchemins[i] == "-":					# Si on veut lire stdin
		analyser_chaine(sys.stdin.read())
	elif os.path.isfile(tchemins[i]):		# si c'est un chemin de fichier
		analyser_fichier(tchemins[i])
	elif os.path.isdir(tchemins[i]):		# si c'est un chemin de dossier
		analyser_dossier(tchemins[i])
	else:
		analyser_url(tchemins[i])			# sinon c'est une URL
if sortie != False: fichier.close()

exit(0)
