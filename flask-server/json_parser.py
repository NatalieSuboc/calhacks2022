import json
import os
import emoji


class JsonParser:
    def __init__(self):
        self.dir_path = "../messages/inbox/"
        self.chats_list = os.listdir(self.dir_path)
        if '.DS_Store' in self.chats_list:
            self.chats_list.remove('.DS_Store')
        # 'self.chat_data': dict('chat_name' -> 'data')
        self.chat_data = self.load_chat_data()
        self.autofill_info = self.load_autofill_info()

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

    def get_message_contents(self, chat_name):
        """
        Gets all message contents for specified chat
        :param chat_name:
        :return: List[(sender name, message content)]
        """
        messages = self.get_messages(chat_name)
        msg_contents = []

        reaction_msg = "eacted XXX to your message "
        for msg in messages:
            if 'content' in msg:
                content = self.convert_to_unicode(msg['content'])
                demojified_content = emoji.replace_emoji(content, "XXX")

                # Filter out reaction messages
                if reaction_msg not in demojified_content:
                    msg_contents += [(msg['sender_name'], content)]

        return msg_contents

    def get_all_messages_contents(self):
        """
        Gets all message contents across all chats
        :return: List[(sender name, message content)]
        """
        msg_contents = []
        for chat_name in self.chats_list:
            msg_contents += self.get_message_contents(chat_name)
        return msg_contents

    def load_autofill_info(self):
        """
        Reads in autofill information (metadata)
        :return:
        """
        autofill_info = {}
        filename = "../messages/autofill_information.json"        
        f = open(filename)
        data = json.load(f)
        return data

    def get_chats_list(self):
        """
        Returns list of chat names
        :return:
        """
        return self.chats_list

    def get_participants(self, chat_name=None):
        """
        Returns list of participants in the specified chat
        :param chat_name: Name of chat
        :return:
        """
        if not chat_name:
            participants = []
            for chat_name in self.chats_list:
                data = self.chat_data[chat_name]['participants']
                participants += [item['name'] for item in data]
            return participants
        else:
            data = self.chat_data[chat_name]['participants']
            return [item['name'] for item in data]

    def get_messages(self, chat_name):
        """
        Returns message data for the specified chat
        :param chat_name: Name of chat
        :return:
        """
        return self.chat_data[chat_name]['messages']
        # sender_name, timestamp_ms, content, reactions/actor

    def get_user_name(self):
        """
        Returns user name
        :return:
        """
        return self.autofill_info['autofill_information_v2']['FULL_NAME'][0]

    @staticmethod
    def convert_to_unicode(string):
        return string.encode('latin1').decode('utf8')

if __name__ == "__main__":
    parser = JsonParser()
    print(parser.get_participants('ashleychang_m8xwv9ddua'))
    print(parser.get_messages('ashleychang_m8xwv9ddua'))
    print(parser.get_all_messages_contents())