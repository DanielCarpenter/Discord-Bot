import random


class SecretSanta:
    
    # retries = -1 infinite retrying on pairing, retries >=0 will retry pairing that many times 
    def __init__(self, group_name):
        self.participant_list = []
        self.previous_gifting_map = {}
        self.gifting_map = {}
        self.sent = []
        self.previous_giftee_weight = 0.0
        self.group = group_name
        self.tries = -1
        self.success = False
        self.weight_function = weighted_by_relative_percent


    def addPerson(self, person):
        if isinstance(person, list):
            for user in person:
                if user not in self.participant_list:
                    self.participant_list.append(user)
        else:
            if person not in self.participant_list:
                self.participant_list.append(person)
    
    
    def remPerson(self, person):
        if isinstance(person, list):
            for user in person:
                if user in self.participant_list:
                    self.participant_list.remove(person)
        else:
            if person in self.participant_list:
                self.participant_list.remove(person)

    
    def setPrevious(self, gifter, previousGifteeList):
        if isinstance(previousGifteeList, list):
            self.previous_gifting_map[gifter] = [giftee for giftee in previousGifteeList]
        else:
            self.previous_gifting_map[gifter] = [previousGifteeList]


    def setPreviousChance(self, newChance):
        self.previous_giftee_weight = float(newChance)/100 


    def matching(self):
        isMatchingSuccessful = False
        if(self.tries is -1):
            while(not isMatchingSuccessful):
                isMatchingSuccessful = self.pair()
        else:
            count = 0
            while(not isMatchingSuccessful and count < self.tries):
                isMatchingSuccessful = self.pair()
                count = count + 1
        self.success = isMatchingSuccessful
        return isMatchingSuccessful


#  Returns False if pair fails to pair gifters with giftees, True if it was successful
#  Matching is used as the wrapper for a while loop on pair.
    def pair(self):
        # possible_giftees is everyone except the current person in the list of names
        possible_giftees = [person for person in self.participant_list]
        # list_of_available_giftees is a list of all persons who do not have a gifter, including the gifter if not gifted
        list_of_available_giftees = [person for person in self.participant_list]
        for person in self.participant_list:
            previous = self.previous_gifting_map.get(person)
            possible_giftees.remove(person)
            #giftee should always be overwritten before it gets placed in the gifting map.  If it does not a logic error has occurred
            giftee = 'Placeholder Value'
            # choices is the intersection of available giftees and the giftees that are possible
            choices = list(set(list_of_available_giftees)&set(possible_giftees))
            if len(choices) > 0:
                #  if they have a previous giftee, use the selected weight function to decrease chance of same giftee otherwise unweighted random choice.
                if previous and previous in choices:
                    giftee = self.weight_function(choices, previous, self.previous_giftee_weight)
                else:
                    giftee = unweighted(list_of_available_giftees=choices)
            else:
                return False
            list_of_available_giftees.remove(giftee)
            self.gifting_map[person] = self.participant_list[self.participant_list.index(giftee)]
            possible_giftees.append(person)
        return True


    def setWeightFunction(self, option):
        new_weight_function = weight_function_switch.get(option)
        if (new_weight_function):
            self.weight_function = new_weight_function
            return new_weight_function.__name__
        return False


#  For each Weight function listed below:
#  list_of_available_giftees are the IDs of every possible giftee for the current person that does not have a gifter yet, including the previousGifteeList if available.  Is a list of unique integers
#  previousGifteeList is the id of the previous giftee of the current person being matched.  Is a unique integer
#  {}_percent is the arbitrary value used to judge how strongly the previous Giftee is weighted. ranges from 0 to 1
#  returns the randomly selected ID from list_of_available_giftees


def weighted_by_relative_percent(list_of_available_giftees, previousGifteeList, relative_percent):
    availableGifteeCount = len(list_of_available_giftees)
    peopleToChooseFrom = availableGifteeCount - len(previousGifteeList)
    # calculates the weight of the previous year's giftee by multiplying the relative_percent value by
    previousGifteeChance = 100/peopleToChooseFrom * relative_percent
    # inserts the giftee from the previous year into the front of the list for ease of setting the weight correctly for the previousGifteeList.
    for previousGiftee in previousGifteeList:
        list_of_available_giftees.insert(0, list_of_available_giftees.pop(list_of_available_giftees.index(previousGiftee)))
    weights = [previousGifteeChance for pGiftee in previousGifteeList] + [((100 - previousGifteeChance * len(previousGifteeList)) / peopleToChooseFrom) for i in range(1,availableGifteeCount)]
    giftee = random.choices(list_of_available_giftees, k = 1, weights = weights)[0]
    return giftee

def weighted_by_absolute_percent(list_of_available_giftees, previousGifteeList, absolute_percent):
    availableGifteeCount = len(list_of_available_giftees)
    peopleToChooseFrom = availableGifteeCount - len(previousGifteeList)
    previousGifteeChance = 100 * absolute_percent
    # inserts the giftee from the previous year into the front of the list for ease of setting the weight correctly for this person.
    for previousGiftee in previousGifteeList:
        list_of_available_giftees.insert(0, list_of_available_giftees.pop(list_of_available_giftees.index(previousGiftee)))
    weights = [previousGifteeChance] + [((100-previousGifteeChance) / peopleToChooseFrom) for i in range(1,availableGifteeCount)]
    giftee = random.choices(list_of_available_giftees, k = 1, weights = weights)[0]
    return giftee

#  unweighted only has previousGifteeList and a {}_percent to comply with the structure of the other weight functions in the event of it being the weight_function of choice

def unweighted(list_of_available_giftees, previousGifteeList=None, placeholder_percent=None):
    giftee = random.choice(list_of_available_giftees)
    return giftee


#add additional options as new weight functions are added
weight_function_switch = {
    1: weighted_by_relative_percent,
    2: weighted_by_absolute_percent,
    3: unweighted
}