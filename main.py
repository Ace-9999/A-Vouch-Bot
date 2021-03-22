import discord, time, datetime, random, asyncio, json, os
gawaid = discord.Client()
@gawaid.event
async def on_ready():
    print('Logged in')
    print("I'm online and working")
    await gawaid.change_presence(activity = discord.Game(name = "Counting Vouches"))
@gawaid.event
async def on_message(message):
    message.content = message.content.lower()
        
    def open_vouches(user):
        users = get_vouches_data
        with open('vouches.json', 'r') as f:
            users = json.load(f)

        if str(user.id) in users:
            return False

        else:
            users[str(user.id)] = {}
            users[str(user.id)]['vouches'] = 0

        with open('vouches.json', 'w') as f:
            json.dump(users, f)
        return True

    def get_vouches_data():
        with open('vouches.json', 'r') as f:
            users = json.load(f)

        return users


    if message.content.startswith('+1'):
        user = message.mentions[0]
        if user == message.author:
            await message.delete()
            x = await message.channel.send('Bruh you cant vouch for yourself. -_-')
            await asyncio.sleep(8)
            await x.delete()
            return
        if 'vouch' not in message.channel.name:
            await message.channel.send('Ay mate, you cant vouch here.')
            return
        open_vouches(user)
        open_vouches(message.author)
        users = get_vouches_data()
        users[str(user.id)]['vouches'] += 1
        await message.add_reaction('👍')
        with open('vouches.json', 'w') as f:
            users = json.dump(users, f)


    if message.content.startswith('/vouch') or message.content.startswith('/v') or message.content.startswith('/vouches'):
        open_vouches(message.author)
        if message.mentions != []:
            user = message.mentions[0]
        else:
            user = message.author
        open_vouches(user)
        users = get_vouches_data()
        vouches_amt = users[str(user.id)]['vouches']
        vem = discord.Embed(title = f"{user.name}'s vouches", colour = discord.Colour.blue())
        vem.add_field(name = "Vouches", value = f"  `{vouches_amt}`")
        if vouches_amt <= 20:
            vem.set_footer(text = "Not Trusted")
        if vouches_amt >= 20 and vouches_amt < 40:
            vem.set_footer(text = "Sort Of Trusted")
        if vouches_amt >= 40 and vouches_amt < 60:
            vem.set_footer(text = "Trusted")
            trustrole = discord.utils.get(message.guild.roles, name = 'Trusted Trader')
            await user.add_roles(trustrole)
        if vouches_amt >= 60:
            vem.set_footer(text = "Extremely Trusted")
        await message.channel.send(embed = vem)
      

gawaid.run('TOKEN')
