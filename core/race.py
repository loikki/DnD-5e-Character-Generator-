import xml.etree.ElementTree as ET
from os.path import join

import core.proficiency as pfy

class RaceParser():
    def __init__(self):
        self.race_file = join('data', 'dnd', 'race.xml')
        self.root = ET.parse(self.race_file).getroot()

    def getRace(self, race):
        """ give the element structure of the required race
        :param str race: Name of the race
        :returns: ElementTree
        """
        for child in self.root:
            if child.get('name') == race:
                return child

    def getListRace(self):
        """ Gives a list of race
        :returns: List of race's name
        """        
        list_race = []
        for child in self.root:
            list_race.append(child.get('name'))
        return list_race

    def getDescription(self, race):
        """ Gives the description of the requested race
        :param str race: Name of the race
        :returns: String containing the full description
        """
        child = self.getRace(race)
        if child == None:
            return None
        description = ET.tostring(child.find('description'))
        ind_open = description.index("<description>")
        ind_close = description.index("</description>")
        description = description[ind_open+13:ind_close]
        return description

    def getChoice(self, race):
        """ Gives the possible choice to make for a race
        :param str race: Name of the race
        :returns: [(choice's tag, choice's list, number of choice), ...]
        """
        child = self.getRace(race)
        list_choice = []
        for choice in child.find('choice'):
            value = (choice.tag, [], int(choice.get('quantity')))
            for key in choice.findall('key'):
                value[1].append(key.get('name'))
            list_choice.append(value)
        return list_choice


    def getListSubrace(self, race):
        """ Gives a list of subrace possible for a given race
        :param str race: Name of the race
        :returns: [str] List of the subraces
        """
        list_subrace = []
        child = self.getRace(race)
        for subrace in child.findall('subrace'):
            list_subrace.append(subrace.get('name'))
        return list_subrace

    def getSubrace(self, race, subrace):
        """ Gives the element structure of the required subrace
        :param str race: Race name
        :param str subrace: Subrace name
        :returns: ElementTree containing the subrace
        """
        child = self.getRace(race)
        for race_child in child.findall('subrace'):
            if race_child.get('name') == subrace:
                return race_child

    def getSubraceDescription(self, race, subrace):
        """ Gives the description of the subrace
        :param str race: Race name
        :param str subrace: Subrace name
        :returns: String containing the full description
        """
        child = self.getSubrace(race, subrace)
        description = ET.tostring(child.find('description'))
        ind_open = description.index("<description>")
        ind_close = description.index("</description>")
        description = description[ind_open+13:ind_close]
        return description

    def getSubraceChoice(self, race, subrace):
        """ Gives the possible choice to make for a subrace
        :param str race: Race name
        :param str subrace: Subrace name
        :returns: [(choice's tag, choice's list, number of choice), ...]
        """
        child = self.getSubrace(race, subrace)
        list_choice = []
        child_test = child.find('choice')
        if child_test is None:
            return []
        for choice in child_test:
            value = (choice.tag, [], int(choice.get('quantity')))
            for key in choice.findall('key'):
                value[1].append(key.get('name'))
            list_choice.append(value)
        return list_choice

    def getTrait(self, race, subrace):
        """
        :param str race: Race name
        :param str subrace: Subrace name
        """
        if race is None:
            return
        child = self.getSubrace(race, subrace)
        list_trait = []
        child_test = child.find('trait')
        if child_test is not None:
            for trait in child_test:
                list_trait.append(trait)

        race_test = self.getRace(race).find('trait')
        if race_test is None:
            return list_trait

        for trait in race_test:
            list_trait.append(trait)
        return list_trait


class Race():
    def __init__(self):
        self.race_name = None
        self.subrace_name = None
        self.choice = []

    def setRace(self, name):
        self.race_name = name

    def setSubrace(self, name):
        self.subrace_name = name

    def write(self):
        print "Race: ", self.race_name
        print "Subrace: ", self.subrace_name
        print "Choices: ", self.choice
        print "Proficiency: "
        self.getProficiency(None)[0].write()


    def getProficiency(self, parser=None, proficiency=None):
        """
        :param RaceParser parser: If none, create one
        """
        if proficiency is None:
            proficiency = pfy.Proficiency()
        if parser is None:
            parser = RaceParser()

        race = parser.getRace(self.race_name)
        prof = race.find('proficiency')
        proficiency, diff = pfy.getLocalProficiency(prof, proficiency)

        if len(self.choice) > 0:
            choice = parser.getChoice(self.race_name)
            i = 0
            for value in choice:
                proficiency, temp = pfy.getChoiceProficiency(
                    proficiency, value, self.choice[i:i+value[2]])
                if not temp:
                    diff = temp
                i += value[2]

        return proficiency, diff
