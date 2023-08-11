import nltk
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.probability import FreqDist
from nltk.tokenize.treebank import TreebankWordDetokenizer
from nltk.cluster.util import cosine_distance
import numpy as np
import networkx as nx
 
nltk.download('punkt')
nltk.download('stopwords')
 
def read_article(article_text):
    sentences = sent_tokenize(article_text)
    return sentences
 
def create_frequency_matrix(sentences):
    stop_words = set(stopwords.words("english"))
    words = word_tokenize(" ".join(sentences).lower())
    words = [word for word in words if word.isalnum()]
    words = [word for word in words if word not in stop_words]
    frequency_matrix = FreqDist(words)
    return frequency_matrix
 
def create_similarity_matrix(sentences):
    similarity_matrix = np.zeros((len(sentences), len(sentences)))
 
    for i in range(len(sentences)):
        for j in range(len(sentences)):
            if i != j:
                similarity_matrix[i][j] = sentence_similarity(
                    sentences[i], sentences[j]
                )
 
    return similarity_matrix
 
def sentence_similarity(sent1, sent2):
    stop_words = set(stopwords.words("english"))
    words1 = word_tokenize(sent1.lower())
    words2 = word_tokenize(sent2.lower())
 
    words1 = [word for word in words1 if word.isalnum()]
    words2 = [word for word in words2 if word.isalnum()]
 
    all_words = list(set(words1 + words2))
 
    vector1 = [0] * len(all_words)
    vector2 = [0] * len(all_words)
 
    for word in words1:
        if word not in stop_words:
            vector1[all_words.index(word)] += 1
 
    for word in words2:
        if word not in stop_words:
            vector2[all_words.index(word)] += 1
 
    return 1 - cosine_distance(vector1, vector2)
 
def generate_summary(article_text, num_sentences=5):
    sentences = read_article(article_text)
    frequency_matrix = create_frequency_matrix(sentences)
    similarity_matrix = create_similarity_matrix(sentences)
    page_rank = nx.pagerank(nx.from_numpy_array(similarity_matrix))
 
    ranked_sentences = sorted(((page_rank[i], s) for i, s in enumerate(sentences)), reverse=True)
 
    selected_sentences = sorted(ranked_sentences[:num_sentences], key=lambda x: x[0])
 
    summary = TreebankWordDetokenizer().detokenize([s[1] for s in selected_sentences])
    return summary
 
if __name__ == "__main__":
    article_text = """
    Insert your news article text here.
    You can include multiple paragraphs.
    """
 
    summary = generate_summary(article_text)
    print("Generated Summary:")
    print(summary)
