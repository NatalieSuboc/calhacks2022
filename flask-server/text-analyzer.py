from parser import JsonParser
import nltk
from nltk.corpus import stopwords

class TextAnalyzer: 
    def __init__(self): 
        self.parser = JsonParser()

    # Example
    def featureExample(self): 
        chat_list = self.parser.get_chats_list()
        chatZeroParticipants = self.parser.get_participants(chat_list[0])
        chatZeroData = self.parser.chat_data[chat_list[0]]
        return

    # Add Additional Features Here 
    '''
    Feature: Most Common Words Used
    - Discerns most common words used by the user.
    '''
    def get_common_words_used(self, name, num=20):
        word_counts = {} # key: word, count: value
        for chat in self.parser.get_chats_list():
            messages = self.parser.get_messages(chat)
            for message in messages:
                # add words if written by the user 
                if message['sender_name'] == name and 'content' in message:
                    text = message['content']
                    words = text.split(' ')
                    for word in words:
                        if word in word_counts.keys():
                            word_counts[word] += 1
                        else:
                            word_counts[word] = 1
        sorted_counts = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)
        word_counts = dict(sorted_counts)
        words = [word for word in list(word_counts) if word.lower() not in set(stopwords.words('english'))]
        return words[:num]

if __name__ == "__main__":
    text_analyzer = TextAnalyzer() 
    print(text_analyzer.featureExample())
    print(text_analyzer.get_common_words_used('Natalie Suboc', num=60))
    # print(text_analyzer.get_common_words_used('Harmony He', num=40))