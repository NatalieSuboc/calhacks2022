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
        f = open("../messages/autofill_information.json")
        personal_data = json.load(f)
        self.name = next(iter(personal_data.values()))["FULL_NAME"][0]
    

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

    def parse_group_chat_name(self, chat_name): 
        """
        Returns a formatted version of a group chat name, removing hash value
        :param chat_name: Name of chat
        :return:

        i.e. natalieandharmony_1ls9g4820 returns Natalie & Harmony & Jessica
        """
        
        participants = self.get_participants(chat_name)
        # if len(participants) == 2:
        #     raise Exception("This is not a group chat.")
        
        # Check if this is a named group chat, or a default named group chat 
        isNamed = False
        selfBuffer = 0 
        for participant in participants: 
            if participant.lower()[0] in chat_name:
                continue 
            else: 
                selfBuffer += 1 
                if selfBuffer > 1:
                    isNamed = True 

        for participant in participants:
            if participant == self.name: 
                continue 
            if participant.lower()[0] in chat_name: 
                continue 
            else: 
                isNamed = True 

        # If the group chat is named, use the name
        if isNamed: 
            return chat_name.split("_")[0].capitalize()
            

        # If the group chat is unnamed, use the names of all participants
        if not isNamed:
            participants.remove(self.name)
            return " & ".join(participants)


if __name__ == "__main__":
    parser = JsonParser()
    # print(parser.get_participants('ashleychang_m8xwv9ddua'))
    # print(parser.get_messages('ashleychang_m8xwv9ddua'))