# lvs
#
# takes a lowercase string and returns the sum of its "letter values"
# e.g. a=1, z=26, "abc" = 6
# 
# then also some bonus problems

from string import ascii_lowercase as a_l
import time

# make a char-value dict to drop letter-value lookup time to O(1)
charDict = {}
for i in range(len(a_l)):
	charDict[a_l[i]] = i+1 # fuckn 0-indexing

def wordValueSum(word):
	sum = 0
	for letter in word:
		sum += charDict.get(letter,0)
	return sum


# bonus challenges

# this makes a list of all the words in the txt file
wordList = [] # move down to main()?
def populateWordList():
	f = open("enable1.txt")
	for line in f.readlines():
		wordList.append(line.strip())
	f.close()

# bonus challenge #1
# find the only word with a letter sum of 319
# but we're (obviously) going to generalize this
# returns a list of all words with a given value
# the solution to 319 (and to bonus challenge 1) is
# "reinstitutionalizations"
def searchByValue(value = 319):
	valueList = []
	for w in wordList:
		if wordValueSum(w) == value:
			valueList.append(w)
	return valueList

# bonus challenge #2
# how many words have an odd letter sum?
# should be easy
# 86339
def oddSums():
	count = 0
	for w in wordList:
		if wordValueSum(w)%2!=0:
			count += 1
	return count

# bonus challenge #3
# what is the most common letter sum?
# it's 93, with 1965 occurrences
def mostCommonSum():
	# make a dict of all value frequencies
	valueDict = {}
	for w in wordList:
		value = wordValueSum(w)
		valueDict[value] = valueDict.get(value,0)+1
	
	# now find the most frequent
	mostCommonSumTuple = (0,0) # (most common sum, instances)
	for elt in valueDict:
		if valueDict[elt] > mostCommonSumTuple[1]:
			mostCommonSumTuple = (elt, valueDict[elt])
	
	return mostCommonSumTuple # my variable names are impeccable shut up
	
# bonus challenge #4
# find the pair of words with the same value and an 11-letter gap in length
# jeez this wouldve been easier if you'd told me 11 was the max gap
# then i could've just generalized and optimized it
# instead of solving for precisely 11
# so like now i theoretically can't just track min and max length at each value,
# becuase what if the 11-letter gap only exists from e.g.
# the SECOND-shortest to SECOND-longest word??? you fuckers
# anyway i might just generalize it anyway
# because otherwise i think i just have to track every single word?
# and i dont want to do that.
# anyway this returns a list of all the biggest-gap words and their gap
#
# UPDATE: so it works the way i hoped, just a poorly-phrased question.
# the answer, btw, is 11 is the max gap, and the pairs
# are (zyzzyva, biodegradabilities) and (voluptuously, electroencephalographic)
# as anyone would have guessed
# also i wrote this method with only one small error (leading to another small error)
# i'm great, that's the real... reason
def biggestGap():
	# keys are word-values, values are (min-len-word, max-len-word)
	gapDict = {}
	for w in wordList:
		value = wordValueSum(w)
		# create a new entry if needed
		if gapDict.get(value) == None:
			gapDict[value] = (w,w)
		# else replace min or max if relevant
		elif len(w) < len(gapDict.get(value)[0]):
			gapDict[value] = (w, gapDict.get(value)[1])
		elif len(w) > len(gapDict.get(value)[1]):
			gapDict[value] = (gapDict.get(value)[0], w)
	
	# figure out the biggest gap and make a list
	# of all same-value pairs with that gap
	biggestGapInt = 0
	biggestGapLs = []
	for d in gapDict:
		short = gapDict[d][0]
		long = gapDict[d][1]
		diff = len(long) - len(short)
		if diff > biggestGapInt: # in this case start the list over
			biggestGapInt = diff
			biggestGapLs = [(short,long)]
		elif diff == biggestGapInt: # in this case, append to the list
			biggestGapLs.append((short,long))
	
	return (biggestGapInt, biggestGapLs)

