# coding: utf8
import codecs
import functools
import string
import pypandoc
import os
#ce fichier reprend le travail du fichier test3.py pour que ce soit plus clair ce qu'il fait
#present dans le code initial
def postFilter(dico, liste):
    for mot in liste:
        f = 0
        if mot in dico:
            f = dico[mot]
            print("removing ", mot)
            del dico[mot]
        dico[mot] = 0
        toRemove = []
        for k in dico:
            if foundIn(k, mot):
                dico[k] = dico[k] - f
                print("... remove ", k, "? ", dico[k] <= 0)
                if dico[k] <= 0:
                    toRemove.append(k)
        for k in toRemove:
            del dico[k]

#present dans le code initial
def postFilterRef(dico, ref):
    for lab in ref:
        for mot in ref[lab]:
            f = 0
            if mot in dico:
                f = dico[mot]
                print("removing ", mot)
            del dico[mot]
            dico[mot] = 0
            toRemove = []
            for k in dico:
                if foundIn(k, mot):
                    dico[k] = dico[k] - f
                    print("... remove ", k, "? ", dico[k] <= 0)
                    if dico[k] <= 0:
                        toRemove.append(k)
            for k in toRemove:
                del dico[k]

#present dans le code initial
def cmp(a, b):
    return (a > b) - (a < b)

#present dans le code initial
def extractFilterRef(dico, ref):
    res = dict()
    keys = sorted(dico, key=functools.cmp_to_key(lambda x, y: cmp(len(y), len(x))))
    for lab in ref:
        res[lab] = 0
        for mot in ref[lab]:

            f = 0
            if mot in dico:
                f = dico[mot]
                res[lab] = res[lab] + dico[mot]
                del dico[mot]
            toRemove = []
            for k in keys:
                k=k[0]
                if foundIn(k, mot) and k in dico:
                    if f == 0:
                        f = dico[k]
                        res[lab] = res[lab] + f
                    dico[k] = dico[k] - f
                    if dico[k] <= 0:
                        toRemove.append(k)
            for k in toRemove:
                del dico[k]

    return res

#present dans le code initial
def extractRef(dico, ref):
    res = dict()
    for lab in ref:
        res[lab] = 0
        for mot in ref[lab]:
            if (mot in dico):
                res[lab] = res[lab] + dico[mot]
    return res

#present dans le code initial
#On suppose que le fichier est dans le bon format c'est à dire <identifiant>:<alias séparés par des | >:<occurences sous forme (fichier,ligne,mot) séparés par des ;>
def loadRef(nomFic,occurences):
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
        mots = line[1].split('|')
        occ=line[2].split(';')
        for o in occ:

            occurences.append(o)
        res[id] = []
        for r in mots:
            res[id].append(r.strip())
    f.close()
    return res,occurences
def loadMiscRef(nomFic,occurences):
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
        occ=line[1].split(';')
        for o in occ:
            occurences.append(o)
        res[mot]=occ
    f.close()
    return res,occurences
#present dans le code initial
def saveRef(d, nomFic):
    f = codecs.open(nomFic, "w+", "utf8", "replace")
    for (lab, liste) in sorted(d.items()):
        line = lab
        for mot in liste[1:]:
            line = line + "|" + mot
        f.write(line + "\n")
        print(line)

#present dans le code initial
def foundIn(mot, expr):
    ind = expr.find(mot)
    if ind < 0:
        return False
    motsM = mot.split()
    motsE = expr.split()
    for m in motsM:
        if not (m in motsE):
            return False
    return True
#present dans le code initial
def isHeadline(line):
    hl = ['id', 'series', 'title', 'creator', 'source', 'created', 'pages', 'subject', 'illustration', 'In']
    for mot in hl:
        if line.startswith(mot):
            return True
    return False

#present dans le code initial
def isPrefixe(mot):
    pref = ['M.', 'Mme', 'Mlle', 'Madame', 'Mademoiselle', 'Monsieur', 'Saint']
    if mot in pref:
        return True
        #    if len(mot)>1 and mot[0].isupper() and mot[1] in {'.'}:
        # return True
    return False

