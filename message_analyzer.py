from credit_keeper import CreditKeeper

FORBIDDEN_WORDS = ['bad', 'stupid', 'worse', 'hate', 'overthrow', 'awful', 'dreadful', 'poor', 'cheap', 'imperfect', 'sucks', 'suck', 'trash', 'garbage', 'dislike', 'shit', 'fuck', 'worst', 'terrible', 'dumb', 'cool', 'amazingly', 'stoopid', 'gey', 'sus', 'imposter', 'corrupt']
PRAISE_WORDS = ['good', '#1', 'number 1', 'great', 'fucks', 'pog', 'poggers', 'best', 'amazing', 'love', 'china#1', 'superior', 'praise', 'very', 'predatorial']
CHINA_WORDS = ['china', 'chinese', 'xi']
NEGATIONS = ['isn\'t', 'not', 'never', 'isnt']

class Message_processor():
    def __init__(self) -> None:
        self.credit_score_keeper = CreditKeeper()

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

    def run_message_checks(self, message_list):
        bad_word_check = any(other_word in message_list for other_word in FORBIDDEN_WORDS)
        praise_word_check = any(other_word in message_list for other_word in PRAISE_WORDS)
        china_check = any(other_word in message_list for other_word in CHINA_WORDS)

        for i in range(len(message_list)):
            if message_list[i] in PRAISE_WORDS and message_list[i-1] in NEGATIONS:
                bad_word_check = True
            elif message_list[i] in FORBIDDEN_WORDS and message_list[i-1] in NEGATIONS:
                bad_word_check = False

        return bad_word_check, praise_word_check, china_check

    def choose_response(self, message, message_list, china_check, bad_word_check, praise_word_check):
        if china_check and bad_word_check: # Punish
            response = '🇨🇳 This message has been reported to The Ministry of State Security 🇨🇳\n🇨🇳 10 Credit Points Have Been Deducted From Your Balance 🇨🇳'
            self.credit_score_keeper.alter_creditscore(member=message.author.name, points=-10)
            return response
        elif china_check and praise_word_check and bad_word_check != True: # Reward
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
        
