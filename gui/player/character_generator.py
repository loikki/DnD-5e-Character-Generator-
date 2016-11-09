# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Desktop/dnd.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
import random
from string import replace
import pickle
import os

from core.character import Character
import core.background as background
import core.race as race
import core.dnd_class as dnd_class
import core.character as character


try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

def rollDice(number_dice, type_dice):
    """ roll (number_dice)d(type_dice)
    :param int number_dice: Number of dice to roll
    :param int type_dice: Type of dice (d4, d6, ...)
    :returns: Value
    """
    value = 0
    for i in range(number_dice):
        value += random.randint(1,type_dice)
    return value

def rollAbility():
    """ Roll 4d6 and remove the lowest one.
    :return: Value of the rolls
    """
    rolls = [rollDice(1,6), rollDice(1,6), rollDice(1,6), rollDice(1,6)]
    min_ind = rolls.index(min(rolls))
    value = 0
    for i in range(len(rolls)):
        if i != min_ind:
            value += rolls[i]
    return value

def choiceLabel(title):
    """ Make the title nice
    :param str title: String to process
    :returns: str with a nice presentation
    """
    title = title.title()
    return replace(title, '_', ' ')

def getLanguages(allow_exotic=False):
    """ Return the list of available languages
    :param bool allow_exotic: Add the exotic languages to the list
    :returns: [str] List of all the available languages
    """
    languages = ['Common', 'Dwarvish', 'Elvish', 'Giant', 'Gnomish',
                 'Goblin', 'Halfling', 'Orc']
    if allow_exotic:
        languages.extend(['Abyssal', 'Celestial', 'Draconic', 'Deep Speech',
                          'Infernal', 'Primordial', 'Sylvan', 'Undercommon'])
    return languages

