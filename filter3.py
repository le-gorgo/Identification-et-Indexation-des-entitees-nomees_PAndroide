#coding: utf8
import functools
from sys import argv
import os, csv, string, codecs
import ast
import textdistance

#present de le programme initial, adapté aux modifications
def loadRef(nomFic,max_id):
    if(os.path.isfile(nomFic)):
        f = codecs.open(nomFic, "r", "utf-8", "replace")
    else:
        f=codecs.open(nomFic, "w+", "utf-8", "replace")
    t = f.read()
    l = t.splitlines()
    res = dict()
    for line in l:
        line=line.split(':')
        id=line[0]
        if(int(id)>max_id):
            max_id=int(id)
        mots = line[1].split('|')
        occurences=line[2].split(';')
        res[id]=(mots,occurences)
    f.close()
    return res,max_id

def loadMiscRef(nomFic):
    if(os.path.isfile(nomFic)):
        f = codecs.open(nomFic, "r", "utf-8", "replace")
    else:
        f=codecs.open(nomFic, "w+", "utf-8", "replace")
    t = f.read()
    l = t.splitlines()
    res = dict()
    for line in l:
        line=line.split(':')
        mot=line[0]
        occurences=line[1].split(';')
        res[mot]=occurences
    f.close()
    return res

#present de le programme initial
def saveRef(d,nomFic):
    f=codecs.open(nomFic,"w+","utf8","strict")
    for (lab,listes) in sorted(d.items()):
        line=lab+":"
        for mot in listes[0]:

            line=line+mot+"|"
        line=line[:-1]+":"
        for occurence in listes[1]:
            line=line+str(occurence)+";"
        line=line[:-1]
        f.write(line+"\n")
        print(line)
    f.close()

def saveMiscRef(d,nomFic):
    f=codecs.open(nomFic,"w+","utf8","replace")
    for mot,occurences in d.items():
        line=mot+":"
        for occ in occurences:
            line=line+str(occ)+";"
        line=line[:-1]
        f.write(line+"\n")
    f.close()

#present de le programme initial, adapté aux modifications
def loadToSort(nomFic):
    f=codecs.open(nomFic,"r","utf8","replace")
    t = f.read()
    l=t.splitlines()
    res=[]
    for line in l:
        mots = line.split('@')
        mot=mots[0]
        pos=mots[1].split(';')[1:]
        coords=[ast.literal_eval(p) for p in pos]
        res.append((mot,coords))
    f.close()

    res.sort(reverse=True,key=lambda x: len(x[0]))

    return res

def cmp(a, b):
    return (a > b) - (a < b)

#initialise les dictionnaires utilisés pour le tri des noms
def initialisation(listDicoFiles,listDicoNames,communFile="communs.txt",noiseFile="noise.txt",toSortFile="toSort.txt"):
    toSort=loadToSort(toSortFile)
    mots=toSort
    dicos=[]
    max_id=0
    for i in range(len(listDicoFiles)):
        dico,id=loadRef(listDicoFiles[i],max_id)
        if(id>max_id):
            max_id=id
        dicos.append((listDicoNames[i],dico,listDicoFiles[i]))
    communs=(loadMiscRef(communFile),communFile)
    noise=(loadMiscRef(noiseFile),noiseFile)
    return toSort,mots,dicos,communs,noise,max_id
#fonction de suggestion en fonction de la distance de sorensen(à ameliorer) renvoie les 5 meilleurs candidats
def suggestion(dicos,mot):
    score=dict()
    for dico in dicos:
        for(id,listes) in dico[1].items():
            alias=listes[0]
            score[id]=0
            for a in alias:
                score_a=textdistance.sorensen(mot,a)
                if(score_a>score[id]):
                    score[id]=score_a
        res=sorted(score.items(), key=lambda item: item[1])

    return res[len(res)-5:len(res)]

def getDicoFromId(dicos,id):
    for dico in dicos:
        if(id in dico[1].keys()):
            return dico
def getAliases(dicos,id):
    for dico in dicos:

        if(id in dico[1].keys()):
            return dico[1][id][0]
def afficher_contexte(occurence,corpus,numWords):
    line=corpus[occurence[0]].splitlines()[int(occurence[1])]
    line=line.split()
    for i in range(numWords):
        line[int(occurence[2])-i]="\033[44;33m"+line[occurence[2]-i]+"\033[m"
    str=""
    for m in line:
        str+=m+" "
    print(str+"\n")

