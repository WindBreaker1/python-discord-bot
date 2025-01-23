# Simple Test Discord Bot

> Add [Py Discord Bot](https://discord.com/oauth2/authorize?client_id=1330094955343122562&permissions=8&integration_type=0&scope=bot) to your server!

## Features

### Custom Embeds!

![embed-test-image](./images/embed-test.png)

### Random Anime Generator!

![random-anime-generator](./images/random-anime-test.png)

### Roll Hundreds of Dice!

![dice-test](./images/dice-test.png)

## Info

If your app scales past 100 servers you need to verify the app.

Every event type for the discord bot:

- on_ready()
- on_message(message)
- on_message_edit(before, after)
- on_message_delete(message)
- on_member_join(member)
- on_member_remove(member)
- on_member_update(before, after)
- on_guild_join(guild)
- on_guild_remove(guild)
- on_reaction_add(reaction, user)
- on_reaction_remove(reaction, user)

You can use `pip freeze > requirements.txt` to easily add all dependencies in a `requirements.text` file!

## Things to add

- [x] Random manga recommendation.
- [x] Allow slash commands on every server.
- [ ] Make the bot run continuously.
- [ ] Make a page on your website for the discord bot and link in the projects page.
- [ ] Beer drink minigame.
- [ ] Fishing minigame.
- [ ] RPG game.
- [ ] More complex slot machine.

## Bugs

- [x] Random Anime Character: about max character limit 1024
- [x] Random Anime Character: other bugs

## Resources

- Video I used for learning: [link](https://youtu.be/CHbN_gB30Tw?si=SAXOYRxdHmqhPtRj);
- To easilt work with your Discord Bot go to the official [developer site](https://discord.com/developers/applications);
- GitHub repo I used to find cool API's: [link](https://github.com/public-apis/public-apis?tab=readme-ov-file);
- Discord API: [DiscordPy](https://github.com/Rapptz/discord.py);
- Quotes Generator API: [pyquotegen](https://github.com/Armanidrisi/pyquotegen);
- Anime & Manga API: [Jikan](https://jikan.moe/);