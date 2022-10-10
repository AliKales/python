import os

howMany = int(input("How many folders do you want to create?\n"))
pathToFiles= input(r"Path:(\lib\ui):")

listFolderNames=[]
currentPath=os.getcwd()

scaffoldString="""import 'package:music_for_everyone/common_libs.dart';

class %s extends StatelessWidget {
  const %s({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold();
  }
}
"""



def createFolder(folderName):
    isFolderCreate = input("File should be created for '{}'?(y/n):\n".format(folderName))
    newPath = '{}{}\{}'.format(currentPath,pathToFiles,folderName) 
    viewPath=""
    if isFolderCreate =="y" or isFolderCreate=="Y":
        viewPath= '{}{}\{}\{}_view.dart'.format(currentPath,pathToFiles,folderName,folderName) 
    else:
        viewPath= '{}{}\{}_view.dart'.format(currentPath,pathToFiles,folderName) 
    
    if not os.path.exists(newPath):
        if isFolderCreate =="y" or isFolderCreate=="Y":
            os.makedirs(newPath)
        with open(viewPath, 'w') as f:
            folderNameSplit = folderName.split("_")
            newFolderName=""

            for x in folderNameSplit:
                newFolderName=newFolderName+x.title()

            newFolderName=newFolderName+"View"

            stringToWrite = scaffoldString % (newFolderName,newFolderName)

            f.write(stringToWrite)

    if not os.path.exists(viewPath):
        os.makedirs(viewPath)

for x in range(howMany):
    getInput=input("{}. Folder Name:\n".format(x+1))
    listFolderNames.append(getInput)

for x in listFolderNames:
    createFolder(x)





