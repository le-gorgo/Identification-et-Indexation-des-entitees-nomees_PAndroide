# coding: utf8
import functools
from sys import argv
import os, csv, string, codecs
import ast
import Identification as id


# present de le programme initial, adapté aux modifications
def loadRef(nomFic):
    f = codecs.open(nomFic, "r", "utf8", "replace")
    t = f.read()
    l = t.splitlines()
    res = dict()
    for line in l:
        mots = line.split('|')
        lab = mots[0]
        res[lab] = []
        for r in mots:
            res[lab].append(r.strip())
    f.close()
    return res


# present de le programme initial
def saveRef(d, nomFic):
    f = codecs.open(nomFic, "w", "utf8", "replace")
    for (lab, liste) in sorted(d.items()):
        line = lab

        for mot in liste[1:]:
            line = line + "|" + mot
        f.write(line + "\n")


# present de le programme initial, adapté aux modifications
def loadToSort(nomFic):
    f = codecs.open(nomFic, "r", "utf8", "replace")
    t = f.read()
    l = t.splitlines()
    res = []
    for line in l:
        mots = line.split('@')
        mot = mots[0]

        coords = ast.literal_eval(mots[1])
        res.append((mot, coords))
    f.close()
    return res


def cmp(a, b):
    return (a > b) - (a < b)


# initialise les dictionnaires utilisés pour le tri des noms
def initialisation(listDicoFiles, listDicoNames, communFile="communs.txt", noiseFile="noise.txt",
                   toSortFile="toSort.txt"):
    toSort = loadToSort("toSort2.txt")
    mots = sorted(toSort, key=functools.cmp_to_key(lambda x, y: cmp(len(y), len(x))))
    dicos = []
    for i in range(len(listDicoFiles)):
        dicos.append((listDicoNames[i], loadRef(listDicoFiles[i]), listDicoFiles[i]))
    communs = (loadRef(communFile), communFile)
    noise = (loadRef(noiseFile), noiseFile)
    return toSort, mots, dicos, communs, noise


# demander au utilisateur de classer les noms : c'est la version initiale un peu modifiée
def classement(toSort, dicos, communs, noise, corpus):
    for mot in toSort:
        lines = corpus.split("\r")
        print("***************\n\n\n", mot[0], ":", '(', type(mot), ')')
        print("\ncontexte: \n")
        # if(mot[1][0]-1>0):
        #    print(lines[mot[1][0]-1],"\n")
        print(lines[mot[1][0]].replace(mot[0], '\033[44;33m{}\033[m'.format(mot[0])), "\n")

        # if(mot[1][0]+1<len(lines)):
        #   print(lines[mot[1][0]+1])
        i = 0
        for dico in dicos:
            i += 1
            print(i, ". ", dico[0])
        i += 1
        print(i, ". Bruit")
        print("0. Ajouter un mot commun")
        print("-1. Ignorer")
        print("-3. Arreter")
        print(searchAlias(mot[0], dicos))
        if searchAlias(mot[0], dicos)[2]:
            n = eval(input("Choix? "))
        else:
            n = -1

        if (n > 0):
            if (n == i):
                noise[0][mot] = [mot]
            else:
                d = dicos[n - 1][1]
                label = input("Label ? ")
                print(label, ':', type(label))
                if len(label) == 0:
                    label = mot[0]
                if not (label in d):
                    d[label] = [label]
                if not (label == mot):
                    d[label].append(mot[0])

        elif (n == -3):
            break
        elif (n == 0):
            label = input("Mot a ajouter ? ")
            communs[0][label] = [label]


# sauvegarde et affiche le contenu de tous les dictionnaires
def sauvegarde(dicos, communs, noise):
    for dico in dicos:
        print("\n", dico[0])
        saveRef(dico[1], dico[2])

    print("\nBruit")
    saveRef(noise[0], noise[1])
    print("\nCommun")
    saveRef(communs[0], communs[1])


# trouver l'entité correspond à l'alias
def searchAlias(alias, dicos):
    Trouv = False
    ent = ""
    dictt = ""
    for dico in dicos:
        keys = list(dico[1].keys())
        for key in keys:
            if key == alias or alias in dico[1][key]:
                if not Trouv:
                    ent = alias
                    dictt = dico[0]
                    Trouv = True
                else:
                    pass
    return ent, dictt, Trouv


import csv

# main de test
if __name__ == "__main__":
    listDicoFiles = ["testLieux.txt", "testAuthors.txt", "testOeuvres.txt", "testPers.txt", "testInst.txt",
                     "testCrit.txt"]
    listDicoNames = ["LIEUX", "AUTHORS", "OEUVRES", "PERSONNAGES", "INSTITUTIONS", "CRITIQUES"]
    communFile = "testCommun.txt"
    noiseFile = "testNoise.txt"
    corpus, logf = id.initCorpus(["articles_presse_yourcenar.txt"], "out.log")
    toSort, mots, dicos, communs, noise = initialisation(listDicoFiles, listDicoNames, communFile, noiseFile,
                                                         "toSort.txt")
    i = 1
    lines = corpus.split("\r")
    with open('dataAnnotated.csv', 'w+', encoding="utf-8", newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Line#", "Word", "Tag"])
        ind = []
        values = []
        for mot in toSort:
            if mot[1][0] not in ind:
                ind.append(mot[1][0])
                values.append([mot])
            else:
                values[ind.index(mot[1][0])].append(mot)
        j = 0
        for t in values:
            print("*************")
            if len(t) >= 2:
                pr = True
            t = sorted(t, key=lambda tup: tup[1][1])
            line = lines[t[0][1][0]]
            for i in range(len(t)):
                res = searchAlias(t[i][0], dicos)
                if res[2]:
                    print(line)
                    ind = line.find(t[i][0])
                    tmpp = line[:ind].split(" ")
                    if pr: print(tmpp)
                    for m in tmpp:
                        if m != '':
                            writer.writerow(["Line" + str(j), m, "NoTag"])
                    if pr: print(t[i][0])
                    writer.writerow(["Line" + str(j), t[i][0], res[1]])
                    tmpp = line[ind + len(t[i][0]):]
                    if i == len(t) - 1:
                        tmpp = line[ind + len(t[i][0]):].split(" ")
                        if pr: print(tmpp)
                        for m in tmpp:
                            if m != '':
                                writer.writerow(["Line" + str(j), m, "NoTag"])
                    line = tmpp
                    j += 1
        # for mot in toSort:
        #     res = searchAlias(mot[0], dicos)
        #     if res[2]:
        #         line = lines[mot[1][0]]
        #         ind = line.find(mot[0])
        #         tmp = line[:ind].split(" ")
        #         for m in tmp:
        #             if m!= '':
        #                 writer.writerow(["Line" + str(i), m, "NoTag"])
        #         writer.writerow(["Line" + str(i), mot[0], res[1]])
        #         tmp = line[ind + len(mot[0]):].split(" ")
        #         for m in tmp:
        #             if m != '':
        #                     writer.writerow(["Line" + str(i), m, "NoTag"])
        #
        #         i += 1
    # classement(toSort,dicos,communs,noise,corpus)
    # sauvegarde(dicos,communs,noise)
