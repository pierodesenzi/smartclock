#original author: anirudhjoshi

#!/usr/bin/python
# HTML Character Convertor
# Replaces HTML entities in a given string - with their correct character.

allLines = open("spcharhtml", 'r').readlines()
dictionary = {}
for line in allLines:
	value, key = line.split(':')
	dictionary[key.rstrip()]=value.strip()

def stringToConvert(string):
	for k in dictionary.keys():
		if k in string:
			string = string.replace(k, dictionary[k])

	return string.replace("\\","")

