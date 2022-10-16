import math
from datetime import datetime, timedelta

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

    def analyze_convo_initiator(self, chat_name, threshold=timedelta(hours=6)):
        """
        Analyze who is initiating conversations in the specified chat.
        :return: dict: (member, init_count)
        """
        init_counts = {}

        # Initialize each chat member's count to 0
        members = self.parser.get_participants(chat_name)
        for member in members:
            init_counts[member] = 0
        # Get time diffs b/t message and previous
        time_diffs = self.get_time_diffs(chat_name)

        for (sender, time_passed) in time_diffs:
            # If the time passed from last text sent is above threshold,
            # then we count it as a new conversation being initiated.
            if time_passed > threshold:
                if sender not in init_counts:
                    init_counts[sender] = 0
                init_counts[sender] += 1
        return init_counts

    # Add Additional Features Here

    # --------------TIME ANALYSIS FUNCTIONS----------------------------
    def get_sender_times(self, chat_name):
        chat_data = self.parser.get_messages(chat_name)
        sender_times = []
        for text in chat_data:
            sender = text['sender_name']
            send_time = self.parse_time(text['timestamp_ms'])
            sender_times = [(sender, send_time)] + sender_times
        return sender_times

    def get_time_diffs(self, chat_name):
        sender_times = self.get_sender_times(chat_name)
        time_diffs = []
        prev_time = None
        for (sender, send_time) in sender_times:
            if prev_time is None:
                time_diffs += [(sender, timedelta.max)]
            else:
                time_passed = send_time - prev_time
                time_diffs += [(sender, time_passed)]
            prev_time = send_time
        return time_diffs

    @staticmethod
    def parse_time(timestamp):
        timestamp_dt = datetime.fromtimestamp(timestamp/1000.0).replace(microsecond=0)
        return timestamp_dt


if __name__ == "__main__":
    text_analyzer = TextAnalyzer() 
    # print(text_analyzer.featureExample())
    # text_analyzer.parse_time(1663036596463)
    # print(text_analyzer.chat_list)
    chat0 = 'jessicaandnatalie_p54k8tywpw'
    chat1 = "nataliesuboc_3kprn6_mtg"
    # print(text_analyzer.get_sender_times(chat0))
    text_analyzer.analyze_convo_initiator(chat0)
