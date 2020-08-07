'''
SOFTWARE DEVELOPMENT PROJECT
Client Search & Filtering Utility - Database Functionality Module

Made by Gerard 12SDA
Started on 03/08/2020

Naming Convention - CamelCase

Module Description
This module contains the functions that search, sort and filter
the database. It also contains the function that imports the database
and appends the fields to there nessescary arrays.

This Uses
- create_database.py
'''

#------------------------------------------------------

#WINDOW CONFIGURATION + IMPORTS



##import create_database as database    Unindent these lines in order to create a new test database 
##database.createNewDatabase()

jobTitle = []
amount = []
jobCode = []

def importDatabase():
    global jobTitle, amount, jobCode
    loadDatabase = open("database.csv","r+")
    array = loadDatabase.readlines()
    jobTitle = []
    amount = []
    jobCode = []
    for i in array:
        temp = i.split(",")
        jobTitle.append(temp[0])
        amount.append(temp[1])
        jobCode.append(temp[2].strip())

filteredJobTitle = []
filteredAmount = []
filteredJobCode = []

filteredSearchJobTitle = []
filteredSearchAmount = []
filteredSearchJobCode = []
    
def searchDatabase(searchTerm):
    global filteredJobTitle, filteredAmount, filteredJobCode, filteredSearchJobTitle, filteredSearchAmount, filteredSearchJobCode
    filteredSearchJobTitle = []
    filteredSearchAmount = []
    filteredSearchJobCode = []
    if searchTerm != "":
        for i in range(0,len(filteredJobTitle)):
            if filteredJobTitle[i].upper().find(searchTerm.upper()) != -1 or filteredAmount[i].find(searchTerm) != -1 or filteredJobCode[i].find(searchTerm.upper()) != -1:
                filteredSearchJobTitle.append(filteredJobTitle[i])
                filteredSearchAmount.append(filteredAmount[i])
                filteredSearchJobCode.append(filteredJobCode[i])
    if filteredSearchAmount == []:
        filteredSearchAmount.append("Nothing Found")
    print(filteredSearchJobTitle, filteredSearchAmount, filteredSearchJobCode)

byJobTitle = []
byAmount = []
byJobCode = []

def filterDatabase(fId):
    global byJobTitle, byAmount, byJobCode, jobTitle, amount, jobCode, filteredJobTitle, filteredAmount, filteredJobCode
    filterbyvalues = open("data/customfilterAttributes.txt","r+")
    filterby = open("data/jobtitlesectors.txt","r+")
    filterAttributes = filterbyvalues.readlines()
    filterbyAttributes = filterby.readlines()
    byJobTitle = []
    byAmount = []
    byJobCode = []
    filteredJobTitle = []
    filteredAmount = []
    filteredJobCode = []
    temp = []
    temp2 = []
    temp3 = []
    num = 0
    content = ""
    
    for i in range(0,len(filterAttributes)):
        content = filterAttributes[i].split(",")
        if i == int(fId):
            byAmount.extend((int(content[2]),int(content[3])))  
            byJobCode.extend((int(content[4]),int(content[5])))
            byJobTitle = filterbyAttributes[i].split(",")
            for j in byJobTitle:
                temp.append(j.strip())
            byJobTitle = temp
    
    for i in range(0,len(jobTitle)):
        if byJobTitle == ['blank']:
            filteredJobTitle = jobTitle[:]
            filteredAmount = amount[:]
            filteredJobCode = jobCode[:]
        elif jobTitle[i] in byJobTitle:
            filteredJobTitle.append(jobTitle[i])
            filteredAmount.append(amount[i])
            filteredJobCode.append(jobCode[i])
    
    temp = []
    temp2 = []
    temp3 = []
    num = 0

    for number in range(0,len(filteredAmount)):
        filteredAmount[number] = filteredAmount[number][1:len(filteredAmount[number])]
    temp = []
    for number in filteredAmount:
        temp.append(int(number))
    filteredAmount = temp[:]
    temp = []
    for i in range(0,len(filteredAmount)):
        if byAmount != [-1,-1]:
            if int(filteredAmount[i]) in range(int(byAmount[0]),int(byAmount[1])+1):
                temp.append(filteredJobTitle[i])
                temp2.append(filteredAmount[i])
                temp3.append(filteredJobCode[i])
        else:
            temp.append(filteredJobTitle[i])
            temp2.append(filteredAmount[i])
            temp3.append(filteredJobCode[i])

    filteredJobTitle = temp[:]
    filteredAmount = temp2[:]
    filteredJobCode = temp3[:]

    
    temp = []
    for j in filteredAmount:
        temp.append("$"+str(j))

    filteredAmount = temp[:]

    temp = []
    temp2 = []
    temp3 = []

    filteringJobCode = filteredJobCode[:]
    for job in range(0,len(filteringJobCode)):
        filteringJobCode[job] = int(filteringJobCode[job][3:len(filteringJobCode[job])])


    for i in range(0,len(filteringJobCode)):
        if byJobCode != [-1,-1]:
            if filteringJobCode[i] in range(byJobCode[0],byJobCode[1]+1):
                    temp.append(filteredJobTitle[i])
                    temp2.append(filteredAmount[i])
                    temp3.append(filteredJobCode[i])
        else:
            temp.append(filteredJobTitle[i])
            temp2.append(filteredAmount[i])
            temp3.append(filteredJobCode[i])
    
    filteredJobTitle = temp[:]
    filteredAmount = temp2[:]
    filteredJobCode = temp3[:]
    
    print(filteredJobTitle, filteredAmount, filteredJobCode)
    
    filterbyvalues.close()
    filterby.close()



sortingArray = []
def sortDatabase():
    global filteredJobTitle, filteredAmount, filteredJobCode, sortingArray
    sortingArray = []
    for i in range(0,len(filteredJobTitle)):
        sortingArray.append([filteredJobTitle[i],filteredAmount[i],filteredJobCode[i]])
    sortingArray.sort(key=lambda x: x[0])
    filteredJobTitle = []
    filteredAmount = []
    filteredJobCode = []
    for i in range(0,len(sortingArray)):
        filteredJobTitle.append(sortingArray[i][0])
        filteredAmount.append(sortingArray[i][1])
        filteredJobCode.append(sortingArray[i][2])




        
