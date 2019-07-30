import discord
from discord.ext import commands
import random
from bs_DND_spells import return_spell
from spell_fight import *

TOKEN = 'NjAxNDA3ODEyMTkwNjAxMjE2.XTB2yw.TUn6NHmWq-akHz-HHHbZnRE7yEU'

client = discord.Client()

@client.event
async def on_ready():
    members = client.get_all_members()
    print('We have logged in as {0.user}'.format(client))
    list_members = []
    for member in members:
        list_members.append(member)
    if not os.path.isfile('DND_player_data.csv'):
        init_players(list_members)

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    try:
        if message.content.startswith('!spell'):
            spell = message.content[7:]
            try:
                spell_data = return_spell(spell)
                string = ''
                for key in spell_data:
                    string += '**%s**: %s\n' % (key, spell_data[key])
                await message.channel.send(string)
            except:
                success = False
                spell_split = spell.split()
                for i in range(len(spell_split)):
                    try:
                        spell_str = ''
                        for j in range(0, i + 1):
                            spell_str += spell_split[j] + ' '
                        spell_str = spell_str[:len(spell_str)-1]
                        spell_data = return_spell(spell_str)
                        spell_info = ''
                        for k in range(i + 1, len(spell_split)):
                            spell_info += spell_split[k].capitalize() + ' '
                        spell_info = spell_info[:len(spell_info)-1]
                        await message.channel.send('**%s**: %s' % (spell_info, spell_data[spell_info]))
                        success = True
                        break
                    except:
                        pass
                if not success:
                    await message.channel.send('That is not a spell')
        elif message.content.startswith('!file'):
            spells = message.content[6:]
            list_spell_names = spells.split(',')
            for i, spell_name in enumerate(list_spell_names):
                if spell_name[0] == ' ':
                    list_spell_names[i] = list_spell_names[i][1:]
            list_spell_names.sort()
            list_spells = []
            list_cantrips = []
            for spell_name in list_spell_names:
                spell_data = return_spell(spell_name)
                if spell_data['Spell Level'] == 'Cantrip':
                    list_cantrips.append(spell_data)
                else:
                    list_spells.append(spell_data)

            list_of_lists = [[], [], [], [], [], [], [], [], [], []]

            for spell in list_spells:
                list_of_lists[int(spell['Spell Level']) - 1].append(spell)

            mes = 'Cantrips:\n\n'
            for cantrip in list_cantrips:
                if len(list_cantrips) == 0:
                    break
                for key in cantrip:
                    mes += '%s: %s\n' % (key, cantrip[key])
                mes += '\n'

            mes += 'Spells:\n'

            for i, li in enumerate(list_of_lists):
                if len(li) == 0:
                    continue
                if i is 1:
                    mes += '\n2nd Level Spells:\n'
                elif i is 2:
                    mes += '\n3rd Level Spells:\n'
                else:
                    mes += '\n%dth Level Spells:\n' % (i +1)
                for spell in li:
                    for key in spell:
                        mes += '%s: %s\n' % (key, spell[key])
                    mes += '\n'
            f = open('DND_spell_%s.doc' % (message.author), 'w+')
            f.write(mes)
            f.close()
            dis_file = discord.File('DND_spell_%s.doc' % (message.author))
            await message.channel.send(file=dis_file)
        elif message.content.startswith('!attack'):
            text = message.content[11:].split()
            att_id = text[0]
            att_id = att_id[:-1]
            spell = ''
            for i in range(1, len(text)):
                spell += text[i].capitalize() + ' '
            spell = spell[:-1]
            damage, att_roll = attack(spell)
            if att_roll == 20:
                damage *= 2
            user = client.get_user(int(att_id))
            attacker = message.author
            mention_id = '<@' + att_id + '>'
            attacker_alive = True
            r = csv.reader(open('DND_player_data.csv'))
            lines = list(r)

            f = open('last_player.txt', 'r')
            last_player = f.read()

            last = False
            if last_player == str(message.author):
                await message.channel.send('You cannot make two actions in a row')
                last = True
            last_player = message.author
            with open('last_player.txt', 'w') as fi:
                fi.write(str(last_player))

            for stats in lines:
                if str(stats[0]) == str(attacker) and not last:
                    if int(stats[5]) != 0 or int(stats[7]) != 0:
                        attacker_alive = False
                        await message.channel.send('You are dead or unstable and cannot make an attack')
                        
            for stats in lines:
                if str(stats[0]) == str(user) and attacker_alive and not last:
                   # if attacker == user:
                       # await message.channel.send('You cannot attack yourself dumbass')
                        #break
                    dead = int(stats[5])
                    if dead is not 0:
                        await message.channel.send('%s is dead and cannot be attacked' % mention_id)
                        break
                    hp = int(stats[1])
                    dsts = int(stats[3])
                    dstf = int(stats[4])
                    unconc = int(stats[7])
                    if hp <= 0 and dstf == 2:
                        await message.channel.send('%s now has 3 death saving throw fails and is now dead' % mention_id)
                        dstf += 1
                        dead = 1
                    elif hp <= 0 and unconc != 0:
                        dstf += 1
                        await message.channel.send('%s is at 0 health and a fail has been added to their death saving throws\n' % mention_id +
                            'Death Saving Throw Successes: %d\nDeath Saving Throw Fails: %d\n' % (dsts, dstf))
                    elif hp <= 0 and unconc == 0:
                        dstf += 1
                        unconc = 1
                        await message.channel.send('%s has been knocked unconcious again and has taken one death save fail' % mention_id)
                    else:
                        if att_roll < int(stats[6]):
                            await message.channel.send('The attack roll was %d and missed!' % (att_roll))
                            break
                        await message.channel.send('The attack roll was %d and hit!' % (att_roll))
                        if att_roll == 20:
                            await message.channel.send('C-C-C-CRITICAL HIT')
                        hp -= damage
                        if hp <= 0:
                            await message.channel.send('%d damage has been dealt and %s has been brought to 0 health and is now unconcious' % (damage,mention_id))
                            unconc = 1
                        else:
                            await message.channel.send('%d damage has been dealt to %s and is now at %d/100 health' % (damage, mention_id, hp))
                    stats[1] = hp
                    stats[3] = dsts
                    stats[4] = dstf
                    stats[5] = dead
                    stats[7] = unconc
            writer = csv.writer(open('DND_player_data.csv', 'w'))
            writer.writerows(lines)
        elif message.content == ('!saveme'):
            user = message.author
            r = csv.reader(open('DND_player_data.csv'))
            lines = list(r)
            f = open('last_player.txt', 'r')
            last_player = f.read()

            last = False
            if last_player == str(message.author):
                await message.channel.send('You cannot make two actions in a row')
                last = True
            last_player = message.author
            with open('last_player.txt', 'w') as fi:
                fi.write(str(last_player))
            for stats in lines:
                if str(stats[0]) == str(user) and not last:
                    hp = int(stats[1])
                    dsts = int(stats[3])
                    dstf = int(stats[4])
                    dead = int(stats[5])
                    unconc = int(stats[7])
                    if dead == 1:
                        await message.channel.send('You are dead and thus cannot make a death saving throw')
                        break
                    if dead == 0 and unconc == 0:
                        await message.channel.send('You are alive and stable and thus cannot make a death saving throw')
                        break
                    saving_throw = roll_die('1d20')
                    if saving_throw < 10:
                        dstf += 1
                        if dstf == 3:
                            await message.channel.send('You rolled a %d and now have 3 death save fails. You are now dead' % saving_throw)
                            dead = 1
                            dstf = 0
                            dsts = 0
                            hp = 0
                        else:
                            await message.channel.send('You have rolled a %d and now have %d death save fail(s)' % (saving_throw, dstf))
                    else:
                        dsts += 1
                        if dsts == 3:
                            await message.channel.send('You rolled a %d and now have 3 death save successes. You have been stabilized' % saving_throw)
                            unconc = 0
                            dsts = 0
                            dstf = 0
                            hp = 0
                        else:
                            await message.channel.send('You rolled a %d and now have %d death save successes' % (saving_throw, dsts))

                    stats[1] = hp
                    stats[3] = dsts
                    stats[4] = dstf
                    stats[5] = dead
                    stats[7] = unconc
            writer = csv.writer(open('DND_player_data.csv', 'w'))
            writer.writerows(lines)
        elif message.content.startswith('!heal'):
            text = message.content[9:]
            heal_id = text[:-1]
            to_heal = client.get_user(int(heal_id))
            mention_id = '<@' + heal_id + '>'
            r = csv.reader(open('DND_player_data.csv'))
            lines = list(r)
            f = open('last_player.txt', 'r')
            last_player = f.read()

            last = False
            if last_player == str(message.author):
                await message.channel.send('You cannot make two actions in a row')
                last = True
            last_player = message.author
            with open('last_player.txt', 'w') as fi:
                fi.write(str(last_player))

            for stats in lines:
                if str(stats[0]) == str(to_heal) and not last:
                    hp = int(stats[1])
                    dsts = int(stats[3])
                    dstf = int(stats[4])
                    dead = int(stats[5])
                    unconc = int(stats[7])
                    if dead == 1:
                        await message.channel.send('Sorry no heal he ded')
                    elif message.author == to_heal and (unconc == 1 or dead == 1):
                        await message.channel.send('You are dead/unconcious and cannot heal yourself')
                    elif dead == 0 and unconc == 1:
                        dsts += 1
                        if dsts == 3:
                            await message.channel.send('%s has 3 death save successes and is now stabilized' % mention_id)
                            hp = 0
                            dsts = 0
                            dstf = 0
                            unconc = 0
                        else:
                            await message.channel.send('%s now has %d death save successes!' % (mention_id, dstf))
                    elif hp == 100:
                        await message.channel.send('%s is already at full health, goddamn idiots' % mention_id)
                    else:
                        heal = roll_die('4d4') + 1
                        hp += heal
                        if hp > 100:
                            hp = 100
                        await message.channel.send('%s has been healed for %d health and is at %d/100 health' % (mention_id, heal, hp))
                    stats[1] = hp
                    stats[3] = dsts
                    stats[4] = dstf
                    stats[5] = dead
                    stats[7] = unconc
            writer = csv.writer(open('DND_player_data.csv', 'w'))
            writer.writerows(lines)
        elif message.content == '!help dsb':
            f = open('dsb.txt', 'r')
            text = f.read()
            await message.channel.send(text)


    except Exception as e:
        print(repr(e))
        pass



client.run(TOKEN)