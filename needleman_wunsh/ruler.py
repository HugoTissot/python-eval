import numpy as np
from colorama import Fore, Style

def red_text(text):
    return f"{Fore.RED}{text}{Style.RESET_ALL}"

#Méthode permettant de déterminer si 2 lettres sont identiques (+0 de distance) et +1 de distance dans le cas contraire
def match(a,b) :
    if a == b :
        return 0
    else :
        return 1
def element_min(L) :
    min = L[0]
    indice = 0
    for i in range(len(L)):
        if L[i] < min :
            min = L[i]
            indice = i
    return(min,indice)



class Ruler :

    def __init__(self , a , b) :
        """Constructeur de l'objet a et b correspondent aux 2 séquences de nucléotides dont on cherche la distance"""
        self.a = a
        self.b = b
        self.parcourscalcul = False     #Variable indiquant si on a déjà réalisé la méthode compute pour cet objet




    #Note : Je n'ai pas suivi le procédé présenté sur wikipedia mais plutôt celui présenté dans une vidéo Youtube, je conseille vivement de la consulter rapidement pour comprendre la construction des matrices de score et de parcours

    #                         https://www.youtube.com/watch?v=vqxc2EfPWdk

    def compute(self) :
        """Méthode calculant la distance entre les 2 séquences"""
        print("Calcul de la distance en cours..")
        i = len(self.a)
        j = len(self.b)


        #Création de la matrice de score nous permettant de déterminer le meilleur alignement possible
        M = np.zeros((i+1,j+1), int)
        M[0,:] = [k for k in range(j+1)]
        M[:,0] = [k for k in range(i+1)]




        #Création de la matrice de parcours, elle explicite à partir de quel coefficient un coefficient a été calculé (coefficient supérieur, de gauche ou diagonale supérieure gauche)
        P = np.array([["" for y in range (j+1)] for x in range(i+1)])
        P[0,:] = ["Bord" for k in range(j+1)]
        P[:,0] = ["Bord" for k in range (i+1)]
        #On remplira cette matrice avec : "Diagonale" (ou "D"), "Haut" (ou "H") ou "Gauche" (ou "G") pour indiquer la provenance du coefficient
        #Elle nous servira à aligner les séquences et non calculer leur distance (voir méthode "report")





        for y in range(1,j+1) :
            for x in range (1,i+1) :
                #Liste des 3 résultats possibles pour remplir la prochaine case de la matrice de score (2 provenants des cases adjacentes et 1 de la case en diagonale)
                Res = []


                Res.append(M[x-1][y-1] + match(self.a[x-1],self.b[y-1]))   #Score si on calcule le coefficient à partir de celui dans la diagonale supérieure gauche
                Res.append(M[x-1][y] + 1)         #Score si on calcule le coefficient à partir de celui d'au dessus
                Res.append(M[x][y-1] + 1)           #Score si on calcule le coefficient à partir de celui à gauche


                M[x][y],indice = element_min(Res)            #On construit le nouveau coefficient en choisissant la méthode qui le minimise
                #Et on retient l'indice dans la liste Res du coefficient ayant engendré le nouveau
                # i = 0 c'est cas ou le coefficient a été calculé à partir de la diagonale : "Diagonale"
                # i = 1 à partir de la gauche : "Gauche"
                # i = 2 à partir du haut : "Haut"

                if indice == 0 :
                    P[x][y] = "Diagonale"
                elif indice == 1 :
                    P[x][y] = "Haut"
                else :
                    P[x][y] = "Gauche"


        self.parcours = P
        self.parcourscalcul = True
        self.distance = M[i][j]         #On lit la distance sur le coefficient dans le coin inférieur droite de la matrice (dernier coefficient construit)



    def report(self) :
        """Méthode qui utilise la matrice de parcours pour obtenir l'alignement des séquences qui minimise la distance"""
        top = ""            #Séquence alignée supérieure
        bottom = ""         #Séquence alignée inférieure
        if not(self.parcourscalcul) :
            print("Veuillez réaliser la méthode compute() au préalable")
            return

        P = self.parcours   #On récupère la matrice de parcours, on va la remonter pour

        x = len(self.a)
        y = len(self.b)

        while x > 0 or y > 0 :


            # Les conditions ne portent que sur la première lettre car on perd de l'information dans le array
            # Cas où on est sur un bord gauche ou supérieur de la matrice de parcours
            if P[x][y] == "B" :
                while x > 0 :
                    top = self.a[x-1] + top
                    bottom = red_text("=") + bottom
                    x -= 1
                while y > 0 :
                    top = red_text("=") + top
                    bottom = self.b[y-1] + bottom
                    y -= 1


            #Cas où le coefficient a été issu à partir d'un coefficient situé en diagonale => pas d'insertion
            if P[x][y] == "D" :
                if self.a[x-1] != self.b[y-1] :
                    top = red_text(self.a[x-1]) + top
                    bottom = red_text(self.b[y-1]) + bottom
                else:

                    top = self.a[x-1] + top
                    bottom = self.b[y-1] + bottom
                x -= 1
                y -= 1


            #Cas où le coefficient a été issus à partir d'un coefficient adjacent => insertion
            elif P[x][y] == "G" :
                top = red_text("=") + top
                bottom = self.b[y-1] + bottom
                y -= 1
            elif P[x][y] == "H" :
                top = self.a[x-1] + top
                bottom = red_text("=") + bottom
                x -= 1

        return top,bottom










