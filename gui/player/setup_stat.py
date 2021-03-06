from PyQt4 import QtCore, QtGui

import core.proficiency as proficiency
import gui.tools as tools


try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s
        
def setupStat(self):
    self.tab0 = QtGui.QWidget()
    self.tab0.setObjectName(_fromUtf8("tab0"))
    self.horizontalLayout_38 = QtGui.QHBoxLayout(self.tab0)
    self.horizontalLayout_38.setObjectName(_fromUtf8("horizontalLayout_38"))
    self.tab0_abilities_proficiencies_layout = QtGui.QVBoxLayout()
    self.tab0_abilities_proficiencies_layout.setObjectName(_fromUtf8("tab0_abilities_proficiencies_layout"))
        
    # abilities
    self.tab0_abilities_layout = QtGui.QGroupBox("Abilities", self.tab0)
    sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Minimum)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.tab0_abilities_layout.sizePolicy().hasHeightForWidth())
    self.tab0_abilities_layout.setSizePolicy(sizePolicy)
    self.tab0_abilities_layout.setObjectName(_fromUtf8("tab0_abilities_layout"))
    self.gridLayout_5 = QtGui.QGridLayout(self.tab0_abilities_layout)
    self.gridLayout_5.setObjectName(_fromUtf8("gridLayout_5"))
    self.tab0_abilities_up_layout = QtGui.QGridLayout()
    self.tab0_abilities_up_layout.setContentsMargins(-1, 0, -1, -1)
    self.tab0_abilities_up_layout.setObjectName(_fromUtf8("tab0_abilities_up_layout"))

    self.tab0_str_label = QtGui.QLabel("Strength", self.tab0_abilities_layout)
    sizePolicy.setHeightForWidth(self.tab0_str_label.sizePolicy().hasHeightForWidth())
    self.tab0_str_label.setSizePolicy(sizePolicy)
    self.tab0_str_label.setMinimumSize(QtCore.QSize(0, 20))
    self.tab0_str_label.setMaximumSize(QtCore.QSize(16777215, 10))
    self.tab0_str_label.setAlignment(QtCore.Qt.AlignCenter)
    self.tab0_str_label.setObjectName(_fromUtf8("tab0_str_label"))
    self.tab0_abilities_up_layout.addWidget(self.tab0_str_label, 0, 0, 1, 1)

    self.tab0_dex_label = QtGui.QLabel("Dexterity", self.tab0_abilities_layout)
    sizePolicy.setHeightForWidth(self.tab0_dex_label.sizePolicy().hasHeightForWidth())
    self.tab0_dex_label.setSizePolicy(sizePolicy)
    self.tab0_dex_label.setMinimumSize(QtCore.QSize(0, 20))
    self.tab0_dex_label.setMaximumSize(QtCore.QSize(16777215, 10))
    self.tab0_dex_label.setAlignment(QtCore.Qt.AlignCenter)
    self.tab0_dex_label.setObjectName(_fromUtf8("tab0_dex_label"))
    self.tab0_abilities_up_layout.addWidget(self.tab0_dex_label, 0, 1, 1, 1)

    self.tab0_con_label = QtGui.QLabel("Constitution", self.tab0_abilities_layout)
    sizePolicy.setHeightForWidth(self.tab0_con_label.sizePolicy().hasHeightForWidth())
    self.tab0_con_label.setSizePolicy(sizePolicy)
    self.tab0_con_label.setMinimumSize(QtCore.QSize(0, 20))
    self.tab0_con_label.setMaximumSize(QtCore.QSize(16777215, 10))
    self.tab0_con_label.setAlignment(QtCore.Qt.AlignCenter)
    self.tab0_con_label.setObjectName(_fromUtf8("tab0_con_label"))
    self.tab0_abilities_up_layout.addWidget(self.tab0_con_label, 0, 2, 1, 1)

    self.tab0_str_value = QtGui.QLabel("", self.tab0_abilities_layout)
    sizePolicy.setHeightForWidth(self.tab0_str_value.sizePolicy().hasHeightForWidth())
    self.tab0_str_value.setSizePolicy(sizePolicy)
    self.tab0_str_value.setMinimumSize(QtCore.QSize(0, 20))
    self.tab0_str_value.setMaximumSize(QtCore.QSize(16777215, 10))
    self.tab0_str_value.setAlignment(QtCore.Qt.AlignCenter)
    self.tab0_str_value.setObjectName(_fromUtf8("tab0_str_value"))
    self.tab0_abilities_up_layout.addWidget(self.tab0_str_value, 1, 0, 1, 1)

    self.tab0_dex_value = QtGui.QLabel("", self.tab0_abilities_layout)
    sizePolicy.setHeightForWidth(self.tab0_dex_value.sizePolicy().hasHeightForWidth())
    self.tab0_dex_value.setSizePolicy(sizePolicy)
    self.tab0_dex_value.setMinimumSize(QtCore.QSize(0, 20))
    self.tab0_dex_value.setMaximumSize(QtCore.QSize(16777215, 10))
    self.tab0_dex_value.setAlignment(QtCore.Qt.AlignCenter)
    self.tab0_dex_value.setObjectName(_fromUtf8("tab0_dex_value"))
    self.tab0_abilities_up_layout.addWidget(self.tab0_dex_value, 1, 1, 1, 1)

    self.tab0_con_value = QtGui.QLabel("", self.tab0_abilities_layout)
    sizePolicy.setHeightForWidth(self.tab0_con_value.sizePolicy().hasHeightForWidth())
    self.tab0_con_value.setSizePolicy(sizePolicy)
    self.tab0_con_value.setMinimumSize(QtCore.QSize(0, 20))
    self.tab0_con_value.setMaximumSize(QtCore.QSize(16777215, 10))
    self.tab0_con_value.setAlignment(QtCore.Qt.AlignCenter)
    self.tab0_con_value.setObjectName(_fromUtf8("tab0_con_value"))
    self.tab0_abilities_up_layout.addWidget(self.tab0_con_value, 1, 2, 1, 1)
    self.gridLayout_5.addLayout(self.tab0_abilities_up_layout, 0, 0, 1, 1)
    self.tab0_abilities_sub_layout = QtGui.QGridLayout()
    self.tab0_abilities_sub_layout.setContentsMargins(-1, 10, -1, 10)
    self.tab0_abilities_sub_layout.setObjectName(_fromUtf8("tab0_abilities_sub_layout"))

    self.tab0_wis_label = QtGui.QLabel("Wisdom", self.tab0_abilities_layout)
    sizePolicy.setHeightForWidth(self.tab0_wis_label.sizePolicy().hasHeightForWidth())
    self.tab0_wis_label.setSizePolicy(sizePolicy)
    self.tab0_wis_label.setMinimumSize(QtCore.QSize(0, 20))
    self.tab0_wis_label.setMaximumSize(QtCore.QSize(16777215, 10))
    self.tab0_wis_label.setAlignment(QtCore.Qt.AlignCenter)
    self.tab0_wis_label.setObjectName(_fromUtf8("tab0_wis_label"))
    self.tab0_abilities_sub_layout.addWidget(self.tab0_wis_label, 0, 1, 1, 1)

    self.tab0_cha_label = QtGui.QLabel("Charisma", self.tab0_abilities_layout)
    sizePolicy.setHeightForWidth(self.tab0_cha_label.sizePolicy().hasHeightForWidth())
    self.tab0_cha_label.setSizePolicy(sizePolicy)
    self.tab0_cha_label.setMinimumSize(QtCore.QSize(0, 20))
    self.tab0_cha_label.setMaximumSize(QtCore.QSize(16777215, 10))
    self.tab0_cha_label.setAlignment(QtCore.Qt.AlignCenter)
    self.tab0_cha_label.setObjectName(_fromUtf8("tab0_cha_label"))
    self.tab0_abilities_sub_layout.addWidget(self.tab0_cha_label, 0, 2, 1, 1)

    self.tab0_int_label = QtGui.QLabel("Intelligence", self.tab0_abilities_layout)
    sizePolicy.setHeightForWidth(self.tab0_int_label.sizePolicy().hasHeightForWidth())
    self.tab0_int_label.setSizePolicy(sizePolicy)
    self.tab0_int_label.setMinimumSize(QtCore.QSize(0, 20))
    self.tab0_int_label.setMaximumSize(QtCore.QSize(16777215, 10))
    self.tab0_int_label.setAlignment(QtCore.Qt.AlignCenter)
    self.tab0_int_label.setObjectName(_fromUtf8("tab0_int_label"))
    self.tab0_abilities_sub_layout.addWidget(self.tab0_int_label, 0, 0, 1, 1)

    self.tab0_int_value = QtGui.QLabel("", self.tab0_abilities_layout)
    sizePolicy.setHeightForWidth(self.tab0_int_value.sizePolicy().hasHeightForWidth())
    self.tab0_int_value.setSizePolicy(sizePolicy)
    self.tab0_int_value.setMinimumSize(QtCore.QSize(0, 20))
    self.tab0_int_value.setMaximumSize(QtCore.QSize(16777215, 10))
    self.tab0_int_value.setAlignment(QtCore.Qt.AlignCenter)
    self.tab0_int_value.setObjectName(_fromUtf8("tab0_int_value"))
    self.tab0_abilities_sub_layout.addWidget(self.tab0_int_value, 1, 0, 1, 1)

    self.tab0_wis_value = QtGui.QLabel("", self.tab0_abilities_layout)
    sizePolicy.setHeightForWidth(self.tab0_wis_value.sizePolicy().hasHeightForWidth())
    self.tab0_wis_value.setSizePolicy(sizePolicy)
    self.tab0_wis_value.setMinimumSize(QtCore.QSize(0, 20))
    self.tab0_wis_value.setMaximumSize(QtCore.QSize(16777215, 10))
    self.tab0_wis_value.setAlignment(QtCore.Qt.AlignCenter)
    self.tab0_wis_value.setObjectName(_fromUtf8("tab0_wis_value"))
    self.tab0_abilities_sub_layout.addWidget(self.tab0_wis_value, 1, 1, 1, 1)

    self.tab0_cha_value = QtGui.QLabel("", self.tab0_abilities_layout)
    sizePolicy.setHeightForWidth(self.tab0_cha_value.sizePolicy().hasHeightForWidth())
    self.tab0_cha_value.setSizePolicy(sizePolicy)
    self.tab0_cha_value.setMinimumSize(QtCore.QSize(0, 20))
    self.tab0_cha_value.setMaximumSize(QtCore.QSize(16777215, 10))
    self.tab0_cha_value.setAlignment(QtCore.Qt.AlignCenter)
    self.tab0_cha_value.setObjectName(_fromUtf8("tab0_cha_value"))
    self.tab0_abilities_sub_layout.addWidget(self.tab0_cha_value, 1, 2, 1, 1)
    self.gridLayout_5.addLayout(self.tab0_abilities_sub_layout, 1, 0, 1, 1)
    self.tab0_abilities_proficiencies_layout.addWidget(self.tab0_abilities_layout)

    # proficiencies
    
    self.tab0_proficiencies_layout = QtGui.QGroupBox("Proficiencies", self.tab0)
    sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Expanding)
    sizePolicy.setHeightForWidth(self.tab0_proficiencies_layout.sizePolicy().hasHeightForWidth())
    self.tab0_proficiencies_layout.setSizePolicy(sizePolicy)
    self.tab0_proficiencies_layout.setObjectName(_fromUtf8("tab0_proficiencies_layout"))

    # saving throw
    self.gridLayout_11 = QtGui.QGridLayout(self.tab0_proficiencies_layout)
    self.gridLayout_11.setObjectName(_fromUtf8("gridLayout_11"))
    self.tab0_saving_layout = QtGui.QGroupBox("Saving Throws", self.tab0_proficiencies_layout)
    sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
    self.tab0_saving_layout.setSizePolicy(sizePolicy)
    self.tab0_saving_layout.setObjectName(_fromUtf8("tab0_saving_layout"))
    self.gridLayout_12 = QtGui.QGridLayout(self.tab0_saving_layout)
    self.gridLayout_12.setObjectName(_fromUtf8("gridLayout_12"))
    self.tab0_list_saving = []    
    self.gridLayout_11.addWidget(self.tab0_saving_layout, 0, 0, 1, 1)

    # skills
    self.tab0_list_skill = []
    self.tab0_skill_layout = QtGui.QGroupBox("Skills", self.tab0_proficiencies_layout)
    self.tab0_skill_layout.setSizePolicy(sizePolicy)
    self.tab0_skill_layout.setObjectName(_fromUtf8("tab0_skill_layout"))
    self.gridLayout_13 = QtGui.QGridLayout(self.tab0_skill_layout)
    self.gridLayout_13.setObjectName(_fromUtf8("gridLayout_13"))
    self.gridLayout_11.addWidget(self.tab0_skill_layout, 1, 0, 1, 1)
    self.tab0_abilities_proficiencies_layout.addWidget(self.tab0_proficiencies_layout)

    # object
    self.tab0_list_object = []
    self.tab0_object_layout = QtGui.QGroupBox("Objects", self.tab0_proficiencies_layout)
    self.tab0_object_layout.setSizePolicy(sizePolicy)
    self.tab0_object_layout.setObjectName(_fromUtf8("tab0_object_layout"))
    self.object_gridLayout = QtGui.QGridLayout(self.tab0_object_layout)
    self.object_gridLayout.setObjectName(_fromUtf8("object_gridLayout"))
    self.gridLayout_11.addWidget(self.tab0_object_layout, 2, 0, 1, 1)

    # language
    self.tab0_list_language = []
    self.tab0_language_layout = QtGui.QGroupBox("Languages", self.tab0_proficiencies_layout)
    self.tab0_language_layout.setSizePolicy(sizePolicy)
    self.tab0_language_layout.setObjectName(_fromUtf8("tab0_language_layout"))
    self.lang_gridLayout = QtGui.QGridLayout(self.tab0_language_layout)
    self.lang_gridLayout.setObjectName(_fromUtf8("lang_gridLayout"))
    self.gridLayout_11.addWidget(self.tab0_language_layout, 3, 0, 1, 1)

    loadProficiency(self)
    self.horizontalLayout_38.addLayout(self.tab0_abilities_proficiencies_layout)

    
    # right part
    self.tab0_right_layout = QtGui.QGroupBox(self.tab0)
    self.tab0_right_layout.setTitle(_fromUtf8(""))
    self.tab0_right_layout.setObjectName(_fromUtf8("tab0_right_layout"))
    self.verticalLayout_16 = QtGui.QVBoxLayout(self.tab0_right_layout)
    self.verticalLayout_16.setObjectName(_fromUtf8("verticalLayout_16"))
    self.tab0_hit_layout = QtGui.QGridLayout()
    self.tab0_hit_layout.setObjectName(_fromUtf8("tab0_hit_layout"))
    # 1st line
    self.long_rest_button = QtGui.QPushButton("Long Rest", self.tab0_right_layout)
    self.long_rest_button.clicked.connect(self.longRest)
    sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Maximum)
    self.long_rest_button.setSizePolicy(sizePolicy)
    self.tab0_hit_layout.addWidget(self.long_rest_button, 0, 0, 2, 1)
    self.heal_button = QtGui.QPushButton("Heal", self.tab0_right_layout)
    self.heal_button.clicked.connect(self.heal)
    self.heal_button.setSizePolicy(sizePolicy)
    self.tab0_hit_layout.addWidget(self.heal_button, 2, 0, 2, 1)
    self.tab0_ac_label = QtGui.QLabel("Armor Class", self.tab0_right_layout)
    self.tab0_ac_label.setAlignment(QtCore.Qt.AlignCenter)
    self.tab0_ac_label.setObjectName(_fromUtf8("tab0_ac_label"))
    self.tab0_hit_layout.addWidget(self.tab0_ac_label, 0, 2, 1, 1)
    self.tab0_hit_points_value = QtGui.QLabel("", self.tab0_right_layout)
    self.tab0_hit_points_value.setObjectName(_fromUtf8("tab0_hit_points_value"))
    self.tab0_hit_points_value.setAlignment(QtCore.Qt.AlignCenter)
    self.tab0_hit_layout.addWidget(self.tab0_hit_points_value, 1, 1, 1, 1)
    self.tab0_ac_value = QtGui.QLabel("+2", self.tab0_right_layout)
    self.tab0_ac_value.setObjectName(_fromUtf8("tab0_ac_value"))
    self.tab0_ac_value.setAlignment(QtCore.Qt.AlignCenter)
    self.tab0_hit_layout.addWidget(self.tab0_ac_value, 1, 2, 1, 1)
    self.tab0_hit_points_label = QtGui.QLabel("Hit Points", self.tab0_right_layout)
    self.tab0_hit_points_label.setObjectName(_fromUtf8("tab0_hit_points_label"))
    self.tab0_hit_points_label.setAlignment(QtCore.Qt.AlignCenter)
    self.tab0_hit_layout.addWidget(self.tab0_hit_points_label, 0, 1, 1, 1)
    # 2nd line
    self.tab0_hit_dice_label = QtGui.QLabel("Hit Dice", self.tab0_right_layout)
    self.tab0_hit_dice_label.setObjectName(_fromUtf8("tab0_hit_dice_label"))
    self.tab0_hit_dice_label.setAlignment(QtCore.Qt.AlignCenter)
    self.tab0_hit_layout.addWidget(self.tab0_hit_dice_label, 2, 1, 1, 1)
    self.tab0_speed_label = QtGui.QLabel("Speed", self.tab0_right_layout)
    self.tab0_speed_label.setObjectName(_fromUtf8("tab0_speed_label"))
    self.tab0_speed_label.setAlignment(QtCore.Qt.AlignCenter)
    self.tab0_hit_layout.addWidget(self.tab0_speed_label, 2, 2, 1, 1)
    self.tab0_hit_dice_value = QtGui.QLabel("", self.tab0_right_layout)
    self.tab0_hit_dice_value.setObjectName(_fromUtf8("tab0_hit_dice_value"))
    self.tab0_hit_dice_value.setAlignment(QtCore.Qt.AlignCenter)
    self.tab0_hit_layout.addWidget(self.tab0_hit_dice_value, 3, 1, 1, 1)
    self.tab0_speed_value = QtGui.QLabel("30", self.tab0_right_layout)
    self.tab0_speed_value.setObjectName(_fromUtf8("tab0_speed_value"))
    self.tab0_speed_value.setAlignment(QtCore.Qt.AlignCenter)
    self.tab0_hit_layout.addWidget(self.tab0_speed_value, 3, 2, 1, 1)
    self.verticalLayout_16.addLayout(self.tab0_hit_layout)

    # trait
    self.tab0_trait_layout = QtGui.QGroupBox("Trait", self.tab0_right_layout)
    self.tab0_trait_layout.setObjectName(_fromUtf8("tab0_trait_layout"))
    self.verticalLayout_28 = QtGui.QVBoxLayout(self.tab0_trait_layout)
    self.verticalLayout_28.setObjectName(_fromUtf8("verticalLayout_28"))
    self.tab0_trait_tree = QtGui.QTreeWidget(self.tab0_trait_layout)
    self.tab0_trait_tree.setObjectName(_fromUtf8("tab0_trait_tree"))
    sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Expanding)
    self.tab0_trait_tree.setSizePolicy(sizePolicy)
    item_0 = QtGui.QTreeWidgetItem(self.tab0_trait_tree)
    self.tab0_trait_tree.headerItem().setText(0, "Name")
    self.tab0_trait_tree.headerItem().setText(1, "Max uses")
    __sortingEnabled = self.tab0_trait_tree.isSortingEnabled()
    self.tab0_trait_tree.setSortingEnabled(False)
    self.tab0_trait_tree.topLevelItem(0).setText(0, "Actor")
    self.tab0_trait_tree.topLevelItem(0).setText(1, "Unlimited")
    self.tab0_trait_tree.setSortingEnabled(__sortingEnabled)
    self.verticalLayout_28.addWidget(self.tab0_trait_tree)
    self.verticalLayout_16.addWidget(self.tab0_trait_layout)
    # spell
    self.tab0_spell_layout = QtGui.QGroupBox("Spells", self.tab0_right_layout)
    self.tab0_spell_layout.setObjectName(_fromUtf8("tab0_spell_layout"))
    self.horizontalLayout_41 = QtGui.QHBoxLayout(self.tab0_spell_layout)
    self.horizontalLayout_41.setObjectName(_fromUtf8("horizontalLayout_41"))
    self.tab0_spell_tree = QtGui.QTreeWidget(self.tab0_spell_layout)
    sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Expanding)
    self.tab0_spell_tree.setSizePolicy(sizePolicy)
    self.tab0_spell_tree.setObjectName(_fromUtf8("tab0_spell_tree"))
    self.tab0_spell_tree.headerItem().setText(0, "Name")
    self.tab0_spell_tree.headerItem().setText(1, "Type")
    self.tab0_spell_tree.headerItem().setText(2, "Casting time")
    self.tab0_spell_tree.headerItem().setText(3, "Range")
    self.tab0_spell_tree.headerItem().setText(4, "Components")
    self.tab0_spell_tree.headerItem().setText(5, "Duration")
    self.tab0_spell_tree.setSortingEnabled(True)
    self.horizontalLayout_41.addWidget(self.tab0_spell_tree)
    self.verticalLayout_16.addWidget(self.tab0_spell_layout)
    self.horizontalLayout_38.addWidget(self.tab0_right_layout)
    self.main_tab.addTab(self.tab0, "Stats")

    self.main_tab.currentChanged.connect(self.updateStatList)


