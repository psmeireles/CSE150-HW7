
# coding: utf-8

# In[162]:


from collections import defaultdict


# In[2]:


wordsFile = open('general/words.txt')
words = []
for word in wordsFile:
    words.append(word.split()[0])


# In[3]:


# creating dict with every category's nGram count distribution
def generate_categories_dict():
    categories = defaultdict()
    for category in ['general', 'business', 'entertainment', 'politics', 'sport', 'tech']:
        ngrams = []
        for n in ['uni', 'bi', 'tri', 'four', 'five']:
            if category == 'general':
                filename = f'{category}/{n}grams.txt'
            else:
                filename = f'{category}/{category}_{n}grams.txt'

            file = open(filename)

            ngramVector = []
            for l in file:
                if n == 'uni':
                    ngramVector.append(int(l))
                else:
                    ngramVector.append([int(x) for x in l.split()])
            file.close()

            # precomputing probabilities for unigrams
            if n == 'uni':
                uniSum = sum(ngramVector)
                ngramVector = [x/uniSum for x in ngramVector]

            ngrams.append(ngramVector)
        categories[category] = ngrams
    return categories


# In[404]:


def probsUnigram(categories, category):
    # Returns the category's unigram probabilities for every word
    return categories[category][0]


# In[405]:


def probsNGram(evidence, categories, category, words):
    # Returns the category's nGram probabilities for every nGrams
    n = len(evidence.split())
    corpus = categories[category][n]
    counts = [[words[v[n]], v[n]] for v in corpus if [words.index(e) for e in evidence.split()] == v[:n]]
    countsSum = sum([v[1] for v in counts])
    probabilities = [[v[0], v[1]/countsSum] for v in counts]
    return probabilities


# In[406]:


def unigramProbability(word, probVector, words):
    # Returns the category's unigram probability for a specific word
    return probVector[words.index(word)]


# In[407]:


def nGramProbability(word, probVector):
    # Returns the category's nGram probability for a specific nGram
    prob = [v[1] for v in probVector if v[0] == word]
    if len(prob) == 0:
        return 0
    else:
        return prob[0]


# In[408]:


def mixedProb(word, words, uniDist, nGramsDists, lambdas):
    # Returs the mixed probability considering all nGrams
    mixed = lambdas[0]*unigramProbability(word, uniDist, words)
    for i in range(0, len(nGramsDists)):
        mixed += lambdas[i+1]*nGramProbability(word, nGramsDists[i])
    return mixed


# In[429]:


def predictNextWord(evidence, categories, category, probsUni, lambdas=[0.2]*5):
    # Predicts the next word given a reference text
    evidenceWords = evidence
    n = len(evidenceWords)
    sumRelevantLambdas = sum(lambdas[:n+1])
    normLambda = [x/sumRelevantLambdas for x in lambdas[:n+1]]
    nGramsDists = []

    """
    with ProcessPoolExecutor() as executor:

        futures = [winprocess.submit(executor, probsNGram, ' '.join(evidenceWords[-i:]), categories, category, words)\
                  for i in range(1, n+1)]

        concurrent.futures.wait(futures)
        nGramsDists = [f.result() for f in futures]
    """

    for i in range(1, n+1):
        newEvidence = ' '.join(evidenceWords[-i:])
        nGramsDists.append(probsNGram(newEvidence, categories, category, words))


    probabilities = []
    """
    with ProcessPoolExecutor() as executor:
        args = categories, category, words, probsUni, nGramsDists, normLambda
        futures = [winprocess.submit(executor, calculateMixedProbs, group, *args)\
                  for group in grouper(words, 1000)]

        concurrent.futures.wait(futures)
        probabilities = list(zip(words, [f.result() for f in futures]))

    """
    for word in words:
        mixed = mixedProb(word, words, probsUni, nGramsDists, normLambda)
        probabilities.append([word, mixed])


    probabilities = sorted(probabilities, key = lambda x:-x[1])
    return [v[0] for v in probabilities[:3]]


# In[433]:


def getAllPredictions(evidence, categories, category, probsUni, lambdas=[0.2]*5):
    # Returns the 3 most probable fivegrams
    recommendedWords = []
    newEvidence = evidence
    for i in range(0, 15):
        newWords = predictNextWord(newEvidence, categories, 'general',                             probsUnigram(categories, 'general'))
        if i == 0:
            for j in range(0, len(newWords)):
                recommendedWords.append([newWords[j]])
        else:
            recommendedWords[i%5].append(newWords[0])

        if i%5 == 0:
            newEvidence = ' '.join(evidence.split()[-3:] + [recommendedWords[i/5][i%5]])
        else:
            newEvidence = ' '.join(newEvidence.split()[-3:] + [recommendedWords[i/5][i%5]])
    return recommendedWords


# In[430]:


#get_ipython().run_cell_magic('time', '', "predictNextWord('tv future in the', categories, 'general', \\\n                        probsUnigram(categories, 'general'))")

#
# In[425]:


#get_ipython().run_cell_magic('time', '', "evidence = 'this is one example'\nfor i in range(0, 5):\n    newWord = predictNextWord(evidence, categories, 'general', \\\n                        probsUnigram(categories, 'general'))\n    evidence = ' '.join(evidence.split()[-3:] + [newWord])\nprint(evidence)")
