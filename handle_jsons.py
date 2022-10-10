import os
import json
import sys
import subprocess

currentPath=os.getcwd()

isFirst=True

pathToFolder=input("Path to Models: \n")

pathToFolder = currentPath+pathToFolder

strPrefix = ""

def getType(value,data):
    if type(value) is str:
        return "String"
    if type(value) is bool:
        return "bool"
    if type(value) is list:
        return "List<{}{}>".format(getPrefixCapitalize(),data.title())
    if type(value) is dict:
        return "Map"
    if type(value) is int or float:
        return "int"
    return "None"

def getJson(path):
    with open(path, encoding="utf8") as f:
        data = json.load(f)
            
        f.close()

        return data

def toLowerCamelCase(value):
    items=value.split("_")
    newString = items[0]

    items.pop(0)

    for x in items:
        newString = newString + x.title()

    return newString
    

def getPrefix():
    if strPrefix == "":
        return ""
    else:
        return "{}_".format(strPrefix)

def getPrefixCapitalize():
    if strPrefix == "":
        return ""
    else:
        if not strPrefix.__contains__("_"):
            return strPrefix.title()
        newPrefix=""
        prefixes=strPrefix.split("_")
        for x in prefixes:
            newPrefix=newPrefix+x.title()
        return newPrefix


def generateFile(fileName,model):
    if type(model) is list:
        model=model[0]

    listOfSubModels=[]
    fileNameTitle="{}{}".format(getPrefixCapitalize(),fileName.title())
    with open(pathToFolder+"\{}{}.dart".format(getPrefix(),fileName),"w+" , encoding="utf8") as f:
        f.write(
'''import 'package:json_annotation/json_annotation.dart';

part '%s%s.g.dart';

@JsonSerializable()
class %s {
'''% (getPrefix(),fileName,fileNameTitle)     )

        for x in model:
            if getType(model[x],"") == "Map":
                f.write("  {}{}? {};\n".format(getPrefixCapitalize(),toLowerCamelCase(x).title(),toLowerCamelCase(x)))
                generateFile(x,model[x])
                listOfSubModels.append(x)
            else:
                if getType(model[x],"").__contains__("List") == True:
                    generateFile(x,model[x])
                    listOfSubModels.append(x)

                f.write("  {}? {};\n".format(getType(model[x],x),toLowerCamelCase(x)))


        f.write("\n  %s({\n" % fileNameTitle)

        for x in model:
            f.write("    this.{},\n".format(toLowerCamelCase(x)))
        
        f.write("  });\n")

        f.write(
''' 
  factory %s.fromJson(Map<String, dynamic> json) => _$%sFromJson(json);

  Map<String, dynamic> toJson() => _$%sToJson(this);  
}       
''' % (fileNameTitle,fileNameTitle,fileNameTitle))

        f.close()

        if listOfSubModels.__len__() >0:
            content = []

            with open(pathToFolder+"\{}{}.dart".format(getPrefix(),fileName),"r", encoding="utf8") as file:
                content = file.readlines()

                for x in listOfSubModels:
                    content.insert(1,"import '{}{}.dart';\n".format(getPrefix(),x))

                file.close()
            
            with open(pathToFolder+"\{}{}.dart".format(getPrefix(),fileName),"w", encoding="utf8") as file:
                file.writelines(content)

                file.close()

listOfJsonFiled=os.listdir(pathToFolder)


for x in listOfJsonFiled:
    isFirst=True

    if x.__contains__(".json"):
        strPrefix = str(input("Would you like to put a prefix before your model? exp: m_my_model.dart ({}): \n".format(x)))

        jsonData = getJson(pathToFolder+"\{}".format(x))

        datas=[]

        for y in jsonData:
            datas.append(y)

        if datas.__len__() == 1:
            generateFile(datas[0],jsonData[datas[0]])
        else:
            firstObject=input("What do you want to call your object?{}:\n".format(x))
            generateFile(firstObject,jsonData)

process=any
process2=any

cmd1="flutter packages pub run build_runner build"
cmd2="flutter packages pub run build_runner build --delete-conflicting-outputs"

isExceptCaught=False


try:
    process = subprocess.Popen(cmd1, shell=True, stdout=subprocess.PIPE)
    process.wait()
    if not process.returncode==0:    
        isExceptCaught=True

except:
    isExceptCaught=True

if isExceptCaught==True:
    try:
        process2 = subprocess.Popen(cmd2, shell=True, stdout=subprocess.PIPE)
        process2.wait()

        if not process2.returncode==0:
            out, err = process2.communicate()
            print(out.decode("utf-8"))
            sys.exit()
    except:
        out, err = process2.communicate()
        print(out.decode("utf-8"))
        sys.exit()


def changeText(fileName,textToReplace,text):
    with open("{}\{}".format(pathToFolder,fileName), "r", encoding="utf8") as f:
        old = f.read()
        old = old.replace(textToReplace,text)
        with open("{}\{}".format(pathToFolder,fileName), 'w', encoding="utf8") as ff:
            ff.write(old)
            ff.close()
        f.close()

listDir=os.listdir(pathToFolder)

listOfSerializables = [item for item in listDir if ".g." in item]

if not os.path.exists(pathToFolder+"\json_serializable"):
    os.makedirs(pathToFolder+"\json_serializable")


for x in listOfSerializables:
    changeText(x,"part of '","part of '../")
    changeText(x.replace(".g.","."),"part '","part 'json_serializable/")
    os.rename(pathToFolder+"\{}".format(x),pathToFolder+"\json_serializable\{}".format(x))
