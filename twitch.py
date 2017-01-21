from sopel import module
import datetime

@module.rule('(\w*) just subscribed with Twitch Prime!')
def prime(bot, trigger):
    if(not bot.memory.contains(trigger.sender)):
        bot.memory[trigger.sender] = {}
    bot.say('Found a Prime Subscriber! -> ' + trigger.split(" ")[0], 'maddosaurus')
    bot.memory[trigger.sender].update(create_info(trigger, 'P'))

@module.rule('(\w*) just subscribed!')
def paid(bot, trigger):
    bot.say('Got a Paid Subscriber! -> ' + trigger.split(" ")[0], 'maddosaurus')
    bot.memory[trigger.sender].update(create_info(trigger, '$'))

@module.commands('twstats')
def twstats(bot, trigger):
    if(not trigger.admin):
        bot.say('Sorry. I am only answering my admins this question.')
        return
    channel = trigger.group(2)
    bot.say('Hey there! Now the subcounter for the channel: ' + channel)
    bot.say('Subcounter for ' + channel + ": " + str(len(bot.memory[channel].keys())))
    bot.say('Subs: ' + ", ".join(bot.memory[channel].keys()))

@module.commands('twdetail')
def twdetail(bot, trigger):
    if(not trigger.admin):
        bot.say('Sorry. I am only answering my admins this question.')
        return
    channel = trigger.group(2)
    bot.say('Preparing detailed stats for the channel: ' + channel)
    bot.say('Legend: [P] is an Amazon Prime Sub, [$] a paid sub')
    for key, values in bot.memory[channel].items():
        bot.say('[' + values['type'] + ']' + key +', Subbed: ' + values['date'].strftime("%Y-%m-%d"))

# Helpers

def create_info(trigger, subtype):
    subber = trigger.split(" ")[0]
    ret = {}

    ret[subber] = {}
    ret[subber]['type'] = subtype
    ret[subber]['date'] = trigger.time

    return ret