#present dans le code initial
def exclus(mot, liste):
    # commun=['Mais','Le', 'La', 'Les', "L'",'Par', 'Quand', 'Que', 'Voir', 'Voici', 'Un', 'Une', 'The', 'Sous','Si','Pour','Et','En','Enfin', 'Entre', 'Dans', "D'apr"+u"\u00e8"+"s", 'Comme', 'Chez', 'Ces', 'Cet', 'Cette', 'Ce', 'Car', 'Apr'+u"\u00e8"+'s', 'Ainsi','Alors','Au']

    return mot in liste

#present dans le code initial
def startsUpper(mot):
    if len(mot) > 0 and mot[0] in string.ascii_uppercase:
        return True
    return False

#present dans le code initial
def isInitiales(mot):
    if len(mot) > 1 and mot[0].isupper() and mot[1] in {'.'} and len(mot) < 3:
        return True
    return False

#present dans le code initial
def purgeNotes(mot):
    while len(mot) > 0 and mot[-1].isdigit():
        mot = mot[:-1]
    return mot

#present dans le code initial
def isParticule(mot):
    particules = ['de', 'du', "d'", "de" + '\u2027' + "la", "de" + '\u2027' + "La", "de" + '\u2027' + "l'",
                  "de" + '\u2027' + "L'"]
    return mot in particules

#ajoute un mot dans le dico
def addDico(dico, mot,pos):
    if mot in dico:
        dico[mot].append(pos)
    else:
        dico[mot] = [pos]


#present dans le fichier initial(pas sur de à quoi ca sert)
def traiterCreator(line):
    critique = line.split(':')[1].strip()
    print(critique)
    if len(critique) > 0:
        k = critique.rfind('(')
        print(k)
        if (k > 0) and critique[k + 1].isdigit():
            nom = critique[:k]
            print(nom)
            k = nom.rfind('(')
            print(k)
        else:
            nom = critique
        if k > 0:
            particule = nom.strip()[k + 1:-1]
            nom = nom[:k]
            print('nom :', nom, 'part : ', particule)
            noms = nom.split(',')
            print(noms)
            if len(noms) > 1:
                recompose = noms[1].strip() + ' ' + particule.strip() + ' ' + noms[0].strip()
                print(recompose)
            else:
                recompose = nom.strip() + ' ' + particule.strip()
                print(recompose)

        else:
            noms = nom.split(',')
            print(noms)
            if len(noms) > 1:
                recompose = noms[1].strip() + ' ' + noms[0].strip()
            else:
                recompose = nom.strip()
                if nom.strip() == 'None' or nom.strip() == 'none':
                    recompose = ""
            print(recompose)
    else:
        recompose = ""
    return recompose


#creer le corpus de textes à pmartir des fichiers passé en arguments
def initCorpus(fileList,log):
    f=[]
    for file in fileList:
        if(".docx" not in file[-5:-1]):
            t=codecs.open(file, "r", "utf-8", "replace")
            f.append(t.read())
            t.close()
        else:
            f.append(pypandoc.convert_file(file,'plain'))
    logf= codecs.open(log, "w+", "utf-8", "replace")

    corpus=dict()
    for i in range(len(fileList)):
        corpus[fileList[i]]=f[i]
    for i in range(len(corpus)):
        corpus[fileList[i]] = corpus[fileList[i]].replace('\u2026', ' ')
        corpus[fileList[i]] = corpus[fileList[i]].replace('\u2019', "'")
        corpus[fileList[i]] = corpus[fileList[i]].replace("de la", "de" + '\u2027' + "la")
        corpus[fileList[i]] = corpus[fileList[i]].replace("de La", "de" + '\u2027' + "La")
        corpus[fileList[i]] = corpus[fileList[i]].replace("de l'", "de" + '\u2027' + "l'")
        corpus[fileList[i]] = corpus[fileList[i]].replace("de L'", "de" + '\u2027' + "L'")
        corpus[fileList[i]] = corpus[fileList[i]].replace("'", "' ")
        corpus[fileList[i]] = corpus[fileList[i]].replace("  ", " ")
    return corpus,logf
