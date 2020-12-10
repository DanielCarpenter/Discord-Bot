from SecretSanta import SecretSanta
from Person import Person

class SecretSantaManager:
    def __init__(self):
        self.SecretSantaSessions = {}

    def get_ss_instance(self, guild_id):
        if not self.SecretSantaSessions.get(guild_id):
            self.SecretSantaSessions[guild_id] = SecretSanta(guild_id)
        return self.SecretSantaSessions.get(guild_id)
    
    def get_ss_by_display_name(self, gifter, giftee_dn):
        for instance in self.SecretSantaSessions.values():
            if instance.gifting_map.get(instance.names[instance.names.index(gifter.id)]).name == giftee_dn:
                print("returned instance")
                return instance
        print("None returned")
        return None