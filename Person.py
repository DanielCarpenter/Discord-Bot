class Person:
    def __init__(self, discord_map): #add name and discord_map=None for test.py
        print(discord_map.display_name)
        if discord_map:
            self.disc = discord_map
            self.name = self.disc.display_name
            self.id = discord_map.id
            self.gifting = ''
            self.gifted = ''
        else:
            self.name = ''
            self.gifting = ''
            self.gifted = ''
        print(self.disc.display_name)
    
    def __eq__(self, other):
        if hasattr(other, 'id'):
            return other.id == self.id
        if isinstance(other, str):
            return self.name == other
        if isinstance(other, int):
            return self.id == other
        if isinstance(other, Person):
            return self.name == other.name

    def __hash__(self):
        if hasattr(self, 'id'):
            return hash(self.id)
        return hash(self.name)
    
    def __repr__(self):
        return str(self.name)



        
