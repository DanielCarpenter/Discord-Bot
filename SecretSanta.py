from Person import Person
import random
import copy
import json
import datetime
import os

class SecretSanta:
    
    def __init__(self, guild_id):
        self.names = []
        self.previous = {}
        self.gifting_map = {}
        self.sent = []
        self.percentOfEqualChance = 0.1
        self.success = False
        self.guild = guild_id
    
    def addPerson(self, person):
        if isinstance(person, list):
            for user in person:
                if user in self.names:
                    continue
                else:
                    self.names.append(Person(user.id, user.display_name))
        else:
            dude = Person(person.id, person.display_name)
            if person not in self.names:
                self.names.append(dude)
            return dude

    
    def updatePrevious(self, gifter, giftee):
        self.previous[gifter.id] = giftee.id
    
    def updateSent(self, giftee):
        if giftee not in self.sent and giftee in self.gifting_map.values():
            self.sent.append(self.names[self.names.index(giftee)])
            with open("{}/{}/sent.json".format(self.guild, datetime.date.today().year), 'w') as fp:
                save_file = [person.id for person in self.sent]
                json.dump(save_file, fp)
                fp.close()


    def setPreviousChance(self, newChance): #unused, might implement later.
        self.percentOfEqualChance = float(newChance)/100 
    
    def save(self, guild_id):
        with open("{}/{}/names.json".format(guild_id, datetime.date.today().year), 'w') as fp:
            save_file = {gifter.name:giftee.name for (gifter, giftee) in self.gifting_map.items()}
            json.dump(save_file, fp)
            fp.close()
        with open("{}/{}/ids.json".format(guild_id, datetime.date.today().year), 'w') as fp:
            save_file = {gifter.id:giftee.id for (gifter, giftee) in self.gifting_map.items()}
            json.dump(save_file, fp)
            fp.close()

    def load(self, guild_id):
        current_year = datetime.date.today().year 
        if os.path.isfile("{}/{}/sent.json".format(guild_id, current_year)):
            with open("{}/{}/sent.json".format(guild_id, datetime.date.today().year)) as sent_list:
                data = sent_list.read()
                sent_list.close()
                self.sent = json.loads(data)
        if os.path.isdir("{}/{}/".format(guild_id, current_year-1)):
            with open("{}/{}/ids.json".format(guild_id, current_year)) as previous_map:
                data = previous_map.read()
                previous_map.close()
                self.previous = json.loads(data)
        if os.path.isdir("{}/{}/".format(guild_id, current_year)):
            with open("{}/{}/ids.json".format(guild_id, current_year)) as gifting_map:
                data = gifting_map.read()
                gifting_map.close()
            with open("{}/{}/names.json".format(guild_id, current_year)) as gifting_names:
                names_data = gifting_names.read()
                gifting_names.close()
            return json.loads(data), json.loads(names_data)
        
        return None

    def pair(self):
        success = True
        peopleToChooseFrom = len(self.names) - 2
        chanceForPrevious = 100/peopleToChooseFrom * self.percentOfEqualChance
        x = chanceForPrevious
        possible_recievers = [ person.id for person in self.names]
        not_recieved = [person.id for person in self.names]
        for person in self.names:
            previous = self.previous.get(person)
            possible_recievers.remove(person.id)
            choices = list(set(not_recieved)&set(possible_recievers))
            if previous and previous in choices:
                not_recieved.insert(0, not_recieved.pop(not_recieved.index(previous)))
                if len(choices) > 0:
                    weights = [x] + [((100-x) / (len(choices) - 1)) for i in range(1,len(choices))]
                    giftee = random.choices(choices, k = 1, weights = weights)[0]
                    self.gifting_map[person] = self.names[self.names.index(giftee)]
                    not_recieved.remove(giftee)
                    possible_recievers.append(person.id)
                else:
                    print("matchmaking failed, rematching")
                    self.pair()
                    success = False
                    break
            else:
                if len(choices) > 0:
                    giftee = random.choice(choices)
                    self.gifting_map[person] = self.names[self.names.index(giftee)]
                    not_recieved.remove(giftee)
                    possible_recievers.append(person.id)
                else:
                    print("matchmaking failed, rematching")
                    self.pair()
                    success = False
                    break
        if success:
            print("Success")
            self.success = True

                


            
    

            