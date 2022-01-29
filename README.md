# Xi-bot
Xi Bot is my first attempt at a Discord bot. Written using Python and Discord.py. It was an excellent learning experience and taught me a great deal about interacting with API's and OOP. Xi Bot was a testing platform for my main bot project, Mi Bot, which will be a much more feature rich and more serious bot (In Development)

Xi bot now uses a Natural Language Processing model (Flair) to perform sentiment analysis on user messages.

Xi Bot is a parody of the social credit system currently in place in China under the CCP. Xi bot monitors the channels of servers its added to and polices what users are saying about China. Users are punished and rewarded using the credit score system. The bot has commands such as !server-ip, which will display the current IP of the server its hosted on (Used by me to show IP of my minecraft server to friends), !show-credit which displays the credit scores of all guild members and !my-credit which displays the users credit score who sent the command.

Credit Score data is stored in the credit_scores.json file. If the file is not present the first time the bot is run it will generate a blank json file.

Usage:
 - Add Xi Bot to your server using the O_auth2 link on the Discord Dev Portak
 - Add DISCORD_TOKEN and GUILD_NAME environment Variable
 - Run main.py()
