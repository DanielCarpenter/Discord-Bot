class Person:
    def __init__(self, d_id, d_name): #add name and discord_map=None for test.py
        self.name = d_name
        self.id = d_id
        self.gifting = ''
        self.gifted = ''
    
    def __eq__(self, other):
        if hasattr(other, 'id'):
            return other.id == self.id
        if isinstance(other, str):
            return self.name == other
        if isinstance(other, int):
            return self.id == other
        if isinstance(other, Person):
            return self.id == other.id

    def __hash__(self):
        if hasattr(self, 'id'):
            return hash(self.id)
        return hash(self.name)
    
    def __repr__(self):
        return str(self.name)



        
