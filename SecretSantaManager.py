from SecretSanta import SecretSanta
from Person import Person
import os
import pathlib
import json
import datetime

class SecretSantaManager:
    def __init__(self):
        self.SecretSantaSessions = {}

    def get_ss_instance(self, group_name):
        if not self.SecretSantaSessions.get(group_name):
            self.SecretSantaSessions[group_name] = SecretSanta(group_name)
            self.load_previous_pairings_history(group_name)
        return self.SecretSantaSessions.get(group_name)
    
    
    def enroll(self, group_name, people):
        if isinstance(people, list):
            self.get_ss_instance(group_name).addPerson([person.id for person in people])
        else:
            self.get_ss_instance(group_name).addPerson(people.id)
    
    
    def remove(self, group_name, people):
        if isinstance(people, list):
            self.get_ss_instance(group_name).remPerson([person.id for person in people])
        else:
            self.get_ss_instance(group_name).remPerson(people.id)
    

    def setPrevious(self, group_name, gifter, people):
        if isinstance(people, list):
            self.get_ss_instance(group_name).setPrevious(gifter, [person.id for person in people])
        else:
            self.get_ss_instance(group_name).setPrevious(gifter, people.id)

    
    def load_previous_pairings_history(self, group_name, prior_pairings_to_load=1):
        current_year = datetime.date.today().year 
        instance = self.get_ss_instance(group_name)
        instance.previous_gifting_map = {}
        for year in range(current_year - prior_pairings_to_load, current_year):
            if os.path.isfile("data/{}/{}/ids.json".format(group_name, year)):
                with open("data/{}/{}/ids.json".format(group_name, year)) as previous_map:
                    data = previous_map.read()
                    previous_map.close()
                    temp_map = json.loads(data)
                    for gifter, giftee in temp_map.items():
                        if gifter in instance.previous_gifting_map:
                            instance.previous_gifting_map.get(int(gifter)).append(giftee)
                        else:
                            instance.previous_gifting_map.setdefault(int(gifter), [giftee])


    def matching(self, group_name):
        instance = self.get_ss_instance(group_name)
        if instance.matching():
            save_instance(instance.group, instance.gifting_map)
        return instance.success

    
        




def save(group, object_to_save, fileName, year):
    path = "data/{}/{}/".format(group, year)
    pathlib.Path(path).mkdir(parents=True, exist_ok=True)
    with open(path + "{}.json".format(fileName), 'w') as fp:
        json.dump(object_to_save, fp)
        fp.close()
    

def load(group, fileName, year):
    if os.path.isfile("data/{}/{}/{}.json".format(group, year, fileName)):
        with open("data/{}/{}/{}.json".format(group, year, fileName)) as file_to_load:
            data = file_to_load.read()
            file_to_load.close()
            return json.loads(data)
    return None


def save_instance(group, map):
    current_year = datetime.date.today().year 
    save_file = {gifter:giftee for (gifter, giftee) in map.items()}
    save(group, save_file, "ids", current_year)



def load_instance(self, instance):
    current_year = datetime.date.today().year 
    if os.path.isfile("data/{}/{}/{}.json".format(self.group, current_year, "ids")):
        with open("data/{}/{}/{}.json".format(self.group, current_year, "ids")) as file_to_load:
            data = file_to_load.read()
            file_to_load.close()
            instance.gifting_map = json.loads(data)


def updateSent(giftee, inst):
    if giftee not in inst.sent and giftee in inst.gifting_map.values():
        inst.sent.append(inst.participant_list[inst.participant_list.index(giftee)])
        with open("data/{}/{}/sent.json".format(inst.guild, datetime.date.today().year), 'w') as fp:
            save_file = [person.id for person in inst.sent]
            json.dump(save_file, fp)
            fp.close()
