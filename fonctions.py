#!/usr/bin/env python
# encoding:utf-8
##############################################################################
# 79 colonnes max-------------------------------------------------------------
##############################################################################

import numpy as np
import copy
import itertools
import sys
sys.dont_write_bytecode = True

##############################################################################
# But : convertit le fichier grille en numpy.array
# Entrées :
#    - fichier : nom du fichier ASCII à lire
# Sorties :
#    - grille : numpy.array(9,9)

def lecture_grille(fichier):
    grille = np.zeros([9,9])
    f = open(fichier, "r")
    i = 0
    for line in f.readlines():
        ligne_char = line.rstrip('\n').replace("x", "0").split()
        grille[i] = [int(c) for c in ligne_char]
        i += 1
    #print(grille)
    f.close()
    return grille



##############################################################################
# But : affiche une grille avec délimitation par quadrant 3*3
# Entrées :
#    - grille : numpy.array(9,9)
# Sorties :
#    (sortie terminal)

def affiche_grille(grille):
    for i in range(9): # lignes
        if i == 0:
            print("+-----+-----+-----+")
        ligne = "|" # on la construit petit à petit
        for j in range(9): # colonnes
            if (j+1)%3 == 0:
                ligne += "{0:.0f}|".format(grille[i,j])
            else:
                ligne += "{0:.0f} ".format(grille[i,j])
        # fin j (colonnes = x)
        print(ligne)
        if (i+1)%3 == 0:
            print("+-----+-----+-----+")
    # fin i (lignes = y)
    return ()


##############################################################################
# But : Regarde la ligne/colonne/carré autour de la position pour réduire les
# possibilités
# Entrées :
#    - i : int. ligne du cas scruté
#    - j : int. colonne du cas scruté
#    - grille : np.array(9,9) = grille que l'on essaye de résoudre
# Sorties :
#    - set_possible : liste des valeurs plausibles - sous forme de set

def scrute_autour(i, j, grille):
    set_possible = set([1,2,3,4,5,6,7,8,9]) # initialement, ça peut être ça
    
    # On scrute la ligne i
    ligne_i = grille[i]
    for c in ligne_i:
        if c in set_possible:
            set_possible.remove(c)
    
    # on scrute la colonne j
    colonne_j = grille[:,j]
    for c in colonne_j:
        if c in set_possible:
            set_possible.remove(c)
    
    # on scrute le carré dans lequel se trouve (i,j)
    imin = 3*(i/3) # division entière python !!
    jmin = 3*(j/3) # division entière python !!
    imax = imin+3  
    jmax = jmin+3
    carre = grille[imin:imax, jmin:jmax]
    #print("\nCarre pour i={0}, j={1} :".format(i, j))
    #print(carre)
    for l in carre:
        for c in l:
            if c in set_possible:
                set_possible.remove(c)
    return set_possible


##############################################################################
# But : Calcule pour chaque position le nombre de chiffres possibles
#       et en place s'il n'y a aucune ambiguite
# Entrées :
#    - grille : grille sudoku de type np.array(9,9)
#    - AIDE : booléen. Dit si on n'affiche que l'aide
# Sorties :
#    - possibilites : tableau de meme type
#    - nouvelle_grille : nouvelle grille sudoku remplie avec les cas évidents
#    - nouveaux_determines: int. nombre de chiffres placés par l'itération
#    - restants : int. nombre de chiffres indéterminés restants
#    - listes_possibilites : grille sudoku comportant des listes de chiffres possibles
#    - erreurs : booléen. Si True, grille mauvaise

def calcul_contraintes(grille, AIDE=False):
    possibilites = np.zeros([9,9])
    listes_possibilites = np.zeros([9,9], dtype=object) # pour pouvoir y mettre des listes
    nouvelle_grille = copy.deepcopy(grille)
    nouveaux_determines = 0
    restants = 0
    erreurs = False # initialisation
    
    for i in range(9): # lignes
        for j in range(9): # colonnes
            if nouvelle_grille[i,j] == 0:
                set_possible = scrute_autour(i, j, nouvelle_grille)
                listes_possibilites[i,j] = set_possible
                possibilites[i,j] = len(set_possible)
                if possibilites[i,j] == 0: # aucun possible alors que la case est vide !
                    erreurs = True
                    #print("Aucune possibilite en ligne {0}, colonne {1} alors que la case est vide !".format(i+1, j+1))
                if possibilites[i,j] == 1:
                    nouvelle_grille[i,j] = list(set_possible)[0]
                    #print("Chiffre {0} place en ligne {1}, colonne {2} par la methode des contraintes".format(nouvelle_grille[i,j], i+1, j+1))
                    if AIDE:
                        print("AIDE: ligne {0} colonne {1} definissable par methode des contraintes".format(i+1, j+1))
                    nouveaux_determines += 1
                if nouvelle_grille[i,j] == 0:
                    restants += 1
                # fin if nouvelle_grille
            # fin if grille
        # fin j (colonnes)
    # fin i (lignes)
    return (possibilites, nouvelle_grille, nouveaux_determines, restants, listes_possibilites, erreurs)