#recupere le contenu des dictionnaires(sous forme de fichier) pour les stocker dans un tableau
def initDicos(dicoNames,dicoFiles,communsFile,noiseFile):
    if(not len(dicoNames)==len(dicoFiles)):
        raise ConfigError("Different number of files and names for dictionnaries")
    dicos={}
    occurences=[]
    for i in range(len(dicoNames)):
        dicos[dicoNames[i]],occurences= loadRef(dicoFiles[i],occurences)

    communs,occurences = loadMiscRef(communsFile,occurences)

    noise =loadMiscRef(noiseFile,occurences)
    return dicos,communs,noise,occurences
#fonction qui detecte les mots qui pourrait etre des noms :
#code présent dans le fichier initial arranger pour les modifications
def identify(corpus,exc,logf,occurences):
    np=dict()
    for (fileName,text) in corpus.items():
        lines = text.splitlines()
        i = 0
        for i in range(len(lines)):#line in lines:

            mots = lines[i].split()
            if len(mots) > 0:
                motprec = mots[0]
            pref = ""
            prec = ""
            for j in range(1,len(mots)):#mot in mots[1:]:
                if(str((fileName,i,j))in occurences):
                    continue
                mot0=mots[j]
                mot = purgeNotes(mots[j])

                if isInitiales(mot):
                    if len(pref) > 0:
                        pref = pref + " " + mot
                    else:
                        pref = mot
                    if len(motprec) > 0 and motprec[-1] in {'.'}:
                        motprec = ""
                elif isParticule(mot) and len(pref) > 0:
                    pref = pref + " " + mot
                    if len(motprec) > 0 and motprec[-1] in {'.'}:
                        motprec = ""
                elif isParticule(mot) and startsUpper(motprec) and not (motprec[-1] in {',', ')'}):
                    pref = motprec + " " + mot
                    motprec = ""
                elif len(pref) == 0 and isPrefixe(mot):
                    pref = mot
                    if len(motprec) > 0 and motprec[-1] in {'.'}:
                        motprec = ""
                elif not (len(motprec) > 0 and motprec[-1] in {'.'}):
                    if startsUpper(mot):
                        if len(pref) > 0:
                            mot = pref + ' ' + mot.strip()
                            pref = ""
                        else:
                            mot = mot.strip()
                        mot2 = mot
                        while (mot2[-1] in string.punctuation) or (mot2[-1] in {')'}):
                            mot2 = mot2[:-1]
                        if not (exclus(mot2, exc)):
                            #print(">>", mot2)
                            logf.write("\t\t>>" + mot2 + "\t[" + motprec + ']\n')
                            addDico(np, mot2,(fileName,i,j))

                            #np.append((mot2,(lines.index(line),mots.index(mot0))))
                            if startsUpper(motprec) and not (
                                    isPrefixe(motprec) or motprec[-1] in {',', ')'} or exclus(motprec, exc)):
                                mot3 = motprec + " " + mot2
                                #print(">>>", mot3)
                                logf.write("\t\t   >>>" + mot3 + '\n')
                                addDico(np, mot3,(fileName,i,j))
                                #np.append((mot3,(lines.index(line),mots.index(mot0))))
                                mot = motprec + " " + mot
                    else:
                        pref = ""
                    motprec = mot
                else:
                    motprec = mot

            i = i + 1
    return np


#creer un fichier à partir de la liste de mots générée
def generateToSort(np,fileName):
    f = codecs.open(fileName, "w+", "utf-8", "replace")
    for mot in np.keys():
        pos=np[mot]
        # print mot, ":", np[mot]
        f.write(mot + "@" )
        for p in pos:
            f.write(";"+str(p))
        f.write('\n')
    f.close()


#main de test
if __name__=="__main__":
    dicoFiles=["testLieux.txt","testAuthors.txt","testOeuvres.txt","testPers.txt","testInst.txt","testCrit.txt"]
    dicoNames=["LIEUX","AUTHORS","OEUVRES","PERSONNAGES","INSTITUTIONS","CRITIQUES"]
    communsFile="testCommun.txt"
    noiseFile="testNoise.txt"
    corpus,logf=initCorpus(["test1.txt","articles_presse_yourcenar.txt"],"out.log")
    dicos,communs,noise=initDicos(dicoNames,dicoFiles,communsFile,noiseFile) #les variables sont inutiles pour l'instant vu qu'on ne teste plus rien sur la presence des mots dans un dico.
    np=identify(corpus,communs,logf)
    generateToSort(np,"toSort2.txt")
