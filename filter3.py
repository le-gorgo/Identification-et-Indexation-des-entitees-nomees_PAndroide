#coding: utf8
import functools
from sys import argv
import os, csv, string, codecs
import ast

#present de le programme initial, adapté aux modifications
def loadRef(nomFic):
    f=codecs.open(nomFic,"r","utf8","replace")
    t = f.read()
    l=t.splitlines()
    res=dict()
    for line in l:
        mots = line.split('|')
        lab=mots[0]
        res[lab]=[]
        for r in mots:
            res[lab].append(r.strip())
    f.close()
    return res
#present de le programme initial
def saveRef(d,nomFic):
    f=codecs.open(nomFic,"w","utf8","replace")
    for (lab,liste) in sorted(d.items()):
        line=lab

        for mot in liste[1:]:

            line=line+"|"+mot
        f.write(line+"\n")
        print(line)

#present de le programme initial, adapté aux modifications
def loadToSort(nomFic):
    f=codecs.open(nomFic,"r","utf8","replace")
    t = f.read()
    l=t.splitlines()
    res=[]
    for line in l:
        mots = line.split('@')
        mot=mots[0]

        coords=ast.literal_eval(mots[1])
        res.append((mot,coords))
    f.close()
    return res

def cmp(a, b):
    return (a > b) - (a < b)

#initialise les dictionnaires utilisés pour le tri des noms
def initialisation(listDicoFiles,listDicoNames,communFile="communs.txt",noiseFile="noise.txt",toSortFile="toSort.txt"):
    toSort=loadToSort("toSort2.txt")
    mots=sorted(toSort,key=functools.cmp_to_key(lambda x, y: cmp(len(y), len(x))))
    dicos=[]
    for i in range(len(listDicoFiles)):
        dicos.append((listDicoNames[i],loadRef(listDicoFiles[i]),listDicoFiles[i]))
    communs=(loadRef(communFile),communFile)
    noise=(loadRef(noiseFile),noiseFile)
    return toSort,mots,dicos,communs,noise


#demander au utilisateur de classer les noms : c'est la version initiale un peu modifiée
def classement(toSort,dicos,communs,noise,corpus):
    for mot in toSort:
        lines=corpus.split("\r")
        print("***************\n\n\n",mot[0], ":",'(',type(mot),')')
        print("\ncontexte: \n")
        if(mot[1][0]-1>0):
            print(lines[mot[1][0]-1],"\n")
        print(lines[mot[1][0]].replace(mot[0],'\033[44;33m{}\033[m'.format(mot[0])),"\n")
        if(mot[1][0]+1<len(lines)):
            print(lines[mot[1][0]+1])
        i=0
        for dico in dicos:
            i+=1
            print(i,". ",dico[0])
        i+=1
        print(i,". Bruit")
        print("0. Ajouter un mot commun")
        print("-1. Ignorer")
        print("-3. Arreter")
        n=eval(input("Choix? "))
        if (n>0):
            if (n==i):
                noise[0][mot]=[mot]
            else:
                d=dicos[n-1][1]
                label=input("Label ? ")
                print(label,':',type(label))
                if len(label)==0:
                    label=mot[0]
                if not(label in d):
                    d[label]=[label]
                if not(label==mot):
                    d[label].append(mot[0])

        elif (n==-3):
            break
        elif (n==0):
            label=input("Mot a ajouter ? ")
            communs[0][label]=[label]

#sauvegarde et affiche le contenu de tous les dictionnaires
def sauvegarde(dicos,communs,noise):
    for dico in dicos:
        print("\n",dico[0])
        saveRef(dico[1],dico[2])


    print("\nBruit")
    saveRef(noise[0],noise[1])
    print("\nCommun")
    saveRef(communs[0],communs[1])


#main de test
if __name__=="__main__":
    listDicoFiles=["testLieux.txt","testAuthors.txt","testOeuvres.txt","testPers.txt","testInst.txt","testCrit.txt"]
    listDicoNames=["LIEUX","AUTHORS","OEUVRES","PERSONNAGES","INSTITUTIONS","CRITIQUES"]
    communFile="testCommun.txt"
    noiseFile="testNoise.txt"
    toSort,mots,dicos,communs,noise=initialisation(listDicoFiles,listDicoNames,communFile,noiseFile,"toSort.txt")
    classement(toSort,dicos,communs,noise)
    sauvegarde(dicos,communs,noise)
