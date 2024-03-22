#By Brendon Amino
import argparse
import string
parser = argparse.ArgumentParser(description = 'Script that turns a graph into a boolean formula that can be read by a MiniSAT')
parser.add_argument('-n', '--namefile', help = 'File name in .txt format.', required=True, dest='file')
args = parser.parse_args()
alphabet = "abcdefghijklmnopqrstuvwxyz"

def turnFileIntoList(text):
	tempList = []
	temp = ""
	F = open(text, "r")
	count = 0
	for letter in F:
		tempList += letter
	F.close()
	finalList = []
	for letter in tempList:
		temp += letter
		#print(temp)
		if "\n" in temp:
			temp = temp[:len(temp)-1]
			finalList.append(temp)
			temp = ""
		if count == len(tempList)-1:
			finalList.append(temp)
		count += 1
	#print(finalList)	
	return finalList

def setNumList(myList):
	finalList = []
	count = 0
	for i in range(len(myList)):
		tempList = []
		count += 1
		tempList.append(count)
		count += 1
		tempList.append(count)
		count += 1
		tempList.append(count)
		finalList.append(tempList)
	#print(finalList)
	return finalList


def setInitialColors(myList):
	finalList = []
	count = 0
	for theList in myList:
		#print(theList)
		tempList = []
		tempList2 = []
		tempList2.append(theList[0] * -1)
		tempList2.append(theList[1] * -1)
		tempList.append(tempList2)
		tempList2 = []
		tempList2.append(theList[0] * -1)
		tempList2.append(theList[2] * -1)
		tempList.append(tempList2)
		tempList2 = []
		tempList2.append(theList[1] * -1)
		tempList2.append(theList[2] * -1)
		tempList.append(tempList2)
		finalList.append(tempList)
	#print(finalList)
	return finalList

def miniSAT(myList, numList):
	myDict = {}
	for i in range(len(myList)):
		myDict[alphabet[i]] = numList[i]
	#print(myDict)
	count = 0
	finalList = []
	for theString in myList:
		for char in theString:
			if char == ' ':
				continue
			else:
				#createColors(char, count, myDict)
				finalList.append(createColors(char, count, myDict))
		count+=1
	#print(finalList)
	return finalList
				
def removeDupes(myList):
	finalList = []
	tempList = []
	for lists in myList:
		for theList in lists:
			tempList += [theList]
	temp = []
	temp2 = []
	indexList = []
	for i in range(len(tempList)):
		#print(i)
		canContinue = False
		temp = tempList[i]
		temp2.append(tempList[i][1])
		temp2.append(tempList[i][0])
		#print(temp)
		for j in range(len(tempList)):
			if j == i:
				continue
			else:
				if tempList[j] == temp or tempList[j] == temp2:
					indexList.append(j)
		for num in indexList:
			if i == num:
				canContinue = True
				break
		if canContinue:
			print(indexList)
			continue
		else:
			finalList.append(tempList[i])
		temp2 = []
	print(finalList)
def createColors(compareChar, currentLine, currentDict):
	finalList = []
	originalLine = currentDict[alphabet[currentLine]]
	compareLine = currentDict[compareChar]
	tempList = []
	tempList.append(originalLine[0]*-1)
	tempList.append(compareLine[0]*-1)
	finalList.append(tempList)
	tempList = []
	tempList.append(originalLine[1]*-1)
	tempList.append(compareLine[1]*-1)
	finalList.append(tempList)
	tempList = []
	tempList.append(originalLine[2]*-1)
	tempList.append(compareLine[2]*-1)
	finalList.append(tempList)
	return finalList
	#print(finalList)
	#print(originalLine)
	#print(compareLine)

def turnFileIntoString(myList):
	string = ""
	finalCount = 0
	for theLists in myList:
		#print(theLists[0])
		numCount = 0
		for nums in theLists[0]:
			if numCount == len(theLists[0])-1:
				string += str(nums) + " 0\n"
			else:
				string += str(nums) + " "
			#print(nums)
			numCount += 1
		for lists in theLists[1]:
			size = 0
			for num in lists:
				if size == len(lists)-1:
					string += str(num) + " 0\n"
				else:
					string += str(num) + " "
				size += 1
		finalCount += 1
	#print(string)
	return string

def turnMiniSatIntoString(myList):
	string = ""
	for theLists in myList:
		#print(theLists)
		for numLists in theLists:
			count = 0
			for num in numLists:
				if count == len(numLists)-1:
					string += str(num) + " 0\n"
				else:
					string += str(num) + " "
				count+=1
	return string[:len(string)-1]

def writeFile(name, string):
	F = open(name, "w")
	F.write(string)

def setName(name):#Helper function to add out to a .txt filename.
	myString = name
	index = myString.find('.')
	tempString = myString[:index]
	tempString2 = myString[index:]
	newString = tempString + "_out" + tempString2
	myString = newString
	#print(myString)
	return myString

def main():
	if args.file:
		myList = turnFileIntoList(args.file)
		theList = []
		numList = setNumList(myList)
		colorsList = setInitialColors(numList)
		finalString = ""
		miniSatList = miniSAT(myList, numList)
		tempList = []
		for i in range(len(numList)):
			tempList.append(numList[i])
			for j in range(len(colorsList)):
				if i == j:
					tempList.append(colorsList[i])
			theList.append(tempList)
			tempList = []
		#print(theList)
		#theList.append(miniSatList)
		finalString = turnFileIntoString(theList)
		finalString += turnMiniSatIntoString(miniSatList)
		outName = ""
		outName = setName(args.file)
		writeFile(outName, finalString)
		#print(finalString)
		#removeDupes(miniSatList)

if __name__ == "__main__":
	main()
