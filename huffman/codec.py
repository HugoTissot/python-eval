def coefficients(chaine):
    """Méthode renvoyant une liste de tuples composés des caractères et leurs occurences dans la chaine, triés par ordre décroissant d'occurence"""
    dico = {}
    for x in chaine :
        if x not in dico.keys() :
            dico[x] = 1
        else :
            dico[x] = dico[x] + 1
    liste = sorted(dico.items(), key = lambda t: t[1])
    liste.reverse()
    return (liste)

def deux_plus_gros (liste_noeud) :
    """Méthode qui renvoit les 2 plus gros scores des noeuds d'un arbre""" #Voir le builder des noeuds
    L = [x.score for x in liste_noeud]
    gros1 = max(L)
    L.remove(gros1)
    gros2 = max(L)
    return (gros1,gros2)

class noeud:
        def __init__(self, chaine, score, noeuds_suivants):
            self.chaine = chaine

            self.score = score  #Score correspond à la somme de toutes les occurences des caractères d'une chaine
            #Le score des noeuds est croissant quand on remonte l'arbre

            self.noeuds_suivants = noeuds_suivants #Si noeuds_suivants = ["",""] il s'agit d'une feuille
            # Le noeud est composé de sa chaine de caractère et des prochains noeuds qu'il forme le premier élément est le noeud
            # de gauche, le second celui de droite
        def __repr__(self):
            return(self.chaine) # Aide pour la construction du code


class TreeBuilder:

    def __init__(self, chaine):
        self.chaine = chaine
        self.coefficients = coefficients(chaine)
    def tree(self) :
        """Méthode pour construire l'arbre"""
        liste = self.coefficients[:] #On récupère la liste des caractères et de leurs occurences
        tree = [] #Liste des noeuds
        for x in liste :
            tree.append(noeud(x[0],x[1],["",""])) #On ajoute à l'arbre les feuilles
        while len(liste) > 1 :
            a = liste.pop()  #On récupère les 2 noeuds au score le plus bas pour les combiner (liste est triée par ordre
            b = liste.pop()   # d'occurence des caractères décroissant)

            lettre1 = a[0]
            occurence1 = a[1]
            lettre2 = b[0]
            occurence2 = b[1]
            nouveau_noeud = noeud(a[0] + b[0],a[1] + b[1] ,[a[0],b[0]])
            tree.append(nouveau_noeud) #On ajoute à l'arbre le noeud issu de leur combinaison
            combinaison = (a[0]+b[0],a[1]+b[1])


            for i in range (len(liste)) :
                if liste[i][1] < a[1] + b[1] :
                    liste = liste[:i] + [combinaison] + liste[i:]  #On place correctement la combinaison dans la liste pour                qu'elle reste triée
                    break
            if combinaison not in liste :
                liste.append(combinaison)


        #On se trouve ici dans le cas où il ne reste plus que la racine à placer dans l'arbre mais on cherche sa descendance

        score1,score2 = deux_plus_gros(tree) #Les 2 noeuds de plus gros scores sont sa descendance

        noeuds_racine = []
        copy_tree = tree[:]
        for x in copy_tree :
            if x.score == score1 :
                noeuds_racine.append(x)
                copy_tree.remove(x)
        for x in copy_tree :
            if x.score == score2 :
                noeuds_racine.append(x)

        tree.append(noeud(liste[0][0],score1 + score2,[noeuds_racine[1],noeuds_racine[0]]))
        self.tree = tree
        return tree




class Codec :

    def __init__(self,tree) :
        self.tree = tree



    def encode(self,text) :
        caracteres = [] #Liste des caractères pouvant composer le message
        codes = [] #Liste de leurs encodage en binaire (le ième élément correspond à l'encodage du ième caractère)
        for noeud in self.tree :
            if len(noeud.chaine) == 1 :
                caracteres.append(noeud.chaine)
        for x in caracteres :
            code_caractere = ""
            parents = [x] #Liste des noeuds parcourus pour atteindre la racine
            for noeud in self.tree :
                if parents[-1] in noeud.noeuds_suivants : #On cherche l'ascendant du dernier noeud parcouru
                    if parents[-1] == noeud.noeuds_suivants[0] : #Cas où le noeud a été généré à gauche de l'ascendant
                        code_caractere = "0" + code_caractere
                    else :
                        code_caractere =  "1" + code_caractere
                    parents.append(noeud.chaine)
            codes.append(code_caractere)

        message_code = ""
        clef = [] #Le ième élément de cette liste correspond au nombre de bits successifs codant la ième lettre du message
        # initiale
        #Malheureusement c'est la seule manière que j'ai trouvé pour séquencer correctement la lecture du message binaire, un
        #autre moyen aurait été de mettre un autre caractère que des 0 et 1 pour séparer 2 encodages de caractère (avec cette
        #méthode on aurait pu décoder un message sans l'encoder au préalable) mais l'énoncé semblait imposer un message codé de
        #sortie composé uniquement de 0 et 1
        for lettre in text : #La variable s'appelle lettre mais il peut s'agir de n'importe quel caractère
            for i in range (len(caracteres)) :
                if lettre == caracteres[i] : #On cherche le code qui correspond au caractère du texte
                    message_code = message_code + codes[i]
                    clef.append(len(codes[i]))

        self.caracteres = caracteres
        self.codes = codes
        self.clef = clef
        return message_code


    def decode(self,text_code) :
        message_decode = ""
        compteur = 0 #Compteur pour découper le message binaire en groupes de bits pertinents
        for x in self.clef :
            bits = text_code[compteur:compteur+x]
            compteur += x
            for i in range (len(self.codes)) :
                if bits == self.codes[i] :
                    message_decode = message_decode + self.caracteres[i]
        return message_decode



text = "L’homme n’est qu’un roseau, le plus faible des roseaux, mais c’est un roseau pensant."
builder = TreeBuilder(text)
binary_tree = builder.tree()


codec = Codec(binary_tree)

encoded = codec.encode(text)
decoded = codec.decode(encoded)
print(encoded)
print(decoded)