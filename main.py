import discord, time, datetime, random, asyncio, json, os
gawaid = discord.Client()
@gawaid.event
async def on_ready():
    print('Logged in')
    print("I'm online and working")
    await gawaid.change_presence(activity = discord.Game(name = "with your auctions and giveaways"))
@gawaid.event
async def on_message(message):
    message.content = message.content.lower()
    if message.content.startswith('av test'):
        await message.channel.send('Hi dude')
    if message.content.startswith("av ghelp"):
        e = discord.Embed(colour = discord.Colour.teal())
        e.set_author(name = "Mr. DankAid")
        e.add_field(name = "Giveaways" , value = "`av gw <prize>` \nAnnounces your giveaway!", inline = False)
        e.add_field(name = "Donator Giveaways" , value = "`av dono gw <@donator> <prize>` \nAnnounces gaw with a request to thank donator!", inline = False)
        e.add_field(name = "Flash Giveaways" , value = "`av flash gw <prize>`", inline = False)
        e.add_field(name = "Disqualification" , value = "`av disqualify @someone` \nDisqualifies someone not following rules of an event!", inline = False)
        await message.channel.send(embed = e)
    if message.content.startswith('av disqualify'):
        sed = message.mentions[0]
        sedid = sed.id
        reason = message.content.replace('av disqualify', '')
        msg = str(reason.replace(f"<@!{sedid}>", ''))
        muted_role = discord.utils.get(message.guild.roles, name="Disqualified from event")
        disx_embed = discord.Embed(title = f'Disqualified {sed.name}', colour = discord.Colour.red())
        disx_embed.add_field(name = 'Reason', value = msg, inline = False)
        disx_embed.add_field(name = 'Mute Duration', value = '5 minutes')
        await message.channel.send(embed=disx_embed)
        await sed.send(f"You were disqualified from the event in {message.guild.name} for{msg}. \nIf you feel this wasn't fair, sorry. But don't DM the host, they are busy with the event.\nAnd you will be automatically unmuted from the events channel within 5 minutes, so if the event is still going on... You can participate!\n||**NOTE:** If, even after 10 minutes, you see that you have the `disqualified from events` role, DM a mod/admin and they'll take care.||")
        await sed.add_roles(muted_role)
        await message.delete()
        await asyncio.sleep(300)
        await sed.remove_roles(muted_role)
    if message.content.startswith('av gw'):
        await message.delete()
        pr = message.content.replace('av gw ', '')
        ping_role = discord.utils.get(message.guild.roles, name = 'Giveaway Ping')
        await message.channel.send(f"{ping_role.mention} Giveaway by {message.author.mention} of {pr}")

    if message.content.startswith('av dono gw'):
        await message.delete()
        per = message.mentions[0]
        pr = message.content.replace('av dono gw ', '')
        rpr = str(pr.replace(f'<@!{per.id}>', ''))
        ping_role = discord.utils.get(message.guild.roles, name = 'Giveaway Ping')
        await message.channel.send(f"{ping_role.mention} Donation by the legendary {per.mention} of**{rpr}**, thank in chat or reroll")
        
    if message.content.startswith('av flash gw'):
        await message.delete()
        pr = message.content.replace('av flash gw ', '')
        ping_role = discord.utils.get(message.guild.roles, name = 'Giveaway Ping')
        await message.channel.send(f"{ping_role.mention} Incoming flash giveaway by of {pr} by {message.author.mention}! Be ready!")

    if message.content.startswith('av blacklist'):
        user = message.mentions[0]
        userid = user.id
        rpr = str(message.content.replace(f'<@!{userid}>', ''))
        no_time = str(rpr.replace('av blacklist', ''))
        if 's' in no_time:
            t = no_time.strip('s')
            t = int(t)
            f_time = int(t)

        if 'h' in no_time:
            t = no_time.strip('h')
            t = int(t)
            f_time = int(t*3600)

        if 'm' in no_time:
            t = no_time.strip('m')
            t = int(t)
            f_time = int(t*60)

        if 'd' in no_time:
            t = no_time.strip('d')
            t = int(t)
            f_time = int(t*86400)

        a = discord.utils.get(message.guild.roles, name = 'Cant Trade')
        b = discord.utils.get(message.guild.roles, name = 'Disqualified from event')
        c = discord.utils.get(message.guild.roles, name = 'Cant gw')
        await user.add_roles(a)
        await user.add_roles(b)
        await user.add_roles(c)
        b_embed = discord.Embed(title = f'Blacklisted {user.name}', colour = discord.Colour.red())
        b_embed.add_field(name = 'Duration', value = f"`{no_time}`")
        await message.channel.send(embed = b_embed)
        await asyncio.sleep(f_time)
        await user.remove_roles(a, b, c)
        
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


    if message.content.startswith('av vouch') or message.content.startswith('avv') or message.content.startswith('av vouches'):
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
        
    if message.content.startswith('av auction'):
        pr1 = message.content.replace('av auction', '')
        pingrole = discord.utils.get(message.guild.roles, name = 'Auctions ping')
        await message.delete()
        await message.channel.send(f"{pingrole.mention}{pr1} \n||If you haven't read the rules yet, go do that first.||")

    if message.content.startswith('av middleman'):
        content = message.content.replace('av middleman', '')
        middlech = discord.utils.get(message.guild.channels, name = '├│🦺│midman-req')
        midrole = discord.utils.get(message.guild.roles, name = 'Middle Man')
        m_e = discord.Embed(colour = discord.Colour.blue())
        m_e.set_author(name = f"{message.author}" , icon_url = f"{message.author.avatar_url}")
        m_e.add_field(name = "Details" , value = content)
        m_e.add_field(name = "Channel", value = message.channel.mention, inline = False)
        m_e.set_footer(text = "Get there ASAP!")
        await middlech.send(midrole.mention)
        await middlech.send(embed = m_e)
        await message.delete()
        awa = await message.channel.send('A request has been sent! A middleman will be here soon!')
        await asyncio.sleep(5)
        await awa.delete() 
