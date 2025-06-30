import string

faq_data = {
    "what is your name": "I am a FAQ Chatbot.",
    "how does this chatbot work": "I match your question with the closest FAQ and provide an answer.",
    "what languages do you speak": "I speak Python and a bit of human language!",
    "how can i contact support": "You can contact support at support@example.com.",
    "what is ai": "AI stands for Artificial Intelligence, which means machines simulating human intelligence.",
}

def preprocess(text):
    text = text.lower()
    text = text.translate(str.maketrans('', '', string.punctuation))
    return text

def find_best_match(user_question, faq_data):
    user_question = preprocess(user_question)
    max_overlap = 0
    best_answer = "Sorry, I don't understand your question."

    for question, answer in faq_data.items():
        question_processed = preprocess(question)
        user_words = set(user_question.split())
        question_words = set(question_processed.split())
        overlap = len(user_words.intersection(question_words))

        if overlap > max_overlap:
            max_overlap = overlap
            best_answer = answer

    return best_answer

def chat():
    print("Hi! Ask me anything. Type 'exit' to quit.")
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'exit':
            print("Chatbot: Goodbye!")
            break
        
        answer = find_best_match(user_input, faq_data)
        print("Chatbot:", answer)

if __name__ == "__main__":
    chat()
