import math
import nltk
import emoji
# from emoji import UNICODE_EMOJI_ENGLISH
from datetime import datetime, timedelta
from nltk.corpus import stopwords

from json_parser import JsonParser

EMOJI_LENGTH = 16


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

    def get_avg_response_times(self, chat_name, threshold=timedelta(hours=6)):
        """
        Returns count + avg response time for each member in the chat
        :param chat_name:
        :param threshold:
        :return:
        """
        # Get time diffs b/t message and previous
        time_diffs = self.get_time_diffs(chat_name)
        time_diffs.pop(0)
        response_rates = {}
        members = self.parser.get_participants(chat_name)
        for member in members:
            response_rates[member] = (0, timedelta(seconds=0))  # (Count, Avg Response Time)

        for (sender, time_passed) in time_diffs:
            # If the time passed from last text sent is less than threshold,
            # then we count it as responding to a text, instead of initiating a new convo.
            if time_passed <= threshold:
                n, avg_response_time = response_rates[sender]

                avg_response_time = self.multiply_td(avg_response_time, n/(n+1)) + (time_passed / (n + 1))
                response_rates[sender] = (n + 1, avg_response_time)

        for member in members:
            formatted_rate = ''
            count, rate = response_rates[member]
            days, remainder = divmod(rate.seconds, 3600 * 24)
            if days > 0:
                formatted_rate += f'{days} Days, '
            hours, remainder = divmod(remainder, 3600)
            if len(formatted_rate) > 0 or hours > 0:
                formatted_rate += f'{hours} Hours, '
            minutes, seconds = divmod(remainder, 60)
            formatted_rate += f'{minutes} Minutes, {seconds} Seconds'
            response_rates[member] = formatted_rate
        return response_rates

    # Add Additional Features Here

    """
    Feature: Most Common Words Used
    - Discerns most common words used by the user.
    """
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

    '''
    Feature: Analyze Number Messages Sent

    '''
    def analyze_num_messages_sent(self):
        # exclude group chats?
        message_counts = {} # (person, message_count)
        for chat in self.parser.get_chats_list():
            messages = self.parser.get_messages(chat)
            for message in messages:
                if message['sender_name'] not in message_counts.keys():
                    message_counts[message['sender_name']] = 1
                else:
                    message_counts[message['sender_name']] += 1
        sorted_counts = sorted(message_counts.items(), key=lambda x: x[1], reverse=True)
        # print(sorted_counts)
        most_sent = sorted_counts[0]
        least_sent = sorted_counts[len(sorted_counts)-1]
        return sorted_counts
    
    '''
    Feature: 
    '''
    def get_responsiveness_over_time(self, name):
        responsiveness = [] # list of (time, responsiveness)


    """
    Feature: Average text length
    """
    def get_avg_text_length(self):
        message_counts = {} # person: (total message len, num messages)
        for chat in self.parser.get_chats_list():
            messages = self.parser.get_messages(chat)
            for message in messages:
                # do not process for image-only / no text content
                if 'content' not in message:
                    continue
                counts = sum(TextAnalyzer.get_emoji_counts(message['content']).values())
                length = len(message['content']) - (counts * 16) # TODO Condense emojis
                if message['sender_name'] not in message_counts.keys(): 
                    message_counts[message['sender_name']] = (length, 1)
                else:
                    cur = message_counts[message['sender_name']]
                    message_counts[message['sender_name']] = (cur[0] + length, cur[1] + 1)
        averages = {}
        for person in message_counts.keys():
            counts = message_counts[person]
            avg = counts[0] / counts[1]
            averages[person] = avg
        sorted_avgs = sorted(averages.items(), key=lambda x: x[1], reverse=True)
        return dict(sorted_avgs)


    # --------------TIME ANALYSIS FUNCTIONS----------------------------
    def get_sender_times(self, chat_name):
        """
        Returns a list of sender and times in chronological order, from earliest to latest message.
        :param chat_name:
        :return:
        """
        chat_data = self.parser.get_messages(chat_name)
        sender_times = []
        for text in chat_data:
            sender = text['sender_name']
            send_time = self.parse_time(text['timestamp_ms'])
            sender_times = [(sender, send_time)] + sender_times
        return sender_times

    def get_time_diffs(self, chat_name):
        """
        Gets time passed from previous message for each sender.
        The first time's time diff is inf(since no prev sender)
        :param chat_name:
        :return:
        """
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
        # Returns timestamp parsed into a datetime obj
        timestamp_dt = datetime.fromtimestamp(timestamp/1000.0).replace(microsecond=0)
        return timestamp_dt

    @staticmethod
    def multiply_td(time_delta, k):
        # Returns 'time_delta' multiplied by 'k'
        return timedelta(seconds=time_delta.total_seconds() * k)

    # ------------------EMOJI ANALYSIS FUNCTIONS---------------------
    def get_emoji_usage(self, chat_name=None, person=None):
        """
        Gets emoji usage for each person, from most used to least used
        :param chat_name:
        :param person:
        :return: dict{('sender': dict{('emoji': 'count')})}
        """
        if not chat_name:  # Across all chats
            msg_contents = self.parser.get_all_messages_contents()
        else:  # Specific to a certain chat
            msg_contents = self.parser.get_message_contents(chat_name)

        usage_dict = {}
        if person: # Only track usage for single person
            usage_dict[person] = {}
        else:
            for member in self.parser.get_participants(chat_name):
                usage_dict[member] = {}

        for sender, text in msg_contents:
            if not person or person == sender:
                emoji_counts = self.get_emoji_counts(text)
                for emoji_uc in emoji_counts:
                    if emoji_uc not in usage_dict[sender]:
                        usage_dict[sender][emoji_uc] = 0
                    usage_dict[sender][emoji_uc] += 1

        for sender in usage_dict:
            # Sort from most used to the least used emoji
            usage_dict[sender] = dict(sorted(usage_dict[sender].items(), key=lambda item: item[1], reverse=True))
        return usage_dict

    @staticmethod
    def get_emoji_counts(string):
        emoji_data = emoji.emoji_list(string)
        distinct_emojis = emoji.distinct_emoji_list(string)
        emoji_counts = {}
        for emoji_str in distinct_emojis:
            emoji_counts[emoji_str] = 0
        for item in emoji_data:
            emoji_str = item['emoji']
            emoji_counts[emoji_str] += 1

        return emoji_counts


