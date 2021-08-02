from SecretSanta import SecretSanta
from Person import Person
import os
import pathlib
import json

class SecretSantaManager:
    def __init__(self):
        self.SecretSantaSessions = {}

    def get_ss_instance(self, group_name):
        if not self.SecretSantaSessions.get(group_name):
            self.SecretSantaSessions[group_name] = SecretSanta(group_name)
        return self.SecretSantaSessions.get(group_name)

    
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


    def save_instance(self):
        current_year = datetime.date.today().year 
        save_file = {gifter.name:giftee.name for (gifter, giftee) in self.gifting_map.items()}
        self.save(save_file, "names", current_year)



    def load_instance(self, fileName, year):
        current_year = datetime.date.today().year 
        if os.path.isfile("data/{}/{}/{}.json".format(self.group, year, fileName)):
            with open("data/{}/{}/{}.json".format(self.group, year, fileName)) as file_to_load:
                data = file_to_load.read()
                file_to_load.close()
                self.sent = json.loads(data)
        for year in range(current_year - self.years_to_count_previous, current_year):
            if os.path.isdir("data/{}/{}/".format(self.group, year)):
                with open("data/{}/{}/ids.json".format(self.group, year)) as previous_map:
                    data = previous_map.read()
                    previous_map.close()
                    temp_map = json.loads.data()
                    for gifter, giftee in temp_map.items():
                        if gifter in self.previous_gifting_map:
                            self.previous_gifting_map.get(gifter).append(giftee)
                        else:
                            self.previous_gifting_map.setdefault(gifter, [giftee])
        if os.path.isdir("{}/{}/".format(self.group, current_year)):
            with open("data/{}/{}/ids.json".format(self.group, current_year)) as gifting_map:
                data = gifting_map.read()
                gifting_map.close()
            with open("data/{}/{}/names.json".format(self.group, current_year)) as gifting_names:
                names_data = gifting_names.read()
                gifting_names.close()
            current_year_ids = json.loads(data)
            current_year_names = json.loads(names_data)
            for (gifter, giftee), (gifter_name, giftee_name) in zip(current_year_ids.items(), current_year_names.items()):
                pgifter = Person(int(gifter), gifter_name)
                pgiftee = Person(int(giftee), giftee_name)
                self.gifting_map[pgifter] = pgiftee
                self.participant_list.append(pgifter)
        
        return self.participant_list

    
    def updateSent(self, giftee):
        if giftee not in self.sent and giftee in self.gifting_map.values():
            self.sent.append(self.participant_list[self.participant_list.index(giftee)])
            with open("data/{}/{}/sent.json".format(self.guild, datetime.date.today().year), 'w') as fp:
                save_file = [person.id for person in self.sent]
                json.dump(save_file, fp)
                fp.close()
