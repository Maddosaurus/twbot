from sopel import module
import datetime

@module.rule('(\w*) just subscribed with Twitch Prime!')
def prime(bot, trigger):
    if(not bot.memory.contains(trigger.sender)):
        bot.memory[trigger.sender] = {}
    bot.say('Found a Prime Subscriber! -> ' + trigger.split(" ")[0], 'maddosaurus')
    bot.memory[trigger.sender].update(create_info(trigger, 'prime'))

@module.rule('(\w*) just subscribed!')
def paid(bot, trigger):
    bot.say('Got a Paid Subscriber! -> ' + trigger.split(" ")[0], 'maddosaurus')
    bot.memory[trigger.sender].update(create_info(trigger, 'paid'))

@module.commands('twstats')
def twstats(bot, trigger):
    if(not trigger.admin):
        bot.say('Sorry. I am only answering my admins this question.')
        return
    channel = trigger.group(2)
    bot.say('Hey there! Now the subcounter for the channel: ' + channel)
    bot.say('Subcounter for ' + channel + ": " + str(len(bot.memory[channel].keys())))
    bot.say('Subs: ' + ", ".join(bot.memory[channel].keys()))


# Helpers

def create_info(trigger, subtype):
    subber = trigger.split(" ")[0]
    ret = {}

    ret[subber] = {}
    ret[subber]['type'] = subtype
    ret[subber]['date'] = trigger.time

    return ret