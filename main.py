import filter3 as filter
import Identification as id
# ce fichier contient le programme principal qui le processus d'identification puis de filtrage.
if __name__=="__main__":

    #pour l'intant les fichiers sont mis directement dans le code, il faudra faire un fonction qui lit un fichier config
    dicoFiles=["dicoTest.txt","testLieux.txt","testAuthors.txt","testOeuvres.txt","testPers.txt","testInst.txt","testCrit.txt"]
    dicoNames=["dicoTest","LIEUX","AUTHORS","OEUVRES","PERSONNAGES","INSTITUTIONS","CRITIQUES"]
    communsFile="testCommun.txt"
    noiseFile="testNoise.txt"

    corpus,logf=id.initCorpus(["articles_presse_yourcenar.txt"],"out.log")#creation d'une variable corpus qui contient tous les textes des fichiers mis en parametre
    dicos,communs,noise=id.initDicos(dicoNames,dicoFiles,communsFile,noiseFile) #les variables sont inutiles pour l'instant vu qu'on ne teste plus rien sur la presence des mots dans un dico.
    np=id.identify(corpus,communs,logf)#c'est la fonction qui reconnais les mots qui peuvent etre des nom propres dans le corpus
    #id.testDicos(dicos,dicoNames,dicoFiles,np) #fonction qui testera les dictionnaires pour la presence (avec la classification par exemple)
    id.generateToSort(np,"toSort.txt")# creer le fichier toSort qui va servir au filtrage
    toSort,mots,dicos,communs,noise=filter.initialisation(dicoFiles,dicoNames,communsFile,noiseFile,"toSort.txt")#creer les variables necessaires au filtrage
    filter.classement(toSort,dicos,communs,noise,corpus)#fonction principale du filtrage qui permet de choisir la classe et le label d'un mot
    filter.sauvegarde(dicos,communs,noise)#met à jours les dictionnaires à la fin du filtrage
