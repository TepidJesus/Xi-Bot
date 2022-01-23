import json

class CreditKeeper():
    def __init__(self):
        try:
            with open('credit_scores.json', 'x'):
                print('No Existing JSON Data Found\nGenerating New File')
        except:
            print('Existing JSON Data Detected\nA New File Will Not Be Generated')

    def refresh_creditscores(self, guild_members):
        with open('credit_scores.json', 'r') as raw_json_scores:
            self.user_credit_scores = json.load(raw_json_scores)
            for member in guild_members:
                if member.name not in self.user_credit_scores.keys():
                    self.user_credit_scores[member.name] = 1000
                else:
                    continue   
        with open('credit_scores.json', 'w') as file:
            json.dump(self.user_credit_scores, file)

    def display_credit_scores(self):
        self.output_string = str()
        with open('credit_scores.json', 'r') as self.raw_json_scores:
            self.user_credit_scores = json.load(self.raw_json_scores)

            for member in self.user_credit_scores.keys():
                self.line_str = f'{member}: {self.user_credit_scores[member]} Points\n'
                self.output_string = self.output_string + self.line_str
        return self.output_string    

    def alter_creditscore(self, member, points):
        with open('credit_scores.json', 'r') as self.raw_json_scores:
            self.user_credit_scores = json.load(self.raw_json_scores)
            self.current_points = self.user_credit_scores[member]
            self.new_points = self.current_points + points
            self.user_credit_scores[member] = self.new_points
        with open('credit_scores.json', 'w') as file:
            json.dump(self.user_credit_scores, file)

    def get_credit_score(self, member_name):
        self.member_score = str()
        with open('credit_scores.json', 'r') as self.raw_json_scores:
            self.user_credit_scores = json.load(self.raw_json_scores)
            self.member_score = f'🇨🇳 You Have A Balance Of: {self.user_credit_scores[member_name]} Points 🇨🇳'
        return self.member_score

    def credit_check(self):
        with open('credit_scores.json', 'r') as raw_json_scores:
            self.user_credit_scores = json.load(raw_json_scores)
            for member in self.user_credit_scores.keys():
                if self.user_credit_scores[member.name] < 800:
                    pass
                elif self.user_credit_scores[member.name] < 600:
                    pass
                elif self.user_credit_scores[member.name] < 400:
                    pass
                elif self.user_credit_scores[member.name] < 200:
                    pass
                elif self.user_credit_scores[member.name] <= 0:
                    pass
                else:
                    continue