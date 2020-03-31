import sys
import ruler

DATASET = sys.argv[1]
# L'argument envoyé par le sytème est [bundle.py, fichier.txt]

with open(DATASET, "r") as dataset:
    sequences = dataset.readlines()

    #On supprime une ligne si leur nombre est impair
    if len(sequences) % 2 == 1 :
        sequences.remove(sequences[-1])

    #On supprime les caractères de saut de ligne
    for k in range (len(sequences)) :
        if sequences[k][-1:] == '\n' :
            sequences[k] = sequences[k][:-1]

    #On forme la liste des duos de séquences de nucléotides à aligner
    rulers = []
    for i in range (0,len(sequences),2) :
        rulers.append(Ruler(sequences[i],sequences[i+1]))

    #On aligne les séquences
    for j in range(len(rulers)) :
        rulers[j].compute()
        top,bottom = rulers[j].report()
        print("====== example # " + str(j+1) + " - distance = " + str(rulers[j].distance))
        print(top)
        print(bottom)
