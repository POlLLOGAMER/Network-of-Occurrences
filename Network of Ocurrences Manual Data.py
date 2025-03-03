# We define the corpus and the associated responses
corpus = {
    "hello how are you": "I'm good, and you?",
    "how's it going": "Everything's good here.",
    "hello friend": "Hello, great to see you!",
    "how's it going for you": "I'm doing great, thanks."
}

# Function to build the relationship network
def build_relation_network(corpus):
    network = {}
    for phrase in corpus:
        words = phrase.split()
        for i, word in enumerate(words):
            if word not in network:
                network[word] = set()
            # Connect to the previous and next words if they exist
            if i > 0:
                network[word].add(words[i-1])
            if i < len(words) - 1:
                network[word].add(words[i+1])
    return network

# Build the network
relation_network = build_relation_network(corpus)

# Function to analyze the question and determine the response
def get_response(question, corpus, network):
    question_words = set(question.lower().split())
    best_score = 0
    best_phrase = None
    for phrase in corpus:
        phrase_words = set(phrase.split())
        # Base score: number of common words
        common_words = question_words.intersection(phrase_words)
        score = len(common_words)
        # Additional score: connections in the network
        for word in common_words:
            if word in network:
                connected_words = network[word]
                for cw in connected_words:
                    if cw in question_words:
                        score += 1
        if score > best_score:
            best_score = score
            best_phrase = phrase
    if best_phrase:
        return corpus[best_phrase]
    else:
        return "I don't understand, can you say something else?"

# Example usage
question = "hello"
response = get_response(question, corpus, relation_network)
print(response)
