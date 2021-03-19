# coding: utf8
import codecs
import functools
import string


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


def cmp(a, b):
    return (a > b) - (a < b)


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


def extractRef(dico, ref):
    res = dict()
    for lab in ref:
        res[lab] = 0
        for mot in ref[lab]:
            if (mot in dico):
                res[lab] = res[lab] + dico[mot]
    return res


def loadRef(nomFic):
    f = codecs.open(nomFic, "r", "utf-8", "replace")
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


def saveRef(d, nomFic):
    f = codecs.open(nomFic, "w", "utf8", "replace")
    for (lab, liste) in sorted(d.items()):
        line = lab
        for mot in liste[1:]:
            line = line + "|" + mot
        f.write(line + "\n")
        print(line)


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


def isHeadline(line):
    hl = ['id', 'series', 'title', 'creator', 'source', 'created', 'pages', 'subject', 'illustration', 'In']
    for mot in hl:
        if line.startswith(mot):
            return True
    return False


def isPrefixe(mot):
    pref = ['M.', 'Mme', 'Mlle', 'Madame', 'Mademoiselle', 'Monsieur', 'Saint']
    if mot in pref:
        return True
        #    if len(mot)>1 and mot[0].isupper() and mot[1] in {'.'}:
        # return True
    return False


def exclus(mot, liste):
    # commun=['Mais','Le', 'La', 'Les', "L'",'Par', 'Quand', 'Que', 'Voir', 'Voici', 'Un', 'Une', 'The', 'Sous','Si','Pour','Et','En','Enfin', 'Entre', 'Dans', "D'apr"+u"\u00e8"+"s", 'Comme', 'Chez', 'Ces', 'Cet', 'Cette', 'Ce', 'Car', 'Apr'+u"\u00e8"+'s', 'Ainsi','Alors','Au']

    return mot in liste


def startsUpper(mot):
    if len(mot) > 0 and mot[0] in string.ascii_uppercase:
        return True
    return False


def isInitiales(mot):
    if len(mot) > 1 and mot[0].isupper() and mot[1] in {'.'} and len(mot) < 3:
        return True
    return False


def purgeNotes(mot):
    while len(mot) > 0 and mot[-1].isdigit():
        mot = mot[:-1]
    return mot


def isParticule(mot):
    particules = ['de', 'du', "d'", "de" + '\u2027' + "la", "de" + '\u2027' + "La", "de" + '\u2027' + "l'",
                  "de" + '\u2027' + "L'"]
    return mot in particules


def addDico(dico, mot):
    if mot in dico:
        dico[mot] = dico[mot] + 1
    else:
        dico[mot] = 1



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



def initCorpus(fileList,log):
    f=[]
    for file in fileList:
        f.append(codecs.open(file, "r", "utf-8", "replace"))
    logf= codecs.open(log, "w+", "utf-8", "replace")
    corpus=""
    for file in f:
        corpus+="\n"+file.read()
        file.close()
    corpus = corpus.replace('\u2026', ' ')
    corpus = corpus.replace('\u2019', "'")
    corpus = corpus.replace("de la", "de" + '\u2027' + "la")
    corpus = corpus.replace("de La", "de" + '\u2027' + "La")
    corpus = corpus.replace("de l'", "de" + '\u2027' + "l'")
    corpus = corpus.replace("de L'", "de" + '\u2027' + "L'")
    corpus = corpus.replace("'", "' ")
    corpus = corpus.replace("  ", " ")
    return corpus,logf

def initDicos(dicoNames,dicoFiles,communsFile,noiseFile):
    if(not len(dicoNames)==len(dicoFiles)):
        raise ConfigError("Different number of files and names for dictionnaries")
    dicos={}
    for i in range(len(dicoNames)):
        dicos[dicoNames[i]]= loadRef(dicoFiles[i])
    f = codecs.open(communsFile, "r", "utf-8", "replace")
    t = f.read()
    communs = t.splitlines()
    f.close()
    f = codecs.open(noiseFile, "r", "utf-8", "replace")
    t = f.read()
    noise = t.splitlines()
    f.close()
    return dicos,communs,noise

