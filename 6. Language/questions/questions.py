import nltk
nltk.download("stopwords")
import sys
import os
import math

FILE_MATCHES = 1
SENTENCE_MATCHES = 1


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """
    file_contents_mapping = {}

    for file_name in os.listdir(directory):
        file_contents_mapping[file_name[:-4]] = open(
            file=os.path.join(directory, file_name),
            mode="r",
            encoding="utf8"
        ).read()
                
    print("Files loaded.")
    return file_contents_mapping


def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    tokens = [word.lower() for word in nltk.word_tokenize(document)]
    
    # Filter out punctuation and stopwords (common words that are unlikely to 
    # be useful for querying). Punctuation is defined as any character in 
    # string.punctuation (after you import string). Stopwords are defined 
    # as any word in nltk.corpus.stopwords.words("english").

    punctuation = [',', '.', '"', ';', '(', ')', ':', '``', '`', "''", "'", '=', '%']
    stopwords = nltk.corpus.stopwords.words("english")
    tokens = [token for token in tokens if (token not in stopwords and token not in punctuation)]


    return tokens


def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    word_frequency = {}
    idf_values = {}

    for document in documents:
        for word in set(documents[document]):
            if word not in word_frequency.keys():
                word_frequency[word] = 1
            else:
                word_frequency[word] += 1

    for word in word_frequency:
        idf_values[word] = 1 + (math.log(len(documents) / word_frequency[word]))

    return idf_values

    
def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    tf_idf = {}

    for file in files:
        tf_idf[file] = 0

        for word in query:
            if word in files[file]:
                frequency = files[file].count(word)
            else:
                frequency = 1

            if word not in idfs.keys():
                idf = 1
            else:
                idf = idfs[word]

            # Recall that tf-idf for a term is computed by multiplying 
            # the number of times the term appears in the document 
            # by the IDF value for that term.
            tf_idf[file] =  frequency * idf


    return sorted(
        tf_idf, 
        key=tf_idf.get, 
        reverse=True
    )[:n]


def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    result = {}

    for sentence in sentences:
        result[sentence] = {}
        result[sentence]['idf'] = 0
        result[sentence]['query_word_count'] = 0

        for word in query:
            if word in sentences[sentence]:
                result[sentence]['idf'] += idfs[word]
                result[sentence]['query_word_count'] += 1

        # If two sentences have the same value according to the matching word measure, 
        # then sentences with a higher “query term density” should be preferred. 
        # Query term density is defined as the proportion of words in the sentence that 
        # are also words in the query. For example, if a sentence has 10 words, 3 of which
        # are in the query, then the sentence’s query term density is 0.3.
        result[sentence]['density'] = float(result[sentence]['query_word_count'] / len(sentences[sentence]))


    return sorted(
        result.keys(),
        key=lambda s: (result[s]['idf'], result[s]['density']),
        reverse=True
    )[:n]


if __name__ == "__main__":
    main()
