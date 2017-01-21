from sopel import module
from datetime import datetime, timedelta

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
    bot.say('Subcounter for ' + channel + ": " + str(len(bot.memory[channel].keys())))
    bot.say('Subs: ' + ", ".join(bot.memory[channel].keys()))

@module.commands('twdetail')
def twdetail(bot, trigger):
    if(not trigger.admin):
        bot.say('Sorry. I am only answering my admins this question.')
        return
    channel = trigger.group(2)
    bot.say('Preparing detailed stats for the channel: ' + channel)
    bot.say('Legend: [P] is an Amazon Prime Sub, [$] a paid sub - WARN: Sub Hours are note calculated correctly ATM!')
    bot.say('______________________________________________')
    for key, values in bot.memory[channel].items():
        bot.say('[' + values['type'] + ']' + key +', Subbed: ' + values['date'].strftime("%Y-%m-%d : %H:%M:%S") + 'Has been subbed for '+ str((datetime.now() - values['date']).days) + ' days and ' + str((datetime.now() - values['date']).seconds/3600) + ' hours')
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