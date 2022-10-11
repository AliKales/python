import os
import sys
import subprocess


print("----------------------------------")
print("This script is helping you to add new strings to all .arb files!")
print("----------------------------------")

def addNewString():
    pathToARBs=os.getcwd() + "\lib\l10n"

    listDir=os.listdir(pathToARBs)

    key=str(input("Key for string:\n"))
    dynamicValues=[]

    whileAddDynamicValues=True

    while(whileAddDynamicValues):
        newValue=str(input("New Dynamic Value (leave empty if you are done):\n"))

        if (newValue.strip()==""):
            whileAddDynamicValues=False
        else:
            dynamicValues.append(newValue)

    valuesForARBS=[]

    def checkAllDynamicValues(value):
        if (dynamicValues.__len__()==0):
            return False
        returnValue = True
        for x in dynamicValues:
            if ("{%s}" % x in value):
                returnValue=False
            else:
                return True
        return returnValue

    for x in listDir:
        end=True
        newString=""
        while(end):
            print("String must contain all dynamic values;")
            print(dynamicValues)
            newString=str(input("String for {} in {}:\n".format(key,x)))
            end = checkAllDynamicValues(newString)
        valuesForARBS.append(newString)
        print("Added\n")

    def checkIfKeyExists(content):
        for x in content:
            if '"{}":'.format(key) in str(x):
                return True

    for x in range(listDir.__len__()):
        pathToOpen=pathToARBs+"\{}".format(listDir[x])
        with open(pathToOpen,"r", encoding="utf8") as file:
            content = file.readlines()

            isContainsKey = checkIfKeyExists(content)

            while(isContainsKey):
                key=str(input("Key ({}) does already exist. Please change it with new key:\n".format(key)))
                isContainsKey = checkIfKeyExists(content)



            content.insert(1,'    "{}": "{}",\n'.format(key,valuesForARBS[x]))

            file.close()
        
        with open(pathToOpen,"w", encoding="utf8") as file:
            file.writelines(content)

            file.close()

isContinue = True

while(isContinue):
    r = str(input("Do you want to add a new String? y/n: "))
    if r == "y":
        addNewString()
    elif r == "n":
        isContinue=False
    else:
        isContinue=False

        
pathToYaml= os.getcwd() + "l10n.yaml"

if os.path.exists(pathToYaml):
    os.remove(pathToYaml)

cmd1="flutter gen-l10n"

error=""

try:
    process = subprocess.Popen(cmd1, shell=True, stdout=subprocess.PIPE)
    process.wait()
    if not process.returncode==0:    
        out, err = process.communicate()
        error = out.decode("utf-8")
        print(error)
        sys.exit()

except:
    print(error)
    sys.exit()

print("DONE!")