##############################################################################
# But : Dit si un chiffre est déjà présent dans le carre de la case considérée
# Entrées :
#    - i : int. numéro de ligne de la case scrutée
#    - j : int. numéro de colonne de la case scrutée
#    - chiffre : int. chiffre à chercher dans le carre
#    - grille : np.array(9,9). Grille dans laquelle on regarde
# Sorties :
#    - carre_oqp : booléen. True si le chiffre est présent dans le carre

def chiffre_present_dans_carre(i, j, chiffre, grille):
    # on scrute le carré dans lequel se trouve (i,j)
    imin = 3*(i/3) # division entière python !!
    jmin = 3*(j/3) # division entière python !!
    imax = imin+3  
    jmax = jmin+3
    carre = grille[imin:imax, jmin:jmax]
    carre_oqp = chiffre in carre
    return carre_oqp

##############################################################################
# But : Regarde pour chaque chiffre et chaque contrainte (ligne/col/carre)
#       les endroits ou il est possible de placer ce chiffre
# Entrées :
#    - chiffre : chiffre à placer dans la grille
#    - grille : grille sudoku de type np.array(9,9)
# Sorties :
#    - possibilites : grilles avec des 0 et des 1

def determiner_possibilites(chiffre, grille):
    possibilites = np.ones([9,9]) # on mettra des 0 là où ya pas moyen
    for i in range(9): # lignes
        for j in range(9): # colonnes
            # Là on scrute chaque case pour construire le masque
            if grille[i,j] != 0: # déjà occupée
                possibilites[i,j] = 0
            else:
                colonne_oqp = chiffre in grille[:,j]
                ligne_oqp = chiffre in grille[i,:]
                carre_oqp = chiffre_present_dans_carre(i,j,chiffre, grille)
                if colonne_oqp or ligne_oqp or carre_oqp:
                    possibilites[i,j] = 0 # c'est mort, on peut pas mettre le chiffre ici
                # fin if occupé
            # fin scrutation de la case
        # fin j (colonnes)
    # fin i (lignes)
    
    #print("Grille des possibilites pour le chiffre {0} :".format(chiffre))
    #affiche_grille(possibilites)
    return possibilites


##############################################################################
# But : place les chiffres suivant les possibilites (si possibilite unique)
# Entrées :
#    - grille : grille sudoku de type np.array(9,9)
#    - AIDE : booléen. Dit si on n'affiche que l'aide
# Sorties :
#    - nouvelle_grille : nouvelle grille sudoku remplie avec les cas évidents
#    - nouveaux_determines : int. Nombre de nouveaux chiffres places

