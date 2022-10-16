from parser import JsonParser

class TextAnalyzer: 
    def __init__(self): 
        self.parser = JsonParser()

    # Example of a simple feature 
    def featureExample(self): 
        participants = self.parser.get_participants('andreakwong_xqvcy4ubsq')
        self.parser.get_messages('andreakwong_xqvcy4ubsq')
        return participants
        
if __name__ == "__main__":
    text_analyzer = TextAnalyzer() 
    print(text_analyzer.featureExample())