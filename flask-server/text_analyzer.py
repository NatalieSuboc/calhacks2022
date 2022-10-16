from cgitb import text
from datetime import datetime
import collections
from json_parser import JsonParser


class TextAnalyzer: 
    def __init__(self): 
        self.parser = JsonParser()
        self.chat_list = self.parser.get_chats_list()
        self.chat_data = self.parser.chat_data
        self.name = self.parser.name


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

    # Most messages received from: 
    def mostReceivedFrom(self):
        sender_names = []
        for chat in self.chat_list: 
            for message in self.parser.get_messages(chat): 
                sender = message['sender_name']
                if sender != self.name:
                    sender_names.append(message['sender_name'])
        
        sender_names_counter = collections.Counter(sender_names)
        return sender_names_counter.most_common()[0]

    # Most messages sent to: 
    def mostSentTo(self):
        sentList = []
        for chat in self.chat_list:
            for message in self.parser.get_messages(chat): 
                sender = message['sender_name']
                if sender == self.name:
                    sentList.append(chat)
        sent_dict_counter = collections.Counter(sentList)
        
        mostSentTo = sent_dict_counter.most_common()[0]
        if len(self.parser.get_participants(mostSentTo[0])) > 2: 
            return self.parser.parse_group_chat_name(mostSentTo[0])
         


if __name__ == "__main__":
    text_analyzer = TextAnalyzer() 
    
    text_analyzer.parse_time(1663036596463)
    print("You received the most messages from: ", text_analyzer.mostReceivedFrom())
    print("You send the most messages to: ", text_analyzer.mostSentTo())

    for chat in text_analyzer.parser.chats_list:
        print(text_analyzer.parser.parse_group_chat_name(chat))
    