#demander au utilisateur de classer les noms : c'est la version initiale un peu modifiée
def classement(toSort,dicos,communs,noise,corpus,max_id):
    done=False
    for mot in toSort:
        if(done==True):
            return
        for occurence in mot[1]:
            print("***************\n\n\n",mot[0], ":",'(',type(mot),')')
            afficher_contexte(occurence,corpus,len(mot[0].split()))
            sugg=suggestion(dicos,mot[0])


            i=0
            ids=[]
            scores=[]
            for s in sugg:
                ids.append(s[0])
                scores.append(s[1])
            for i in range(1,len(sugg)+1):

                a=getAliases(dicos,ids[len(sugg)-i])
                line=str(i)+". "
                for alias in a:
                    line+=alias+', '
                line+='SCORE : '+str(scores[len(sugg)-i])+"\n"
                print(line)
            print(0,". Autre")
            print("-1. Ignorer")
            print("-3. Arreter")
            n=-2
            while((n!=-1 and n!=-3 and n<0) or n>i):
                n=eval(input("Choix? "))
                if(n<0 or n>i):
                    print("choisissez parmis les options")
            if(n>0):
                print("Peut-il y avoir des ambiguités sur ce mot?")
                print("1. Oui")
                print("2. Non")
                c=eval(input("Choix ?"))
                if(c==1):
                    d=getDicoFromId(dicos,ids[len(sugg)-n-1])
                    if(mot[0] not in d[1][ids[len(sugg)-n-1]][0]):
                        d[1][ids[len(sugg)-n-1]][0].append(mot[0])
                    d[1][ids[len(sugg)-n-1]][1].append(occurence)
                elif(c==2):
                    d=getDicoFromId(dicos,ids[len(sugg)-n-1])
                    if(mot[0] not in d[1][ids[len(sugg)-n-1]][0]):
                        d[1][ids[len(sugg)-n-1]][0].append(mot[0])
                    for occ in mot[1]:
                        d[1][ids[len(sugg)-n-1]][1].append(occ)

                    break
            elif(n==-3):
                done=True
                break
            elif(n==0):
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
                        print("Peut-il y avoir des ambiguités sur ce mot?")
                        print("1. Oui")
                        print("2. Non")
                        c=eval(input("Choix ?"))
                        if(c==1):
                            if(mot[0] in noise[0].keys()):
                                noise[0][mot[0]].append(occurence)
                            else:
                                noise[0][mot[0]]=[occurence]
                        if(c==2):
                            if(mot[0] in noise[0].keys()):
                                for occ in mot[1]:
                                    noise[0][mot[0]].append(occ)
                            else:
                                noise[0][mot[0]]=[]
                                for occ in mot[1]:
                                    noise[0][mot[0]].append(occ)
                            break
                    else:
                        print("Peut-il y avoir des ambiguités sur ce mot?")
                        print("1. Oui")
                        print("2. Non")
                        c=eval(input("Choix ?"))
                        max_id=max_id+1

                        if(c==1):
                            dicos[n-1][1][str(max_id)]=([mot[0]],[occurence])
                        elif(c==2):

                            dicos[n-1][1][str(max_id)]=([mot[0]],[])
                            for occ in mot[1]:
                                dicos[n-1][1][str(max_id)][1].append(occ)

                            break

                elif (n==-3):
                    done=True
                    break
                elif (n==0):
                    print("Peut-il y avoir des ambiguités sur ce mot?")
                    print("1. Oui")
                    print("2. Non")
                    c=eval(input("Choix ?"))
                    if(c==1):
                        if(mot[0] in communs[0].keys()):
                            communs[0][mot[0]].append(occurence)
                        else:
                            communs[0][mot[0]]=[occurence]
                    if(c==2):
                        if(mot[0] in communs[0].keys()):
                            for occ in mot[1]:
                                communs[0][mot[0]].append(occ)
                        else:
                            communs[0][mot[0]]=[]
                            for occ in mot[1]:
                                communs[0][mot[0]].append(occ)
                        break

#sauvegarde et affiche le contenu de tous les dictionnaires
def sauvegarde(dicos,communs,noise):
    for dico in dicos:
        print("\n",dico[0])
        saveRef(dico[1],dico[2])


    print("\nBruit")
    saveMiscRef(noise[0],noise[1])
    print("\nCommun")
    saveMiscRef(communs[0],communs[1])
