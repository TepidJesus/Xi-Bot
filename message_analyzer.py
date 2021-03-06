import flair

CHINA_WORDS = ['china', 'chinese', 'xi']

class Message_processor():
    def __init__(self) -> None:
        self.flair_sentiment = flair.models.TextClassifier.load('en-sentiment')
        print('[INFO] NLP Network Loaded')

    def listify_message(self, message_raw):
        print(f'[MESSAGE]: {message_raw.author} Says \"{message_raw.content}\"')
        self.message_list = list()
        self.message_list = message_raw.content.split(' ')
        for i in range(len(self.message_list)):
            if self.message_list[i].isalpha():
                self.message_list[i] = self.message_list[i].lower()
            elif self.message_list[i].isalnum() != True:
                self.message_list[i] = self.message_list[i].strip('!')
                self.message_list[i] = self.message_list[i].strip('.')
                self.message_list[i] = self.message_list[i].strip(',')
                self.message_list[i] = self.message_list[i].strip('-')
                self.message_list[i] = self.message_list[i].strip('?')
                self.message_list[i] = self.message_list[i].lower()
            else:
                continue
        return self.message_list

    def run_message_checks(self, message, message_list):
        s = flair.data.Sentence(message)
        self.flair_sentiment.predict(s)
        sentiment_score = s.labels

        china_check = any(other_word in message_list for other_word in CHINA_WORDS)
        return sentiment_score, china_check

    def choose_response(self, message, message_list, china_check, raw_sentiment_score):
        message_sentiment = str(raw_sentiment_score[0])
        message_sentiment = message_sentiment[0:8]

        if china_check and message_sentiment == 'NEGATIVE': # Punish
            response = 'šØš³ This message has been reported to The Ministry of State Security šØš³\nšØš³ 10 Credit Points Have Been Deducted From Your Balance šØš³'
            credit_change = -10
            return response, credit_change
        elif china_check and message_sentiment == 'POSITIVE': # Reward
            response = 'šØš³ The People Of China Thank You For Your Kind Words šØš³\nšØš³ 1 Credit Point Has Been Added To Your Balance šØš³'
            credit_change = 1
            return response, credit_change
        elif 'taiwan' in message_list:
            response = 'šØš³ Did You Mean Chinese Taipei? šØš³'
            return response, None
        elif 'tiananmen' in message_list:
            response = 'šØš³ Odd Of You To Mention A Place Where Nothing Has Ever Happened... Especially on June 4th 1989 šØš³\n'
            return response, None
        elif china_check:
            response = 'šØš³ China #1 šØš³'
            return response, None
        else:
            return None
        
