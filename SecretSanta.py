from Person import Person
import random
import copy
import json
import datetime

class SecretSanta:
    
    def __init__(self):
        self.names = []
        self.previous = {}
        self.gifting_map = {}
        self.percentOfEqualChance = 0.1
        self.success = False
    
    def addPerson(self, person):
        if isinstance(person, list):
            for user in person:
                if user in self.names:
                    continue
                else:
                    self.names.append(Person(user))
        else:
            if person not in self.names:
                self.names.append(Person(person))
    
    def updatePrevious(self, gifter, giftee):
        self.previous[gifter.id] = giftee.id
    
    def setPreviousChance(self, newChance):
        self.percentOfEqualChance = float(newChance)/100
    
    def save(self):
        with open("{}.json".format(datetime.date.today().year), 'w') as fp:
            save_file = {gifter.name:giftee.name for (gifter, giftee) in self.gifting_map.items()}
            json.dump(save_file, fp)
            fp.close()
        with open("prev.json", 'w') as fp:
            save_file = {gifter.id:giftee.id for (gifter, giftee) in self.gifting_map.items()}
            json.dump(save_file, fp)
            fp.close()
    


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
            print(self.gifting_map)
            self.success = True
            self.save()

                


            
    

            