class CharacterGenerator(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(1005, 719)
        MainWindow.setWindowTitle("Loikki's Character Generator")

        # by default, no character is loaded
        self.character = character.Character()
        self.background_parser = background.BackgroundParser()
        self.race_parser = race.RaceParser()
        self.class_parser = dnd_class.DnDClassParser()
        
        # Create main tab
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.main_tab = QtGui.QTabWidget(self.centralwidget)
        self.main_tab.setObjectName(_fromUtf8("main_tab"))

        # create each individual tabs
        self.setupCharacterChoice()
        self.setupDescription()
        self.setupRace()
        self.setupClass()
        self.setupSpell()
        self.setupBackground()
        self.setupEquipment()
        self.setupNotes()
        self.setupStat()

        # create toolbar
        self.horizontalLayout.addWidget(self.main_tab)
        MainWindow.setCentralWidget(self.centralwidget)
        self.toolBar = QtGui.QToolBar(MainWindow)
        self.toolBar.setObjectName(_fromUtf8("toolBar"))
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.actionPrint = QtGui.QAction("Print", MainWindow)
        self.actionPrint.setObjectName(_fromUtf8("actionPrint"))
        self.actionPrint.triggered.connect(self.printCharacter)

        self.actionSave = QtGui.QAction("Save", MainWindow)
        self.actionSave.setObjectName(_fromUtf8("actionSave"))
        self.actionSave.triggered.connect(self.saveCharacter)
        
        self.actionQuit = QtGui.QAction("Quit", MainWindow)
        self.actionQuit.setObjectName(_fromUtf8("actionQuit"))
        self.actionQuit.triggered.connect(QtGui.qApp.quit)

        self.toolBar.addAction(self.actionSave)
        self.toolBar.addAction(self.actionPrint)
        self.toolBar.addAction(self.actionQuit)

    # ------------------ ACTION ---------------------------------------
    
    # tool bar
    def saveCharacter(self):
        pickle.dump(self.character, open(
            "data/saved/player/" + self.character.name + ".p", 'wb'))

    def printCharacter(self):
        print "Not implemented yet"

    # character choice tab
    def newCharacter(self):
        self.character = Character()
        
    def loadCharacter(self):
        character = self.tab0_character_choice.currentItem().text()
        for c in self.list_character:
            if character == c.name:
                character = c
                break
        self.character = character
        print "Need to update all the windows"
        
    # description tab
    def importImage(self):
        openfile = QtGui.QFileDialog.getOpenFileName(self.centralwidget) # Filename line
        self.tab1_img.setPixmap(QtGui.QPixmap(openfile))
        f = open(openfile, 'r') # New line
        self.character.image = f.read() # New line

    def removeImage(self):
        self.character.image = None
        self.tab1_img.clear()

    # --------------- Character Choice ------------------------------------

    def loadListCharacters(self):
        self.list_character = []
        character_directory = "data/saved/player/"
        for character_file in os.listdir(character_directory):
            self.list_character.append(pickle.load(
                open(character_directory + character_file, 'rb')))
        for character in self.list_character:
            self.tab0_character_choice.addItem(character.name)

    def printSummary(self):
        character = self.tab0_character_choice.currentItem().text()
        for c in self.list_character:
            if character == c.name:
                character = c
                break

        self.tab0_raceLineEdit.setText(character.race.subrace_name)
        self.tab0_classLineEdit.setText(character.dnd_class.class_name)
        self.tab0_specializationLineEdit.setText(
            character.dnd_class.specialization_name)
        self.tab0_backgroundLineEdit.setText(
            character.background.background_name)
        self.tab0_experienceLevelLineEdit.setText(
            str(character.experience))
        self.tab0_str_value.setText(str(character.getStrength()))
        self.tab0_dex_value.setText(str(character.getDexterity()))
        self.tab0_con_value.setText(str(character.getConstitution()))
        self.tab0_int_value.setText(str(character.getIntelligence()))
        self.tab0_wis_value.setText(str(character.getWisdom()))
        self.tab0_cha_value.setText(str(character.getCharisma()))

    # --------------- DESCRIPTION FUNCTIONS -------------------------------
        
    def rollAbilities(self):
        """ Roll 6 times 4d6 and remove the lowest one
        """
        roll = rollAbility()
        self.tab1_ability_value_1.setText(str(roll))
        roll = rollAbility()
        self.tab1_ability_value_2.setText(str(roll))
        roll = rollAbility()
        self.tab1_ability_value_3.setText(str(roll))
        roll = rollAbility()
        self.tab1_ability_value_4.setText(str(roll))
        roll = rollAbility()
        self.tab1_ability_value_5.setText(str(roll))
        roll = rollAbility()
        self.tab1_ability_value_6.setText(str(roll))
        self.character.write()

    def notableFeaturesChanged(self):
        features = self.tab1_features.toPlainText()
        self.character.notable_features = features

    def changeAbilityRoll(self):
        list_ability = [self.tab1_str_combo, self.tab1_dex_combo, self.tab1_con_combo,
                        self.tab1_int_combo, self.tab1_wis_combo, self.tab1_cha_combo]
        for combo in list_ability:
            combo.clear()
        self.changeAttributionAbility(None)

    def changeAttributionAbility(self, not_used):
        list_ability = [self.tab1_str_combo, self.tab1_dex_combo, self.tab1_con_combo,
                        self.tab1_int_combo, self.tab1_wis_combo, self.tab1_cha_combo]
        list_value = [self.tab1_ability_value_1.text(), self.tab1_ability_value_2.text(),
                      self.tab1_ability_value_3.text(), self.tab1_ability_value_4.text(),
                      self.tab1_ability_value_5.text(), self.tab1_ability_value_6.text()]
        for combo in list_ability:
            if combo.currentText() != '':
                list_value.remove(combo.currentText())
        for combo in list_ability:
            temp = combo.currentText()
            combo.clear()
            if temp != '':
                combo.addItem(temp)
            combo.addItem("")
            for i in range(len(list_value)):
                combo.addItem(list_value[i])
        
    # --------------- RACE FUNCTIONS --------------------------------------
    def changeRace(self, race):
        """ Action that will be done when the user change the race
        """
        self.tab2_race_description.setText(self.race_parser.getDescription(race))
        self.updateSubrace()
        self.character.race.setRace(race)

    def updateSubrace(self):
        """ Update the list of subrace
        """
        race = self.tab2_race_choice_combo.currentText()
        self.tab2_subrace_choice_combo.clear()
        for i in self.race_parser.getListSubrace(race):
            self.tab2_subrace_choice_combo.addItem(i)
        self.changeSubrace(self.tab2_subrace_choice_combo.currentText())
        
    def changeSubrace(self, subrace):
        race = self.tab2_race_choice_combo.currentText()
        self.tab2_subrace_description.setText(
            self.race_parser.getSubraceDescription(race, subrace))
        self.changeRaceTabChoice()
        self.character.race.setSubrace(subrace)

    def changeRaceTabChoice(self):
        """ Update the race choice widgets
        :param str background: race name
        """
        race = self.tab2_race_choice_combo.currentText()
        subrace = self.tab2_subrace_choice_combo.currentText()
        list_choice = self.race_parser.getChoice(race)
        list_choice.extend(self.race_parser.getSubraceChoice(race, subrace))
        sizePolicy = QtGui.QSizePolicy(
            QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)

        for i in range(len(self.tab2_choice_list)):
            self.tab2_choices_layout.removeWidget(self.tab2_choice_list[i])
            self.tab2_choice_list[i].deleteLater()

        j = -1
        self.tab2_choice_list = []
        for choice in list_choice:
            for i in range(choice[2]):
                j += 1
                label = QtGui.QLabel(choiceLabel(choice[0]), self.tab2)
                label.setSizePolicy(sizePolicy)
                label.setAlignment(
                    QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
                self.tab2_choices_layout.addWidget(label, int(j/4), j%4)
                self.tab2_choice_list.append(label)
                j += 1
                combo = QtGui.QComboBox(self.tab2)
                if choice[0] == 'language' and choice[1][0] == 'any':
                    choice = (choice[0], getLanguages())
                for i in choice[1]:
                    combo.addItem(i)
                self.tab2_choices_layout.addWidget(combo, int(j/4), j%4)
                self.tab2_choice_list.append(combo)

        if j < 3:
            while j<3:
                j += 1
                label = QtGui.QLabel("", self.tab2)
                label.setSizePolicy(sizePolicy)
                self.tab2_choices_layout.addWidget(label, int(j/4), j%4)
                self.tab2_choice_list.append(label)


    # --------------- CLASS FUNCTIONS --------------------------------------

    def changeClass(self, dnd_class):
        """ Action that will be done when the user change the class
        :param str dnd_class: class in the combo box
        """
        self.tab3_class_description.setText(self.class_parser.getDescription(dnd_class))
        self.updateSpecialization()
        self.character.dnd_class.class_name = dnd_class

    def updateSpecialization(self):
        """ Update the list of specialization
        """
        dnd_class = self.tab3_class_combo.currentText()
        self.tab3_specialization_combo.clear()
        for i in self.class_parser.getListSpecialization(dnd_class):
            self.tab3_specialization_combo.addItem(i)
        self.changeSpecialization(self.tab3_specialization_combo.currentText())
        
    def changeSpecialization(self, specialization):
        """ Action that will be done when the user change the specialization
        :param str specialization: specialization selected
        """
        dnd_class = self.tab3_class_combo.currentText()
        self.tab3_specialization_description.setText(
            self.class_parser.getSpecializationDescription(dnd_class, specialization))
        self.changeClassTabChoice()
        self.character.dnd_class.specialization_name = specialization

    def changeClassTabChoice(self):
        """ Update the class choice widgets
        """
        dnd_class = self.tab3_class_combo.currentText()
        specialization = self.tab3_specialization_combo.currentText()
        list_choice = self.class_parser.getChoice(dnd_class)
        list_choice.extend(self.class_parser.getSpecializationChoice(dnd_class, specialization))
        sizePolicy = QtGui.QSizePolicy(
            QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)

        for i in range(len(self.tab3_choice_list)):
            if (i == 0) or (i == len(self.tab3_choice_list)-1):
                self.tab3_choices_layout.removeItem(self.tab3_choice_list[i])
            else:
                self.tab3_choices_layout.removeWidget(self.tab3_choice_list[i])
                self.tab3_choice_list[i].deleteLater()

        self.tab3_choice_list = []

        spacer = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        self.tab3_choice_list.append(spacer)
        self.tab3_choices_layout.addItem(spacer)
        j = 0
        for choice in list_choice:
            for i in range(choice[2]):
                j += 1
                label = QtGui.QLabel(choiceLabel(choice[0]), self.tab3)
                label.setSizePolicy(sizePolicy)
                label.setAlignment(
                    QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
                self.tab3_choices_layout.addWidget(label, j, 0)
                self.tab3_choice_list.append(label)
                combo = QtGui.QComboBox(self.tab3)
                if choice[0] == 'language' and choice[1][0] == 'any':
                    choice = (choice[0], getLanguages())
                for i in choice[1]:
                    combo.addItem(i)
                self.tab3_choices_layout.addWidget(combo, j, 1)
                self.tab3_choice_list.append(combo)

        spacer = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        self.tab3_choice_list.append(spacer)
        self.tab3_choices_layout.addItem(spacer)

    # --------------- BACKGROUND FUNCTIONS ---------------------------------
        
    def changeBackground(self, background):
        """ action that will be done when the user change the background
        :param str background: New background
        """
        self.tab5_ideal_combo.clear()
        self.tab5_background_description.setText(
            self.background_parser.getDescription(background))
        perso_max = self.background_parser.getNumberPersonality(background)
        self.tab5_personality_spinbox_1.setMaximum(perso_max)
        self.tab5_personality_spinbox_2.setMaximum(perso_max)
        flaw_max = self.background_parser.getNumberFlaw(background)
        self.tab5_flaw_spinbox.setMaximum(flaw_max)
        bond_max = self.background_parser.getNumberBond(background)
        self.tab5_bond_spinbox.setMaximum(bond_max)
        for ideal in self.background_parser.getListIdeal(background):
            self.tab5_ideal_combo.addItem(ideal)
        self.changeBackgroundChoice(background)
        self.character.background.setBackgroundName(background)

    def changeIdealDescription(self, ideal):
        """ Update the text of the ideal
        :param str ideal: New Ideal
        """
        background = self.tab5_background_combo.currentText()
        self.tab5_ideal_description.setText(
            self.background_parser.getIdealDescription(background, ideal))
        self.character.background.setIdeal(ideal)

    def changePersonalityDescription(self, personality):
        """ Update the description text of the personality
        :param personality: Not used (present due to Qt)
        """
        background = self.tab5_background_combo.currentText()
        perso1 = self.tab5_personality_spinbox_1.value()
        perso2 = self.tab5_personality_spinbox_2.value()
        if perso1 == perso2:
            self.tab5_personality_description.setText(
                "Please choose two different personalities!")
            return
        self.character.background.setPersonality0(perso1)
        self.character.background.setPersonality1(perso2)
        perso1 = self.background_parser.getPersonalityDescription(
            background, perso1)
        perso2 = self.background_parser.getPersonalityDescription(
            background, perso2)
        text = "<p>" + perso1 + "</p> <p>" + perso2 + "</p>"
        self.tab5_personality_description.setText(text)

    def changeBackgroundChoice(self, background):
        """ Update the background choice widgets
        :param str background: Background name
        """
        list_choice = self.background_parser.getChoice(background)
        sizePolicy = QtGui.QSizePolicy(
            QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)

        for i in range(len(self.tab5_choice_list)):
            # delete spacer
            if i%3 == 0:
                self.horizontalLayout_33.removeItem(self.tab5_choice_list[i])
            # delete widget
            else:
                self.horizontalLayout_33.removeWidget(self.tab5_choice_list[i])
                self.tab5_choice_list[i].deleteLater()
                
        self.tab5_choice_list = []
        spacer = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.tab5_choice_list.append(spacer)
        self.horizontalLayout_33.addItem(spacer)
        for choice in list_choice:
            for i in range(choice[2]):
                label = QtGui.QLabel(choiceLabel(choice[0]), self.tab5_choice_layout)
                label.setSizePolicy(sizePolicy)
                label.setAlignment(
                    QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
                self.horizontalLayout_33.addWidget(label)
                self.tab5_choice_list.append(label)
                combo = QtGui.QComboBox(self.tab5_choice_layout)
                if choice[0] == 'language' and choice[1][0] == 'any':
                    choice = (choice[0], getLanguages())
                for i in choice[1]:
                    combo.addItem(i)
                self.horizontalLayout_33.addWidget(combo)
                self.tab5_choice_list.append(combo)
                spacer = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
                self.tab5_choice_list.append(spacer)
                self.horizontalLayout_33.addItem(spacer)
        
        
    def changeFlawDescription(self, flaw):
        """ Update the description of the flaw
        :param int flaw: value of the flaw
        """
        background = self.tab5_background_combo.currentText()
        self.tab5_flaw_description.setText(
            self.background_parser.getFlawDescription(background, flaw))
        self.character.background.setFlaw(flaw)

    def changeBondDescription(self, bond):
        """ Update the description of the bond
        :param int bond: value of the bond
        """
        background = self.tab5_background_combo.currentText()
        self.tab5_bond_description.setText(
            self.background_parser.getBondDescription(background, bond))
        self.character.background.setBond(bond)
        
    def fullRandomBackground(self):
        """ Choose randomly the background, personality, ideal, bond
        and flaw of the character
        """
        nber_background = len(self.background_parser.getListBackground())
        self.tab5_background_combo.setCurrentIndex(
            rollDice(1, nber_background) - 1)
        background = self.tab5_background_combo.currentText()
        self.changeBackground(background)
        self.randomPersonality()

    def randomPersonality(self):
        """ Choose the personality of the character (bond, flaw, ideal,
        personality)
        """
        background = self.tab5_background_combo.currentText()
        nber_perso = self.background_parser.getNumberPersonality(background)
        nber_flaw = self.background_parser.getNumberFlaw(background)
        nber_bond = self.background_parser.getNumberBond(background)
        nber_ideal = len(self.background_parser.getListIdeal(background))
        # bond
        self.tab5_bond_spinbox.setValue(rollDice(1, nber_bond))
        # flaw
        self.tab5_flaw_spinbox.setValue(rollDice(1, nber_flaw))
        # personality
        roll1 = rollDice(1, nber_perso)
        self.tab5_personality_spinbox_1.setValue(roll1)
        roll2 = rollDice(1, nber_perso - 1)
        if roll2 >= roll1:
            roll2 += 1
        self.tab5_personality_spinbox_2.setValue(roll2)
        # ideal
        self.tab5_ideal_combo.setCurrentIndex(rollDice(1, nber_ideal)-1)
        ideal = self.tab5_ideal_combo.currentText()
        self.changeIdealDescription(ideal)
        # alignment
        self.tab5_alignment_combo.setCurrentIndex(rollDice(1,9)-1)
        self.character.background.setAlignment(
            self.tab5_alignment_combo.currentText())
        
    # --------------------------- GUI ---------------------------------
        
    def setupCharacterChoice(self):
        # create tab
        self.tab0 = QtGui.QWidget()
        self.tab0.setObjectName(_fromUtf8("tab0"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.tab0)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))

        # create character choice tree
        self.tab0_character_choice_layout = QtGui.QVBoxLayout()
        self.tab0_character_choice_layout.setObjectName(_fromUtf8("tab0_character_choice_layout"))
        self.tab0_character_choice = QtGui.QListWidget(self.tab0)
        self.tab0_character_choice.currentRowChanged.connect(self.printSummary)
        self.tab0_character_choice.setSortingEnabled(False)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tab0_character_choice.sizePolicy().hasHeightForWidth())
        self.tab0_character_choice.setSizePolicy(sizePolicy)
        self.tab0_character_choice.setObjectName(_fromUtf8("tab0_character_choice"))
        # create and add an item into the list
        item = QtGui.QListWidgetItem()
        self.loadListCharacters()
        self.tab0_character_choice.addItem(item)
        # add the list
        self.tab0_character_choice_layout.addWidget(self.tab0_character_choice)

        # create buttons
        self.tab0_button_layout = QtGui.QHBoxLayout()
        self.tab0_button_layout.setObjectName(_fromUtf8("tab0_button_layout"))
        self.tab0_new_character = QtGui.QPushButton("New Character", self.tab0)
        self.tab0_new_character.clicked.connect(self.newCharacter)
        self.tab0_new_character.setObjectName(_fromUtf8("tab0_new_character"))
        self.tab0_button_layout.addWidget(self.tab0_new_character)
        self.tab0_choose_current = QtGui.QPushButton("Choose Current Character", self.tab0)
        self.tab0_choose_current.setObjectName(_fromUtf8("tab0_choose_current"))
        self.tab0_choose_current.clicked.connect(self.loadCharacter)
        self.tab0_button_layout.addWidget(self.tab0_choose_current)
        self.tab0_character_choice_layout.addLayout(self.tab0_button_layout)

        # create summary part
        self.horizontalLayout_2.addLayout(self.tab0_character_choice_layout)
        self.tab0_summary_layout = QtGui.QGroupBox("Summary", self.tab0)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tab0_summary_layout.sizePolicy().hasHeightForWidth())

        # create class/background/race part
        self.tab0_summary_layout.setSizePolicy(sizePolicy)
        self.tab0_summary_layout.setObjectName(_fromUtf8("tab0_summary_layout"))
        self.verticalLayout_17 = QtGui.QVBoxLayout(self.tab0_summary_layout)
        self.verticalLayout_17.setObjectName(_fromUtf8("verticalLayout_17"))
        self.tab0_img_background_layout = QtGui.QHBoxLayout()
        self.tab0_img_background_layout.setContentsMargins(-1, 0, -1, -1)
        self.tab0_img_background_layout.setObjectName(_fromUtf8("tab0_img_background_layout"))
        self.tab0_background_layout = QtGui.QFormLayout()
        self.tab0_background_layout.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.tab0_background_layout.setFormAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.tab0_background_layout.setObjectName(_fromUtf8("tab0_background_layout"))
        self.tab0_classLabel_2 = QtGui.QLabel("Class", self.tab0_summary_layout)
        self.tab0_classLabel_2.setObjectName(_fromUtf8("tab0_classLabel_2"))
        self.tab0_background_layout.setWidget(0, QtGui.QFormLayout.LabelRole, self.tab0_classLabel_2)
        self.tab0_classLineEdit = QtGui.QLineEdit(self.tab0_summary_layout)
        self.tab0_classLineEdit.setReadOnly(True)
        self.tab0_classLineEdit.setObjectName(_fromUtf8("tab0_classLineEdit"))
        self.tab0_background_layout.setWidget(0, QtGui.QFormLayout.FieldRole, self.tab0_classLineEdit)
        self.tab0_raceLineEdit = QtGui.QLineEdit(self.tab0_summary_layout)
        self.tab0_raceLineEdit.setReadOnly(True)
        self.tab0_raceLineEdit.setObjectName(_fromUtf8("tab0_raceLineEdit"))
        self.tab0_background_layout.setWidget(1, QtGui.QFormLayout.FieldRole, self.tab0_raceLineEdit)
        self.tab0_specializationLabel_2 = QtGui.QLabel("Specialization", self.tab0_summary_layout)
        self.tab0_specializationLabel_2.setObjectName(_fromUtf8("tab0_specializationLabel_2"))
        self.tab0_background_layout.setWidget(2, QtGui.QFormLayout.LabelRole, self.tab0_specializationLabel_2)
        self.tab0_specializationLineEdit = QtGui.QLineEdit(self.tab0_summary_layout)
        self.tab0_specializationLineEdit.setReadOnly(True)
        self.tab0_specializationLineEdit.setObjectName(_fromUtf8("tab0_specializationLineEdit"))
        self.tab0_background_layout.setWidget(2, QtGui.QFormLayout.FieldRole, self.tab0_specializationLineEdit)
        self.tab0_raceLabel = QtGui.QLabel("Race", self.tab0_summary_layout)
        self.tab0_raceLabel.setObjectName(_fromUtf8("tab0_raceLabel"))
        self.tab0_background_layout.setWidget(1, QtGui.QFormLayout.LabelRole, self.tab0_raceLabel)
        self.tab0_backgroundLabel = QtGui.QLabel("Background", self.tab0_summary_layout)
        self.tab0_backgroundLabel.setObjectName(_fromUtf8("tab0_backgroundLabel"))
        self.tab0_background_layout.setWidget(3, QtGui.QFormLayout.LabelRole, self.tab0_backgroundLabel)
        self.tab0_backgroundLineEdit = QtGui.QLineEdit(self.tab0_summary_layout)
        self.tab0_backgroundLineEdit.setReadOnly(True)
        self.tab0_backgroundLineEdit.setObjectName(_fromUtf8("tab0_backgroundLineEdit"))
        self.tab0_background_layout.setWidget(3, QtGui.QFormLayout.FieldRole, self.tab0_backgroundLineEdit)
        self.tab0_experienceLevelLabel = QtGui.QLabel("Experience (Level)", self.tab0_summary_layout)
        self.tab0_experienceLevelLabel.setObjectName(_fromUtf8("tab0_experienceLevelLabel"))
        self.tab0_background_layout.setWidget(4, QtGui.QFormLayout.LabelRole, self.tab0_experienceLevelLabel)
        self.tab0_experienceLevelLineEdit = QtGui.QLineEdit(self.tab0_summary_layout)
        self.tab0_experienceLevelLineEdit.setReadOnly(True)
        self.tab0_experienceLevelLineEdit.setObjectName(_fromUtf8("tab0_experienceLevelLineEdit"))
        self.tab0_background_layout.setWidget(4, QtGui.QFormLayout.FieldRole, self.tab0_experienceLevelLineEdit)

        # create image
        self.tab0_img_background_layout.addLayout(self.tab0_background_layout)
        self.tab0_img = QtGui.QLabel(self.tab0_summary_layout)
        self.tab0_img.setMaximumSize(QtCore.QSize(150, 150))
        self.tab0_img.setText(_fromUtf8(""))
        self.tab0_img.setPixmap(QtGui.QPixmap(_fromUtf8("/home/loikki/Downloads/test.jpeg")))
        self.tab0_img.setScaledContents(True)
        self.tab0_img.setObjectName(_fromUtf8("tab0_img"))
        self.tab0_img_background_layout.addWidget(self.tab0_img)

        # create ability layout
        self.verticalLayout_17.addLayout(self.tab0_img_background_layout)
        self.tab0_ability_layout = QtGui.QGridLayout()
        self.tab0_ability_layout.setObjectName(_fromUtf8("tab0_ability_layout"))
        self.tab0_dex_label = QtGui.QLabel("Dexterity", self.tab0_summary_layout)
        self.tab0_dex_label.setAlignment(QtCore.Qt.AlignCenter)
        self.tab0_dex_label.setObjectName(_fromUtf8("tab0_dex_label"))
        self.tab0_ability_layout.addWidget(self.tab0_dex_label, 0, 1, 1, 1)
        self.tab0_con_label = QtGui.QLabel("Constitution", self.tab0_summary_layout)
        self.tab0_con_label.setAlignment(QtCore.Qt.AlignCenter)
        self.tab0_con_label.setObjectName(_fromUtf8("tab0_con_label"))
        self.tab0_ability_layout.addWidget(self.tab0_con_label, 0, 2, 1, 1)
        self.tab0_int_label = QtGui.QLabel("Intelligence", self.tab0_summary_layout)
        self.tab0_int_label.setAlignment(QtCore.Qt.AlignCenter)
        self.tab0_int_label.setObjectName(_fromUtf8("tab0_int_label"))
        self.tab0_ability_layout.addWidget(self.tab0_int_label, 0, 3, 1, 1)
        self.tab0_wis_label = QtGui.QLabel("Wisdom", self.tab0_summary_layout)
        self.tab0_wis_label.setAlignment(QtCore.Qt.AlignCenter)
        self.tab0_wis_label.setObjectName(_fromUtf8("tab0_wis_label"))
        self.tab0_ability_layout.addWidget(self.tab0_wis_label, 0, 4, 1, 1)
        self.tab0_cha_label = QtGui.QLabel("Charisma", self.tab0_summary_layout)
        self.tab0_cha_label.setAlignment(QtCore.Qt.AlignCenter)
        self.tab0_cha_label.setObjectName(_fromUtf8("tab0_cha_label"))
        self.tab0_ability_layout.addWidget(self.tab0_cha_label, 0, 5, 1, 1)
        self.tab0_str_label = QtGui.QLabel("Strength", self.tab0_summary_layout)
        self.tab0_str_label.setAlignment(QtCore.Qt.AlignCenter)
        self.tab0_str_label.setObjectName(_fromUtf8("tab0_str_label"))
        self.tab0_ability_layout.addWidget(self.tab0_str_label, 0, 0, 1, 1)
        self.tab0_str_value = QtGui.QLabel("12", self.tab0_summary_layout)
        self.tab0_str_value.setAlignment(QtCore.Qt.AlignCenter)
        self.tab0_str_value.setObjectName(_fromUtf8("tab0_str_value"))
        self.tab0_ability_layout.addWidget(self.tab0_str_value, 1, 0, 1, 1)
        self.tab0_dex_value = QtGui.QLabel("10", self.tab0_summary_layout)
        self.tab0_dex_value.setAlignment(QtCore.Qt.AlignCenter)
        self.tab0_dex_value.setObjectName(_fromUtf8("tab0_dex_value"))
        self.tab0_ability_layout.addWidget(self.tab0_dex_value, 1, 1, 1, 1)
        self.tab0_con_value = QtGui.QLabel("9", self.tab0_summary_layout)
        self.tab0_con_value.setAlignment(QtCore.Qt.AlignCenter)
        self.tab0_con_value.setObjectName(_fromUtf8("tab0_con_value"))
        self.tab0_ability_layout.addWidget(self.tab0_con_value, 1, 2, 1, 1)
        self.tab0_int_value = QtGui.QLabel("16", self.tab0_summary_layout)
        self.tab0_int_value.setAlignment(QtCore.Qt.AlignCenter)
        self.tab0_int_value.setObjectName(_fromUtf8("tab0_int_value"))
        self.tab0_ability_layout.addWidget(self.tab0_int_value, 1, 3, 1, 1)
        self.tab0_wis_value = QtGui.QLabel("8", self.tab0_summary_layout)
        self.tab0_wis_value.setAlignment(QtCore.Qt.AlignCenter)
        self.tab0_wis_value.setObjectName(_fromUtf8("tab0_wis_value"))
        self.tab0_ability_layout.addWidget(self.tab0_wis_value, 1, 4, 1, 1)
        self.tab0_cha_value = QtGui.QLabel("11", self.tab0_summary_layout)
        self.tab0_cha_value.setAlignment(QtCore.Qt.AlignCenter)
        self.tab0_cha_value.setObjectName(_fromUtf8("tab0_cha_value"))
        self.tab0_ability_layout.addWidget(self.tab0_cha_value, 1, 5, 1, 1)
        self.verticalLayout_17.addLayout(self.tab0_ability_layout)

        # proficiencies
        self.tab0_proficiencies_layout = QtGui.QGroupBox("Proficiencies", self.tab0_summary_layout)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tab0_proficiencies_layout.sizePolicy().hasHeightForWidth())
        self.tab0_proficiencies_layout.setSizePolicy(sizePolicy)
        self.tab0_proficiencies_layout.setObjectName(_fromUtf8("tab0_proficiencies_layout"))
        self.horizontalLayout_42 = QtGui.QHBoxLayout(self.tab0_proficiencies_layout)
        self.horizontalLayout_42.setObjectName(_fromUtf8("horizontalLayout_42"))

        # saving throws
        self.tab0_saving_skill_layout = QtGui.QVBoxLayout()
        self.tab0_saving_skill_layout.setObjectName(_fromUtf8("tab0_saving_skill_layout"))
        self.tab0_saving_layout = QtGui.QGroupBox("Saving Throws", self.tab0_proficiencies_layout)
        self.tab0_saving_layout.setObjectName(_fromUtf8("tab0_saving_layout"))
        self.verticalLayout_30 = QtGui.QVBoxLayout(self.tab0_saving_layout)
        self.verticalLayout_30.setObjectName(_fromUtf8("verticalLayout_30"))
        self.tab0_1_saving = QtGui.QLabel("Strength", self.tab0_saving_layout)
        self.tab0_1_saving.setAlignment(QtCore.Qt.AlignCenter)
        self.tab0_1_saving.setObjectName(_fromUtf8("tab0_1_saving"))
        self.verticalLayout_30.addWidget(self.tab0_1_saving)
        self.tab0_2_saving = QtGui.QLabel("Wisdom", self.tab0_saving_layout)
        self.tab0_2_saving.setAlignment(QtCore.Qt.AlignCenter)
        self.tab0_2_saving.setObjectName(_fromUtf8("tab0_2_saving"))
        self.verticalLayout_30.addWidget(self.tab0_2_saving)
        self.tab0_saving_skill_layout.addWidget(self.tab0_saving_layout)

        # skills
        self.tab0_skill_layout = QtGui.QGroupBox("Skills", self.tab0_proficiencies_layout)
        self.tab0_skill_layout.setObjectName(_fromUtf8("tab0_skill_layout"))
        self.gridLayout_15 = QtGui.QGridLayout(self.tab0_skill_layout)
        self.gridLayout_15.setObjectName(_fromUtf8("gridLayout_15"))
        self.tab0_4_skill = QtGui.QLabel("Athletics", self.tab0_skill_layout)
        self.tab0_4_skill.setAlignment(QtCore.Qt.AlignCenter)
        self.tab0_4_skill.setObjectName(_fromUtf8("tab0_4_skill"))
        self.gridLayout_15.addWidget(self.tab0_4_skill, 1, 1, 1, 1)
        self.tab0_3_skill = QtGui.QLabel("Acrobatics", self.tab0_skill_layout)
        self.tab0_3_skill.setAlignment(QtCore.Qt.AlignCenter)
        self.tab0_3_skill.setObjectName(_fromUtf8("tab0_3_skill"))
        self.gridLayout_15.addWidget(self.tab0_3_skill, 1, 0, 1, 1)
        self.tab0_2_skill = QtGui.QLabel("Religion", self.tab0_skill_layout)
        self.tab0_2_skill.setAlignment(QtCore.Qt.AlignCenter)
        self.tab0_2_skill.setObjectName(_fromUtf8("tab0_2_skill"))
        self.gridLayout_15.addWidget(self.tab0_2_skill, 0, 1, 1, 1)
        self.tab0_5_skill = QtGui.QLabel("Insight", self.tab0_skill_layout)
        self.tab0_5_skill.setAlignment(QtCore.Qt.AlignCenter)
        self.tab0_5_skill.setObjectName(_fromUtf8("tab0_5_skill"))
        self.gridLayout_15.addWidget(self.tab0_5_skill, 2, 0, 1, 1)
        self.tab0_1_skill = QtGui.QLabel("Perception", self.tab0_skill_layout)
        self.tab0_1_skill.setAlignment(QtCore.Qt.AlignCenter)
        self.tab0_1_skill.setObjectName(_fromUtf8("tab0_1_skill"))
        self.gridLayout_15.addWidget(self.tab0_1_skill, 0, 0, 1, 1)
        self.tab0_6_skill = QtGui.QLabel("Survival", self.tab0_skill_layout)
        self.tab0_6_skill.setAlignment(QtCore.Qt.AlignCenter)
        self.tab0_6_skill.setObjectName(_fromUtf8("tab0_6_skill"))
        self.gridLayout_15.addWidget(self.tab0_6_skill, 2, 1, 1, 1)
        self.tab0_saving_skill_layout.addWidget(self.tab0_skill_layout)
        self.horizontalLayout_42.addLayout(self.tab0_saving_skill_layout)

        # Object proficiencies
        self.tab0_object_proficiency_layout = QtGui.QGroupBox("Objects", self.tab0_proficiencies_layout)
        self.tab0_object_proficiency_layout.setObjectName(_fromUtf8("tab0_object_proficiency_layout"))
        self.gridLayout_16 = QtGui.QGridLayout(self.tab0_object_proficiency_layout)
        self.gridLayout_16.setObjectName(_fromUtf8("gridLayout_16"))
        self.tab0_1_object = QtGui.QLabel("Artisan's tools", self.tab0_object_proficiency_layout)
        self.tab0_1_object.setAlignment(QtCore.Qt.AlignCenter)
        self.tab0_1_object.setObjectName(_fromUtf8("tab0_1_object"))
        self.gridLayout_16.addWidget(self.tab0_1_object, 1, 0, 1, 1)
        self.tab0_3_object = QtGui.QLabel("Club", self.tab0_object_proficiency_layout)
        self.tab0_3_object.setAlignment(QtCore.Qt.AlignCenter)
        self.tab0_3_object.setObjectName(_fromUtf8("tab0_3_object"))
        self.gridLayout_16.addWidget(self.tab0_3_object, 2, 0, 1, 1)
        self.tab0_4_object = QtGui.QLabel("Shortsword", self.tab0_object_proficiency_layout)
        self.tab0_4_object.setAlignment(QtCore.Qt.AlignCenter)
        self.tab0_4_object.setObjectName(_fromUtf8("tab0_4_object"))
        self.gridLayout_16.addWidget(self.tab0_4_object, 2, 1, 1, 1)
        self.tab0_6_object = QtGui.QLabel("Shortbow", self.tab0_object_proficiency_layout)
        self.tab0_6_object.setAlignment(QtCore.Qt.AlignCenter)
        self.tab0_6_object.setObjectName(_fromUtf8("tab0_6_object"))
        self.gridLayout_16.addWidget(self.tab0_6_object, 3, 1, 1, 1)
        self.tab0_2_object = QtGui.QLabel("Longsword", self.tab0_object_proficiency_layout)
        self.tab0_2_object.setAlignment(QtCore.Qt.AlignCenter)
        self.tab0_2_object.setObjectName(_fromUtf8("tab0_2_object"))
        self.gridLayout_16.addWidget(self.tab0_2_object, 1, 1, 1, 1)
        self.tab0_5_object = QtGui.QLabel("Light Armor", self.tab0_object_proficiency_layout)
        self.tab0_5_object.setAlignment(QtCore.Qt.AlignCenter)
        self.tab0_5_object.setObjectName(_fromUtf8("tab0_5_object"))
        self.gridLayout_16.addWidget(self.tab0_5_object, 3, 0, 1, 1)
        self.horizontalLayout_42.addWidget(self.tab0_object_proficiency_layout)
        self.verticalLayout_17.addWidget(self.tab0_proficiencies_layout)
        self.horizontalLayout_2.addWidget(self.tab0_summary_layout)
        self.main_tab.addTab(self.tab0, "Character Choice")
    
    def setupDescription(self):
        # create tab
        self.tab1 = QtGui.QWidget()
        self.tab1.setObjectName(_fromUtf8("tab1"))
        self.horizontalLayout_19 = QtGui.QHBoxLayout(self.tab1)
        self.horizontalLayout_19.setObjectName(_fromUtf8("horizontalLayout_19"))

        # create left side
        self.tab1_character_layout = QtGui.QGroupBox("Character", self.tab1)
        self.tab1_character_layout.setObjectName(_fromUtf8("tab1_character_layout"))
        self.verticalLayout_22 = QtGui.QVBoxLayout(self.tab1_character_layout)
        self.verticalLayout_22.setObjectName(_fromUtf8("verticalLayout_22"))

        # create character's form
        self.tab1_character_form = QtGui.QFormLayout()
        self.tab1_character_form.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.tab1_character_form.setObjectName(_fromUtf8("tab1_character_form"))
        self.tab1_characterNameLabel = QtGui.QLabel("Character Name", self.tab1_character_layout)
        self.tab1_characterNameLabel.setObjectName(_fromUtf8("tab1_characterNameLabel"))
        self.tab1_character_form.setWidget(0, QtGui.QFormLayout.LabelRole, self.tab1_characterNameLabel)
        self.tab1_characterNameLineEdit = QtGui.QLineEdit(self.tab1_character_layout)
        self.tab1_characterNameLineEdit.textChanged.connect(self.character.setName)
        self.tab1_characterNameLineEdit.setObjectName(_fromUtf8("tab1_characterNameLineEdit"))
        self.tab1_character_form.setWidget(0, QtGui.QFormLayout.FieldRole, self.tab1_characterNameLineEdit)
        self.tab1_playerNameLabel = QtGui.QLabel("Player Name", self.tab1_character_layout)
        self.tab1_playerNameLabel.setObjectName(_fromUtf8("tab1_playerNameLabel"))
        self.tab1_character_form.setWidget(1, QtGui.QFormLayout.LabelRole, self.tab1_playerNameLabel)
        self.tab1_playerNameLineEdit = QtGui.QLineEdit(self.tab1_character_layout)
        self.tab1_playerNameLineEdit.textChanged.connect(self.character.setPlayer)
        self.tab1_playerNameLineEdit.setObjectName(_fromUtf8("tab1_playerNameLineEdit"))
        self.tab1_character_form.setWidget(1, QtGui.QFormLayout.FieldRole, self.tab1_playerNameLineEdit)
        self.tab1_campaignLabel = QtGui.QLabel("Campaign", self.tab1_character_layout)
        self.tab1_campaignLabel.setObjectName(_fromUtf8("tab1_campaignLabel"))
        self.tab1_character_form.setWidget(2, QtGui.QFormLayout.LabelRole, self.tab1_campaignLabel)
        self.tab1_campaignComboBox = QtGui.QComboBox(self.tab1_character_layout)
        self.tab1_campaignComboBox.activated[str].connect(self.character.setCampaign)
        self.tab1_campaignComboBox.setEditable(True)
        self.tab1_campaignComboBox.setObjectName(_fromUtf8("tab1_campaignComboBox"))
        self.tab1_character_form.setWidget(2, QtGui.QFormLayout.FieldRole, self.tab1_campaignComboBox)
        self.tab1_genderLabel = QtGui.QLabel("Gender", self.tab1_character_layout)
        self.tab1_genderLabel.setObjectName(_fromUtf8("tab1_genderLabel"))
        self.tab1_character_form.setWidget(3, QtGui.QFormLayout.LabelRole, self.tab1_genderLabel)
        self.tab1_genderComboBox = QtGui.QComboBox(self.tab1_character_layout)
        self.tab1_genderComboBox.activated.connect(self.character.setGender)
        self.tab1_genderComboBox.setObjectName(_fromUtf8("tab1_genderComboBox"))
        self.tab1_genderComboBox.addItem("Male")
        self.tab1_genderComboBox.addItem("Female")
        self.tab1_character_form.setWidget(3, QtGui.QFormLayout.FieldRole, self.tab1_genderComboBox)
        self.tab1_ageLabel = QtGui.QLabel("Age", self.tab1_character_layout)
        self.tab1_ageLabel.setObjectName(_fromUtf8("tab1_ageLabel"))
        self.tab1_character_form.setWidget(4, QtGui.QFormLayout.LabelRole, self.tab1_ageLabel)
        self.tab1_ageLineEdit = QtGui.QLineEdit(self.tab1_character_layout)
        self.tab1_ageLineEdit.textChanged.connect(self.character.setAge)
        self.tab1_ageLineEdit.setObjectName(_fromUtf8("tab1_ageLineEdit"))
        self.tab1_character_form.setWidget(4, QtGui.QFormLayout.FieldRole, self.tab1_ageLineEdit)
        self.tab1_heightLabel = QtGui.QLabel("Height", self.tab1_character_layout)
        self.tab1_heightLabel.setObjectName(_fromUtf8("tab1_heightLabel"))
        self.tab1_character_form.setWidget(5, QtGui.QFormLayout.LabelRole, self.tab1_heightLabel)
        self.tab1_heightLineEdit = QtGui.QLineEdit(self.tab1_character_layout)
        self.tab1_heightLineEdit.textChanged.connect(self.character.setHeight)
        self.tab1_heightLineEdit.setObjectName(_fromUtf8("tab1_heightLineEdit"))
        self.tab1_character_form.setWidget(5, QtGui.QFormLayout.FieldRole, self.tab1_heightLineEdit)
        self.tab1_weightLabel = QtGui.QLabel("Weight", self.tab1_character_layout)
        self.tab1_weightLabel.setObjectName(_fromUtf8("tab1_weightLabel"))
        self.tab1_character_form.setWidget(6, QtGui.QFormLayout.LabelRole, self.tab1_weightLabel)
        self.tab1_weightLineEdit = QtGui.QLineEdit(self.tab1_character_layout)
        self.tab1_weightLineEdit.textChanged.connect(self.character.setWeight)
        self.tab1_weightLineEdit.setObjectName(_fromUtf8("tab1_weightLineEdit"))
        self.tab1_character_form.setWidget(6, QtGui.QFormLayout.FieldRole, self.tab1_weightLineEdit)
        self.tab1_hairLabel = QtGui.QLabel("Hair", self.tab1_character_layout)
        self.tab1_hairLabel.setObjectName(_fromUtf8("tab1_hairLabel"))
        self.tab1_character_form.setWidget(7, QtGui.QFormLayout.LabelRole, self.tab1_hairLabel)
        self.tab1_hairLineEdit = QtGui.QLineEdit(self.tab1_character_layout)
        self.tab1_hairLineEdit.textChanged.connect(self.character.setHair)
        self.tab1_hairLineEdit.setObjectName(_fromUtf8("tab1_hairLineEdit"))
        self.tab1_character_form.setWidget(7, QtGui.QFormLayout.FieldRole, self.tab1_hairLineEdit)
        self.tab1_eyeslabel = QtGui.QLabel("Eyes", self.tab1_character_layout)
        self.tab1_eyeslabel.setObjectName(_fromUtf8("tab1_eyeslabel"))
        self.tab1_character_form.setWidget(8, QtGui.QFormLayout.LabelRole, self.tab1_eyeslabel)
        self.tab1_eyesLineEdit = QtGui.QLineEdit(self.tab1_character_layout)
        self.tab1_eyesLineEdit.textChanged.connect(self.character.setEyes)
        self.tab1_eyesLineEdit.setObjectName(_fromUtf8("tab1_eyesLineEdit"))
        self.tab1_character_form.setWidget(8, QtGui.QFormLayout.FieldRole, self.tab1_eyesLineEdit)
        self.tab1_experienceLabel = QtGui.QLabel("Experience", self.tab1_character_layout)
        self.tab1_experienceLabel.setObjectName(_fromUtf8("tab1_experienceLabel"))
        self.tab1_character_form.setWidget(10, QtGui.QFormLayout.LabelRole, self.tab1_experienceLabel)
        self.tab1_experienceSpinBox = QtGui.QSpinBox(self.tab1_character_layout)
        self.tab1_experienceSpinBox.valueChanged.connect(self.character.setExperience)
        self.tab1_experienceSpinBox.setMaximum(400000)
        self.tab1_experienceSpinBox.setObjectName(_fromUtf8("tab1_experienceSpinBox"))
        self.tab1_character_form.setWidget(10, QtGui.QFormLayout.FieldRole, self.tab1_experienceSpinBox)
        self.verticalLayout_22.addLayout(self.tab1_character_form)

        # Notable features
        self.tab1_features_layout = QtGui.QGroupBox("Notable Features", self.tab1_character_layout)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tab1_features_layout.sizePolicy().hasHeightForWidth())
        self.tab1_features_layout.setSizePolicy(sizePolicy)
        self.tab1_features_layout.setObjectName(_fromUtf8("tab1_features_layout"))
        self.verticalLayout_21 = QtGui.QVBoxLayout(self.tab1_features_layout)
        self.verticalLayout_21.setObjectName(_fromUtf8("verticalLayout_21"))
        self.tab1_features = QtGui.QTextEdit(self.tab1_features_layout)
        self.tab1_features.textChanged.connect(self.notableFeaturesChanged)
        self.tab1_features.setObjectName(_fromUtf8("tab1_features"))
        self.verticalLayout_21.addWidget(self.tab1_features)
        self.verticalLayout_22.addWidget(self.tab1_features_layout)
        self.horizontalLayout_19.addWidget(self.tab1_character_layout)

        # image
        self.tab1_img_abilities_layout = QtGui.QVBoxLayout()
        self.tab1_img_abilities_layout.setContentsMargins(0, -1, -1, -1)
        self.tab1_img_abilities_layout.setObjectName(_fromUtf8("tab1_img_abilities_layout"))
        self.tab1_img_layout = QtGui.QHBoxLayout()
        self.tab1_img_layout.setObjectName(_fromUtf8("tab1_img_layout"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.tab1_img_layout.addItem(spacerItem)
        self.tab1_img = QtGui.QLabel(self.tab1)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tab1_img.sizePolicy().hasHeightForWidth())
        self.tab1_img.setSizePolicy(sizePolicy)
        self.tab1_img.setMaximumSize(QtCore.QSize(400, 400))
        self.tab1_img.setMinimumHeight(400)
        self.tab1_img.setText(_fromUtf8(""))
        self.tab1_img.setPixmap(QtGui.QPixmap("/home/loikki/Downloads/test.jpeg"))
        self.tab1_img.setScaledContents(True)
        self.tab1_img.setAlignment(QtCore.Qt.AlignCenter)
        self.tab1_img.setObjectName(_fromUtf8("tab1_img"))
        self.tab1_img_layout.addWidget(self.tab1_img)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.tab1_img_layout.addItem(spacerItem1)
        self.tab1_img_button_layout = QtGui.QVBoxLayout()
        self.tab1_img_button_layout.setObjectName(_fromUtf8("tab1_img_button_layout"))
        self.tab1_import_button = QtGui.QPushButton("Import Image", self.tab1)
        self.tab1_import_button.setObjectName(_fromUtf8("tab1_import_button"))
        self.tab1_import_button.clicked.connect(self.importImage)
        self.tab1_img_button_layout.addWidget(self.tab1_import_button)
        self.tab1_remove_button = QtGui.QPushButton("Remove Image", self.tab1)
        self.tab1_remove_button.setObjectName(_fromUtf8("tab1_remove_button"))
        self.tab1_remove_button.clicked.connect(self.removeImage)
        self.tab1_img_button_layout.addWidget(self.tab1_remove_button)
        self.tab1_img_layout.addLayout(self.tab1_img_button_layout)
        self.tab1_img_abilities_layout.addLayout(self.tab1_img_layout)

        # abilities
        self.tab1_abilities_layout = QtGui.QGroupBox("Abilities", self.tab1)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tab1_abilities_layout.sizePolicy().hasHeightForWidth())
        self.tab1_abilities_layout.setSizePolicy(sizePolicy)
        self.tab1_abilities_layout.setObjectName(_fromUtf8("tab1_abilities_layout"))
        self.verticalLayout_19 = QtGui.QVBoxLayout(self.tab1_abilities_layout)
        self.verticalLayout_19.setSpacing(25)
        self.verticalLayout_19.setObjectName(_fromUtf8("verticalLayout_19"))
        
        # Choose Value
        self.tab1_ability_style_layout = QtGui.QHBoxLayout()
        self.tab1_ability_style_layout.setObjectName(_fromUtf8("tab1_ability_style_layout"))
        self.tab1_ability_style_combo = QtGui.QComboBox(self.tab1_abilities_layout)
        self.tab1_ability_style_combo.setMinimumSize(QtCore.QSize(120, 0))
        self.tab1_ability_style_combo.setObjectName(_fromUtf8("tab1_ability_style_combo"))
        self.tab1_ability_style_combo.addItem("Random")
        self.tab1_ability_style_combo.addItem("Free")
        self.tab1_ability_style_combo.addItem("Pregenerated")
        self.tab1_ability_style_combo.addItem("Points")
        self.tab1_ability_style_layout.addWidget(self.tab1_ability_style_combo)
        self.tab1_roll_button = QtGui.QPushButton("Roll", self.tab1_abilities_layout)
        self.tab1_roll_button.setObjectName(_fromUtf8("tab1_roll_button"))
        self.tab1_roll_button.clicked.connect(self.rollAbilities)
        self.tab1_ability_style_layout.addWidget(self.tab1_roll_button)
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.tab1_ability_style_layout.addItem(spacerItem2)
        self.verticalLayout_19.addLayout(self.tab1_ability_style_layout)

        # Show Value
        self.tab1_abilities_value_layout = QtGui.QHBoxLayout()
        self.tab1_abilities_value_layout.setObjectName(_fromUtf8("tab1_abilities_value_layout"))
        self.tab1_ability_value_1 = QtGui.QLineEdit(self.tab1_abilities_layout)
        self.tab1_ability_value_1.textChanged.connect(self.changeAbilityRoll)
        self.tab1_ability_value_1.setReadOnly(False)
        self.tab1_ability_value_1.setObjectName(_fromUtf8("tab1_ability_value_1"))
        self.tab1_abilities_value_layout.addWidget(self.tab1_ability_value_1)
        self.tab1_ability_value_2 = QtGui.QLineEdit(self.tab1_abilities_layout)
        self.tab1_ability_value_2.textChanged.connect(self.changeAbilityRoll)
        self.tab1_ability_value_2.setObjectName(_fromUtf8("tab1_ability_value_2"))
        self.tab1_abilities_value_layout.addWidget(self.tab1_ability_value_2)
        self.tab1_ability_value_3 = QtGui.QLineEdit(self.tab1_abilities_layout)
        self.tab1_ability_value_3.textChanged.connect(self.changeAbilityRoll)
        self.tab1_ability_value_3.setObjectName(_fromUtf8("tab1_ability_value_3"))
        self.tab1_abilities_value_layout.addWidget(self.tab1_ability_value_3)
        self.tab1_ability_value_4 = QtGui.QLineEdit(self.tab1_abilities_layout)
        self.tab1_ability_value_4.textChanged.connect(self.changeAbilityRoll)
        self.tab1_ability_value_4.setObjectName(_fromUtf8("tab1_ability_value_4"))
        self.tab1_abilities_value_layout.addWidget(self.tab1_ability_value_4)
        self.tab1_ability_value_5 = QtGui.QLineEdit(self.tab1_abilities_layout)
        self.tab1_ability_value_5.textChanged.connect(self.changeAbilityRoll)
        self.tab1_ability_value_5.setObjectName(_fromUtf8("tab1_ability_value_5"))
        self.tab1_abilities_value_layout.addWidget(self.tab1_ability_value_5)
        self.tab1_ability_value_6 = QtGui.QLineEdit(self.tab1_abilities_layout)
        self.tab1_ability_value_6.textChanged.connect(self.changeAbilityRoll)
        self.tab1_ability_value_6.setObjectName(_fromUtf8("tab1_ability_value_6"))
        self.tab1_abilities_value_layout.addWidget(self.tab1_ability_value_6)
        self.verticalLayout_19.addLayout(self.tab1_abilities_value_layout)

        # Score attribution
        self.tab1_abilities_choice_layout = QtGui.QGridLayout()
        self.tab1_abilities_choice_layout.setObjectName(_fromUtf8("tab1_abilities_choice_layout"))
        self.tab1_cha_combo = QtGui.QComboBox(self.tab1_abilities_layout)
        self.tab1_cha_combo.setObjectName(_fromUtf8("tab1_cha_combo"))
        self.tab1_cha_combo.activated[str].connect(self.character.setCharisma)
        self.tab1_cha_combo.activated.connect(self.changeAttributionAbility)
        self.tab1_abilities_choice_layout.addWidget(self.tab1_cha_combo, 1, 5, 1, 1)
        self.tab1_wis_combo = QtGui.QComboBox(self.tab1_abilities_layout)
        self.tab1_wis_combo.activated[str].connect(self.character.setWisdom)
        self.tab1_wis_combo.activated.connect(self.changeAttributionAbility)
        self.tab1_wis_combo.setObjectName(_fromUtf8("tab1_wis_combo"))
        self.tab1_abilities_choice_layout.addWidget(self.tab1_wis_combo, 1, 4, 1, 1)
        self.tab1_int_combo = QtGui.QComboBox(self.tab1_abilities_layout)
        self.tab1_int_combo.activated[str].connect(self.character.setIntelligence)
        self.tab1_int_combo.activated.connect(self.changeAttributionAbility)
        self.tab1_int_combo.setObjectName(_fromUtf8("tab1_int_combo"))
        self.tab1_abilities_choice_layout.addWidget(self.tab1_int_combo, 1, 3, 1, 1)
        self.tab1_con_combo = QtGui.QComboBox(self.tab1_abilities_layout)
        self.tab1_con_combo.activated[str].connect(self.character.setConstitution)
        self.tab1_con_combo.activated.connect(self.changeAttributionAbility)
        self.tab1_con_combo.setObjectName(_fromUtf8("tab1_con_combo"))
        self.tab1_abilities_choice_layout.addWidget(self.tab1_con_combo, 1, 2, 1, 1)
        self.tab1_dex_combo = QtGui.QComboBox(self.tab1_abilities_layout)
        self.tab1_dex_combo.activated[str].connect(self.character.setDexterity)
        self.tab1_dex_combo.activated.connect(self.changeAttributionAbility)
        self.tab1_dex_combo.setObjectName(_fromUtf8("tab1_dex_combo"))
        self.tab1_abilities_choice_layout.addWidget(self.tab1_dex_combo, 1, 1, 1, 1)
        self.tab1_str_combo = QtGui.QComboBox(self.tab1_abilities_layout)
        self.tab1_str_combo.activated[str].connect(self.character.setStrength)
        self.tab1_str_combo.activated.connect(self.changeAttributionAbility)
        self.tab1_str_combo.setObjectName(_fromUtf8("tab1_str_combo"))
        self.tab1_abilities_choice_layout.addWidget(self.tab1_str_combo, 1, 0, 1, 1)
        # labels
        self.tab1_cha_label = QtGui.QLabel("Charisma", self.tab1_abilities_layout)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tab1_cha_label.sizePolicy().hasHeightForWidth())
        self.tab1_cha_label.setSizePolicy(sizePolicy)
        self.tab1_cha_label.setAlignment(QtCore.Qt.AlignCenter)
        self.tab1_cha_label.setObjectName(_fromUtf8("tab1_cha_label"))
        self.tab1_abilities_choice_layout.addWidget(self.tab1_cha_label, 0, 5, 1, 1)
        self.tab1_wis_label = QtGui.QLabel("Wisdom", self.tab1_abilities_layout)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tab1_wis_label.sizePolicy().hasHeightForWidth())
        self.tab1_wis_label.setSizePolicy(sizePolicy)
        self.tab1_wis_label.setAlignment(QtCore.Qt.AlignCenter)
        self.tab1_wis_label.setObjectName(_fromUtf8("tab1_wis_label"))
        self.tab1_abilities_choice_layout.addWidget(self.tab1_wis_label, 0, 4, 1, 1)
        self.tab1_str_label = QtGui.QLabel("Strength", self.tab1_abilities_layout)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tab1_str_label.sizePolicy().hasHeightForWidth())
        self.tab1_str_label.setSizePolicy(sizePolicy)
        self.tab1_str_label.setAlignment(QtCore.Qt.AlignCenter)
        self.tab1_str_label.setObjectName(_fromUtf8("tab1_str_label"))
        self.tab1_abilities_choice_layout.addWidget(self.tab1_str_label, 0, 0, 1, 1)
        self.tab1_dex_label = QtGui.QLabel("Dexterity", self.tab1_abilities_layout)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tab1_dex_label.sizePolicy().hasHeightForWidth())
        self.tab1_dex_label.setSizePolicy(sizePolicy)
        self.tab1_dex_label.setAlignment(QtCore.Qt.AlignCenter)
        self.tab1_dex_label.setObjectName(_fromUtf8("tab1_dex_label"))
        self.tab1_abilities_choice_layout.addWidget(self.tab1_dex_label, 0, 1, 1, 1)
        self.tab1_con_label = QtGui.QLabel("Constitution", self.tab1_abilities_layout)
        self.tab1_con_label.setAlignment(QtCore.Qt.AlignCenter)
        self.tab1_con_label.setObjectName(_fromUtf8("tab1_con_label"))
        self.tab1_abilities_choice_layout.addWidget(self.tab1_con_label, 0, 2, 1, 1)
        self.tab1_int_label = QtGui.QLabel("Intelligence", self.tab1_abilities_layout)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tab1_int_label.sizePolicy().hasHeightForWidth())
        self.tab1_int_label.setSizePolicy(sizePolicy)
        self.tab1_int_label.setAlignment(QtCore.Qt.AlignCenter)
        self.tab1_int_label.setObjectName(_fromUtf8("tab1_int_label"))
        self.tab1_abilities_choice_layout.addWidget(self.tab1_int_label, 0, 3, 1, 1)
        self.verticalLayout_19.addLayout(self.tab1_abilities_choice_layout)
        spacerItem3 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_19.addItem(spacerItem3)
        self.tab1_img_abilities_layout.addWidget(self.tab1_abilities_layout)
        self.horizontalLayout_19.addLayout(self.tab1_img_abilities_layout)
        self.main_tab.addTab(self.tab1, "Description")

        
    def setupRace(self):
        # create tab
        self.tab2 = QtGui.QWidget()
        self.tab2.setObjectName(_fromUtf8("tab2"))

        # create race part
        self.verticalLayout_26 = QtGui.QVBoxLayout(self.tab2)
        self.verticalLayout_26.setObjectName(_fromUtf8("verticalLayout_26"))
        self.tab2_race_subrace_layout = QtGui.QHBoxLayout()
        self.tab2_race_subrace_layout.setContentsMargins(0, -1, -1, -1)
        self.tab2_race_subrace_layout.setObjectName(_fromUtf8("tab2_race_subrace_layout"))
        self.tab2_race_layout = QtGui.QGroupBox("Race", self.tab2)
        self.tab2_race_layout.setObjectName(_fromUtf8("tab2_race_layout"))
        self.verticalLayout = QtGui.QVBoxLayout(self.tab2_race_layout)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.tab2_race_choice_layout = QtGui.QHBoxLayout()
        self.tab2_race_choice_layout.setObjectName(_fromUtf8("tab2_race_choice_layout"))
        self.tab2_race_choice_combo = QtGui.QComboBox(self.tab2_race_layout)
        for i in self.race_parser.getListRace():
            self.tab2_race_choice_combo.addItem(i)
        self.tab2_race_choice_combo.activated[str].connect(self.changeRace)
        self.tab2_race_choice_combo.setMinimumSize(QtCore.QSize(150, 5))
        self.tab2_race_choice_combo.setObjectName(_fromUtf8("tab2_race_choice_combo"))
        self.tab2_race_choice_layout.addWidget(self.tab2_race_choice_combo)
        spacerItem4 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.tab2_race_choice_layout.addItem(spacerItem4)
        self.verticalLayout.addLayout(self.tab2_race_choice_layout)
        self.tab2_race_description = QtGui.QTextBrowser(self.tab2_race_layout)
        self.tab2_race_description.setObjectName(_fromUtf8("tab2_race_description"))
        self.verticalLayout.addWidget(self.tab2_race_description)
        self.tab2_race_subrace_layout.addWidget(self.tab2_race_layout)

        # subrace
        self.tab2_subrace_layout = QtGui.QGroupBox("Subrace", self.tab2)
        self.tab2_subrace_layout.setObjectName(_fromUtf8("tab2_subrace_layout"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.tab2_subrace_layout)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.tab2_subrace_choice_layout = QtGui.QHBoxLayout()
        self.tab2_subrace_choice_layout.setObjectName(_fromUtf8("tab2_subrace_choice_layout"))
        self.tab2_subrace_choice_combo = QtGui.QComboBox(self.tab2_subrace_layout)
        self.tab2_subrace_choice_combo.activated[str].connect(self.changeSubrace)
        self.tab2_subrace_choice_combo.setMinimumSize(QtCore.QSize(150, 5))
        self.tab2_subrace_choice_combo.setObjectName(_fromUtf8("tab2_subrace_choice_combo"))
        self.tab2_subrace_choice_combo.addItem("Mountain Dwarf")
        self.tab2_subrace_choice_layout.addWidget(self.tab2_subrace_choice_combo)
        spacerItem5 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.tab2_subrace_choice_layout.addItem(spacerItem5)
        self.verticalLayout_2.addLayout(self.tab2_subrace_choice_layout)
        self.tab2_subrace_description = QtGui.QTextBrowser(self.tab2_subrace_layout)
        self.tab2_subrace_description.setObjectName(_fromUtf8("tab2_subrace_description"))
        self.verticalLayout_2.addWidget(self.tab2_subrace_description)
        self.tab2_race_subrace_layout.addWidget(self.tab2_subrace_layout)
        self.verticalLayout_26.addLayout(self.tab2_race_subrace_layout)

        # choices
        self.tab2_choices_layout = QtGui.QGridLayout()
        self.tab2_choices_layout.setContentsMargins(-1, -1, -1, 0)
        self.tab2_choices_layout.setObjectName(_fromUtf8("tab2_choices_layout"))
        self.tab2_choice_list = []
        self.verticalLayout_26.addLayout(self.tab2_choices_layout)

        self.changeRace(self.tab2_race_choice_combo.currentText())
        self.main_tab.addTab(self.tab2, "Race")


        
    def setupClass(self):
        # tab
        self.tab3 = QtGui.QWidget()
        self.tab3.setObjectName(_fromUtf8("tab3"))
        self.horizontalLayout_9 = QtGui.QHBoxLayout(self.tab3)
        self.horizontalLayout_9.setObjectName(_fromUtf8("horizontalLayout_9"))
        self.tab3_layout = QtGui.QGridLayout()
        self.tab3_layout.setObjectName(_fromUtf8("tab3_layout"))
        # description
        self.tab3_class_description = QtGui.QTextBrowser(self.tab3)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tab3_class_description.sizePolicy().hasHeightForWidth())
        self.tab3_class_description.setSizePolicy(sizePolicy)
        self.tab3_class_description.setObjectName(_fromUtf8("tab3_class_description"))
        self.tab3_layout.addWidget(self.tab3_class_description, 0, 1, 1, 1)
        
        self.tab3_specialization_description = QtGui.QTextBrowser(self.tab3)
        self.tab3_specialization_description.setObjectName(_fromUtf8("tab3_specialization_description"))
        self.tab3_layout.addWidget(self.tab3_specialization_description, 1, 1, 1, 1)

        # Choice
        sizePolicy = QtGui.QSizePolicy(
            QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)

        self.tab3_class_choice_layout = QtGui.QVBoxLayout()
        
        spacer = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.tab3_class_choice_layout.addItem(spacer)

        self.tab3_class_choice_layout.setObjectName(_fromUtf8("tab3_class_choice_layout"))
        self.tab3_class_label = QtGui.QLabel("Class", self.tab3)
        self.tab3_class_label.setSizePolicy(sizePolicy)
        self.tab3_class_label.setObjectName(_fromUtf8("tab3_class_label"))
        self.tab3_class_choice_layout.addWidget(self.tab3_class_label)
        self.tab3_class_combo = QtGui.QComboBox(self.tab3)
        self.tab3_class_combo.setSizePolicy(sizePolicy)
        for i in self.class_parser.getListClass():
            self.tab3_class_combo.addItem(i)
        self.tab3_class_combo.activated[str].connect(self.changeClass)
        self.tab3_class_combo.setObjectName(_fromUtf8("tab3_class_combo"))
        self.tab3_class_choice_layout.addWidget(self.tab3_class_combo)
        # specialization
        self.tab3_specialization_label = QtGui.QLabel("Specialization", self.tab3)
        self.tab3_specialization_label.setSizePolicy(sizePolicy)
        self.tab3_specialization_label.setObjectName(_fromUtf8("tab3_specialization_label"))
        self.tab3_class_choice_layout.addWidget(self.tab3_specialization_label)

        self.tab3_specialization_combo = QtGui.QComboBox(self.tab3)
        self.tab3_specialization_combo.activated[str].connect(self.changeSpecialization)
        self.tab3_specialization_combo.setMinimumSize(QtCore.QSize(120, 0))
        self.tab3_specialization_combo.setSizePolicy(sizePolicy)
        self.tab3_specialization_combo.setObjectName(_fromUtf8("tab3_specialization_combo"))
        self.tab3_class_choice_layout.addWidget(self.tab3_specialization_combo)
        self.tab3_layout.addLayout(self.tab3_class_choice_layout, 0, 0, 1, 1)

        spacer = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.tab3_class_choice_layout.addItem(spacer)

        self.tab3_choices_layout = QtGui.QGridLayout()
        self.tab3_layout.addLayout(self.tab3_choices_layout, 1, 0, 1, 1)
        self.tab3_choice_list = []
        self.tab3_choices_layout.setObjectName(_fromUtf8("tab3_choice_layout"))
        self.horizontalLayout_9.addLayout(self.tab3_layout)

        self.changeClass(self.tab3_class_combo.currentText())
        self.main_tab.addTab(self.tab3, "Class")

        
    def setupSpell(self):
        # tab
        self.tab4 = QtGui.QWidget()
        self.tab4.setObjectName(_fromUtf8("tab4"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.tab4)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        # spell tab
        self.tab4_spell_tab = QtGui.QTabWidget(self.tab4)
        self.tab4_spell_tab.setObjectName(_fromUtf8("tab4_spell_tab"))
        self.tab4_tab0 = QtGui.QWidget()
        self.tab4_tab0.setObjectName(_fromUtf8("tab4_tab0"))
        self.verticalLayout_9 = QtGui.QVBoxLayout(self.tab4_tab0)
        self.verticalLayout_9.setObjectName(_fromUtf8("verticalLayout_9"))

        # cantrip tab
        self.tab4_tab0_list_layout = QtGui.QGroupBox("List", self.tab4_tab0)
        self.tab4_tab0_list_layout.setObjectName(_fromUtf8("tab4_tab0_list_layout"))
        self.horizontalLayout_36 = QtGui.QHBoxLayout(self.tab4_tab0_list_layout)
        self.horizontalLayout_36.setObjectName(_fromUtf8("horizontalLayout_36"))
        # list
        self.tab4_tab0_list_tree = QtGui.QTreeWidget(self.tab4_tab0_list_layout)
        self.tab4_tab0_list_tree.setObjectName(_fromUtf8("tab4_tab0_list_tree"))
        self.tab4_tab0_list_tree.headerItem().setText(0, "Name")
        self.tab4_tab0_list_tree.headerItem().setText(1, "Casting time")
        self.tab4_tab0_list_tree.headerItem().setText(2, "Range")
        self.tab4_tab0_list_tree.headerItem().setText(3, "Components")
        self.tab4_tab0_list_tree.headerItem().setText(4, "Duration")
        
        self.horizontalLayout_36.addWidget(self.tab4_tab0_list_tree)
        self.verticalLayout_9.addWidget(self.tab4_tab0_list_layout)
        self.tab4_tab0_button_layout = QtGui.QHBoxLayout()
        self.tab4_tab0_button_layout.setContentsMargins(-1, 0, -1, -1)
        self.tab4_tab0_button_layout.setObjectName(_fromUtf8("tab4_tab0_button_layout"))
        self.tab4_tab0_add_button = QtGui.QPushButton("Add", self.tab4_tab0)
        self.tab4_tab0_add_button.setObjectName(_fromUtf8("tab4_tab0_add_button"))
        self.tab4_tab0_button_layout.addWidget(self.tab4_tab0_add_button)
        self.tab4_tab0_remove_button = QtGui.QPushButton("Remove", self.tab4_tab0)
        self.tab4_tab0_remove_button.setObjectName(_fromUtf8("tab4_tab0_remove_button"))
        self.tab4_tab0_button_layout.addWidget(self.tab4_tab0_remove_button)
        self.verticalLayout_9.addLayout(self.tab4_tab0_button_layout)
        self.tab4_tab0_lower_layout = QtGui.QHBoxLayout()
        self.tab4_tab0_lower_layout.setObjectName(_fromUtf8("tab4_tab0_lower_layout"))
        # known
        self.tab4_tab0_know_layout = QtGui.QGroupBox("Known", self.tab4_tab0)
        self.tab4_tab0_know_layout.setObjectName(_fromUtf8("tab4_tab0_know_layout"))
        self.verticalLayout_11 = QtGui.QVBoxLayout(self.tab4_tab0_know_layout)
        self.verticalLayout_11.setObjectName(_fromUtf8("verticalLayout_11"))
        self.tab4_tab0_known_tree = QtGui.QTreeWidget(self.tab4_tab0_know_layout)
        self.tab4_tab0_known_tree.setObjectName(_fromUtf8("tab4_tab0_known_tree"))
        self.tab4_tab0_known_tree.headerItem().setText(0, "Name")
        self.tab4_tab0_known_tree.headerItem().setText(1, "Casting time")
        self.tab4_tab0_known_tree.headerItem().setText(2, "Range")
        self.tab4_tab0_known_tree.headerItem().setText(3, "Components")
        self.tab4_tab0_known_tree.headerItem().setText(4, "Duration")
        self.verticalLayout_11.addWidget(self.tab4_tab0_known_tree)
        self.tab4_tab0_lower_layout.addWidget(self.tab4_tab0_know_layout)
        self.tab4_tab0_description = QtGui.QTextBrowser(self.tab4_tab0)
        self.tab4_tab0_description.setObjectName(_fromUtf8("tab4_tab0_description"))
        self.tab4_tab0_lower_layout.addWidget(self.tab4_tab0_description)
        self.verticalLayout_9.addLayout(self.tab4_tab0_lower_layout)
        self.tab4_tab0_available_label = QtGui.QLabel("Cantrip known: 4/6", self.tab4_tab0)
        self.tab4_tab0_available_label.setAlignment(QtCore.Qt.AlignCenter)
        self.tab4_tab0_available_label.setObjectName(_fromUtf8("tab4_tab0_available_label"))
        self.verticalLayout_9.addWidget(self.tab4_tab0_available_label)
        self.tab4_spell_tab.addTab(self.tab4_tab0, "Cantrips")

        # Spells
        self.tab4_tab1 = QtGui.QWidget()
        self.tab4_tab1.setObjectName(_fromUtf8("tab4_tab1"))
        self.verticalLayout_5 = QtGui.QVBoxLayout(self.tab4_tab1)
        self.verticalLayout_5.setObjectName(_fromUtf8("verticalLayout_5"))
        # list
        self.tab4_tab1_list_layout = QtGui.QGroupBox("List", self.tab4_tab1)
        self.tab4_tab1_list_layout.setObjectName(_fromUtf8("tab4_tab1_list_layout"))
        self.horizontalLayout_7 = QtGui.QHBoxLayout(self.tab4_tab1_list_layout)
        self.horizontalLayout_7.setObjectName(_fromUtf8("horizontalLayout_7"))
        self.tab4_tab1_list_tree = QtGui.QTreeWidget(self.tab4_tab1_list_layout)
        self.tab4_tab1_list_tree.setObjectName(_fromUtf8("tab4_tab1_list_tree"))
        item_0 = QtGui.QTreeWidgetItem(self.tab4_tab1_list_tree, ["1st Level"])
        item_1 = QtGui.QTreeWidgetItem(item_0, [
            "Alarm", "1min", "30", "V,S,M (a tiny bell and a piece of fine silver wire)",
            "8h", "Abjuration"])
        self.tab4_tab1_list_tree.headerItem().setText(0, "Name")
        self.tab4_tab1_list_tree.headerItem().setText(1, "Casting Time")
        self.tab4_tab1_list_tree.headerItem().setText(2, "Range")
        self.tab4_tab1_list_tree.headerItem().setText(3, "Components")
        self.tab4_tab1_list_tree.headerItem().setText(4, "Duration")
        self.tab4_tab1_list_tree.headerItem().setText(5,"Type")
        __sortingEnabled = self.tab4_tab1_list_tree.isSortingEnabled()
        self.tab4_tab1_list_tree.setSortingEnabled(__sortingEnabled)
        self.tab4_tab1_list_tree.setSortingEnabled(False)
        self.horizontalLayout_7.addWidget(self.tab4_tab1_list_tree)
        self.verticalLayout_5.addWidget(self.tab4_tab1_list_layout)
        self.tab4_tab1_button_layout = QtGui.QHBoxLayout()
        self.tab4_tab1_button_layout.setContentsMargins(-1, 0, -1, -1)
        self.tab4_tab1_button_layout.setObjectName(_fromUtf8("tab4_tab1_button_layout"))
        self.tab4_tab1_add_button = QtGui.QPushButton("Add", self.tab4_tab1)
        self.tab4_tab1_add_button.setObjectName(_fromUtf8("tab4_tab1_add_button"))
        self.tab4_tab1_button_layout.addWidget(self.tab4_tab1_add_button)
        self.tab4_tab1_remove_button = QtGui.QPushButton("Remove", self.tab4_tab1)
        self.tab4_tab1_remove_button.setObjectName(_fromUtf8("tab4_tab1_remove_button"))
        self.tab4_tab1_button_layout.addWidget(self.tab4_tab1_remove_button)
        self.verticalLayout_5.addLayout(self.tab4_tab1_button_layout)
        self.tab4_tab1_lower_layout = QtGui.QHBoxLayout()
        self.tab4_tab1_lower_layout.setObjectName(_fromUtf8("tab4_tab1_lower_layout"))
        # known
        self.tab4_tab1_known_layout = QtGui.QGroupBox("Known", self.tab4_tab1)
        self.tab4_tab1_known_layout.setObjectName(_fromUtf8("tab4_tab1_known_layout"))
        self.horizontalLayout_8 = QtGui.QHBoxLayout(self.tab4_tab1_known_layout)
        self.horizontalLayout_8.setObjectName(_fromUtf8("horizontalLayout_8"))
        self.tab4_tab1_known_tree = QtGui.QTreeWidget(self.tab4_tab1_known_layout)
        self.tab4_tab1_known_tree.setObjectName(_fromUtf8("tab4_tab1_known_tree"))
        self.tab4_tab1_known_tree.headerItem().setText(0, _fromUtf8("Name"))
        self.horizontalLayout_8.addWidget(self.tab4_tab1_known_tree)
        self.tab4_tab1_lower_layout.addWidget(self.tab4_tab1_known_layout)
        self.tab4_tab1_known_tree.headerItem().setText(1, "Casting time")
        self.tab4_tab1_known_tree.headerItem().setText(2, "Range")
        self.tab4_tab1_known_tree.headerItem().setText(3, "Components")
        self.tab4_tab1_known_tree.headerItem().setText(4, "Duration")
        
        self.tab4_tab1_description = QtGui.QTextBrowser(self.tab4_tab1)
        self.tab4_tab1_description.setObjectName(_fromUtf8("tab4_tab1_description"))
        self.tab4_tab1_lower_layout.addWidget(self.tab4_tab1_description)
        self.verticalLayout_5.addLayout(self.tab4_tab1_lower_layout)
        self.tab4_tab1_available_label = QtGui.QLabel("Spells known: 4/5", self.tab4_tab1)
        self.tab4_tab1_available_label.setAlignment(QtCore.Qt.AlignCenter)
        self.tab4_tab1_available_label.setObjectName(_fromUtf8("tab4_tab1_available_label"))
        self.verticalLayout_5.addWidget(self.tab4_tab1_available_label)
        self.tab4_spell_tab.addTab(self.tab4_tab1, "Spells")

        # Spell slots
        self.tab4_tab2 = QtGui.QWidget()
        self.tab4_tab2.setObjectName(_fromUtf8("tab4_tab2"))
        self.verticalLayout_12 = QtGui.QVBoxLayout(self.tab4_tab2)
        self.verticalLayout_12.setObjectName(_fromUtf8("verticalLayout_12"))
        # button
        self.tab4_tab2_button_layout = QtGui.QHBoxLayout()
        self.tab4_tab2_button_layout.setObjectName(_fromUtf8("tab4_tab2_button_layout"))
        self.tab4_tab2_rest_button = QtGui.QPushButton("Long Rest", self.tab4_tab2)
        self.tab4_tab2_rest_button.setObjectName(_fromUtf8("tab4_tab2_rest_button"))
        self.tab4_tab2_button_layout.addWidget(self.tab4_tab2_rest_button)
        self.tab4_tab2_reset_button = QtGui.QPushButton("Reset Spell Choice", self.tab4_tab2)
        self.tab4_tab2_reset_button.setObjectName(_fromUtf8("tab4_tab2_reset_button"))
        self.tab4_tab2_button_layout.addWidget(self.tab4_tab2_reset_button)
        spacerItem6 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.tab4_tab2_button_layout.addItem(spacerItem6)
        self.verticalLayout_12.addLayout(self.tab4_tab2_button_layout)
        # 1st level
        self.tab4_tab2_1_layout = QtGui.QGroupBox("1st Level", self.tab4_tab2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tab4_tab2_1_layout.sizePolicy().hasHeightForWidth())
        self.tab4_tab2_1_layout.setSizePolicy(sizePolicy)
        self.tab4_tab2_1_layout.setObjectName(_fromUtf8("tab4_tab2_1_layout"))
        self.gridLayout_3 = QtGui.QGridLayout(self.tab4_tab2_1_layout)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.tab4_tab2_1_used3 = QtGui.QRadioButton("Used", self.tab4_tab2_1_layout)
        self.tab4_tab2_1_used3.setObjectName(_fromUtf8("tab4_tab2_1_used3"))
        self.gridLayout_3.addWidget(self.tab4_tab2_1_used3, 1, 1, 1, 1)
        self.tab4_tab2_1_used1 = QtGui.QRadioButton("Used", self.tab4_tab2_1_layout)
        self.tab4_tab2_1_used1.setObjectName(_fromUtf8("tab4_tab2_1_used1"))
        self.gridLayout_3.addWidget(self.tab4_tab2_1_used1, 0, 1, 1, 1)
        self.tab4_tab2_1_used2 = QtGui.QRadioButton("Used", self.tab4_tab2_1_layout)
        self.tab4_tab2_1_used2.setObjectName(_fromUtf8("tab4_tab2_1_used2"))
        self.gridLayout_3.addWidget(self.tab4_tab2_1_used2, 0, 3, 1, 1)
        self.tab4_tab2_1_used4 = QtGui.QRadioButton("Used", self.tab4_tab2_1_layout)
        self.tab4_tab2_1_used4.setObjectName(_fromUtf8("tab4_tab2_1_used4"))
        self.gridLayout_3.addWidget(self.tab4_tab2_1_used4, 1, 3, 1, 1)
        self.tab4_tab2_1_slot1 = QtGui.QPushButton("Empty Spell Slot", self.tab4_tab2_1_layout)
        self.tab4_tab2_1_slot1.setObjectName(_fromUtf8("tab4_tab2_1_slot1"))
        self.gridLayout_3.addWidget(self.tab4_tab2_1_slot1, 0, 0, 1, 1)
        self.tab4_tab2_1_slot3 = QtGui.QPushButton("Empty Spell Slot", self.tab4_tab2_1_layout)
        self.tab4_tab2_1_slot3.setObjectName(_fromUtf8("tab4_tab2_1_slot3"))
        self.gridLayout_3.addWidget(self.tab4_tab2_1_slot3, 1, 0, 1, 1)
        self.tab4_tab2_1_slot2 = QtGui.QPushButton("Empty Spell Slot", self.tab4_tab2_1_layout)
        self.tab4_tab2_1_slot2.setObjectName(_fromUtf8("tab4_tab2_1_slot2"))
        self.gridLayout_3.addWidget(self.tab4_tab2_1_slot2, 0, 2, 1, 1)
        self.tab4_tab2_1_slot4 = QtGui.QPushButton("Empty Spell Slot", self.tab4_tab2_1_layout)
        self.tab4_tab2_1_slot4.setObjectName(_fromUtf8("tab4_tab2_1_slot4"))
        self.gridLayout_3.addWidget(self.tab4_tab2_1_slot4, 1, 2, 1, 1)
        self.verticalLayout_12.addWidget(self.tab4_tab2_1_layout)
        # 2nd level
        self.tab4_tab2_2_layout = QtGui.QGroupBox("2nd Level", self.tab4_tab2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tab4_tab2_2_layout.sizePolicy().hasHeightForWidth())
        self.tab4_tab2_2_layout.setSizePolicy(sizePolicy)
        self.tab4_tab2_2_layout.setObjectName(_fromUtf8("tab4_tab2_2_layout"))
        self.verticalLayout_12.addWidget(self.tab4_tab2_2_layout)
        # 3rd level
        self.tab4_tab2_3_layout = QtGui.QGroupBox("3rd Level", self.tab4_tab2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tab4_tab2_3_layout.sizePolicy().hasHeightForWidth())
        self.tab4_tab2_3_layout.setSizePolicy(sizePolicy)
        self.tab4_tab2_3_layout.setObjectName(_fromUtf8("tab4_tab2_3_layout"))
        self.verticalLayout_12.addWidget(self.tab4_tab2_3_layout)
        self.tab4_tab2_lower_layout = QtGui.QGridLayout()
        self.tab4_tab2_lower_layout.setObjectName(_fromUtf8("tab4_tab2_lower_layout"))
        # 4th level
        self.tab4_tab2_4_layout = QtGui.QGroupBox("4th Level", self.tab4_tab2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tab4_tab2_4_layout.sizePolicy().hasHeightForWidth())
        self.tab4_tab2_4_layout.setSizePolicy(sizePolicy)
        self.tab4_tab2_4_layout.setObjectName(_fromUtf8("tab4_tab2_4_layout"))
        self.tab4_tab2_lower_layout.addWidget(self.tab4_tab2_4_layout, 1, 0, 1, 1)
        # 5th level
        self.tab4_tab2_5_layout = QtGui.QGroupBox("5th Level", self.tab4_tab2)
        self.tab4_tab2_5_layout.setObjectName(_fromUtf8("tab4_tab2_5_layout"))
        self.tab4_tab2_lower_layout.addWidget(self.tab4_tab2_5_layout, 1, 1, 1, 1)
        # 6th level
        self.tab4_tab2_6_layout = QtGui.QGroupBox("6th Level", self.tab4_tab2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tab4_tab2_6_layout.sizePolicy().hasHeightForWidth())
        self.tab4_tab2_6_layout.setSizePolicy(sizePolicy)
        self.tab4_tab2_6_layout.setObjectName(_fromUtf8("tab4_tab2_6_layout"))
        # 7th level
        self.tab4_tab2_lower_layout.addWidget(self.tab4_tab2_6_layout, 2, 0, 1, 1)
        self.tab4_tab2_7_layout = QtGui.QGroupBox("7th Level", self.tab4_tab2)
        self.tab4_tab2_7_layout.setObjectName(_fromUtf8("tab4_tab2_7_layout"))
        self.tab4_tab2_lower_layout.addWidget(self.tab4_tab2_7_layout, 2, 1, 1, 1)
        # 8th level
        self.tab4_tab2_8_layout = QtGui.QGroupBox("8th Level", self.tab4_tab2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tab4_tab2_8_layout.sizePolicy().hasHeightForWidth())
        self.tab4_tab2_8_layout.setSizePolicy(sizePolicy)
        self.tab4_tab2_8_layout.setObjectName(_fromUtf8("tab4_tab2_8_layout"))
        self.tab4_tab2_lower_layout.addWidget(self.tab4_tab2_8_layout, 3, 0, 1, 1)
        # 9th level
        self.tab4_tab2_9_layout = QtGui.QGroupBox("9th Level", self.tab4_tab2)
        self.tab4_tab2_9_layout.setObjectName(_fromUtf8("tab4_tab2_9_layout"))
        self.tab4_tab2_lower_layout.addWidget(self.tab4_tab2_9_layout, 3, 1, 1, 1)
        self.verticalLayout_12.addLayout(self.tab4_tab2_lower_layout)
        self.tab4_spell_tab.addTab(self.tab4_tab2, "Spell Slots")

        # Trait
        self.tab4_tab3 = QtGui.QWidget()
        self.tab4_tab3.setObjectName(_fromUtf8("tab4_tab3"))
        self.horizontalLayout_40 = QtGui.QHBoxLayout(self.tab4_tab3)
        self.horizontalLayout_40.setObjectName(_fromUtf8("horizontalLayout_40"))
        self.tab4_tab3_tree = QtGui.QTreeWidget(self.tab4_tab3)
        self.tab4_tab3_tree.setObjectName(_fromUtf8("tab4_tab3_tree"))
        self.tab4_tab3_tree.headerItem().setText(0, "Name")
        self.tab4_tab3_tree.headerItem().setText(1, "Max uses")
        self.horizontalLayout_40.addWidget(self.tab4_tab3_tree)
        self.tab4_tab3_description = QtGui.QTextBrowser(self.tab4_tab3)
        self.tab4_tab3_description.setObjectName(_fromUtf8("tab4_tab3_description"))
        self.horizontalLayout_40.addWidget(self.tab4_tab3_description)
        self.tab4_spell_tab.addTab(self.tab4_tab3, "Trait")

        self.verticalLayout_3.addWidget(self.tab4_spell_tab)
        self.main_tab.addTab(self.tab4, "Spells/Traits")

        
    def setupBackground(self):
        self.tab5 = QtGui.QWidget()
        self.tab5.setObjectName(_fromUtf8("tab5"))
        self.verticalLayout_10 = QtGui.QVBoxLayout(self.tab5)
        self.verticalLayout_10.setObjectName(_fromUtf8("verticalLayout_10"))
        # background
        self.tab5_background_layout = QtGui.QGroupBox("Background", self.tab5)
        self.tab5_background_layout.setObjectName(_fromUtf8("tab5_background_layout"))
        self.horizontalLayout_16 = QtGui.QHBoxLayout(self.tab5_background_layout)
        self.horizontalLayout_16.setObjectName(_fromUtf8("horizontalLayout_16"))
        self.tab5_background_choice_layout = QtGui.QVBoxLayout()
        self.tab5_background_choice_layout.setObjectName(_fromUtf8("tab5_background_choice_layout"))
        self.tab5_full_random_button = QtGui.QPushButton("Full Random", self.tab5_background_layout)
        self.tab5_full_random_button.clicked.connect(self.fullRandomBackground)
        self.tab5_full_random_button.setObjectName(_fromUtf8("tab5_full_random_button"))
        self.tab5_background_choice_layout.addWidget(self.tab5_full_random_button)
        self.tab5_background_combo = QtGui.QComboBox(self.tab5_background_layout)
        self.tab5_background_combo.setObjectName(_fromUtf8("tab5_background_combo"))
        for i in self.background_parser.getListBackground():
            self.tab5_background_combo.addItem(i)

        self.tab5_background_choice_layout.addWidget(self.tab5_background_combo)
        self.tab5_random_personality_button = QtGui.QPushButton("Random Personality", self.tab5_background_layout)
        self.tab5_random_personality_button.clicked.connect(self.randomPersonality)

        self.tab5_random_personality_button.setObjectName(_fromUtf8("tab5_random_personality_button"))
        self.tab5_background_choice_layout.addWidget(self.tab5_random_personality_button)
        self.horizontalLayout_16.addLayout(self.tab5_background_choice_layout)
        self.tab5_background_description = QtGui.QTextBrowser(self.tab5_background_layout)
        self.tab5_background_description.setObjectName(_fromUtf8("tab5_background_description"))
        self.tab5_background_combo.activated[str].connect(self.changeBackground)
        self.horizontalLayout_16.addWidget(self.tab5_background_description)
        self.verticalLayout_10.addWidget(self.tab5_background_layout)
        self.tab5_lower_layout = QtGui.QVBoxLayout()
        self.tab5_lower_layout.setObjectName(_fromUtf8("tab5_lower_layout"))
        # choice
        self.tab5_choice_layout = QtGui.QGroupBox("Choices", self.tab5)
        self.tab5_choice_layout.setObjectName(_fromUtf8("tab5_choice_layout"))
        self.horizontalLayout_33 = QtGui.QHBoxLayout(self.tab5_choice_layout)
        #
        self.tab5_choice_list = []
        self.tab5_lower_layout.addWidget(self.tab5_choice_layout)
        # personality
        self.tab5_personality_layout = QtGui.QGroupBox("Personality", self.tab5)
        self.tab5_personality_layout.setObjectName(_fromUtf8("tab5_personality_layout"))
        self.horizontalLayout_12 = QtGui.QHBoxLayout(self.tab5_personality_layout)
        self.horizontalLayout_12.setObjectName(_fromUtf8("horizontalLayout_12"))
        self.tab5_personality_choice_layout = QtGui.QVBoxLayout()
        self.tab5_personality_choice_layout.setObjectName(_fromUtf8("tab5_personality_choice_layout"))
        self.tab5_personality_spinbox_1 = QtGui.QSpinBox(self.tab5_personality_layout)
        self.tab5_personality_spinbox_1.setMinimum(1)
        self.tab5_personality_spinbox_1.valueChanged.connect(self.changePersonalityDescription)
        self.tab5_personality_spinbox_1.setObjectName(_fromUtf8("tab5_personality_spinbox_1"))
        self.tab5_personality_choice_layout.addWidget(self.tab5_personality_spinbox_1)
        self.tab5_personality_spinbox_2 = QtGui.QSpinBox(self.tab5_personality_layout)
        self.tab5_personality_spinbox_2.setMinimum(1)
        self.tab5_personality_spinbox_2.valueChanged.connect(self.changePersonalityDescription)
        self.tab5_personality_spinbox_2.setObjectName(_fromUtf8("tab5_personality_spinbox_2"))
        self.tab5_personality_choice_layout.addWidget(self.tab5_personality_spinbox_2)
        self.horizontalLayout_12.addLayout(self.tab5_personality_choice_layout)
        self.tab5_personality_description = QtGui.QTextBrowser(self.tab5_personality_layout)
        self.tab5_personality_description.setObjectName(_fromUtf8("tab5_personality_description"))
        self.horizontalLayout_12.addWidget(self.tab5_personality_description)
        self.tab5_lower_layout.addWidget(self.tab5_personality_layout)
        # ideal
        self.tab5_ideal_layout = QtGui.QGroupBox("Ideal", self.tab5)
        self.tab5_ideal_layout.setObjectName(_fromUtf8("tab5_ideal_layout"))
        self.horizontalLayout_13 = QtGui.QHBoxLayout(self.tab5_ideal_layout)
        self.horizontalLayout_13.setObjectName(_fromUtf8("horizontalLayout_13"))
        self.tab5_ideal_choice_layout = QtGui.QVBoxLayout()
        self.tab5_ideal_choice_layout.setContentsMargins(0, -1, -1, -1)
        self.tab5_ideal_choice_layout.setObjectName(_fromUtf8("tab5_ideal_choice_layout"))
        self.tab5_ideal_combo = QtGui.QComboBox(self.tab5_ideal_layout)
        self.tab5_ideal_combo.activated[str].connect(self.changeIdealDescription)
        self.tab5_ideal_combo.setObjectName(_fromUtf8("tab5_ideal_combo"))        
        self.tab5_ideal_choice_layout.addWidget(self.tab5_ideal_combo)
        self.tab5_alignment_combo = QtGui.QComboBox(self.tab5_ideal_layout)
        self.tab5_alignment_combo.setMinimumSize(QtCore.QSize(120, 0))
        self.tab5_alignment_combo.setObjectName(_fromUtf8("tab5_alignment_combo"))
        # alignment
        self.tab5_alignment_combo.addItem("Lawful Good")
        self.tab5_alignment_combo.addItem("Neutral Good")
        self.tab5_alignment_combo.addItem("Chaotic Good")
        self.tab5_alignment_combo.addItem("Lawful Neutral")
        self.tab5_alignment_combo.addItem("True Neutral")
        self.tab5_alignment_combo.addItem("Chaotic Neutral")
        self.tab5_alignment_combo.addItem("Lawful Evil")
        self.tab5_alignment_combo.addItem("Neutral Evil")
        self.tab5_alignment_combo.addItem("Chaotic Evil")
        self.tab5_alignment_combo.activated[str].connect(self.character.background.setAlignment)
        self.tab5_ideal_choice_layout.addWidget(self.tab5_alignment_combo)
        self.horizontalLayout_13.addLayout(self.tab5_ideal_choice_layout)
        self.tab5_ideal_description = QtGui.QTextBrowser(self.tab5_ideal_layout)
        self.tab5_ideal_description.setObjectName(_fromUtf8("tab5_ideal_description"))
        self.horizontalLayout_13.addWidget(self.tab5_ideal_description)
        self.tab5_lower_layout.addWidget(self.tab5_ideal_layout)
        # bond
        self.tab5_bond_layout = QtGui.QGroupBox("Bond", self.tab5)
        self.tab5_bond_layout.setObjectName(_fromUtf8("tab5_bond_layout"))
        self.horizontalLayout_15 = QtGui.QHBoxLayout(self.tab5_bond_layout)
        self.horizontalLayout_15.setObjectName(_fromUtf8("horizontalLayout_15"))
        self.tab5_bond_spinbox = QtGui.QSpinBox(self.tab5_bond_layout)
        self.tab5_bond_spinbox.setMinimum(1)
        self.tab5_bond_spinbox.valueChanged.connect(self.changeBondDescription)
        self.tab5_bond_spinbox.setObjectName(_fromUtf8("tab5_bond_spinbox"))
        self.horizontalLayout_15.addWidget(self.tab5_bond_spinbox)
        self.tab5_bond_description = QtGui.QTextBrowser(self.tab5_bond_layout)
        self.tab5_bond_description.setObjectName(_fromUtf8("tab5_bond_description"))
        self.horizontalLayout_15.addWidget(self.tab5_bond_description)
        self.tab5_lower_layout.addWidget(self.tab5_bond_layout)
        # flaw
        self.tab5_flaw_layout = QtGui.QGroupBox("Flaw", self.tab5)
        self.tab5_flaw_layout.setObjectName(_fromUtf8("tab5_flaw_layout"))
        self.horizontalLayout_14 = QtGui.QHBoxLayout(self.tab5_flaw_layout)
        self.horizontalLayout_14.setObjectName(_fromUtf8("horizontalLayout_14"))
        self.tab5_flaw_spinbox = QtGui.QSpinBox(self.tab5_flaw_layout)
        self.tab5_flaw_spinbox.setMinimum(1)
        self.tab5_flaw_spinbox.valueChanged.connect(self.changeFlawDescription)
        self.tab5_flaw_spinbox.setObjectName(_fromUtf8("tab5_flaw_spinbox"))
        self.horizontalLayout_14.addWidget(self.tab5_flaw_spinbox)
        self.tab5_flaw_description = QtGui.QTextBrowser(self.tab5_flaw_layout)
        self.tab5_flaw_description.setObjectName(_fromUtf8("tab5_flaw_description"))
        self.horizontalLayout_14.addWidget(self.tab5_flaw_description)
        self.tab5_lower_layout.addWidget(self.tab5_flaw_layout)
        self.verticalLayout_10.addLayout(self.tab5_lower_layout)

        self.fullRandomBackground()
        self.main_tab.addTab(self.tab5, "Background")

        
    def setupEquipment(self):
        self.tab6 = QtGui.QWidget()
        self.tab6.setObjectName(_fromUtf8("tab6"))
        self.verticalLayout_6 = QtGui.QVBoxLayout(self.tab6)
        self.verticalLayout_6.setObjectName(_fromUtf8("verticalLayout_6"))
        self.tab6_tabwidget = QtGui.QTabWidget(self.tab6)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tab6_tabwidget.sizePolicy().hasHeightForWidth())
        self.tab6_tabwidget.setSizePolicy(sizePolicy)
        self.tab6_tabwidget.setObjectName(_fromUtf8("tab6_tabwidget"))

        # weapons
        self.tab6_tab0 = QtGui.QWidget()
        self.tab6_tab0.setObjectName(_fromUtf8("tab6_tab0"))
        self.horizontalLayout_11 = QtGui.QHBoxLayout(self.tab6_tab0)
        self.horizontalLayout_11.setObjectName(_fromUtf8("horizontalLayout_11"))
        # list
        self.tab6_tab0_list_layout = QtGui.QGroupBox("List", self.tab6_tab0)
        self.tab6_tab0_list_layout.setObjectName(_fromUtf8("tab6_tab0_list_layout"))
        self.horizontalLayout_31 = QtGui.QHBoxLayout(self.tab6_tab0_list_layout)
        self.horizontalLayout_31.setObjectName(_fromUtf8("horizontalLayout_31"))
        self.tab6_tab0_list_tree = QtGui.QTreeWidget(self.tab6_tab0_list_layout)
        self.tab6_tab0_list_tree.setRootIsDecorated(True)
        self.tab6_tab0_list_tree.setObjectName(_fromUtf8("tab6_tab0_list_tree"))
        item_0 = QtGui.QTreeWidgetItem(self.tab6_tab0_list_tree)
        item_0 = QtGui.QTreeWidgetItem(self.tab6_tab0_list_tree)
        item_1 = QtGui.QTreeWidgetItem(item_0)
        item_0 = QtGui.QTreeWidgetItem(self.tab6_tab0_list_tree)
        item_0 = QtGui.QTreeWidgetItem(self.tab6_tab0_list_tree)
        self.horizontalLayout_31.addWidget(self.tab6_tab0_list_tree)
        self.horizontalLayout_11.addWidget(self.tab6_tab0_list_layout)
        self.tab6_tab0_list_tree.setSortingEnabled(True)
        self.tab6_tab0_list_tree.headerItem().setText(0, "Name")
        self.tab6_tab0_list_tree.headerItem().setText(1, "Cost")
        self.tab6_tab0_list_tree.headerItem().setText(2, "Damage")
        self.tab6_tab0_list_tree.headerItem().setText(3, "Weight")
        self.tab6_tab0_list_tree.headerItem().setText(4, "Properties")
        __sortingEnabled = self.tab6_tab0_list_tree.isSortingEnabled()
        self.tab6_tab0_list_tree.setSortingEnabled(False)
        self.tab6_tab0_list_tree.topLevelItem(1).setText(0, "Simple Melee Weapons")
        self.tab6_tab0_list_tree.topLevelItem(1).child(0).setText(0, "Club")
        self.tab6_tab0_list_tree.topLevelItem(1).child(0).setText(1, "1sp")
        self.tab6_tab0_list_tree.topLevelItem(1).child(0).setText(2, "1d4 Bludgeoning")
        self.tab6_tab0_list_tree.topLevelItem(1).child(0).setText(3, "2lb.")
        self.tab6_tab0_list_tree.topLevelItem(1).child(0).setText(4, "Light")
        self.tab6_tab0_list_tree.setSortingEnabled(__sortingEnabled)
        # owned
        self.tab6_tab0_owned_layout = QtGui.QGroupBox("Owned", self.tab6_tab0)
        self.tab6_tab0_owned_layout.setObjectName(_fromUtf8("tab6_tab0_owned_layout"))
        self.horizontalLayout_32 = QtGui.QHBoxLayout(self.tab6_tab0_owned_layout)
        self.horizontalLayout_32.setObjectName(_fromUtf8("horizontalLayout_32"))
        self.tab6_tab0_owned_tree = QtGui.QTreeWidget(self.tab6_tab0_owned_layout)
        self.tab6_tab0_owned_tree.setObjectName(_fromUtf8("tab6_tab0_owned_tree"))
        self.horizontalLayout_32.addWidget(self.tab6_tab0_owned_tree)
        self.horizontalLayout_11.addWidget(self.tab6_tab0_owned_layout)
        self.tab6_tab0_owned_layout.setTitle("Weapon Owned")
        self.tab6_tab0_owned_tree.headerItem().setText(0, "Name")
        self.tab6_tab0_owned_tree.headerItem().setText(1, "Cost")
        self.tab6_tab0_owned_tree.headerItem().setText(2, "Damage")
        self.tab6_tab0_owned_tree.headerItem().setText(3, "Weight")
        self.tab6_tab0_owned_tree.headerItem().setText(4, "Properties")
        self.tab6_tabwidget.addTab(self.tab6_tab0, "Weapons")

        # armor
        self.tab6_tab1 = QtGui.QWidget()
        self.tab6_tab1.setObjectName(_fromUtf8("tab6_tab1"))
        self.horizontalLayout_23 = QtGui.QHBoxLayout(self.tab6_tab1)
        self.horizontalLayout_23.setObjectName(_fromUtf8("horizontalLayout_23"))
        # list
        self.tab6_tab1_list_layout = QtGui.QGroupBox("List", self.tab6_tab1)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tab6_tab1_list_layout.sizePolicy().hasHeightForWidth())
        self.tab6_tab1_list_layout.setSizePolicy(sizePolicy)
        self.tab6_tab1_list_layout.setObjectName(_fromUtf8("tab6_tab1_list_layout"))
        self.horizontalLayout_29 = QtGui.QHBoxLayout(self.tab6_tab1_list_layout)
        self.horizontalLayout_29.setObjectName(_fromUtf8("horizontalLayout_29"))
        self.tab6_tab1_list_tree = QtGui.QTreeWidget(self.tab6_tab1_list_layout)
        self.tab6_tab1_list_tree.setRootIsDecorated(True)
        self.tab6_tab1_list_tree.setObjectName(_fromUtf8("tab6_tab1_list_tree"))
        item_0 = QtGui.QTreeWidgetItem(self.tab6_tab1_list_tree)
        item_1 = QtGui.QTreeWidgetItem(item_0)
        item_1 = QtGui.QTreeWidgetItem(item_0)
        self.tab6_tab1_list_tree.setSortingEnabled(True)
        self.tab6_tab1_list_tree.headerItem().setText(0, "Name")
        self.tab6_tab1_list_tree.headerItem().setText(1, "Cost")
        self.tab6_tab1_list_tree.headerItem().setText(2, "Armor")
        self.tab6_tab1_list_tree.headerItem().setText(3, "Strength")
        self.tab6_tab1_list_tree.headerItem().setText(4, "Stealth")
        self.tab6_tab1_list_tree.headerItem().setText(5, "Weight")
        __sortingEnabled = self.tab6_tab1_list_tree.isSortingEnabled()
        self.tab6_tab1_list_tree.setSortingEnabled(False)
        self.tab6_tab1_list_tree.topLevelItem(0).setText(0, "Light Armor")
        self.tab6_tab1_list_tree.topLevelItem(0).child(0).setText(0, "Padded")
        self.tab6_tab1_list_tree.topLevelItem(0).child(0).setText(1, "5gp")
        self.tab6_tab1_list_tree.topLevelItem(0).child(0).setText(2, "11+Dex")
        self.tab6_tab1_list_tree.topLevelItem(0).child(0).setText(4, "Disadvantage")
        self.tab6_tab1_list_tree.topLevelItem(0).child(0).setText(5, "8lb.")
        self.tab6_tab1_list_tree.setSortingEnabled(__sortingEnabled)
        self.horizontalLayout_29.addWidget(self.tab6_tab1_list_tree)
        self.horizontalLayout_23.addWidget(self.tab6_tab1_list_layout)
        # owned
        self.tab6_tab1_owned_layout = QtGui.QGroupBox("Owned", self.tab6_tab1)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tab6_tab1_owned_layout.sizePolicy().hasHeightForWidth())
        self.tab6_tab1_owned_layout.setSizePolicy(sizePolicy)
        self.tab6_tab1_owned_layout.setObjectName(_fromUtf8("tab6_tab1_owned_layout"))
        self.horizontalLayout_30 = QtGui.QHBoxLayout(self.tab6_tab1_owned_layout)
        self.horizontalLayout_30.setObjectName(_fromUtf8("horizontalLayout_30"))
        self.tab6_tab1_owned_tree = QtGui.QTreeWidget(self.tab6_tab1_owned_layout)
        self.tab6_tab1_owned_tree.setObjectName(_fromUtf8("tab6_tab1_owned_tree"))
        self.tab6_tab1_owned_tree.headerItem().setText(0, "Name")
        self.tab6_tab1_owned_tree.headerItem().setText(1, "Cost")
        self.tab6_tab1_owned_tree.headerItem().setText(2, "Armor")
        self.tab6_tab1_owned_tree.headerItem().setText(3, "Strength")
        self.tab6_tab1_owned_tree.headerItem().setText(4, "Stealth")
        self.tab6_tab1_owned_tree.headerItem().setText(5, "Weight")
        self.horizontalLayout_30.addWidget(self.tab6_tab1_owned_tree)
        self.horizontalLayout_23.addWidget(self.tab6_tab1_owned_layout)
        self.tab6_tabwidget.addTab(self.tab6_tab1, "Armor")

        # Gear
        self.tab6_tab2 = QtGui.QWidget()
        self.tab6_tab2.setObjectName(_fromUtf8("tab6_tab2"))
        self.horizontalLayout_24 = QtGui.QHBoxLayout(self.tab6_tab2)
        self.horizontalLayout_24.setObjectName(_fromUtf8("horizontalLayout_24"))
        # list
        self.tab6_tab2_list_layout = QtGui.QGroupBox("List", self.tab6_tab2)
        self.tab6_tab2_list_layout.setObjectName(_fromUtf8("tab6_tab2_list_layout"))
        self.horizontalLayout_28 = QtGui.QHBoxLayout(self.tab6_tab2_list_layout)
        self.horizontalLayout_28.setObjectName(_fromUtf8("horizontalLayout_28"))
        self.tab6_tab2_list_tree = QtGui.QTreeWidget(self.tab6_tab2_list_layout)
        self.tab6_tab2_list_tree.setObjectName(_fromUtf8("tab6_tab2_list_tree"))
        item_0 = QtGui.QTreeWidgetItem(self.tab6_tab2_list_tree)
        item_0 = QtGui.QTreeWidgetItem(self.tab6_tab2_list_tree)
        item_1 = QtGui.QTreeWidgetItem(item_0)
        item_1 = QtGui.QTreeWidgetItem(item_0)
        item_1 = QtGui.QTreeWidgetItem(item_0)
        item_1 = QtGui.QTreeWidgetItem(item_0)
        item_1 = QtGui.QTreeWidgetItem(item_0)
        item_1 = QtGui.QTreeWidgetItem(item_0)
        item_1 = QtGui.QTreeWidgetItem(item_0)
        self.tab6_tab2_list_tree.headerItem().setText(0, "Name")
        self.tab6_tab2_list_tree.headerItem().setText(1, "Cost")
        self.tab6_tab2_list_tree.headerItem().setText(2, "Weight")
        self.tab6_tab2_list_tree.headerItem().setText(3, "Quantity")
        __sortingEnabled = self.tab6_tab2_list_tree.isSortingEnabled()
        self.tab6_tab2_list_tree.setSortingEnabled(False)
        self.tab6_tab2_list_tree.topLevelItem(0).setText(0, "Abacus")
        self.tab6_tab2_list_tree.topLevelItem(0).setText(1, "2gp")
        self.tab6_tab2_list_tree.topLevelItem(0).setText(2, "2lb.")
        self.tab6_tab2_list_tree.topLevelItem(1).setText(0, "Explorer\'s pack")
        self.tab6_tab2_list_tree.topLevelItem(1).setText(1, "10gp")
        self.tab6_tab2_list_tree.topLevelItem(1).child(0).setText(0, "Backpack")
        self.tab6_tab2_list_tree.topLevelItem(1).child(1).setText(0, "Bedroll")
        self.tab6_tab2_list_tree.topLevelItem(1).child(2).setText(0, "Mess kit")
        self.tab6_tab2_list_tree.topLevelItem(1).child(3).setText(0, "Tinderbox")
        self.tab6_tab2_list_tree.topLevelItem(1).child(4).setText(0, "Torche")
        self.tab6_tab2_list_tree.topLevelItem(1).child(4).setText(3, "10")
        self.tab6_tab2_list_tree.topLevelItem(1).child(5).setText(0, "Ration")
        self.tab6_tab2_list_tree.topLevelItem(1).child(5).setText(3, "10")
        self.tab6_tab2_list_tree.topLevelItem(1).child(6).setText(0, "Waterskin")
        self.tab6_tab2_list_tree.setSortingEnabled(__sortingEnabled)
        self.horizontalLayout_28.addWidget(self.tab6_tab2_list_tree)
        self.horizontalLayout_24.addWidget(self.tab6_tab2_list_layout)
        # owned
        self.tab6_tab2_owned_layout = QtGui.QGroupBox("Owned", self.tab6_tab2)
        self.tab6_tab2_owned_layout.setObjectName(_fromUtf8("tab6_tab2_owned_layout"))
        self.verticalLayout_23 = QtGui.QVBoxLayout(self.tab6_tab2_owned_layout)
        self.verticalLayout_23.setObjectName(_fromUtf8("verticalLayout_23"))
        self.tab6_tab2_owned_tree = QtGui.QTreeWidget(self.tab6_tab2_owned_layout)
        self.tab6_tab2_owned_tree.setObjectName(_fromUtf8("tab6_tab2_owned_tree"))
        self.tab6_tab2_owned_tree.headerItem().setText(0, "Name")
        self.tab6_tab2_owned_tree.headerItem().setText(1, "Cost")
        self.tab6_tab2_owned_tree.headerItem().setText(2, "Weight")
        self.tab6_tab2_owned_tree.headerItem().setText(3, "Quantity")
        self.verticalLayout_23.addWidget(self.tab6_tab2_owned_tree)
        self.horizontalLayout_24.addWidget(self.tab6_tab2_owned_layout)
        self.tab6_tabwidget.addTab(self.tab6_tab2, "Gear")

        # lower part
        self.verticalLayout_6.addWidget(self.tab6_tabwidget)
        self.tab6_gold_layout = QtGui.QHBoxLayout()
        self.tab6_gold_layout.setContentsMargins(0, 0, -1, -1)
        # money
        self.tab6_gold_layout.setObjectName(_fromUtf8("tab6_gold_layout"))
        spacerItem9 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.tab6_gold_layout.addItem(spacerItem9)
        self.tab6_gold_label = QtGui.QLabel("1gp, 2sp, 1cp", self.tab6)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tab6_gold_label.sizePolicy().hasHeightForWidth())
        self.tab6_gold_label.setSizePolicy(sizePolicy)
        self.tab6_gold_label.setAlignment(QtCore.Qt.AlignCenter)
        self.tab6_gold_label.setObjectName(_fromUtf8("tab6_gold_label"))
        self.tab6_gold_layout.addWidget(self.tab6_gold_label)
        spacerItem10 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Minimum)
        self.tab6_gold_layout.addItem(spacerItem10)
        self.tab6_gold_button = QtGui.QPushButton("Earn/Loose Money", self.tab6)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tab6_gold_button.sizePolicy().hasHeightForWidth())
        self.tab6_gold_button.setSizePolicy(sizePolicy)
        self.tab6_gold_button.setObjectName(_fromUtf8("tab6_gold_button"))
        self.tab6_gold_layout.addWidget(self.tab6_gold_button)
        self.verticalLayout_6.addLayout(self.tab6_gold_layout)

        # description
        self.tab6_description_layout = QtGui.QGroupBox("Description", self.tab6)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tab6_description_layout.sizePolicy().hasHeightForWidth())
        self.tab6_description_layout.setSizePolicy(sizePolicy)
        self.tab6_description_layout.setObjectName(_fromUtf8("tab6_description_layout"))
        self.horizontalLayout_25 = QtGui.QHBoxLayout(self.tab6_description_layout)
        self.horizontalLayout_25.setObjectName(_fromUtf8("horizontalLayout_25"))
        self.tab6_buy_layout = QtGui.QVBoxLayout()
        self.tab6_buy_layout.setObjectName(_fromUtf8("tab6_buy_layout"))
        self.tab6_buy_button = QtGui.QPushButton("Buy", self.tab6_description_layout)
        self.tab6_buy_button.setObjectName(_fromUtf8("tab6_buy_button"))
        self.tab6_buy_layout.addWidget(self.tab6_buy_button)
        self.tab6_add_button = QtGui.QPushButton("Add", self.tab6_description_layout)
        self.tab6_add_button.setObjectName(_fromUtf8("tab6_add_button"))
        self.tab6_buy_layout.addWidget(self.tab6_add_button)
        self.horizontalLayout_25.addLayout(self.tab6_buy_layout)
        self.tab6_description = QtGui.QTextBrowser(self.tab6_description_layout)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tab6_description.sizePolicy().hasHeightForWidth())
        self.tab6_description.setSizePolicy(sizePolicy)
        self.tab6_description.setObjectName(_fromUtf8("tab6_description"))
        self.horizontalLayout_25.addWidget(self.tab6_description)
        self.tab6_sell_layout = QtGui.QVBoxLayout()
        self.tab6_sell_layout.setObjectName(_fromUtf8("tab6_sell_layout"))
        self.tab6_sell_button = QtGui.QPushButton("Sell", self.tab6_description_layout)
        self.tab6_sell_button.setObjectName(_fromUtf8("tab6_sell_button"))
        self.tab6_sell_layout.addWidget(self.tab6_sell_button)
        self.tab6_remove_button = QtGui.QPushButton("Remove", self.tab6_description_layout)
        self.tab6_remove_button.setObjectName(_fromUtf8("tab6_remove_button"))
        self.tab6_sell_layout.addWidget(self.tab6_remove_button)
        self.horizontalLayout_25.addLayout(self.tab6_sell_layout)
        self.verticalLayout_6.addWidget(self.tab6_description_layout)
        self.main_tab.addTab(self.tab6, "Equipment")

        
    def setupNotes(self):
        self.tab7 = QtGui.QWidget()
        self.tab7.setObjectName(_fromUtf8("tab7"))
        self.horizontalLayout_21 = QtGui.QHBoxLayout(self.tab7)
        self.horizontalLayout_21.setObjectName(_fromUtf8("horizontalLayout_21"))
        self.tab7_notes = QtGui.QPlainTextEdit(self.tab7)
        self.tab7_notes.setObjectName(_fromUtf8("tab7_notes"))
        self.horizontalLayout_21.addWidget(self.tab7_notes)
        self.main_tab.addTab(self.tab7, "Notes")

        
    def setupStat(self):
        self.tab8 = QtGui.QWidget()
        self.tab8.setObjectName(_fromUtf8("tab8"))
        self.horizontalLayout_38 = QtGui.QHBoxLayout(self.tab8)
        self.horizontalLayout_38.setObjectName(_fromUtf8("horizontalLayout_38"))
        self.tab8_abilities_proficiencies_layout = QtGui.QVBoxLayout()
        self.tab8_abilities_proficiencies_layout.setObjectName(_fromUtf8("tab8_abilities_proficiencies_layout"))
        
        # abilities
        self.tab8_abilities_layout = QtGui.QGroupBox("Abilities", self.tab8)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tab8_abilities_layout.sizePolicy().hasHeightForWidth())
        self.tab8_abilities_layout.setSizePolicy(sizePolicy)
        self.tab8_abilities_layout.setObjectName(_fromUtf8("tab8_abilities_layout"))
        self.gridLayout_5 = QtGui.QGridLayout(self.tab8_abilities_layout)
        self.gridLayout_5.setObjectName(_fromUtf8("gridLayout_5"))
        self.tab8_abilities_up_layout = QtGui.QGridLayout()
        self.tab8_abilities_up_layout.setContentsMargins(-1, 0, -1, -1)
        self.tab8_abilities_up_layout.setObjectName(_fromUtf8("tab8_abilities_up_layout"))
        self.tab8_str_label = QtGui.QLabel("Strength", self.tab8_abilities_layout)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tab8_str_label.sizePolicy().hasHeightForWidth())
        self.tab8_str_label.setSizePolicy(sizePolicy)
        self.tab8_str_label.setMinimumSize(QtCore.QSize(0, 20))
        self.tab8_str_label.setMaximumSize(QtCore.QSize(16777215, 10))
        self.tab8_str_label.setAlignment(QtCore.Qt.AlignCenter)
        self.tab8_str_label.setObjectName(_fromUtf8("tab8_str_label"))
        self.tab8_abilities_up_layout.addWidget(self.tab8_str_label, 0, 0, 1, 1)
        self.tab8_dex_label = QtGui.QLabel("Dexterity", self.tab8_abilities_layout)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tab8_dex_label.sizePolicy().hasHeightForWidth())
        self.tab8_dex_label.setSizePolicy(sizePolicy)
        self.tab8_dex_label.setMinimumSize(QtCore.QSize(0, 20))
        self.tab8_dex_label.setMaximumSize(QtCore.QSize(16777215, 10))
        self.tab8_dex_label.setAlignment(QtCore.Qt.AlignCenter)
        self.tab8_dex_label.setObjectName(_fromUtf8("tab8_dex_label"))
        self.tab8_abilities_up_layout.addWidget(self.tab8_dex_label, 0, 1, 1, 1)
        self.tab8_con_label = QtGui.QLabel("Constitution", self.tab8_abilities_layout)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tab8_con_label.sizePolicy().hasHeightForWidth())
        self.tab8_con_label.setSizePolicy(sizePolicy)
        self.tab8_con_label.setMinimumSize(QtCore.QSize(0, 20))
        self.tab8_con_label.setMaximumSize(QtCore.QSize(16777215, 10))
        self.tab8_con_label.setAlignment(QtCore.Qt.AlignCenter)
        self.tab8_con_label.setObjectName(_fromUtf8("tab8_con_label"))
        self.tab8_abilities_up_layout.addWidget(self.tab8_con_label, 0, 2, 1, 1)
        self.tab8_str_value = QtGui.QLabel("12 (+1)", self.tab8_abilities_layout)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tab8_str_value.sizePolicy().hasHeightForWidth())
        self.tab8_str_value.setSizePolicy(sizePolicy)
        self.tab8_str_value.setMinimumSize(QtCore.QSize(0, 20))
        self.tab8_str_value.setMaximumSize(QtCore.QSize(16777215, 10))
        self.tab8_str_value.setAlignment(QtCore.Qt.AlignCenter)
        self.tab8_str_value.setObjectName(_fromUtf8("tab8_str_value"))
        self.tab8_abilities_up_layout.addWidget(self.tab8_str_value, 1, 0, 1, 1)
        self.tab8_dex_value = QtGui.QLabel("11 (+0)", self.tab8_abilities_layout)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tab8_dex_value.sizePolicy().hasHeightForWidth())
        self.tab8_dex_value.setSizePolicy(sizePolicy)
        self.tab8_dex_value.setMinimumSize(QtCore.QSize(0, 20))
        self.tab8_dex_value.setMaximumSize(QtCore.QSize(16777215, 10))
        self.tab8_dex_value.setAlignment(QtCore.Qt.AlignCenter)
        self.tab8_dex_value.setObjectName(_fromUtf8("tab8_dex_value"))
        self.tab8_abilities_up_layout.addWidget(self.tab8_dex_value, 1, 1, 1, 1)
        self.tab8_con_value = QtGui.QLabel("9 (-1)", self.tab8_abilities_layout)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tab8_con_value.sizePolicy().hasHeightForWidth())
        self.tab8_con_value.setSizePolicy(sizePolicy)
        self.tab8_con_value.setMinimumSize(QtCore.QSize(0, 20))
        self.tab8_con_value.setMaximumSize(QtCore.QSize(16777215, 10))
        self.tab8_con_value.setAlignment(QtCore.Qt.AlignCenter)
        self.tab8_con_value.setObjectName(_fromUtf8("tab8_con_value"))
        self.tab8_abilities_up_layout.addWidget(self.tab8_con_value, 1, 2, 1, 1)
        self.gridLayout_5.addLayout(self.tab8_abilities_up_layout, 0, 0, 1, 1)
        self.tab8_abilities_sub_layout = QtGui.QGridLayout()
        self.tab8_abilities_sub_layout.setContentsMargins(-1, 10, -1, 10)
        self.tab8_abilities_sub_layout.setObjectName(_fromUtf8("tab8_abilities_sub_layout"))
        self.tab8_wis_label = QtGui.QLabel("Wisdom", self.tab8_abilities_layout)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tab8_wis_label.sizePolicy().hasHeightForWidth())
        self.tab8_wis_label.setSizePolicy(sizePolicy)
        self.tab8_wis_label.setMinimumSize(QtCore.QSize(0, 20))
        self.tab8_wis_label.setMaximumSize(QtCore.QSize(16777215, 10))
        self.tab8_wis_label.setAlignment(QtCore.Qt.AlignCenter)
        self.tab8_wis_label.setObjectName(_fromUtf8("tab8_wis_label"))
        self.tab8_abilities_sub_layout.addWidget(self.tab8_wis_label, 0, 1, 1, 1)
        self.tab8_cha_label = QtGui.QLabel("Charisma", self.tab8_abilities_layout)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tab8_cha_label.sizePolicy().hasHeightForWidth())
        self.tab8_cha_label.setSizePolicy(sizePolicy)
        self.tab8_cha_label.setMinimumSize(QtCore.QSize(0, 20))
        self.tab8_cha_label.setMaximumSize(QtCore.QSize(16777215, 10))
        self.tab8_cha_label.setAlignment(QtCore.Qt.AlignCenter)
        self.tab8_cha_label.setObjectName(_fromUtf8("tab8_cha_label"))
        self.tab8_abilities_sub_layout.addWidget(self.tab8_cha_label, 0, 2, 1, 1)
        self.tab8_int_label = QtGui.QLabel("Intelligence", self.tab8_abilities_layout)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tab8_int_label.sizePolicy().hasHeightForWidth())
        self.tab8_int_label.setSizePolicy(sizePolicy)
        self.tab8_int_label.setMinimumSize(QtCore.QSize(0, 20))
        self.tab8_int_label.setMaximumSize(QtCore.QSize(16777215, 10))
        self.tab8_int_label.setAlignment(QtCore.Qt.AlignCenter)
        self.tab8_int_label.setObjectName(_fromUtf8("tab8_int_label"))
        self.tab8_abilities_sub_layout.addWidget(self.tab8_int_label, 0, 0, 1, 1)
        self.tab8_int_value = QtGui.QLabel("16 (+3)", self.tab8_abilities_layout)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tab8_int_value.sizePolicy().hasHeightForWidth())
        self.tab8_int_value.setSizePolicy(sizePolicy)
        self.tab8_int_value.setMinimumSize(QtCore.QSize(0, 20))
        self.tab8_int_value.setMaximumSize(QtCore.QSize(16777215, 10))
        self.tab8_int_value.setAlignment(QtCore.Qt.AlignCenter)
        self.tab8_int_value.setObjectName(_fromUtf8("tab8_int_value"))
        self.tab8_abilities_sub_layout.addWidget(self.tab8_int_value, 1, 0, 1, 1)
        self.tab8_wis_value = QtGui.QLabel("10 (+0)", self.tab8_abilities_layout)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tab8_wis_value.sizePolicy().hasHeightForWidth())
        self.tab8_wis_value.setSizePolicy(sizePolicy)
        self.tab8_wis_value.setMinimumSize(QtCore.QSize(0, 20))
        self.tab8_wis_value.setMaximumSize(QtCore.QSize(16777215, 10))
        self.tab8_wis_value.setAlignment(QtCore.Qt.AlignCenter)
        self.tab8_wis_value.setObjectName(_fromUtf8("tab8_wis_value"))
        self.tab8_abilities_sub_layout.addWidget(self.tab8_wis_value, 1, 1, 1, 1)
        self.tab8_cha_value = QtGui.QLabel("10 (+0)", self.tab8_abilities_layout)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tab8_cha_value.sizePolicy().hasHeightForWidth())
        self.tab8_cha_value.setSizePolicy(sizePolicy)
        self.tab8_cha_value.setMinimumSize(QtCore.QSize(0, 20))
        self.tab8_cha_value.setMaximumSize(QtCore.QSize(16777215, 10))
        self.tab8_cha_value.setAlignment(QtCore.Qt.AlignCenter)
        self.tab8_cha_value.setObjectName(_fromUtf8("tab8_cha_value"))
        self.tab8_abilities_sub_layout.addWidget(self.tab8_cha_value, 1, 2, 1, 1)
        self.gridLayout_5.addLayout(self.tab8_abilities_sub_layout, 1, 0, 1, 1)

        # proficiencies
        self.tab8_abilities_proficiencies_layout.addWidget(self.tab8_abilities_layout)
        self.tab8_proficiencies_layout = QtGui.QGroupBox("Proficiencies", self.tab8)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tab8_proficiencies_layout.sizePolicy().hasHeightForWidth())
        self.tab8_proficiencies_layout.setSizePolicy(sizePolicy)
        self.tab8_proficiencies_layout.setObjectName(_fromUtf8("tab8_proficiencies_layout"))
        self.gridLayout_11 = QtGui.QGridLayout(self.tab8_proficiencies_layout)
        self.gridLayout_11.setObjectName(_fromUtf8("gridLayout_11"))
        self.tab8_saving_layout = QtGui.QGroupBox("Saving Throws", self.tab8_proficiencies_layout)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tab8_saving_layout.sizePolicy().hasHeightForWidth())
        self.tab8_saving_layout.setSizePolicy(sizePolicy)
        self.tab8_saving_layout.setObjectName(_fromUtf8("tab8_saving_layout"))
        self.gridLayout_12 = QtGui.QGridLayout(self.tab8_saving_layout)
        self.gridLayout_12.setObjectName(_fromUtf8("gridLayout_12"))
        self.tab8_saving_1_label = QtGui.QLabel("Dexterity", self.tab8_saving_layout)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tab8_saving_1_label.sizePolicy().hasHeightForWidth())
        self.tab8_saving_1_label.setSizePolicy(sizePolicy)
        self.tab8_saving_1_label.setMinimumSize(QtCore.QSize(20, 0))
        self.tab8_saving_1_label.setAlignment(QtCore.Qt.AlignCenter)
        self.tab8_saving_1_label.setObjectName(_fromUtf8("tab8_saving_1_label"))
        self.gridLayout_12.addWidget(self.tab8_saving_1_label, 0, 0, 1, 1)
        self.tab8_saving_2_label = QtGui.QLabel("Intelligence", self.tab8_saving_layout)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tab8_saving_2_label.sizePolicy().hasHeightForWidth())
        self.tab8_saving_2_label.setSizePolicy(sizePolicy)
        self.tab8_saving_2_label.setMinimumSize(QtCore.QSize(20, 0))
        self.tab8_saving_2_label.setAlignment(QtCore.Qt.AlignCenter)
        self.tab8_saving_2_label.setObjectName(_fromUtf8("tab8_saving_2_label"))
        self.gridLayout_12.addWidget(self.tab8_saving_2_label, 0, 1, 1, 1)
        self.gridLayout_11.addWidget(self.tab8_saving_layout, 0, 0, 1, 1)
        # skills
        self.tab8_skill_layout = QtGui.QGroupBox("Skills", self.tab8_proficiencies_layout)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tab8_skill_layout.sizePolicy().hasHeightForWidth())
        self.tab8_skill_layout.setSizePolicy(sizePolicy)
        self.tab8_skill_layout.setObjectName(_fromUtf8("tab8_skill_layout"))
        self.gridLayout_13 = QtGui.QGridLayout(self.tab8_skill_layout)
        self.gridLayout_13.setObjectName(_fromUtf8("gridLayout_13"))
        self.tab8_skill3 = QtGui.QLabel("Insight (Wisdom +2)", self.tab8_skill_layout)
        self.tab8_skill3.setObjectName(_fromUtf8("tab8_skill3"))
        self.gridLayout_13.addWidget(self.tab8_skill3, 1, 1, 1, 1)
        self.tab8_skill2 = QtGui.QLabel("Religion (Wisdom +2)", self.tab8_skill_layout)
        self.tab8_skill2.setObjectName(_fromUtf8("tab8_skill2"))
        self.gridLayout_13.addWidget(self.tab8_skill2, 1, 0, 1, 1)
        self.tab8_skill4 = QtGui.QLabel("Club (Strength +2)", self.tab8_skill_layout)
        self.tab8_skill4.setObjectName(_fromUtf8("tab8_skill4"))
        self.gridLayout_13.addWidget(self.tab8_skill4, 2, 0, 1, 1)
        self.tab8_skill5 = QtGui.QLabel("Survival (Wisdom +2)", self.tab8_skill_layout)
        self.tab8_skill5.setObjectName(_fromUtf8("tab8_skill5"))
        self.gridLayout_13.addWidget(self.tab8_skill5, 2, 1, 1, 1)
        self.tab8_skill6 = QtGui.QLabel("Ligth Armor", self.tab8_skill_layout)
        self.tab8_skill6.setObjectName(_fromUtf8("tab8_skill6"))
        self.gridLayout_13.addWidget(self.tab8_skill6, 3, 0, 1, 1)
        self.tab8_skill7 = QtGui.QLabel("Perception (Wisdom +2)", self.tab8_skill_layout)
        self.tab8_skill7.setObjectName(_fromUtf8("tab8_skill7"))
        self.gridLayout_13.addWidget(self.tab8_skill7, 3, 1, 1, 1)
        self.tab8_skill1 = QtGui.QLabel("Shortsword (Dexterity +2)", self.tab8_skill_layout)
        self.tab8_skill1.setObjectName(_fromUtf8("tab8_skill1"))
        self.gridLayout_13.addWidget(self.tab8_skill1, 0, 1, 1, 1)
        self.tab8_passive_perc = QtGui.QLabel("Passive Perception (12)", self.tab8_skill_layout)
        self.tab8_passive_perc.setObjectName(_fromUtf8("tab8_passive_perc"))
        self.gridLayout_13.addWidget(self.tab8_passive_perc, 0, 0, 1, 1)
        self.gridLayout_11.addWidget(self.tab8_skill_layout, 1, 0, 1, 1)
        self.tab8_abilities_proficiencies_layout.addWidget(self.tab8_proficiencies_layout)
        self.horizontalLayout_38.addLayout(self.tab8_abilities_proficiencies_layout)

        # right part
        self.tab8_right_layout = QtGui.QGroupBox(self.tab8)
        self.tab8_right_layout.setTitle(_fromUtf8(""))
        self.tab8_right_layout.setObjectName(_fromUtf8("tab8_right_layout"))
        self.verticalLayout_16 = QtGui.QVBoxLayout(self.tab8_right_layout)
        self.verticalLayout_16.setObjectName(_fromUtf8("verticalLayout_16"))
        self.tab8_hit_layout = QtGui.QGridLayout()
        self.tab8_hit_layout.setObjectName(_fromUtf8("tab8_hit_layout"))
        # 1st line
        self.tab8_ac_label = QtGui.QLabel("Armor Class", self.tab8_right_layout)
        self.tab8_ac_label.setAlignment(QtCore.Qt.AlignCenter)
        self.tab8_ac_label.setObjectName(_fromUtf8("tab8_ac_label"))
        self.tab8_hit_layout.addWidget(self.tab8_ac_label, 0, 2, 1, 1)
        self.tab8_max_hit_points_label = QtGui.QLabel("Max Hit Points", self.tab8_right_layout)
        self.tab8_max_hit_points_label.setObjectName(_fromUtf8("tab8_max_hit_points_label"))
        self.tab8_max_hit_points_label.setAlignment(QtCore.Qt.AlignCenter)
        self.tab8_hit_layout.addWidget(self.tab8_max_hit_points_label, 0, 1, 1, 1)
        self.tab8_hit_points_value = QtGui.QLabel("10", self.tab8_right_layout)
        self.tab8_hit_points_value.setObjectName(_fromUtf8("tab8_hit_points_value"))
        self.tab8_hit_points_value.setAlignment(QtCore.Qt.AlignCenter)
        self.tab8_hit_layout.addWidget(self.tab8_hit_points_value, 1, 0, 1, 1)
        self.tab8_max_hit_points_value = QtGui.QLabel("12", self.tab8_right_layout)
        self.tab8_max_hit_points_value.setObjectName(_fromUtf8("tab8_max_hit_points_value"))
        self.tab8_max_hit_points_value.setAlignment(QtCore.Qt.AlignCenter)
        self.tab8_hit_layout.addWidget(self.tab8_max_hit_points_value, 1, 1, 1, 1)
        self.tab8_ac_value = QtGui.QLabel("+2", self.tab8_right_layout)
        self.tab8_ac_value.setObjectName(_fromUtf8("tab8_ac_value"))
        self.tab8_ac_value.setAlignment(QtCore.Qt.AlignCenter)
        self.tab8_hit_layout.addWidget(self.tab8_ac_value, 1, 2, 1, 1)
        self.tab8_hit_points_label = QtGui.QLabel("Hit Points", self.tab8_right_layout)
        self.tab8_hit_points_label.setObjectName(_fromUtf8("tab8_hit_points_label"))
        self.tab8_hit_points_label.setAlignment(QtCore.Qt.AlignCenter)
        # 2nd line
        self.tab8_hit_layout.addWidget(self.tab8_hit_points_label, 0, 0, 1, 1)
        self.tab8_hit_dice_label = QtGui.QLabel("Hit Dice", self.tab8_right_layout)
        self.tab8_hit_dice_label.setObjectName(_fromUtf8("tab8_hit_dice_label"))
        self.tab8_hit_dice_label.setAlignment(QtCore.Qt.AlignCenter)
        self.tab8_hit_layout.addWidget(self.tab8_hit_dice_label, 2, 0, 1, 1)
        self.tab8_max_hit_dice_label = QtGui.QLabel("Max Hit Dice", self.tab8_right_layout)
        self.tab8_max_hit_dice_label.setObjectName(_fromUtf8("tab8_max_hit_dice_label"))
        self.tab8_max_hit_dice_label.setAlignment(QtCore.Qt.AlignCenter)
        self.tab8_hit_layout.addWidget(self.tab8_max_hit_dice_label, 2, 1, 1, 1)
        self.tab8_max_hit_dice_value = QtGui.QLabel("1d4", self.tab8_right_layout)
        self.tab8_max_hit_dice_value.setObjectName(_fromUtf8("tab8_max_hit_dice_value"))
        self.tab8_max_hit_dice_value.setAlignment(QtCore.Qt.AlignCenter)
        self.tab8_hit_layout.addWidget(self.tab8_max_hit_dice_value, 3, 1, 1, 1)
        self.tab8_speed_label = QtGui.QLabel("Speed", self.tab8_right_layout)
        self.tab8_speed_label.setObjectName(_fromUtf8("tab8_speed_label"))
        self.tab8_speed_label.setAlignment(QtCore.Qt.AlignCenter)
        self.tab8_hit_layout.addWidget(self.tab8_speed_label, 2, 2, 1, 1)
        self.tab8_hit_dice_value = QtGui.QLabel("0d4", self.tab8_right_layout)
        self.tab8_hit_dice_value.setObjectName(_fromUtf8("tab8_hit_dice_value"))
        self.tab8_hit_dice_value.setAlignment(QtCore.Qt.AlignCenter)
        self.tab8_hit_layout.addWidget(self.tab8_hit_dice_value, 3, 0, 1, 1)
        self.tab8_speed_value = QtGui.QLabel("30", self.tab8_right_layout)
        self.tab8_speed_value.setObjectName(_fromUtf8("tab8_speed_value"))
        self.tab8_speed_value.setAlignment(QtCore.Qt.AlignCenter)
        self.tab8_hit_layout.addWidget(self.tab8_speed_value, 3, 2, 1, 1)
        self.verticalLayout_16.addLayout(self.tab8_hit_layout)

        # features
        self.tab8_features_layout = QtGui.QGroupBox("Features", self.tab8_right_layout)
        self.tab8_features_layout.setObjectName(_fromUtf8("tab8_features_layout"))
        self.verticalLayout_28 = QtGui.QVBoxLayout(self.tab8_features_layout)
        self.verticalLayout_28.setObjectName(_fromUtf8("verticalLayout_28"))
        self.tab8_features_tree = QtGui.QTreeWidget(self.tab8_features_layout)
        self.tab8_features_tree.setObjectName(_fromUtf8("tab8_features_tree"))
        item_0 = QtGui.QTreeWidgetItem(self.tab8_features_tree)
        self.tab8_features_tree.headerItem().setText(0, "Name")
        self.tab8_features_tree.headerItem().setText(1, "Max uses")
        __sortingEnabled = self.tab8_features_tree.isSortingEnabled()
        self.tab8_features_tree.setSortingEnabled(False)
        self.tab8_features_tree.topLevelItem(0).setText(0, "Actor")
        self.tab8_features_tree.topLevelItem(0).setText(1, "Unlimited")
        self.tab8_features_tree.setSortingEnabled(__sortingEnabled)
        self.verticalLayout_28.addWidget(self.tab8_features_tree)
        self.verticalLayout_16.addWidget(self.tab8_features_layout)
        # spell
        self.tab8_spell_layout = QtGui.QGroupBox("Spells", self.tab8_right_layout)
        self.tab8_spell_layout.setObjectName(_fromUtf8("tab8_spell_layout"))
        self.horizontalLayout_41 = QtGui.QHBoxLayout(self.tab8_spell_layout)
        self.horizontalLayout_41.setObjectName(_fromUtf8("horizontalLayout_41"))
        self.tab8_spell_tree = QtGui.QTreeWidget(self.tab8_spell_layout)
        self.tab8_spell_tree.setObjectName(_fromUtf8("tab8_spell_tree"))
        item_0 = QtGui.QTreeWidgetItem(self.tab8_spell_tree)
        item_1 = QtGui.QTreeWidgetItem(item_0)
        self.tab8_spell_tree.headerItem().setText(0, "Name")
        self.tab8_spell_tree.headerItem().setText(1, "Type")
        self.tab8_spell_tree.headerItem().setText(2, "Casting time")
        self.tab8_spell_tree.headerItem().setText(3, "Range")
        self.tab8_spell_tree.headerItem().setText(4, "Components")
        self.tab8_spell_tree.headerItem().setText(5, "Duration")
        __sortingEnabled = self.tab8_spell_tree.isSortingEnabled()
        self.tab8_spell_tree.setSortingEnabled(False)
        self.tab8_spell_tree.topLevelItem(0).setText(0, "1st Level")
        self.tab8_spell_tree.topLevelItem(0).child(0).setText(0, "Animal Friendship")
        self.tab8_spell_tree.topLevelItem(0).child(0).setText(1, "Enchantment")
        self.tab8_spell_tree.topLevelItem(0).child(0).setText(2, "1 action")
        self.tab8_spell_tree.topLevelItem(0).child(0).setText(3, "30")
        self.tab8_spell_tree.topLevelItem(0).child(0).setText(4, "V, S, M (a morsel of food)")
        self.tab8_spell_tree.topLevelItem(0).child(0).setText(5, "24h")
        self.tab8_spell_tree.setSortingEnabled(__sortingEnabled)
        self.horizontalLayout_41.addWidget(self.tab8_spell_tree)
        self.verticalLayout_16.addWidget(self.tab8_spell_layout)
        self.horizontalLayout_38.addWidget(self.tab8_right_layout)
        self.main_tab.addTab(self.tab8, "Stats")
        