#custom responses on request
    if '775198018441838642' in str(message.content):
        if message.author.bot == True:
            return
        emote = '<a:pingrage:799132559807610880>'
        await message.add_reaction(emote)
        pingem = discord.Embed(title = 'Pinging the Messiah?', colour = discord.Colour.red())
        pingem.add_field(name = 'He is a co-owner here you know...', value = 'If you have pinged for no reason.... <a:ban:790094405125013504>')
        pingem.set_footer(text = 'Good luck appealing!')
        x = await message.channel.send(embed=pingem)
        await asyncio.sleep(5)
        await x.delete()
    if 'messiah' in message.content:
        await message.add_reaction('<a:coolpika:790186095467560990>')

    if '750755612505407530' in str(message.content):
        if message.author.bot == True:
            return
        emote = '<a:pingrage:799132559807610880>'
        await message.add_reaction(emote)
        pingem = discord.Embed(title = 'Skull Crusher was pinged!', colour = discord.Colour.red())
        pingem.add_field(name = 'Umm....', value = 'If you have pinged for no reason.... <a:ban:790094405125013504>')
        pingem.set_footer(text = 'Good luck appealing!')
        x = await message.channel.send(embed=pingem)
        await asyncio.sleep(5)
        await x.delete()
    if 'skull crusher' in message.content:
        await message.add_reaction('<a:coolpika:790186095467560990>')

    
    if '579905582778155008' in str(message.content):
        if message.author.bot == True:
            return
        emote = '<a:catrage:799153167458762782>'
        await message.add_reaction(emote)
        pingem = discord.Embed(title = 'Pinging Levi?', colour = discord.Colour.red())
        pingem.add_field(name = 'He is a co-owner here you know...', value = 'If you have pinged for no reason.... <a:ban:790094405125013504>')
        pingem.set_footer(text = 'Good luck appealing!')
        x = await message.channel.send(embed=pingem)
        await asyncio.sleep(5)
        await x.delete()
    if "levi'" in message.content or "levi" in message.content:
        await message.add_reaction('<a:coolpika:790186095467560990>')

    if '746904488396324864' in str(message.content):
        if message.author.bot == True:
            return
        emote = '<a:catvibe:799215448763531294>'
        await message.add_reaction(emote)
        pingem = discord.Embed(title = 'Full Counter! :crossed_swords:', colour = discord.Colour.red())
        x = await message.channel.send(embed=pingem)
        await asyncio.sleep(5)
        await x.delete()
    if "meliodas" in message.content:
        await message.add_reaction('<a:catvibe:799215448763531294>')

gawaid.run('Nzk4ODE2MTAwNjI3Nzc1NTI5.X_6hdw.UbM03OmqDkAPtZCsLNL8Z1Zy-cw')