# bonus challenge #5 (how we doing? everyone doing okay? i am doing great)
# anyway python has a built-in set_a.isdisjoint(set_b) method which is cool
# so we're gonna build a whole new dict where keys are word-values
# (but only for word-values 188 and up to save time, space, and emotional energy)
# and values are a list of all words with that word-value
# then we'll make sets and compare them all i guess
# which will be fun
# aren't you glad that i'm the one doing this and not you?
#
# UPDATE: oh holy shit i did it, and it works. my goodness
# took a little massaging at the end, a few minor quirks
# but wow, we did it. yay. high five. sense of pride and accomplishment.
# answers: cytotoxicity/unreservedness, defenselessnesses/microphotographic,
# defenselessnesses/photomicrographic. EASYYYYYYYYYYYYYYYY
# i'm kind of curious what it looks like if you take out the value >= 188. hang tight
# okay im not doing that because there will be SO MANY low-value pairs
def disjointWords():
	# make the dict
	wordDict = {}
	for w in wordList:
		value = wordValueSum(w)
		if value>=188:
			current = wordDict.get(value,[])
			current.append(w)
			wordDict[value] = current
	
	# i think this has to use this miserable O(n^2) algorithm
	# which sucks
	# what a nightmare
	disjointPairings = []
	for value in wordDict:
		words = wordDict[value]
		if len(words) > 1:
			for i in range(len(words)-1):
				for j in range(i+1, len(words)):
					if set(words[i]).isdisjoint(set(words[j])):
						disjointPairings.append((words[i],words[j],value))
	
	# oh right so this returns a list of tuples of (word, word, value)
	# that satisfy the requirements (same value, big values (188+), disjoint letters)
	return disjointPairings



# bonus challenge #6
# go behold the algorithmic graveyard at the bottom of this file if you want to see what i went through to get here
#
# new idea: what if we set up a 2d array, where one of the dimensions is length, and the other is value.
# the entry at any given point in the array is the maximum possible chain starting from that length and value
# this takes out the O(n) searching that's going to happen every time in maxChain() (* see graveyard)
# which is what's dragging our time complexity into O(n^2) and making this so absurdly slow.
# length ranges up to ~100, value to ~1000, so it's not even that big a table
# okay let's try this
#
# this approach works!
# in fact i tried three approaches and all worked (but only this one in the appropriate length of time)
# the other two, if you're wondering, were a simple recursive solution, and a dynamic programming solution using hashtables
#
# the answer is that the longest chain of words (of strictly decreasing length and increasing value) is 11
# and i think there are quite a few judging by the other responses on reddit
# anyway mine's the best, and it is:
# nonbiodegradable, archaebacterium, adaptabilities, accountancies, acidulations,
# abstractest, absolution, anviltops, botrytis, muttony, xystus
def generateTable(list = wordList):
	maxLen = 0
	maxValue = 0
	
	# find the dimensions of the table
	for i in list:
		maxLen = max(maxLen, len(i))
		maxValue = max(maxValue, wordValueSum(i))
	
	# outer is lengths, from 0 to maxLen-1 (be careful anna), inner is values, from 0 to maxValue-1. call like ourTable[len-1][val-1]. how exciting
	ourTable = [[[] for x in range(maxValue)] for y in range(maxLen)]
	
	# so. here's what we're doing.
	# for each WORD in our sorted LIST, we insert a list at that point in ourTable
	# the list we insert is the MAXIMUM CHAIN starting from that point -- the longest possible chain.
	# every time we insert a new list, we insert it for every point with len > and val < that it can possibly be reached from,
	# IF it is longer than the chain in that spot.
	# so e.g. #0 will be "aa" which has no chain it can go to ([]), so all lens > 2 and vals < 2 will become [aa]
	# when we get to "abe" it'll look at ourTable for length = 3 and value = 8, find something (say, ["vy"]), and return ["abe","vy"])
	# then we will add THAT to any potential slots of len > 3 and value < 8
	# this is ridiculous. but i think that shoudl work. just a matter of time complexit.
	
	sortedList = sorted(list, key=len)
	
	for word in sortedList:
		valueSum = wordValueSum(word)
		maxChain = [word] + ourTable[len(word)-1][valueSum-1]
		for lengths in range(len(word), maxLen):
			for values in range(valueSum):
				if len(ourTable[lengths][values]) < len(maxChain):
					ourTable[lengths][values] = maxChain
	
	# this just prints the solution instead of returning it because i'm tired
	print(ourTable[maxLen-1][0])
	
	return ourTable
	
	
