from pathlib import Path

import json
import pandas as pd
import re

assetsPath = Path("./assets")
dataPath = Path("./data")

runePath = dataPath / "runelex.tsv"

# Load rune dictionary in memory using a panda frame
runeTableHeaderNames = ["Latin", "Futhorc", "Shavian", "IPA", "POS"]

runeTable = pd.read_table(
    runePath,
    index_col=0,
    header=None, 
    thousands=",",
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
for langaugeFilePath in languages:
    with open(langaugeFilePath.as_posix(), mode='r+') as langaugeFile:
        languageJson = json.load(langaugeFile)

        # for every key value pair
        for key, value in languageJson.items():
            replaceValue = value
            words = set(re.findall(r'(?<!\$)\b\w+\b', value))

            # check each word
            for word in words:
                print(word)
                replaceWord = runeSeries.get(str.lower(word))
                
                # and replace if runic alternative is found
                if replaceWord is not None:
                    matchRegex = r'\b' + re.escape(word) + r'\b'
                    replaceValue = re.sub(matchRegex, replaceWord, replaceValue)



                    # splitValue[wordNum] = replaceWord
            languageJson[key] = replaceValue  # " ".join(splitValue)
        
        # Write back to json file
        separatedPath = langaugeFilePath.as_posix().split("/")
        # separatedPath
        separatedPath[-1] = "en_Runr.json"
        newPath = "/".join(separatedPath)
        print(newPath)
        with open(newPath, "w", encoding='utf8') as output:
            json.dump(languageJson, output, ensure_ascii=False, indent=4)


# for key, value in languageJson.items():
#    print(key, value)
# print(languageJson)