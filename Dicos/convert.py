import codecs
dicos=["dicoTest.txt","testLieux.txt","testAuthors.txt","testOeuvres.txt","testPers.txt","testInst.txt","testCrit.txt"]
misc=["testNoise.txt","testCommun.txt"]
id=0
for dico in dicos:

    t=codecs.open(dico, "r", "utf-8", "replace")
    lines=t.read().splitlines()
    t.close()
    f = codecs.open("converted_"+dico, "w", "utf-8", "replace")
    res=""
    for line in lines:
        f.write(str(id)+":"+line+":\n")
        id+=1

for dico in misc:

    t=codecs.open(dico, "r", "utf-8", "replace")
    lines=t.read().splitlines()
    t.close()
    f = codecs.open("converted_"+dico, "w", "utf-8", "replace")
    res=""
    for line in lines:
        f.write(line+":\n")
