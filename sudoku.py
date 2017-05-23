#!/usr/bin/env python
# encoding:utf-8
# Exemple d'appel :
# python sudoku.py grille_diabolique --AIDE
##############################################################################
# 79 colonnes max-------------------------------------------------------------
##############################################################################

import numpy as np
import sys
import copy
from docopt import docopt # pour l'argument --AIDE
import itertools

# Import des fonctions persos
import fonctions

__version__="0.5"
__date__="23/05/2017"
__author__="Y. WRTAL"


help = """
sudoku.py

Usage:
  sudoku.py <nom_fichier_grille> [--AIDE]
 
Options:
  -h --help          C'est généré automatiquement.
  -a --AIDE          Pour n'afficher que les aides
"""



##############################################################################
# MAIN

if  __name__ == "__main__":
    arguments = docopt(help)
    if arguments['--AIDE']:
        AIDE = True
    else:
        AIDE = False
    #raw_input("Parametre d'aide egal a {0}".format(AIDE))
    
    sys.dont_write_bytecode = True
    
    grille_connue = fonctions.lecture_grille(sys.argv[1])
    
    iterations = 0
    restants = 81
    while (restants > 0):
        iterations += 1
        print("\nNOUVELLE ITERATION ({0}) : travail sur la grille suivante :".format(iterations))
        fonctions.affiche_grille(grille_connue)
        (possibilites, nouvelle_grille, nouveaux_determines, restants, listes_possibilites, erreurs) = fonctions.calcul_contraintes(grille_connue, AIDE)
        #print("\nIteration n{0} : tableau du nombre de possibilites :".format(iterations))
        #fonctions.affiche_grille(possibilites)
        if not AIDE:
            print("Iteration n{0} :\t{1} nouveaux chiffres places par la methode des contraintes, {2} inconnus restants".format(iterations, nouveaux_determines, restants))
        if nouveaux_determines == 0:
            if not AIDE:
                print("  Aucun nouveau chiffre place par contrainte : mise en oeuvre de la methode des masques.")
            (nouvelle_grille, nouveaux_determines, erreurs) = fonctions.calcul_masques(grille_connue, AIDE)
            if not AIDE:
                print("  Iteration n{0} :\t{1} nouveaux chiffres places par la methode des masques".format(iterations, nouveaux_determines, restants))
        # fin if
        if nouveaux_determines == 0:
            print("\nIteration n{0} : tableau du nombre de possibilites :".format(iterations))
            fonctions.affiche_grille(possibilites)
            print("Liste des chiffres possibles pour chaque case :")
            print(listes_possibilites)
            print("  Niveau de complexite necessitant des tests recursifs")

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
            cas_a_explorer = [cas_a_explorer[::-1]][0]
            #print(cas_a_explorer)
           
            for (nb_cas, i_essai, j_essai, set_possible) in cas_a_explorer:
                for nombre_possible in set_possible:
                    erreurs = False
                    print("  Niveau 0 : appel recursif avec le nombre {0} (du {1}) en ligne {2}, colonne {3}".format(nombre_possible, set_possible, i_essai+1, j_essai+1))
                    (grille_remplie, erreurs) = fonctions.resolution_recursive(nouvelle_grille, nombre_possible, i_essai, j_essai)
                    if not erreurs:
                        print("Grille remplie : on sort ! Inutile de tester le reste.")
                        nouvelle_grille = copy.copy(grille_remplie)
                        restants = 0
                        break
                # fin for nombre_possible
                if not erreurs:
                    break
            # fin itérations sur cas à explorer

            #exit()
        grille_connue = copy.copy(nouvelle_grille)
    # fin du while
    
    if not AIDE:
        print("\nRESULTAT FINAL :")
        fonctions.affiche_grille(nouvelle_grille)