if __name__ == "__main__":
    text_analyzer = TextAnalyzer() 
    # print(text_analyzer.featureExample())
    # text_analyzer.parse_time(1663036596463)
    # print(text_analyzer.chat_list)
    chat0 = 'jessicaandnatalie_p54k8tywpw'
    chat1 = "nataliesuboc_3kprn6_mtg"
    chat2 = 'juliadeng_ceaz1qgcsg'
    chat3 = 'juliaandnatalie_ut8vdbynta'
    chat4 = 'up_d9qf1gvmwg'
    # print(text_analyzer.get_sender_times(chat0))
    # text_analyzer.analyze_convo_initiator(chat0)
    # print(text_analyzer.get_avg_response_times(chat3))

    print(text_analyzer.get_emoji_usage(person='Natalie Suboc'))
    print(text_analyzer.get_emoji_usage(person='Jessica Liang'))
    print(text_analyzer.get_emoji_usage(person='Harmony He'))
    print(text_analyzer.get_emoji_usage(chat0))
    print(text_analyzer.get_emoji_usage(chat4))

    # print(text_analyzer.chat_list)
    #chat0 = 'jessicaandnatalie_p54k8tywpw'
    #chat1 = "nataliesuboc_3kprn6_mtg"
    # print(text_analyzer.get_sender_times(chat0))
    #text_analyzer.analyze_convo_initiator(chat0)
    #print(text_analyzer.get_common_words_used('Natalie Suboc', num=60))
    print(text_analyzer.get_avg_text_length())
    # print(text_analyzer.analyze_num_messages_sent())

