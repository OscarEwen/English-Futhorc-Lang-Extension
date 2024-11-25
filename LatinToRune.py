from pathlib import Path

import json
import pandas as pd
import regex

assetsPath = Path("./assets")
dataPath = Path("./data")

runePath = dataPath / "runelex.tsv"

# Load rune dictionary in memory using a panda frame
runeTable = pd.read_table(
    runePath,
    index_col=0,
    header=None,
    dtype=str
    )

runeTable = runeTable.dropna(axis=1)
runeTable = runeTable[~runeTable.index.duplicated(keep='first')]
runeSeries = runeTable.drop([2,3,4,5], axis=1)[1]
runeSeries = runeSeries.rename("Latin-Futhorc")
runeSeries = runeSeries.rename_axis("Latin")

# runeSeries = runeSeries.drop_duplicates()
# print(type(runeSeries.get(str.lower("after"))))

# get language files
languages =  list(assetsPath.glob("**/**/lang/*.json"))

# iterate through each file, performing data manipulation operations on each
matchesList = []

for langaugeFilePath in languages:
    with open(langaugeFilePath.as_posix(), mode='r+') as langaugeFile:
        languageJson = json.load(langaugeFile)

        # for every key value pair
        for key, value in languageJson.items():
            replaceValue = value
            
            pairWords = regex.findall(
                r'((?<!\$|\%|\'|@|/)\m[A-Za-z]+\M(?!\'))|(\m[A-Za-z]*\'[A-Za-z]*\M)', 
                value
                )
            words = set()
            for word1, word2 in pairWords:
                words.add(word1)
                words.add(word2)

            matchesList.append(len(words))

            # check each word
            for word in words:
                replaceWord = runeSeries.get(str.lower(word))

                if replaceWord is None:
                    replaceWord = runeSeries.get(str.upper(word))
                
                if replaceWord is None:
                    replaceWord = runeSeries.get(str.capitalize(word))
                
                # and replace if runic alternative is found
                if replaceWord is not None:
                    matchRegex = r'\b' + regex.escape(word) + r'\b'
                    replaceValue = regex.sub(
                        matchRegex, 
                        replaceWord, 
                        replaceValue)



                    # splitValue[wordNum] = replaceWord
            languageJson[key] = replaceValue  # " ".join(splitValue)
        
        # Write back to json file
        separatedPath = langaugeFilePath.as_posix().split("/")
        # separatedPath
        separatedPath[-1] = "en_Runr.json"
        newPath = "/".join(separatedPath)
        with open(newPath, "w", encoding='utf8') as output:
            json.dump(languageJson, output, ensure_ascii=False, indent=4)

print(sum(matchesList), "matches")

# for key, value in languageJson.items():
#    print(key, value)
# print(languageJson)