def calcul_masques(grille, AIDE=False):
    nouvelle_grille = copy.deepcopy(grille)
    nouveaux_determines = 0 # on va les compter
    erreurs = False
    for chiffre in range(1,10): # on scrute tous les chiffres
        possibilites = determiner_possibilites(chiffre, nouvelle_grille)
 
        # Ici on a construit le masque (tableau de zéros et de uns)
        # qui dit où on a le droit de placer le chiffre
        # Maintenant on regarde si dans une structure (ligne, colonne ou carré)
        # il n'y a qu'une seule possibilité de placer le chiffre, alors on le place.
        # donc on scrute les 9 lignes, puis les 9 colonnes, puis les 9 carrés
        
        # v0.2 : et dès qu'on a placé un chiffre, on actualise le tableau
        # des possibilites !
        
        for X in range(9):
            if possibilites[:,X].sum() == 1: # 1 seule possibilite dans la colonne X
                colonne = list(possibilites[:,X])
                num_colonne = X
                num_ligne = colonne.index(1)
                nouvelle_grille[num_ligne, num_colonne] = chiffre
                possibilites = determiner_possibilites(chiffre, nouvelle_grille) # actualisation
                if not AIDE:
                    #print("    Chiffre {0} place en ligne {1}, colonne {2} par la methode des masques (colonne)".format(chiffre, num_ligne+1, num_colonne+1))
                    pass
                else:
                    print("AIDE: Le chiffre {1} peut etre place dans la colonne {0} (methode des masques)".format(num_colonne+1, chiffre))
                nouveaux_determines += 1
                #print(num_ligne, num_colonne)
            # fin possibilite dans la colonne X
            if possibilites[:,X].sum() == 0 and not (chiffre in nouvelle_grille[:,X]):
                erreurs = True # car on n'a aucune possibilité dans la colonne mais le chiffre n'y est pas !
                break
            # fin if
            if possibilites[X,:].sum() == 1: # 1 seule possibilite dans la ligne X
                ligne = list(possibilites[X,:])
                num_ligne = X
                num_colonne = ligne.index(1)
                if not AIDE:
                    #print("    Chiffre {0} place en ligne {1}, colonne {2} par la methode des masques (ligne)".format(chiffre, num_ligne+1, num_colonne+1))
                    pass
                else:
                    print("AIDE: Le chiffre {1} peut etre place dans la ligne {0} (methode des masques)".format(num_ligne+1, chiffre))
                if nouvelle_grille[num_ligne, num_colonne] != chiffre: # s'il n'a pas déjà été placé par ailleurs
                    nouvelle_grille[num_ligne, num_colonne] = chiffre
                    possibilites = determiner_possibilites(chiffre, nouvelle_grille) # actualisation
                    nouveaux_determines += 1
                # fin if
                #print(num_ligne, num_colonne)
            # fin possibilite dans la ligne X
            if possibilites[X,:].sum() == 0 and not (chiffre in nouvelle_grille[X,:]):
                erreurs = True # car on n'a aucune possibilité dans la ligne mais le chiffre n'y est pas !
                break
            # fin if
        # fin X
        
        for I in range(3): # ligne de carres
            for J in range(3): # colonne de carres
                carre = possibilites[3*I:3*I+3, 3*J:3*J+3] # on a 9 carres comme ça
                if carre.sum() == 1: # 1 seule possibilite dans tout le carre !
                    (l, c) = np.where(carre == 1)
                    ligne_dans_carre = int(l)
                    col_dans_carre = int(c)
                    num_ligne = 3*I + ligne_dans_carre
                    num_colonne = 3*J + col_dans_carre
                    nouvelle_grille[num_ligne, num_colonne] = chiffre
                    if not AIDE:
                        #print("    Chiffre {0} en ligne {1}, colonne {2} par la methode des masques (carre)".format(chiffre, num_ligne+1, num_colonne+1))
                        pass
                    else:
                        print("AIDE: Le chiffre {2} peut etre place dans le carre ({0},{1}) (methode des masques)".format(I+1, J+1, chiffre))
                    if nouvelle_grille[num_ligne, num_colonne] != chiffre: # s'il n'a pas déjà été placé par ailleurs
                        nouvelle_grille[num_ligne, num_colonne] = chiffre
                        possibilites = determiner_possibilites(chiffre, nouvelle_grille) # actualisation
                        nouveaux_determines += 1
                    # fin if nouvelle_grille
                    #print(num_ligne, num_colonne)
                # fin if
                if carre.sum() == 0 and not (chiffre in nouvelle_grille[3*I:3*I+3, 3*J:3*J+3]):
                    erreurs = True
                    break
                # fin if
            # fin for J
        # fin I (lignes de carres)

        #raw_input("Passer au chiffre suivant.")
    # fin for chiffre
    return (nouvelle_grille, nouveaux_determines, erreurs)


##############################################################################
# But : essaye de résoudre la grille en plaçant un chiffre à un endroit
# Entrées :
#    - grille : grille de base, connue et incomplète
#   - nombre : nombre à placer pour essai à la position donnée par :
#    - i_essai : ligne (int)
#    - j_essai : colonne (int)
#    - niveau : int. profondeur d'itération
# Sorties :
#    - grille_remplie : grille remplie de façon sûre
#    - erreurs : booléen. Présence d'une grille problématique (= hypothèse mauvaise)

