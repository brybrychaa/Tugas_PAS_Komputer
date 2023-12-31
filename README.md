﻿# Tugas_PAS_Komputer
Tadbot - Discord Bot
Overview
Tadbot is a simple Discord bot designed to enhance your server with various features and commands. It responds to greetings, farewells, and reacts to specific words in messages. Additionally, it has voice channel commands and moderation features such as kick and ban.

Setup
Make sure you have Python installed on your system.

Install the required libraries by running:

Copy code
pip install discord.py python-dotenv
Create a config.json file in the same directory as the bot script with the following structure:

json
Copy code
{
    "Token": "YOUR_DISCORD_BOT_TOKEN",
    "Prefix": "!"
}
Replace "YOUR_DISCORD_BOT_TOKEN" with your actual Discord bot token.

Run the bot script.

bash
Copy code
python your_bot_script.py
Commands
!hello: Greets the user with a welcome message.
!goodbye: Sends a farewell message.
!join: Joins the voice channel of the user who issued the command.
!leave: Leaves the voice channel.
!kick: Kicks a mentioned user from the server. (Moderator-only)
!ban: Bans a mentioned user from the server. (Moderator-only)
Events
on_member_join: Sends a welcome message when a new member joins.
on_member_remove: Sends a farewell message when a member leaves.
on_message: Reacts to specific words in messages and deletes messages containing the word "ugly."
on_reaction_add: Sends a message when a user adds or removes a reaction.
Notes
The bot uses a configuration file (config.json) to store the bot token and command prefix.
Make sure to customize the bot's activity in the on_ready event.
Moderation commands (!kick and !ban) require appropriate permissions.
Feel free to customize and expand upon this bot to suit your server's needs! If you have any questions or issues, please refer to the Discord.py documentation or contact the bot's developer.