def loadProficiency(self):
    # skills
    prof, diff = self.character.getProficiency()
    skills = prof.skills
    j = 0
    for i in range(len(skills)):
        if skills[i]:
            label = QtGui.QLabel(
                tools.choiceLabel(proficiency.SkillProficiency(i).name),
                self.tab0_skill_layout)
            label.setAlignment(QtCore.Qt.AlignCenter)
            self.gridLayout_13.addWidget(label, int(j/3), j%3)
            self.tab0_list_skill.append(label)
            j += 1

    # Saving
    saving = prof.saving
    j = 0
    for i in range(len(saving)):
        if saving[i]:
            label = QtGui.QLabel(
                tools.choiceLabel(proficiency.Ability(i).name),
                self.tab0_saving_layout)
            label.setAlignment(QtCore.Qt.AlignCenter)
            self.gridLayout_12.addWidget(label, int(j/3), j%3)
            self.tab0_list_saving.append(label)
            j += 1

    # Object
    weapon = prof.weapons
    j = tools.createObjectProficiencyLabel(
        self, weapon, proficiency.WeaponProficiency, parent='play',
        column=3)
    tool = prof.tools
    j = tools.createObjectProficiencyLabel(
        self, tool, proficiency.ToolProficiency, j, parent='play',
        column=3)
    armor = prof.armors
    j = tools.createObjectProficiencyLabel(
        self, armor, proficiency.ArmorProficiency, j, parent='play',
        column=3)

    # Languages        
    lang = prof.languages
    j = 0
    for i in range(len(lang)):
        if lang[i]:
            label = QtGui.QLabel(
                tools.choiceLabel(proficiency.LanguageProficiency(i).name),
                self.tab0_language_layout)
            label.setAlignment(QtCore.Qt.AlignCenter)
            self.lang_gridLayout.addWidget(label, int(j/3), j%3)
            self.tab0_list_language.append(label)
            j += 1