def resolution_recursive(grille, nombre, i_essai, j_essai, niveau=1, chemin=""):
    chaine = "   "+"*"*niveau
    chemin += "+{0}en(l{1}c{2})".format(nombre, i_essai+1, j_essai+1)
    print(chaine+"Resolution recursive de niveau {0}".format(niveau))
    print(chaine+"++"+chemin)
    #print(chaine+"Essai avec le chiffre {0} en ligne {1}, colonne {2}".format(nombre, i_essai+1, j_essai+1))
    #Essai avec la nouvelle grille :
    grille_essai = copy.deepcopy(grille)
    grille_essai[i_essai, j_essai] = nombre
    
    # résolution de cette grille d'essai
    restants = 81 # nombre d'initialisation sans importance
    erreurs = False
    while (not erreurs and restants>0):
        # Résolution par méthode des masques
        (grille_apres_masques, nouveaux_determines1, erreurs) = calcul_masques(grille_essai)
        if erreurs:
            print(chaine+"ACHTUNG : erreur detectee dans le calcul par masques en niveau {0}".format(niveau))
            print(chaine+"          --> hypothese rejetee, on remonte d'un niveau et on teste la suivante")
            return (grille_essai, erreurs)
        else:
            grille_essai = copy.deepcopy(grille_apres_masques)
            print(chaine+"Methode des masques au niveau {1} sans erreur : {0} nouveaux elements places".format(nouveaux_determines1, niveau))
            #affiche_grille(grille_essai)
        # Résolution par méthode des contraintes
        (possibilites, grille_apres_contrainte, nouveaux_determines2, restants, listes_possibilites, erreurs) = calcul_contraintes(grille_essai)
        if erreurs:
            print(chaine+"ACHTUNG : erreur detectee dans le calcul par contraintes en niveau {0}".format(niveau))
            print(chaine+"          --> hypothese rejetee, on remonte d'un niveau et on teste la suivante")
            return (grille_essai, erreurs)
        else:
            grille_essai = copy.deepcopy(grille_apres_contrainte)
            print(chaine+"Methode des contraintes au niveau {1} sans erreur : {0} nouveaux elements places".format(nouveaux_determines2, niveau))

        #print(listes_possibilites)
        if nouveaux_determines1 + nouveaux_determines2 == 0:
            # Il faut rappeler cette fonction
            cas_a_explorer = []
            # les éléments seront de type :
            # [nb_possibilites,
            #  i_essai,
            #  j_essai,
            #  listes_possibilites]
            # et on les classe par ordre de nb_possibilites
            for i_essai, j_essai in itertools.product(range(9), range(9)):
                if possibilites[i_essai, j_essai] > 1:
                    cas_a_explorer.append((possibilites[i_essai, j_essai],
                                           i_essai,
                                           j_essai,
                                           listes_possibilites[i_essai, j_essai]
                                           ))
                # fin if
            # fin définition cas_a_explorer
            # Maintenant on doit le classer
            cas_a_explorer.sort()
            cas_a_explorer = cas_a_explorer[::-1]
            #print(cas_a_explorer)
            #raw_input("qu'est-ce qu'on attend ?")
            
            # Et là on itère
            erreurs = False
            for (nb_cas, i_essai, j_essai, set_possible) in cas_a_explorer:
                #erreurs = False
                for nombre_possible in set_possible:
                    print(chaine+"Niveau {0} : appel recursif plus profond avec le nombre {1} (du {2}) en ligne {3}, colonne {4}".format(niveau, nombre_possible, set_possible, i_essai+1, j_essai+1))
                    (grille_remplie, erreurs) = resolution_recursive(grille_essai, nombre_possible, i_essai, j_essai, niveau+1, chemin)
                    if not erreurs:
                        #print(chaine+"Sortie du niveau {0} sans erreur. Grille remplie :".format(niveau))
                        #restants = 0
                        #affiche_grille(grille_remplie)
                        return (grille_remplie, False)
                    #else:
                    #    print(chaine+"ACHTUNG : erreur detectee dans le calcul recursif en niveau {0}".format(niveau))
                    #    print(chaine+"          --> hypothese rejetee, on remonte d'un niveau et on teste la suivante")
                    #    return (grille_essai, erreurs)
    # fin while
    # Si on sort d'ici, c'est qu'il n'y a plus rien à déterminer
    #raw_input("cOUcOU : on est sorti !!")
    if nouveaux_determines1 + nouveaux_determines2 != 0:
        grille_remplie = copy.deepcopy(grille_essai)
        erreurs = False
    elif erreurs:
        grille_remplie = copy.deepcopy(grille) # on revient à la grille initiale
    return (grille_remplie, erreurs)    
