from sopel import module
from datetime import datetime

@module.rule('(\w*) just subscribed with Twitch Prime!')
def prime(bot, trigger):
    if(not bot.memory.contains(trigger.sender)):
        bot.memory[trigger.sender] = {}
    bot.say('['+ trigger.sender +']: Found a Prime Subscriber! -> ' + trigger.split(" ")[0], 'maddosaurus')
    bot.memory[trigger.sender].update(create_info(trigger, 'P'))

@module.rule('(\w*) just subscribed!')
def paid(bot, trigger):
    if(not bot.memory.contains(trigger.sender)):
        bot.memory[trigger.sender] = {}
    bot.say('['+ trigger.sender +']: Got a Paid Subscriber! -> ' + trigger.split(" ")[0], 'maddosaurus')
    bot.memory[trigger.sender].update(create_info(trigger, '$'))


@module.require_privmsg
@module.require_admin
@module.commands('twstats')
def twstats(bot, trigger):
    channel = trigger.group(2)
    if(trigger.group(2) is None):
        bot.say('Usage: .twstats #channelname - Print stat overview for given channel')
        return
    if(not bot.memory.contains(channel)):
        bot.say('No stats found for this channel. Please wait for the first sub')
        return
    
    bot.say('Eyeballing subs for ' + channel + ": ")
    bot.say(buildStats(bot, channel)) 

@module.require_privmsg
@module.require_admin
@module.commands('twsubs')
def twsubs(bot, trigger):
    channel = trigger.group(2)
    if(trigger.group(2) is None):
        bot.say('Usage: .twsubs #channelname - list *all* subscribers of the given channel. Be warned! This may be big output!')
        return
    if(not bot.memory.contains(channel)):
        bot.say('No stats found for this channel. Please wait for the first sub')
        return
    
    bot.say('Listing all subs for channel ' + channel)
    bot.say(buildPrint(bot, channel)) 


# Helpers

def create_info(trigger, subtype):
    subber = trigger.split(" ")[0]
    ret = {}

    ret[subber] = {}
    ret[subber]['type'] = subtype
    ret[subber]['date'] = trigger.time

    return ret

def buildPrint(bot, channel):
    subs = ""
    for key, values in bot.memory[channel].items():
        subs += '[' + values['type'] + ']' + key +'('+  values['date'].strftime("%Y-%m-%d") +'), '
    return subs

# Bear in mind! I'm eyeballing this right here.
# You can sub in 3 oder 6 Month periods. I don't know how common this is.
# Also, the resub grace time is 30 days for your streak. 
# So it would be 60 days for a monthly sub!
# This stats will never be accurate, sorry :/
def buildStats(bot, channel):
    paid = 0
    prime = 0
    subs = 0
    for key, values in bot.memory[channel].items():
        if((datetime.now() - values['date']).days < 37):
           subs+=1
        else:
            break
        if (values['type'] == '$'):
            paid+=1
        elif (values['type'] == 'P'):
            prime+=1
    return "All in all: " + str(subs) + " -- Paid: "+ str(paid/subs*100) + "% (" + str(paid) + ") -- Twitch Prime: " + str(prime/subs*100) +"% ("+ str(prime) + ")"