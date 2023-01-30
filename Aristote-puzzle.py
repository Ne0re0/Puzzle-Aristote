from Application import Application
from random import choice
from copy import deepcopy

class Aristote:
    def __init__(self):
        self.largeur = 5
        self.hauteur = 5
        self.nb_click = 0
        self.root = Node([[('a'),("b"),('c')],[('d'),('e'),('f'),('g')],[('h'),('i'),('j'),('k'),('l')],[('m'),('n'),('o'),('p')],[('q'),('r'),('s')]],[k for k in range(1,20)])
        self.coordonnees()
        self.generer()
        self.creer_appli()
        self.appli.run()
        
        
    
    def coordonnees(self):
        """renvoie les coordonnées de toutes les cases jouables"""
        self.coordonnees = [(x,y) for x in range(self.largeur) for y in range(self.hauteur) if abs(x)+abs(y) < 7]
        self.coordonnees.remove((3,0))
        self.coordonnees.remove((4,0))
        self.coordonnees.remove((4,1))

    def generer(self) :
        """génère des nombres aléatoires entre 1 et 19 compris dans les cases valables aka self.coordonnees"""
        lien = {}
        possibles = [k for k in range(1,20)]
        for case in self.coordonnees:
            v = choice(possibles)
            possibles.remove(v)
            lien[case] = v
        self.lien = lien
        self.l0 = self.ligne(0)
        self.l1 = self.ligne(1)
        self.l2 = self.ligne(2)
        self.l3 = self.ligne(3)
        self.l4 = self.ligne(4)
        self.en_cours = True
        
        

    def ligne(self,y) :
        '''renvoie dans une liste les valeurs dune ligne de hauteur y (entre 0 et 4 compris)'''
        res = []
        for x in range(5):
            if (x,y) in self.coordonnees :
                res.append(self.lien[(x,y)])
        return res

    def echange(self, case1, case2):
        """Met la valeur de case1 dans case2 et inversement : case rentrées sous la forme (x,y)"""
        a = self.lien[case1]
        b = self.lien[case2]
        self.lien[case1] = b
        self.lien[case2] = a
        
    def victoire(self):
        """Stop le jeu si le joueur à gagné"""
        if sum(self.ligne(0)) == 38 and sum(self.ligne(1)) == 38 and sum(self.ligne(2)) == 38 and sum(self.ligne(3)) == 38 and sum(self.ligne(4)) == 38 :
            self.en_cours = False
            self.afficher("mes_images/carre_vert.png")
            
    ################################## partie graphique ###########################

    # Initialisation de l'interface
    def creer_appli(self):
        self.appli = Application('Puzzle Aristote', 1200, 900)
        self.en_cours = True
        self.appli.quadriller(6, 5, self.callback)
        self.afficher()

    # Gestion lors de l'affichage
    def afficher(self, couleur = "mes_images/carre_gris.jpg" ):
        """Affiche les valeurs au niveau des cases"""
        for key, value in self.lien.items():
            self.appli.boutons[key].background_normal = couleur
            self.appli.boutons[key].text = str(value)
        case_somme = [(5,0),((5,1)),(5,2),(5,3),(5,4)]
        for k in range(5):
            case = case_somme[k]
            value = str(sum(self.ligne(k)))
            self.appli.boutons[case].text = value
            if value == "38" :
                self.appli.boutons[case].background_color = (0,1,0,1)
            else :
                self.appli.boutons[case].background_color = (1,0,0,1)
            self.appli.boutons[(4,4)].background_normal = "mes_images/retry.jpg"
            self.appli.boutons[(4,0)].background_normal = "mes_images/loupe.jpg"
            
        
    # Action lors du click
    def callback(self, mon_bouton):
        if mon_bouton.identifiant == (4,4):
            self.generer()
            self.afficher()
        elif mon_bouton.identifiant == (4,0) :
            solution = self.root.parcourir()
            for key, value in self.lien.items() :
                self.lien[key] = solution[key[1]][key[0]]
            self.victoire()
            self.afficher("mes_images/carre_vert.png")       
        elif self.en_cours == True :
            if mon_bouton.identifiant in self.coordonnees:
                if mon_bouton.background_color == [0, 0, 1, 1] :
                    mon_bouton.reinitialiser()
                    self.afficher()
                    self.nb_click = 0
                else :
                    if self.nb_click == 0 :
                        self.nb_click = 1
                        mon_bouton.background_color = (0,0,1,1)
                        self.premier = mon_bouton
                    elif self.nb_click == 1 :
                        self.nb_click = 0
                        self.deuxieme = mon_bouton
                        a = self.lien[self.premier.identifiant]
                        self.lien[self.premier.identifiant] = self.lien[self.deuxieme.identifiant]
                        self.lien[self.deuxieme.identifiant] = a
                        self.premier.reinitialiser()
                        self.ligne(self.premier.identifiant[1])
                        self.ligne(self.deuxieme.identifiant[1])
                        self.afficher()
                        self.victoire()


    ################################## partie résolution ###########################
    
class Node:
    def __init__(self, etat, possibles):
        self.etat = etat
        self.possibles = possibles
        self.valeur_a_changer()

    def valeur_a_changer(self):
        """actualise self.valeur_a_changer avec les coordonnées de la prochaine valeur a modifier : (x,y)"""
        for l in range(5) :
            for c in range(len(self.etat[l])) :
                if type(self.etat[l][c]) != int :
                    self.valeur_a_changer = (l,c)
                    return
                    

    def creer_fils(self) :
        """renvoie la liste de tous les fils de pere"""
        pere = deepcopy(self.etat)
        lst_fils = []
        for element in self.possibles :
            pere[self.valeur_a_changer[0]][self.valeur_a_changer[1]] = element
            if self.valeur_a_changer == (0,2) or self.valeur_a_changer == (1,3) or self.valeur_a_changer == (2,4) or self.valeur_a_changer == (3,3) or self.valeur_a_changer == (5,2) :
                if sum(pere[self.valeur_a_changer[0]]) == 38 :
                    fils = Node(deepcopy(pere), deepcopy(self.possibles))
                    fils.possibles.remove(element)
                    lst_fils.append(fils)
            else :
                fils = Node(deepcopy(pere), deepcopy(self.possibles))
                fils.possibles.remove(element)
                lst_fils.append(fils)            
        self.fils = lst_fils
    
    def parcourir(self):
        """parcours l'arbre en profondeur"""
        racine = [self]
        k = 0
        while k != 1200 :
            x = racine.pop(-1)
            x.creer_fils()
            for fils in x.fils :
                racine.append(fils)
                try :
                    if sum(x.etat[0]) == 38 and sum(x.etat[1])== 38 and sum(x.etat[2])== 38 and sum(x.etat[3])== 38 :
                        break
                except :
                    pass
            k += 1
        return(fils.etat)


# Lancer une partie
if __name__ == '__main__' :
    a = Aristote()
