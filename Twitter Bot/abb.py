import enchant

wordDict = enchant.Dict("en_US")

inputWords = ['wtrbtl','bwlingbl','bsktball']
for word in inputWords:
    print wordDict.suggest(word)