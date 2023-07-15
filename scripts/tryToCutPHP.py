import splitPHPDueToTokens
import scriptOldButStillWork
import os

f = open('phpCut.txt', 'w', encoding='utf-8', errors='replace')
f.close()
os.remove('phpCut.txt')
f = open('phpCut.txt', 'w', encoding='utf-8', errors='replace')

data = scriptOldButStillWork.split_text('php.txt')
for code in data:
    segments = splitPHPDueToTokens.split_text(code)
    for segment in segments:
        f.writelines(segment)
        f.write("\n")


f.close()