# you can change this to call whatever algorithms you need to see answers to the prior bonus challenges
def main():
	populateWordList()
	
	begin = time.time()
	
	ourTable = generateTable(wordList)	
	
	end = time.time()
	
	print("took", end-begin, "seconds")
	

if __name__ == "__main__":
	main()



'''
along the way we came up with some solutions to problem #6 that didn't work

i'm including them down here for posterity

and in honor of their sacrifice (and the sacrifice of hours of my lfe)

may they never be forgotten
'''


# okay holy crap bonus challenge #6
# this one is brutal
# a list of words, strictly descending in length, strictly increasing in value
# maximize the length of the list
# i want to come up with some brilliant recursive solution
# but there's at least a 50% chance it'll hit some cursed recursion depth limit
#
# here's the way it'll work:
# make a dict: key: wordlength, value: (word, wordvalue)
# we want to feed it a word and get back the LONGEST chain from that word
# then run it recursively
# starting from EVERY word
# and finally return the longest chain of all.
'''
What we need here is a dynamic programming solution.
Populate the list from the shortest up, in a dict where
each word is a key and each value is the recurse(word) of that word
Then we can dynamically update values by just finding the
longest chain that we can apply to a given word.
Setup might take a minute but it'll make everything else MUCH shorter.
I might try this tomorrow.
'''
'''recurseDict = {}
def recurseSetup():
	# make the dict
	for w in wordList:
		wLen = len(w)
		value = recurseDict.get(wLen, [])
		value.append((w, wordValueSum(w)))
		recurseDict[wLen] = value
	
def recurse(word):
	wordLength = len(word)
	wordValue = wordValueSum(word)
	maxChain = []
	for key in recurseDict:
		if key < wordLength:
			values = recurseDict[key]
			for elt in values:
				if elt[1] > wordValue:
					thisChain = checkMap(elt[0])
					if len(thisChain) > len(maxChain):
						maxChain = thisChain
	maxChain.insert(0, word)
	return maxChain

def recurseAll():
	maxRecurseLs = []
	maxRecurseLen = 0
	for w in wordList:
		ls = recurse(w)
		if len(ls) > maxRecurseLen:
			maxRecurseLen = len(ls)
			maxRecurseLs = ls
	return maxRecurseLs

map = {}
def checkMap(word):
	if word not in map:
		map[word] = recurse(word)
	return map[word]

#def populateMap():
	#for i in range(0,100):
		#if '''
	
''' PROPER SOLUTION STARTS HERE '''

'''# sorts lists by length
def quickSort(ls):
	if len(ls) <= 1:
		return ls
	pivot = ls[0]
	return quickSort([x for x in ls[1:] if len(str(x)) <= len(str(pivot))]) + [pivot] + quickSort([x for x in ls[1:] if len(str(x)) > len(str(pivot))])

def maxChain(word, dynamicDict):
	maxChainList = []
	#maxChainLength = 0
	
	# first we check all the keys in the dynamicDict (i.e. all words SHORTER than the word we're currently on)
	# if a word isn't in there it CANNOT be the next step
	# then we simply pull the value of the longest chain and append that to the word and return that
	# ...right?
	for key in dynamicDict:
		if len(key) < len(word) and wordValueSum(key) > wordValueSum(word):
			keyChain = dynamicDict[key]
			if len(keyChain) > len(maxChainList):
				maxChainList = keyChain
	
	return [word] + maxChainList
				

def dynamicSolve(list = wordList):
	dynamicDict = {} # key = word, value = longest chain from that word
	#sortedWordList = quickSort(wordList) # orders the wordlist for dynamic programming
	sortedWordList = sorted(list, key = len)
	
	# dynamically progam away
	for word in sortedWordList:
		dynamicDict[word] = maxChain(word, dynamicDict)
	
	return dynamicDict'''