import numpy as np
from numpy.random import randn
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity, euclidean_distances

documents = ["Memes are the best",
"I love dogs",
"I love Mr Goose",
"Computer Science is my passion"]

def find_similar_question(question="I love cats"):
    documents.append(question)

    count_vectorizer = CountVectorizer()
    sparse_matrix = count_vectorizer.fit_transform(documents)

    similar_matrix = cosine_similarity(sparse_matrix[-1], sparse_matrix)
    similar_array = similar_matrix[0][:-1]
    
    max_val = max(similar_array)
    max_index = -1

    for i, val in enumerate(similar_array):
        if val == max_val:
            max_index = i

    return documents[max_index]

    '''
    for doc in sparse_matrix:
        print(euclidean_distances(sparse_matrix[-1], doc))
    '''

print(find_similar_question())

# Cosine similarity -> higher the better and Euclidean distance -> lower the better

'''
def avg_sentence_vector(words, model, num_features, index2word_set):
    #function to average all words vectors in a given paragraph
    featureVec = np.zeros((num_features,), dtype="float32")
    nwords = 0

    for word in words:
        if word in index2word_set:
            nwords = nwords+1
            featureVec = np.add(featureVec, model[word])

    if nwords>0:
        featureVec = np.divide(featureVec, nwords)
    return featureVec

from sklearn.metrics.pairwise import cosine_similarity


#get average vector for sentence 1
sentence_1 = "this is sentence number one"
sentence_1_avg_vector = avg_sentence_vector(sentence_1.split(), model=word2vec_model, num_features=100)

#get average vector for sentence 2
sentence_2 = "this is sentence number two"
sentence_2_avg_vector = avg_sentence_vector(sentence_2.split(), model=word2vec_model, num_features=100)

sen1_sen2_similarity =  cosine_similarity(sentence_1_avg_vector,sentence_2_avg_vector)
'''
