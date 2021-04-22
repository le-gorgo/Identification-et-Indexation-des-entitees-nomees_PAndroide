#coding: utf8
from sys import argv
import os, csv, string, codecs


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

def saveRef(d,nomFic):
    f=codecs.open(nomFic,"w","utf8","replace")
    for (lab,liste) in sorted(d.items()):
        line=lab
        for mot in liste[1:]:
            line=line+u"|"+mot
        f.write(line+u"\n")
        print(line)


def loadToSort(nomFic):
    f=codecs.open(nomFic,"r","utf8","replace")
    t = f.read()
    l=t.splitlines()
    res=dict()
    for line in l:
        mots = line.split(':')
        lab=mots[0]
        res[lab]=mots[1]
    f.close()
    return res

dico=loadToSort("toSort.txt")
keys=sorted(dico,lambda a,b:cmp(len(b),len(a)))

lieux=loadRef("testLieux.txt")
pers=loadRef("testPers.txt")
authors=loadRef("testAuthors.txt")
oeuvres=loadRef("testOeuvres.txt")
inst=loadRef("testInst.txt")
crit=loadRef("testCrit.txt")
communs=loadRef("testCommun.txt")
noise=loadRef("testNoise.txt")

for mot in keys:
    print "***************\n\n\n",mot, ":", dico[mot],'(',type(mot),')'
    print "1. Lieu"
    print "2. Auteur"
    print "3. Institution"
    print "4. Personnage"
    print "5. Oeuvre"
    print "6. Critique"
    print "7. Bruit"
    print "0. Ajouter un mot commun"
    print "-1. Ignorer"
    print "-3. Arreter"
    n=input("Choix? ")
    if (n>0):
        if (n==7):
            noise[mot]=[mot]
        else:
            if (n==1):
                d=lieux
            elif (n==2):
                d=authors
            elif (n==3):
                d=inst
            elif (n==4):
                d=pers
            elif (n==5):
                d=oeuvres
            elif (n==6):
                d=crit
            label=raw_input("Label ? ").decode('utf8')
            print label,':',type(label)
            if len(label)==0:
                label=mot
            if not(label in d):
                d[label]=[label]
            if not(label==mot):
                d[label].append(mot)

    elif (n==-3):
        break
    elif (n==0):
        label=raw_input("Mot a ajouter ? ").decode('utf8')
        communs[label]=[label]


print "\nLIEUX"
saveRef(lieux, "testLieux.txt")
print "\nAUTHORS"
saveRef(authors, "testAuthors.txt")
print "\nOEUVRES"
saveRef(oeuvres, "testOeuvres.txt")
print "\nPERSONNAGES"
saveRef(pers, "testPers.txt")
print "\nINSTITUTIONS"
saveRef(inst, "testInst.txt")
print "\nCRITIQUES"
saveRef(crit, "testCrit.txt")
print "\nBRUIT"
saveRef(noise, "testNoise.txt")
print "\nCOMMUN"
saveRef(communs, "testCommun.txt")

print "T"
print type('T'.encode('ascii'))
print type('T'.decode('ascii'))
print type('T'.encode('utf8'))
print type('T'.decode('utf8'))

