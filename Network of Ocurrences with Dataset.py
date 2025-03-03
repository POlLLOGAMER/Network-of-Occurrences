!pip install datasets
from datasets import load_dataset

# Load the dataset
dataset = load_dataset("daily_dialog")

# View the first entries
print(dataset["train"][0])
# Extract the questions and answers from the dataset
corpus = {}
for conversation in dataset["train"]:
    for i in range(len(conversation["dialog"]) - 1):
        # Use a question from the conversation as "input" and the next as "response"
        question = conversation["dialog"][i]
        response = conversation["dialog"][i + 1]
        corpus[question] = response

print(f"Corpus built with {len(corpus)} question-answer pairs.")
# Function to build the relation network (same as before)
def build_relation_network(corpus):
    network = {}
    for phrase in corpus:
        words = phrase.split()
        for i, word in enumerate(words):
            if word not in network:
                network[word] = set()
            if i > 0:
                network[word].add(words[i-1])
            if i < len(words) - 1:
                network[word].add(words[i+1])
    return network

# Build the network with the corpus
relation_network = build_relation_network(corpus)

# Function to get response (same as before)
def get_response(question, corpus, network):
    question_words = set(question.lower().split())
    best_score = 0
    best_phrase = None
    for phrase in corpus:
        phrase_words = set(phrase.split())
        common_words = question_words.intersection(phrase_words)
        score = len(common_words)
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
question = "Hello how are you bro"
response = get_response(question, corpus, relation_network)
print(response)
