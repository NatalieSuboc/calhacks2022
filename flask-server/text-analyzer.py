from parser import JsonParser

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


if __name__ == "__main__":
    text_analyzer = TextAnalyzer() 
    print(text_analyzer.featureExample())