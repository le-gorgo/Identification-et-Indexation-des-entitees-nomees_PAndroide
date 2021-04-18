import filter3 as filter
import Identification as id
import configparser
import os
# ce fichier contient le programme principal qui le processus d'identification puis de filtrage.
def readConfig(fileName):
    config=configparser.ConfigParser()
    config.read("config.txt")
    f=config["Corpus"]["fichiers"].split(',')
    corpus=[]
    for name in f:
        if(os.path.isdir(name)):
            for(repertoire,sousRep,fichiers) in os.walk(name):
                for fic in fichiers:
                    corpus.append(os.path.join(repertoire,fic))
        else:
            corpus.append(name)
    f=config["Dictionnaires"]
    dicoFiles=[]
    dicoNames=[]
    for(nom,fichier) in f.items():
        dicoFiles.append(fichier)
        dicoNames.append(nom)
    f=config["Autre"]
    communsFile=f["Communs"]
    noiseFile=f["Bruits"]

    return corpus,dicoFiles,dicoNames,communsFile,noiseFile

if __name__=="__main__":

    #pour l'intant les fichiers sont mis directement dans le code, il faudra faire un fonction qui lit un fichier config
    corpusFiles,dicoFiles,dicoNames,communsFile,noiseFile=readConfig("config.txt")

    corpus,logf=id.initCorpus(corpusFiles,"out.log")#creation d'une variable corpus qui contient tous les textes des fichiers mis en parametre
    dicos,communs,noise,occurences=id.initDicos(dicoNames,dicoFiles,communsFile,noiseFile) #les variables sont inutiles pour l'instant vu qu'on ne teste plus rien sur la presence des mots dans un dico.
    np=id.identify(corpus,communs,logf,occurences)#c'est la fonction qui reconnais les mots qui peuvent etre des nom propres dans le corpus
     #fonction qui testera les dictionnaires pour la presence (avec la classification par exemple)
    id.generateToSort(np,"toSort.txt")# creer le fichier toSort qui va servir au filtrage
    toSort,mots,dicos,communs,noise,max_id=filter.initialisation(dicoFiles,dicoNames,communsFile,noiseFile,"toSort.txt")#creer les variables necessaires au filtrage
    filter.classement(toSort,dicos,communs,noise,corpus,max_id)#fonction principale du filtrage qui permet de choisir la classe et le label d'un mot
    filter.sauvegarde(dicos,communs,noise)#met à jours les dictionnaires à la fin du filtrage
