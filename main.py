import filter3 as filter
import Identification as id

if __name__=="__main__":
    dicoFiles=["dicoTest.txt","testLieux.txt","testAuthors.txt","testOeuvres.txt","testPers.txt","testInst.txt","testCrit.txt"]#"testLieux.txt","testAuthors.txt","testOeuvres.txt","testPers.txt","testInst.txt","testCrit.txt"
    dicoNames=["dicoTest","LIEUX","AUTHORS","OEUVRES","PERSONNAGES","INSTITUTIONS","CRITIQUES"]#LIEUX","AUTHORS","OEUVRES","PERSONNAGES","INSTITUTIONS","CRITIQUES"
    communsFile="testCommun.txt"
    noiseFile="testNoise.txt"

    corpus,logf=id.initCorpus(["articles_presse_yourcenar.txt"],"out.log")#,"articles_presse_yourcenar.txt"
    dicos,communs,noise=id.initDicos(dicoNames,dicoFiles,communsFile,noiseFile) #les variables sont inutiles pour l'instant vu qu'on ne teste plus rien sur la presence des mots dans un dico.
    np=id.identify(corpus,communs,logf)
    #id.testDicos(dicos,dicoNames,dicoFiles,np)
    id.generateToSort(np,"toSort.txt")
    toSort,mots,dicos,communs,noise=filter.initialisation(dicoFiles,dicoNames,communsFile,noiseFile,"toSort2.txt")
    filter.classement(toSort,dicos,communs,noise,corpus)
    filter.sauvegarde(dicos,communs,noise)
