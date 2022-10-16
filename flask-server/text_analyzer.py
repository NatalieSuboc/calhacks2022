from datetime import datetime

from json_parser import JsonParser


class TextAnalyzer: 
    def __init__(self): 
        self.parser = JsonParser()
        self.chat_list = self.parser.get_chats_list()


    # Example
    def featureExample(self): 
        chat_list = self.parser.get_chats_list()
        chatZeroParticipants = self.parser.get_participants(chat_list[0])
        chatZeroData = self.parser.chat_data[chat_list[0]]
        return


    def analyze_convo_initiator(self, chat_name):
        """
        Analyze who is initiating conversations in the specified chat.
        :return:
        """
        a = 0

    # Add Additional Features Here
    @staticmethod
    def parse_time(timestamp):
        timestamp_dt = datetime.fromtimestamp(timestamp/1000.0)
        return timestamp_dt


if __name__ == "__main__":
    text_analyzer = TextAnalyzer() 
    # print(text_analyzer.featureExample())
    text_analyzer.parse_time(1663036596463)