def identify(corpus,exc,logf):
    lines = corpus.split('\r')
    i = 0
    np = []
    # print "Line 1 :", lines[0]
    for line in lines:
        # print("Line : ", line, ">>", isHeadline(line))
        # if not (isHeadline(line)):
        #     f2.write("\n")
        # f2.write("Line : " + line + "\n")
        # if isHeadline(line):
        #     if line.startswith("creator"):
        #         recompose = traiterCreator(line)
        #         if len(recompose) > 0:
        #             if not (recompose in crit):
        #                 crit[recompose] = [recompose]
        #             alias = line.split(':')[1].strip()
        #             if not (alias in crit[recompose]):
        #                 crit[recompose].append(alias)
        # else:
        mots = line.split()
        # print "Mots : ", mots
        if len(mots) > 0:
            motprec = mots[0]
        pref = ""
        prec = ""
        for mot in mots[1:]:
            mot0=mot
            mot = purgeNotes(mot)

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
                        print(">>", mot2)
                        logf.write("\t\t>>" + mot2 + "\t[" + motprec + ']\n')
                        # addDico(np, mot2)

                        np.append((mot2,(lines.index(line),mots.index(mot0))))
                        if startsUpper(motprec) and not (
                                isPrefixe(motprec) or motprec[-1] in {',', ')'} or exclus(motprec, exc)):
                            mot3 = motprec + " " + mot2
                            print(">>>", mot3)
                            logf.write("\t\t   >>>" + mot3 + '\n')
                            # addDico(np, mot3)
                            np.append((mot3,(lines.index(line),mots.index(mot0))))
                            mot = motprec + " " + mot
                else:
                    pref = ""
                motprec = mot
            else:
                motprec = mot

        i = i + 1
    return np

def testDicos(dicos,dicoNames,dicoFiles,np):
    before = len(np)
    dDicos={}
    for i in range(len(dicoNames)):
        dicos[dicoNames[i]]= loadRef(dicoFiles[i])
        dDicos[dicoNames[i]]=extractFilterRef(np,dicos[dicoNames[i]])

    # lieux = loadRef("testLieux.txt")
    # dlieux = extractFilterRef(np, lieux)
    # # pers=loadRef("refPerson.txt")
    # pers = loadRef("testPers.txt")
    # dpers = extractFilterRef(np, pers)
    # # authors=loadRef("refAuthor.txt")
    # authors = loadRef("testAuthors.txt")
    # dauthors = extractFilterRef(np, authors)
    # # oeuvres=loadRef("refOeuvre.txt")
    # oeuvres = loadRef("testOeuvres.txt")
    # doeuvres = extractFilterRef(np, oeuvres)
    # # inst=loadRef("refInst.txt")
    # inst = loadRef("testInst.txt")
    # dinst = extractFilterRef(np, inst)
    # crit = loadRef("testCrit.txt")
    # dcrit = extractFilterRef(np, crit)
    # noise = loadRef("testNoise.txt")
    # dnoise = extractFilterRef(np, noise)

def generateToSort(np,fileName):
    f = codecs.open(fileName, "w+", "utf-8", "replace")
    for mot in sorted(np, key=functools.cmp_to_key(lambda x, y: cmp(len(x[0]), len(y[0])))):
        # print mot, ":", np[mot]
        f.write(mot[0] + "@" + str(mot[1]) + "\n")
    f.close()



if __name__=="__main__":
    dicoFiles=["testLieux.txt","testAuthors.txt","testOeuvres.txt","testPers.txt","testInst.txt","testCrit.txt"]
    dicoNames=["LIEUX","AUTHORS","OEUVRES","PERSONNAGES","INSTITUTIONS","CRITIQUES"]
    communsFile="testCommun.txt"
    noiseFile="testNoise.txt"
    corpus,logf=initCorpus(["test1.txt","articles_presse_yourcenar.txt"],"out.log")
    dicos,communs,noise=initDicos(dicoNames,dicoFiles,communsFile,noiseFile) #les variables sont inutiles pour l'instant vu qu'on ne teste plus rien sur la presence des mots dans un dico.
    np=identify(corpus,communs,logf)
    generateToSort(np,"toSort2.txt")

