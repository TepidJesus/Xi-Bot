from credit_keeper import CreditKeeper
import flair

CHINA_WORDS = ['china', 'chinese', 'xi']


class Message_processor():
    def __init__(self) -> None:
        self.credit_score_keeper = CreditKeeper()
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
            response = '🇨🇳 This message has been reported to The Ministry of State Security 🇨🇳\n🇨🇳 10 Credit Points Have Been Deducted From Your Balance 🇨🇳'
            self.credit_score_keeper.alter_creditscore(member=message.author.name, points=-10)
            return response
        elif china_check and message_sentiment == 'POSITIVE': # Reward
            response = '🇨🇳 The People Of China Thank You For Your Kind Words 🇨🇳\n🇨🇳 1 Credit Point Has Been Added To Your Balance 🇨🇳'
            self.credit_score_keeper.alter_creditscore(member=message.author.name, points=1)
            return response
        elif 'taiwan' in message_list:
            response = '🇨🇳 Did You Mean Chinese Taipei? 🇨🇳'
            return response
        elif 'tiananmen' in message_list:
            response = '🇨🇳 Odd Of You To Mention A Place Where Nothing Has Ever Happened... Especially on June 4th 1989 🇨🇳\n'
            return response
        elif china_check:
            response = '🇨🇳 China #1 🇨🇳'
            return response
        else:
            return None
        
