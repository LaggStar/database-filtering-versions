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



#imports all required libraries
import create_database as database

#database.createNewDatabase()

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
importDatabase()

byJobTitle = False
byAmount = False
byJobCode = False

filteredJobTitle = []
filteredAmount = []
filteredJobCode = []
    
searchingArray = []
def searchDatabase(searchTerm):
    global jobTitle, amount, jobCode, filteredJobTitle, filteredAmount, filteredJobCode, byJobTitle, byAmount, byJobCode
    if searchTerm != "":
        filteredJobTitle = []
        filteredAmount = []
        filteredJobCode = []
        for i in range(0,len(jobTitle)):
            if jobTitle[i].find(searchTerm.upper()) != -1 or amount[i].find(searchTerm) != -1 or jobCode[i].find(searchTerm.upper()) != -1:
                filteredJobTitle.append(jobTitle[i])
                filteredAmount.append(amount[i])
                filteredJobCode.append(jobCode[i])
    
def filterDatabase(fId):
    global byJobTitle, byAmount, byJobCode
    filtervalues = open("data/filtervalues.txt","r+")
    filterAttributes = filtervalues.readlines()
    filterBy = ""
    for i in range(0,len(filterAttributes)):
        if i == int(fId):
            filterBy = filterAttributes[i].strip()
            filterBy = filterBy.split(",")
            output = []
            for j in filterBy:
                if j == "True":
                    j = True
                elif j == "False":
                    j = False
                output.append(j)
            print(output)
            byJobTitle = output[0]
            byAmount = output[1]
            byJobCode = output[2]
    filtervalues.close()


def sortDatabase():
    global filteredJobTitle, filteredAmount, filteredJobCode
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
    print(sortingArray)




        