# f1 = codecs.open("articles_presse_yourcenar.txt", "r", "utf-8", "replace")
# f2 = codecs.open("out.log", "w", "utf-8", "replace")
# text = f1.read()
#
# text = text.replace('\u2026', ' ')
# text = text.replace('\u2019', "'")
# text = text.replace("de la", "de" + '\u2027' + "la")
# text = text.replace("de La", "de" + '\u2027' + "La")
# text = text.replace("de l'", "de" + '\u2027' + "l'")
# text = text.replace("de L'", "de" + '\u2027' + "L'")
# text = text.replace("'", "' ")
# text = text.replace("  ", " ")
# text=text.decode('unicode_escape','replace').encode('ascii','replace')
# text=text.replace(u'\xc3\xa9','e')
# text=text.replace("\xc2\xa0"," ")
# f3 = codecs.open("testCommun.txt", "r", "utf-8", "replace")
# t = f3.read()
# commun = t.splitlines()
# f3.close()
# exc = commun

# f3=codecs.open("dicoLieux.txt","r","utf-8","replace")
# t = f3.read()
# lieux=t.splitlines()
# f3.close()
# crit = loadRef("testCrit.txt")


    # if i>20 :
# break

# f1.close()

# saveRef(crit, "testCrit.txt")
#
# before = len(np)
# # lieux=loadRef("refLieux.txt")
# lieux = loadRef("testLieux.txt")
# dlieux = extractFilterRef(np, lieux)
# # pers=loadRef("refPerson.txt")
# pers = loadRef("testPers.txt")
# dpers = extractFilterRef(np, pers)
# # authors=loadRef("refAuthor.txt")
# authors = loadRef("testAuthors.txt")
# dauthors = extractFilterRef(np, authors)
# # oeuvres=loadRef("refOeuvre.txt")
# oeuvres = loadRef("testOeuvres.txt")
# doeuvres = extractFilterRef(np, oeuvres)
# # inst=loadRef("refInst.txt")
# inst = loadRef("testInst.txt")
# dinst = extractFilterRef(np, inst)
# crit = loadRef("testCrit.txt")
# dcrit = extractFilterRef(np, crit)
# noise = loadRef("testNoise.txt")
# dnoise = extractFilterRef(np, noise)

# print("Resultats : ")
# f2.write("\n\n Resultats : \n")
# for mot in sorted(np):
#     print(mot, ":", np[mot])
#     f2.write(mot + " : " + str(np[mot]) + "\n")
# f2.close()

# print "RESTE"
# for (mot,f) in sorted(np.items(),lambda a,b:cmp(a[1],b[1])):
#   print mot, ":", f

# print("\nLIEUX")
# for (mot, f) in sorted(list(dlieux.items()), key=functools.cmp_to_key(lambda x, y: cmp(len(y), len(x)))):
#     print(mot, ":", f)
# print("\nAUTHORS")
# for (mot, f) in sorted(list(dauthors.items()), key=functools.cmp_to_key(lambda x, y: cmp(len(y), len(x)))):
#     print(mot, ":", f)
# print("\nCRITIQUES")
# for (mot, f) in sorted(list(dcrit.items()), key=functools.cmp_to_key(lambda x, y: cmp(len(y), len(x)))):
#     print(mot, ":", f)
# print("\nOEUVRES")
# for (mot, f) in sorted(list(doeuvres.items()), key=functools.cmp_to_key(lambda x, y: cmp(len(y), len(x)))):
#     print(mot, ":", f)
# print("\nPERSONNAGES")
# for (mot, f) in sorted(list(dpers.items()), key=functools.cmp_to_key(lambda x, y: cmp(len(y), len(x)))):
#     print(mot, ":", f)
# print("\nINSTITUTIONS")
# for (mot, f) in sorted(list(dinst.items()), key=functools.cmp_to_key(lambda x, y: cmp(len(y), len(x)))):
#     print(mot, ":", f)

# f2 = codecs.open("toSort.txt", "w", "utf-8", "replace")
# for mot in sorted(np):
#     # print mot, ":", np[mot]
#     f2.write(mot + " : " + str(np[mot]) + "\n")
# f2.close()

# print("Nb References : ", len(np), "avant posfiltering : ", before, "lieux : ", len(dlieux), "auteurs : ",
#       len(dauthors))
