import json
import os


class JsonParser:
    def __init__(self):
        self.dir_path = "../messages/inbox/"
        self.chats_list = os.listdir(self.dir_path)
        if '.DS_Store' in self.chats_list:
            self.chats_list.remove('.DS_Store')
        # 'self.chat_data': dict('chat_name' -> 'data')
        self.chat_data = self.load_chat_data()

    def load_chat_data(self):
        """
        Reads in message JSON for the chat
        :param chat_name: Name of the chat
        :return:
        """
        chat_data = {}
        for chat_name in self.chats_list:
            # Open JSON file
            filename = self.dir_path + chat_name + "/message_1.json"
            f = open(filename)
            # Turn JSON object as a dictionary
            data = json.load(f)
            chat_data[chat_name] = data
            # Fields: messages,title,is_still_participant,thread_type,thread_path,magic_words,joinable_mode,participants
        return chat_data

    def get_chats_list(self):
        """
        Returns list of chat names
        :return:
        """
        return self.chats_list

    def get_participants(self, chat_name):
        """
        Returns list of participants in the specified chat
        :param chat_name: Name of chat
        :return:
        """
        data = self.chat_data[chat_name]['participants']
        return [item['name'] for item in data]

    def get_messages(self, chat_name):
        """
        Returns list of participants in the specified chat
        :param chat_name: Name of chat
        :return:
        """
        return self.chat_data[chat_name]['messages']
        # sender_name, timestamp_ms, content, reactions/actor


if __name__ == "__main__":
    parser = JsonParser()
    print(parser.get_participants('ashleychang_m8xwv9ddua'))
    print(parser.get_messages('ashleychang_m8xwv9ddua'))