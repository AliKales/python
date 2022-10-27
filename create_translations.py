import os


print("----------------------------------")
print("This script is going to create new translations")
print("----------------------------------")

currentPath=os.getcwd()

enPath = "{}\lib\l10n\{}".format(currentPath,"app_en.arb")
enContent = []

with open(enPath,"r", encoding="utf8") as file:
    enContent=file.readlines()
    file.close()

enContent.pop(0)
enContent.pop(enContent.__len__()-1)

for x in range(enContent.__len__()):
    v=enContent[x].split('":')[0]
    enContent[x] = v.lstrip('  "')


newLang = str(input("What language to add? (es): "))

newPath = "{}\lib\l10n\{}".format(currentPath,"app_{}.arb".format(newLang))

newContent=[]

with open(newPath,"r", encoding="utf8") as file:
    newContent=file.readlines()
    file.close()


for x in range(newContent.__len__()):
    newString = newContent[x]
    if newString.__contains__('"'):
        start = newString.find('"')
        end = newString.find('":')

        newContent[x] = newString[:5]+enContent[x-1]+newString[end:]

with open(newPath,"w", encoding="utf8") as file:
    file.writelines(newContent)
    file.close()