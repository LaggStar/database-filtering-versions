jobTitle = ["IT","Acounting","Finace","Consulting","Business","Construction","Government","Education","Game Development","Arts","Media","Film","Banking","Engineering","Energy","Water","Charity","Law","Enviroment","Agriculture","Healthcare","Lesiure","Marketing","Real Estate","Retail","Science","Pharmaceuticals","Transport"]
def createNewDatabase():
    global jobTitle
    import random
    file = open("database.csv","r+")
    file.seek(0)
    file.truncate()
    jobTitle = ["IT","Acounting","Finace","Consulting","Business","Construction","Government","Education","Game Development","Arts","Media","Film","Banking","Engineering","Energy","Water","Charity","Law","Enviroment","Agriculture","Healthcare","Lesiure","Marketing","Real Estate","Retail","Science","Pharmaceuticals","Transport"]
    for i in range(1,801):
        rndElement = jobTitle[random.randint(0,len(jobTitle)-1)]
        jobCode = ""
        jobCodeShortened = ""
        amount = "$" + str(random.randint(1000,10000000))
        if len(rndElement) < 3:
            jobCodeShortened = rndElement[0:2].upper()+"_"
        else:
            jobCodeShortened = rndElement[0:3].upper()
        if len(str(i)) == 1:
            jobCode = str(jobCodeShortened) + "00" + str(i)
        elif len(str(i)) == 2:
            jobCode = str(jobCodeShortened) + "0" + str(i)
        else:
            jobCode = str(jobCodeShortened) + str(i)
        file.write(str(rndElement)+","+str(amount)+","+str(jobCode)+"\n")
    file.close()
createNewDatabase()
