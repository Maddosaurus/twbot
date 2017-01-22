from sopel import module
from datetime import datetime, timedelta

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
    if(trigger.group(2) is None):
        bot.say('Usage: .twdetail #channelname')
        return
    channel = trigger.group(2)
    bot.say('Subcounter for ' + channel + ": " + str(len(bot.memory[channel].keys())))
    bot.say('Subs: ' + ", ".join(bot.memory[channel].keys())) # Debug output! This will be too much on regular basis

@module.require_privmsg
@module.require_admin
@module.commands('twdetail')
def twdetail(bot, trigger):
    if(trigger.group(2) is None):
        bot.say('Usage: .twdetail #channelname')
        return
    channel = trigger.group(2)
    if(not bot.memory.contains(channel)):
        bot.say('No stats found for this channel. Please wait for the first sub')
        return
    
    # FIXME: Freakin' UTC time stuff driving me crazy -_-
    dtnow = datetime.now()
    dtutc = datetime.utcnow()
    delta = dtnow -dtutc
    # done with the time blackmagic - just addin' this on the subdate. Dammit!

    bot.say('Preparing detailed stats for the channel: ' + channel)
    bot.say('Legend: [P] is an Amazon Prime Sub, [$] a paid sub')
    bot.say('______________________________________________')
    for key, values in bot.memory[channel].items():
        bot.say('[' + values['type'] + ']' + key +', Subbed: ' + (values['date'] + delta).strftime("%Y-%m-%d : %H:%M:%S")  + ' || Has been subbed for '+ str((datetime.now() - values['date']).days) + ' days, or roughly ' + str(int((datetime.utcnow() - values['date']).seconds/60)) + ' minutes')
    bot.say('______________________________________________')
    bot.say('For the completionzz: Output of twstats')
    twstats(bot, trigger)

# Helpers

def create_info(trigger, subtype):
    subber = trigger.split(" ")[0]
    ret = {}

    ret[subber] = {}
    ret[subber]['type'] = subtype
    ret[subber]['date'] = trigger.time

    return ret