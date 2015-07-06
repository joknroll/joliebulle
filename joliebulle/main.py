#!/usr/bin/python3
#­*­coding: utf­8 -­*­

#joliebulle 3.4
#Copyright (C) 2010-2014 Pierre Tavares
#Copyright (C) 2012-2014 joliebulle's authors
#See AUTHORS file.

#This program is free software; you can redistribute it and/or
#modify it under the terms of the GNU General Public License
#as published by the Free Software Foundation; either version 3        
#of the License, or (at your option) any later version.

#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.

#You should have received a copy of the GNU General Public License
#along with this program; if not, write to the Free Software
#Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
import time

import shutil
import os
import os.path
import glob
import logging
import logging.config
from sys import platform
import PyQt4
import sys
from PyQt4 import QtGui
from PyQt4 import QtCore
from reader_ui import *
from settings import *
from about import *
from base import *
from editgrain import *
from edithoublon import *
from editdivers import * 
from editlevures import *
from helper.toolExporterRepository import *
from helper.libExporterRepository import *
from helper.brewdayExporterRepository import *
from importIng import *
from preBoilDialog import *
from stepEditWindow import *
from mashEditWindow import *
from mashDetail import * 
from exportMash import *
from preferences import *
from home import *
from globals import *
#from ui.MainWindow import *

import xml.etree.ElementTree as ET
from model.recipe import *
from model.journal import *
from model.hop import *
from model import recipe
import model.constants
import view.constants
from view.fermentableview import *
from view.recipeview import *
from view.hopview import *
from view.yeastview import *
from view.mashstepview import *
import view.base
import itertools
from errors import *



def initLogging():
    home = QtCore.QDir(home_dir)
    config = QtCore.QDir(config_dir)
    if not config.exists() :
        home.mkpath (config_dir)
    config = {
        'version': 1,              
        'root': {
            'handlers': ['console'],
            'level': 'DEBUG'
        },
        'disable_existing_loggers': False,
        'formatters': {
            'standard': {
                'format': '%(asctime)s [%(levelname)s]: %(message)s'
            },
            'detailed': {
                'format': '%(asctime)s %(module)-17s line:%(lineno)-4d %(levelname)-8s %(message)s'
            }
        },
        'handlers': {
            'console': {
                'level':'DEBUG',
                'class':'logging.StreamHandler',
                'stream':'ext://sys.stdout',
                'formatter':'standard'
            },
        }
    }
    logging.config.dictConfig(config)


class IngDelegate(QtGui.QItemDelegate):
    def __init__(self, parent=None):
        QtGui.QItemDelegate.__init__(self, parent)
    def createEditor(self, parent, option, index) :  
        #return editor
        pass
    def setEditorData(self, spinBox, index):
        pass
    def setModelData(self, spinBox, model, index):
        pass
    def updateEditorGeometry(self, editor, option, index):
        editor.setGeometry(option.rect)

class AmountDelegate(QtGui.QItemDelegate):
    def __init__(self, parent=None):
            QtGui.QItemDelegate.__init__(self, parent)

    def createEditor(self, parent, option, index) :
        editor = None
        modele = index.model()
        data = modele.data(index, view.constants.MODEL_DATA_ROLE)
        if isinstance(data, Fermentable) or isinstance(data, Hop) or isinstance(data, Misc):
            editor = QtGui.QLineEdit(parent)
            editor.installEventFilter(self)
        else:
            logger.debug("Selection is not a Fermentable or Hop or Misc:%s", type(data))
        return editor

    def setEditorData(self, lineEdit, index):
        value= index.model().data(index, QtCore.Qt.DisplayRole)
        lineEdit.setText(value)
        #spinBox.setSuffix(" g")

    def setModelData(self, lineEdit, model, index):
        data = index.data(view.constants.MODEL_DATA_ROLE)
        value = lineEdit.text()
        model.setData(index, value)
        self.emit( QtCore.SIGNAL( "pySig"))
        
    def updateEditorGeometry(self, editor, option, index):
        editor.setGeometry(option.rect)
        
        
class TimeDelegate(QtGui.QItemDelegate):
    def __init__(self, parent=None):
        QtGui.QItemDelegate.__init__(self, parent)

    def createEditor(self, parent, option, index) :
        editor = None
        data = index.data(view.constants.MODEL_DATA_ROLE)
        if isinstance(data, Hop) or isinstance(data, Misc):        
            editor = QtGui.QSpinBox(parent)
            editor.setMinimum(0)
            editor.setMaximum(20000)
            editor.installEventFilter(self)
        return editor

    def setEditorData(self, spinBox, index):
        data = index.data(view.constants.MODEL_DATA_ROLE)
        value = index.data(QtCore.Qt.DisplayRole)
        if isinstance(data, Hop):
            spinBox.setValue(HopView.display_to_time(value))
        elif isinstance(data, Misc):
            spinBox.setValue(MiscView.display_to_time(value))
        spinBox.setSuffix(" min")

    def setModelData(self, spinBox, model, index):
        data = index.data(view.constants.MODEL_DATA_ROLE)
        spinBox.interpretText()
        value = spinBox.value()
        if isinstance(data, Hop):
            model.setData(index, HopView.time_to_display(value))
        elif isinstance(data, Misc):
            model.setData(index, MiscView.time_to_display(value))
        self.emit( QtCore.SIGNAL( "pySig"))
                            
    def updateEditorGeometry(self, editor, option, index):
        editor.setGeometry(option.rect)
    

class AlphaDelegate(QtGui.QItemDelegate):
    def __init__(self, parent=None):
        QtGui.QItemDelegate.__init__(self, parent)
        self.hopLabels = HopViewLabels()
        self.hopView = HopView(None)

    def createEditor(self, parent, option, index) :
        editor = None
        data = index.data(view.constants.MODEL_DATA_ROLE)
        if isinstance(data, Hop):
            editor = QtGui.QDoubleSpinBox(parent)
            editor.setMinimum(0)
            editor.setMaximum(100)
            editor.installEventFilter(self)
        return editor

    def setEditorData(self, spinBox, index):
        value = index.data(QtCore.Qt.DisplayRole)
        spinBox.setValue(HopView.display_to_alpha(value))
        spinBox.setSuffix(" %")

    def setModelData(self, spinBox, model, index):
        spinBox.interpretText()
        value = spinBox.value()
        model.setData(index, HopView.alpha_to_display(value))
        self.emit( QtCore.SIGNAL( "pySig"))
                            
    def updateEditorGeometry(self, editor, option, index):
        editor.setGeometry(option.rect)


class HopFormComboBoxDelegate(QtGui.QItemDelegate):
    def __init__(self, parent = None):
        QtGui.QItemDelegate.__init__(self, parent)
        self.hopLabels = HopViewLabels()

    def createEditor(self, parent, option, index):
        editor = None
        data = index.data(view.constants.MODEL_DATA_ROLE)
        if isinstance(data, Hop):
            editor = QtGui.QComboBox( parent )
            for (k,v) in self.hopLabels.formLabels.items():
                editor.addItem(v, k)
        return editor

    def setEditorData( self, comboBox, index ):
        display = index.data(QtCore.Qt.DisplayRole)
        value = 0
        for (k,v) in self.hopLabels.formLabels.items():
            if display == v:
                break
            value += 1
        comboBox.setCurrentIndex(value)
        
    def setModelData(self, editor, model, index):
        value = editor.currentText()
        model.setData( index, value )
        self.emit( QtCore.SIGNAL( "pySig"))    

    def updateEditorGeometry( self, editor, option, index ):

        editor.setGeometry(option.rect)
        
class UseDelegate(QtGui.QItemDelegate):
    def __init__(self, parent = None):
        QtGui.QItemDelegate.__init__(self, parent)
        self.hopLabels = HopViewLabels()
        self.fermentableLabels = FermentableViewLabels()
        self.miscLabels = MiscViewLabels()

    def createEditor(self, parent, option, index):
        editor = None
        data = index.data(view.constants.MODEL_DATA_ROLE)
        if isinstance(data, Fermentable):
            editor = QtGui.QComboBox( parent )
            for (k,v) in self.fermentableLabels.useLabels.items():
                editor.addItem(v, k)
        elif isinstance(data, Hop):
            editor = QtGui.QComboBox( parent )
            for (k,v) in self.hopLabels.useLabels.items():
                editor.addItem(v, k)
        elif isinstance(data, Misc):        
            editor = QtGui.QComboBox( parent )
            for (k,v) in self.miscLabels.useLabels.items():
                editor.addItem(v, k)
        return editor

    def setEditorData( self, comboBoxUse, index ):
        display = index.data(QtCore.Qt.DisplayRole)
        data = index.data(view.constants.MODEL_DATA_ROLE)
        value = 0
        if isinstance(data, Fermentable):
            for (k,v) in self.fermentableLabels.useLabels.items():
                if display == v:
                    break
                value += 1
        elif isinstance(data, Hop):
            for (k,v) in self.hopLabels.useLabels.items():
                if display == v:
                    break
                value += 1
        elif isinstance(data, Misc):
            for (k,v) in self.miscLabels.useLabels.items():
                if display == v:
                    break
                value += 1
        comboBoxUse.setCurrentIndex(value)
        
    def setModelData(self, editor, model, index):
        value = editor.currentText()
        model.setData( index, value )
        self.emit( QtCore.SIGNAL( "pySig"))

    def updateEditorGeometry( self, editor, option, index ):
        editor.setGeometry(option.rect)
        


class AppWindow(QtGui.QMainWindow,Ui_MainWindow):
    def __init__(self, parent = None):
        QtGui.QMainWindow.__init__(self, parent)
        self.setupUi(self)




######################################################################################
######################################################################################
        self.settings = Settings()
        self.initRep()
        self.dlgEditG = Dialog(self)
        self.dlgEditH = DialogH(self)
        self.dlgEditD = DialogD(self)
        self.dlgEditY = DialogL(self)
        self.dlgPref = DialogPref(self)
        self.dlgStep = DialogStep(self)
        self.dlgMash = DialogMash(self)
        
        

        self.base = ImportBase()
        self.mashProfileExport = ExportMash()
        
        
#        self.base.importBeerXML()
        self.s=0
        self.recipe = None
        
        self.baseStyleListe = [self.trUtf8('Générique'), '1A. Lite American Lager', '1B. Standard American Lager', '1C. Premium American Lager', '1D. Munich Helles', '1E. Dortmunder Export', '2A. German Pilsner (Pils)', '2B. Bohemian Pilsener', '2C. Classic American Pilsner', '3A. Vienna Lager', '3B. Oktoberfest/Märzen', '4A. Dark American Lager', '4B. Munich Dunkel', '4C. Schwarzbier (Black Beer)', '5A. Maibock/Helles Bock', '5B. Traditional Bock', '5C. Doppelbock', '5D. Eisbock', '6A. Cream Ale', '6B. Blonde Ale', '6C. Kölsch', '6D. American Wheat or Rye Beer', '7A. Northern German Altbier', '7B. California Common Beer', '7C. Düsseldorf Altbier', '8A. Standard/Ordinary Bitter', '8B. Special/Best/Premium Bitter', '8C. Extra Special/Strong Bitter (English Pale Ale)', '9A. Scottish Light 60/-', '9B. Scottish Heavy 70/-', '9C. Scottish Export 80/- ', '9D. Irish Red Ale', '9E. Strong Scotch Ale', '10A. American Pale Ale', '10B. American Amber Ale', '10C. American Brown Ale', '11A. Mild','11B. Southern English Brown', '11C. Northern English Brown Ale', '12A. Brown Porter', '12B. Robust Porter', '12C. Baltic Porter', '13A. Dry Stout', '13B. Sweet Stout', '13C. Oatmeal Stout', '13D. Foreign Extra Stout', '13E. American Stout', '13F. Russian Imperial Stout', '14A. English IPA', '14B. American IPA', '14C. Imperial IPA','15A. Weizen/Weissbier', '15B. Dunkelweizen', '15C. Weizenbock', '15D. Roggenbier (German Rye Beer)','16A. Witbier', '16B. Belgian Pale Ale', '16C. Saison', '16D. Bière de Garde', '16E. Belgian Specialty Ale', '17A. Berliner Weisse', '17B. Flanders Red Ale', '17C. Flanders Brown Ale/Oud Bruin', '17D. Straight (Unblended) Lambic', '17E. Gueuze', '17F. Fruit Lambic', '18A. Belgian Blond Ale', '18B. Belgian Dubbel', '18C. Belgian Tripel', '18D. Belgian Golden Strong Ale', '18E. Belgian Dark Strong Ale', '19A. Old Ale', '19B. English Barleywine', '19C. American Barleywine', '20. Fruit Beer', '21A. Spice, Herb, or Vegetable Beer', '21B. Christmas/Winter Specialty Spiced Beer', '22A. Classic Rauchbier', '22B. Other Smoked Beer', '22C. Wood-Aged Beer', '23. Specialty Beer', '24A. Dry Mead', '24B. Semi-sweet Mead', '24C. Sweet Mead', '25A. Cyser', '25B. Pyment', '25C. Other Fruit Melomel', '26A. Metheglin', '26B. Braggot', '26C. Open Category Mead', '27A. Common Cider', '27B. English Cider', '27C. French Cider', '27D. Common Perry', '27E. Traditional Perry', '28A. New England Cider', '28B. Fruit Cider', '28C. Applewine', '28D. Other Specialty Cider/Perry']
       
        self.typesList = [self.trUtf8("Tout grain"), self.trUtf8("Extrait"), self.trUtf8("Partial mash")]


        #Les connexions
        self.connect(self.actionNouvelle_recette, QtCore.SIGNAL("triggered()"), self.newRecipeFromLibrary)
        self.connect(self.actionEnregistrer, QtCore.SIGNAL("triggered()"), self.enregistrer)
        self.connect(self.actionEnregistrerToolBar, QtCore.SIGNAL("triggered()"), self.enregistrer)
        self.connect(self.actionEnregistrer_Sous, QtCore.SIGNAL("triggered()"), self.enregistrerSous)
        self.connect(self.actionExporterHtml, QtCore.SIGNAL("triggered()"), self.exporterHtml)
        self.connect(self.actionCopierBbcode, QtCore.SIGNAL("triggered()"), self.copierBbcode)
        self.connect(self.actionRecharger, QtCore.SIGNAL("triggered()"), self.recharger)
        #self.connect(self.actionSwitch, QtCore.SIGNAL("triggered()"), self.switch)
        self.actionImporter.triggered.connect(self.importInLib)
        self.connect(self.actionQuitter, QtCore.SIGNAL("triggered()"), app, QtCore.SLOT("quit()"))

        self.actionShowJournal.triggered.connect(self.showJournal)
        
        
        self.connect(self.actionEditGrains, QtCore.SIGNAL("triggered()"), self.editGrains)
        self.connect(self.actionEditHoublons, QtCore.SIGNAL("triggered()"), self.editHoublons)
        self.connect(self.actionEditDivers, QtCore.SIGNAL("triggered()"), self.editDivers)
        self.connect(self.actionEditLevures, QtCore.SIGNAL("triggered()"), self.editLevures)
        self.connect(self.actionRestaurerIngredients, QtCore.SIGNAL("triggered()"), self.restoreDataBase)
        self.actionImportIng.triggered.connect(self.importIng)
        self.actionManageProfiles.triggered.connect(self.seeMash)
        
        self.connect(self.actionAbout, QtCore.SIGNAL("triggered()"), self.about)

        self.connect(self.actionAllTools, QtCore.SIGNAL("triggered()"), self.showTools)

        self.connect(self.actionPreferences, QtCore.SIGNAL("triggered()"), self.dialogPreferences)
        
        

        self.pushButtonSave.clicked.connect(self.enregistrer)
        self.pushButtonCancel.clicked.connect(self.cancelRecipe)
        self.pushButtonOk.clicked.connect(self.okRecipe)
        

        
        #Les vues
        #####################################################################################
        #####################################################################################
        self.connect(self.actionVueEditeur, QtCore.SIGNAL("triggered()"), self.switchToEditor)
        self.connect(self.actionVueBibliotheque, QtCore.SIGNAL("triggered()"), self.switchToLibrary)
        
        self.connect(self.actionVueEditeurToolBar, QtCore.SIGNAL("triggered()"), self.switchToEditor)
        self.connect(self.actionVueBibliothequeToolBar, QtCore.SIGNAL("triggered()"), self.switchToLibrary)

        

        # self.connect(self.buttonEditor, QtCore.SIGNAL("clicked()"),self.switchToEditor)
        # self.connect(self.buttonLibrary, QtCore.SIGNAL("clicked()"), self.switchToLibrary)
        # self.connect(self.buttonBrewday, QtCore.SIGNAL("clicked()"), self.switchToBrewday)

        
        #############################################################################################
        #############################################################################################
        
        
        ##########################
        #Boutons notes
        ##########################
        self.pushButtonRecipeNotes.clicked.connect(self.recipeNotesClicked)
        self.buttonBoxRecipeNotes.accepted.connect(self.recipeNotesAccepted)
        self.buttonBoxRecipeNotes.rejected.connect(self.recipeNotesRejected)
        
        
        #############################################################################################
        self.connect(self.actionImprimer, QtCore.SIGNAL("triggered()"), self.printRecipe)
        
        self.connect(self.doubleSpinBoxRendemt, QtCore.SIGNAL("valueChanged(QString)"), self.rendemt_changed)
        self.connect(self.doubleSpinBox_2Volume, QtCore.SIGNAL("valueChanged(QString)"), self.volume_changed)
        self.connect(self.pushButtonAjouter_2, QtCore.SIGNAL("clicked()"), self.ajouterF)
        self.connect(self.pushButtonAjouterH, QtCore.SIGNAL("clicked()"), self.ajouterH)
        self.connect(self.pushButtonAjouterY, QtCore.SIGNAL("clicked()"), self.ajouterY)
        self.connect(self.pushButtonAjouterM, QtCore.SIGNAL("clicked()"), self.ajouterM)
        self.connect(self.pushButtonEnlever, QtCore.SIGNAL("clicked()"), self.enlever)
        self.connect(self.pushButtonChangerStyle, QtCore.SIGNAL("clicked()"), self.modifierStyle)

        
        
        self.connect(self.comboBoxStyle, QtCore.SIGNAL("currentIndexChanged(QString)"), self.addStyle)
        #self.connect(self.pushButtonEssai, QtCore.SIGNAL("clicked()"), self.essai)
        self.connect(self.comboBoxType, QtCore.SIGNAL("currentIndexChanged(QString)"), self.typeChanged)
        
        #######################################################################################################
        # Profil de brassage       #########################################################################################################
        
        self.pushButtonMashDetails.clicked.connect(self.mashDetails)
        self.listWidgetSteps.itemSelectionChanged.connect (self.stepDetails)
        self.listWidgetMashProfiles.itemSelectionChanged.connect (self.mashClicked)
        self.buttonBoxMashDetails.rejected.connect(self.mashRejected)
#        self.comboBoxStepType.addItems(["Infusion", "Température", "Décoction"])
        self.pushButtonStepEdit.clicked.connect(self.stepEdit)
        self.dlgStep.stepChanged.connect(self.stepReload)
        self.pushButtonStepRemove.clicked.connect(self.removeStep)
        self.pushButtonNewStep.clicked.connect(self.addStep)
        self.pushButtonMashEdit.clicked.connect(self.mashEdit)
        self.dlgMash.mashChanged.connect(self.mashReload)
        self.pushButtonNewProfile.clicked.connect(self.addMash)
        self.pushButtonRemoveProfile.clicked.connect(self.removeMash)
        
        
        self.popMashCombo()
        self.comboBoxMashProfiles.setCurrentIndex(-1)
        self.comboBoxMashProfiles.currentIndexChanged.connect(self.mashComboChanged)

        
        self.pushButtonSaveProfile.clicked.connect(self.saveProfile)


        
        #On connecte ici les signaux émits à la fermeture des fenêtres d'édition de la base
        #########################################################################################
        ##########################################################################################
        #self.connect(self.dlgEditG, QtCore.SIGNAL( "baseChanged"), self.baseReload)
        self.dlgEditG.baseChanged.connect(self.baseReload)
        self.dlgEditH.baseChanged.connect(self.baseReload)
        self.dlgEditD.baseChanged.connect(self.baseReload)
        self.dlgEditY.baseChanged.connect(self.baseReload)
        
        #Signal pour l'affichage du widget de modif des ingrédients
        self.pushButtonChangeIngredients.clicked.connect(self.displayIngredients) 
        
        
        #Les modeles et vues du widget central
        self.modele = QtGui.QStandardItemModel(0, 7)
        self.connect(self.modele, QtCore.SIGNAL("itemChanged(QStandardItem *)"), self.reverseMVC)
        
        liste_headers = [self.trUtf8("Ingrédients"),self.trUtf8("Quantité (g)"),self.trUtf8("Temps (min)"),self.trUtf8("Acide Alpha (%)"),self.trUtf8("Type"),self.trUtf8("Proportion"), self.trUtf8("Étape")]
        self.modele.setHorizontalHeaderLabels(liste_headers)
        
        
        
        self.deleg = AmountDelegate(self)
        self.tableViewF.setItemDelegateForColumn(1,self.deleg)
        self.connect(self.deleg, QtCore.SIGNAL( "pySig"), self.modeleProportion)
        
        
        
        self.delegT = TimeDelegate(self)
        self.tableViewF.setItemDelegateForColumn(2,self.delegT)
        self.connect(self.delegT, QtCore.SIGNAL( "pySig"), self.modeleProportion)

        self.delegA = AlphaDelegate(self)
        self.tableViewF.setItemDelegateForColumn(3,self.delegA)
        self.connect(self.delegA, QtCore.SIGNAL( "pySig"), self.modeleProportion)
        
        self.delegC = HopFormComboBoxDelegate(self)
        self.tableViewF.setItemDelegateForColumn(4,self.delegC)  
        self.connect(self.delegC, QtCore.SIGNAL( "pySig"), self.modeleProportion)
        
        self.delegI = IngDelegate(self)
        self.tableViewF.setItemDelegateForColumn(0,self.delegI)
        self.tableViewF.setItemDelegateForColumn(5,self.delegI)
        
        self.delegUse = UseDelegate(self)
        self.tableViewF.setItemDelegateForColumn(6,self.delegUse)
        self.connect(self.delegUse, QtCore.SIGNAL( "pySig"), self.modeleProportion)
        

        self.tableViewF.setModel(self.modele)
        
        self.tableViewF.resizeColumnsToContents()
        self.tableViewF.setColumnWidth(0,250)
        self.tableViewF.setColumnWidth(1,125)
        self.tableViewF.setColumnWidth(3,125)
        self.tableViewF.setColumnWidth(4,150)
        self.tableViewF.setColumnWidth(6,150)
        
        #La bibliotheque
        ###################################################################################################################
        ###################################################################################################################
        self.modeleBiblio = QtGui.QFileSystemModel()
        self.modeleBiblio.setReadOnly(False)
        self.modeleBiblio.setRootPath(recettes_dir)

        self.listdir(recettes_dir)
        self.showLib() 


        # le menu "nouveau"
        newLibMenu = QtGui.QMenu()
        newLibMenu.addAction(self.actionNouveau_Dossier)
        newLibMenu.addAction(self.actionNouvelle_recette_2)
        # self.pushButtonNewFolderBiblio.setMenu(newLibMenu)

 
        self.actionNouvelle_recette_2.triggered.connect(self.newRecipeFromLibrary)

        
        ##on cree un modele pour les ingredients dispo dans la base
        #self.modeleIngBase = QtGui.QStandardItemModel()
        ##la vue correspondante
        #self.treeViewIng.setModel(self.modeleIngBase)
        ##on va remplir tout ça... avec une autre fonction
        #self.listeIng()
        self.comboBox.setModel(view.base.getFermentablesQtModel() )
        
        self.comboBoxH.setModel(view.base.getHopsQtModel() )
        
        self.comboBoxY.setModel(view.base.getYeastsQtModel() )
        
        self.comboBoxM.setModel(view.base.getMiscsQtModel() )
       
        self.comboBoxStyle.hide()
        self.comboBoxStyle.addItems(self.baseStyleListe)
        
        self.comboBoxType.addItems(self.typesList)
        self.comboBoxType.setCurrentIndex(0)
        
        self.nouvelle()
 
        self.widgetIngredients.hide()

        self.actionVueEditeurToolBar.setChecked(False)




###################################################################################################
######## gestion des arguments au lancement du programme  #########################################


        argumentsList=QtGui.QApplication.arguments()
        if len(argumentsList) > 1 :
            logger.debug("la liste d'arguments: %s",argumentsList)
            logger.debug("le chemin: %s",argumentsList[1])
            # for part in argumentsList :
            #     recipePath=recipePath + " " + part
            try:
                recipePath= argumentsList[1]
                for part in argumentsList[2:] :
                    recipePath= recipePath +" " + part
                
                self.openRecipeFile(recipePath)
            except :
                pass
        else:
            pass
            
########################################################################################################################
####################################################################################################################
# le signal émit à la fermeture de la fenêtre de préférences
        self.dlgPref.prefAccepted.connect(self.prefReload)

#####################################################################
        ###on configure la vue par défaut à l'ouverture
#####################################################################
        self.stackedWidget.setCurrentIndex(1)
        self.actionVueEditeurToolBar.setChecked(False)
        self.actionVueBibliothequeToolBar.setChecked(True)
        
        # self.buttonSave.hide()
        # self.buttonNewRecipe.show()

        self.previousPage = [1]
        self.stackedWidget.currentChanged.connect(self.pageChanged)



###########################################################
############### Journal ##############################
######################################################

    def loadJournal(self):
        self.journal=Journal()
        self.journal.loadJournal()
        # self.actionEditJournal.setEnabled(True)     

    @QtCore.pyqtSlot()
    def showJournal(self,entry=" '' ") :
        self.stackedWidget.setCurrentIndex(1)
        self.loadJournal()
        pyDir = os.path.abspath(os.path.dirname(__file__))
        baseUrl = QtCore.QUrl.fromLocalFile(os.path.join(pyDir, "static/"))
        self.webViewBiblio.setHtml(self.journal.export("html",entry), baseUrl)
        self.webViewBiblio.page().mainFrame().addToJavaScriptWindowObject("main", self)
        # self.webViewBiblio.page().settings().setAttribute(QtWebKit.QWebSettings.DeveloperExtrasEnabled, True)
        # self.webInspector = QtWebKit.QWebInspector(self)
        # self.webInspector.setPage(self.webViewBiblio.page())
        # self.webInspector.setVisible(True)
        # self.verticalLayout_13.addWidget(self.webInspector)


    @QtCore.pyqtSlot(str)
    def addToJournal(self,event) :
        self.loadJournal()
        entry = '''{recipe:%s,date:%s,event:%s,editing:'True'} ''' %( "'" + self.recipe.name + "'", "'" + str(int(time.time())) + "'" , "'" + self.journal.eventsLabels[event] + "'")
        self.showJournal(entry)


    @QtCore.pyqtSlot(str)
    def dumpJournal(self,journalJson) :
        journalJson= '{"name":"journal","items": %s }' %journalJson 
        d=json.loads(journalJson)
        with open(journal_file, mode="w", encoding="utf-8") as f :
            json.dump(d,f,indent=2)



############## Bibliothèque ##############################
##########################################################
    @QtCore.pyqtSlot()
    def showLib(self) :
        # data = json.dumps(self.recipesSummary)
        # data = data.replace("'","&#39;")
        self.stackedWidget.setCurrentIndex(1)
        self.brewdayLock = 0
        data = self.recipesSummary
        profiles = self.mashProfileExport.exportJson(ImportBase().listeMashes)

        pyDir = os.path.abspath(os.path.dirname(__file__))
        baseUrl = QtCore.QUrl.fromLocalFile(os.path.join(pyDir, "static/"))
        self.webViewBiblio.setHtml(LibExporterRepository['html'](data,ImportBase().exportjson(), profiles), baseUrl)
        # url = QtCore.QUrl("http://google.com")
        # self.webViewBiblio.load(url)

        

        self.webViewBiblio.page().mainFrame().addToJavaScriptWindowObject("main", self)
        self.webViewBiblio.page().settings().setAttribute(QtWebKit.QWebSettings.DeveloperExtrasEnabled, True)
        self.webViewBiblio.page().action(QtWebKit.QWebPage.Reload).setVisible(False)


    @QtCore.pyqtSlot(str)
    def deleteLib(self,path) :
        confirmation = QtGui.QMessageBox.question(self,
                            self.trUtf8("Supprimer"),
                            self.trUtf8("La recette sera définitivement supprimée <br/> Continuer ?"),
                            QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
        if (confirmation == QtGui.QMessageBox.Yes):
            os.remove(path)
            self.listdir(recettes_dir)
            self.showLib()
        else :
            self.showLib()
        

    @QtCore.pyqtSlot()   
    def backWebViewBiblio(self) : 
        self.stackedWidget.setCurrentIndex(1)

    
    @QtCore.pyqtSlot(str, str)
    def saveRecipe(self, recipe, path) :
        recipeFile = QtCore.QFile(path)
        if recipeFile.open(QtCore.QIODevice.WriteOnly):
            try:
                stream = QtCore.QTextStream(recipeFile)
                stream.setCodec("UTF-8")
                stream << recipe
            finally:
                recipeFile.close()
                print(recipe)
        else:
            # TODO : Prévenir l'utilisateur en cas d'échec de l'enregistrement
            pass  





############# Vue recette ################################
##########################################################

    @QtCore.pyqtSlot(str)
    def viewRecipeLib(self,path):
        self.actionEnregistrer.setEnabled(True)
        self.actionEnregistrer_Sous.setEnabled(True)
        self.actionExporterHtml.setEnabled(True)
        self.actionCopierBbcode.setEnabled(True)

        self.purge()
        
        self.s = path

        self.importBeerXML()



############# Mode Brassage ################################
############################################################

    @QtCore.pyqtSlot()
    def showBrewdayMode(self):
        if self.brewdayLock == 0 : 
            self.stackedWidget.setCurrentIndex(2)
            self.brewdayLock = 1 
            data = self.recipe.export("json")
            pyDir = os.path.abspath(os.path.dirname(__file__))
            baseUrl = QtCore.QUrl.fromLocalFile(os.path.join(pyDir, "static/"))
            self.webViewBrewday.setHtml(BrewdayExporterRepository['html'](data), baseUrl)
            self.webViewBrewday.page().mainFrame().addToJavaScriptWindowObject("main", self)
            # self.webViewBrewday.page().settings().setAttribute(QtWebKit.QWebSettings.DeveloperExtrasEnabled, True)
        else :
            self.stackedWidget.setCurrentIndex(2)





        





###### Outils ############################################
##########################################################

    @QtCore.pyqtSlot()
    def showTools(self):
        self.stackedWidget.setCurrentIndex(1)
        pyDir = os.path.abspath(os.path.dirname(__file__))
        baseUrl = QtCore.QUrl.fromLocalFile(os.path.join(pyDir, "static/"))
        self.webViewBiblio.setHtml(ToolExporterRepository["html"](), baseUrl)
        self.webViewBiblio.page().mainFrame().addToJavaScriptWindowObject("main", self)
        # self.webViewBiblio.page().settings().setAttribute(QtWebKit.QWebSettings.DeveloperExtrasEnabled, True)
        # self.webInspector = QtWebKit.QWebInspector(self)
        # self.webInspector.setPage(self.webViewBiblio.page())
        # self.webInspector.setVisible(True)
        # self.verticalLayout_13.addWidget(self.webInspector)
        





        

        
    #Une fonction qui gère l'aperçu des couleurs. 
    #Contient un tupple avec plusieurs références de couleurs, classées par rang selon la valeur SRM.
    #################################################################################################
    def colorPreview (self) :
        self.colorTuppleSrm = ('FFE699', 'FFD878', 'FFCA5A', 'FFBF42', 'FBB123', 'F8A600', 'F39C00', 'EA8F00', 'E58500', 'DE7C00', 'D77200', 'CF6900', 'CB6200', 'C35900','BB5100', 'B54C00', 'B04500', 'A63E00', 'A13700', '9B3200', '952D00', '8E2900', '882300', '821E00', '7B1A00', '771900', '701400', '6A0E00', '660D00','5E0B00','5A0A02','600903', '520907', '4C0505', '470606', '440607', '3F0708', '3B0607', '3A070B', '36080A')
        
        colorRef= round(self.recipe.compute_EBC()/1.97)
        
        if colorRef >= 30 :
            color = "#" + self.colorTuppleSrm[30]
        elif colorRef <= 1 :
            color = "#" + self.colorTuppleSrm[0]
        else :
            color = "#" + self.colorTuppleSrm[colorRef-1]
        self.widgetColor.setStyleSheet("background-color :" + color)
        
        
    def displayIngredients(self) :
        if self.pushButtonChangeIngredients.isChecked() :
            self.widgetIngredients.show()
        else :
            self.widgetIngredients.hide()
        
        
    #Une fonction qui recharge les combobox qd la base d'ingrédients a été modifiée. Pratique.
    #############################################################################################   
    def baseReload (self): 
        if self.base is None:
            self.base = ImportBase()
        
        self.comboBox.clear()
        self.comboBox.setModel(view.base.getFermentablesQtModel() )
        
        self.comboBoxH.clear()
        self.comboBoxH.setModel(view.base.getHopsQtModel() )
        
        self.comboBoxY.clear()
        self.comboBoxY.setModel(view.base.getYeastsQtModel() )
        
        self.comboBoxM.clear()
        self.comboBoxM.setModel(view.base.getMiscsQtModel() )



    def listdir(self, rootdir) :
        self.recipesSummary="["
        fileList=[]
        filenameList=[]
        for root, subFolders, files in os.walk(rootdir):
            for file2 in files:
                fileList.append(os.path.join(root,file2))
                filenameList.append(file2)

        #on parse
        j=0
        while j < len(filenameList) :
            j=j+1
            recipe = fileList[j-1]
            try :
                self.recipesSummary += str (self.jsonRecipeLib(recipe))
                if j < len(filenameList) :
                    self.recipesSummary += ","
            except :
                logger.debug("le fichier %s n'est pas une recette" %(recipe))
                
        self.recipesSummary += "]"
        logger.debug("%s fichiers détectés" %(len(filenameList)))
        

                
    def jsonRecipeLib(self,recipe) :
        self.s = recipe
        self.recipe = Recipe.parse(recipe)
        data = self.recipe.export("json")
        data = data[1:-1]
        return data
   

  
    @QtCore.pyqtSlot()               
    def editCurrentRecipe(self):
        self.switchToEditor()
        # self.s = self.chemin
        
        self.importBeerXML()
        # self.modele.blockSignals(True)
        logger.debug("editCurrentRecipe -> initModele")
        self.initModele()
        # self.modele.blockSignals(False)
        self.stackedWidget.setCurrentIndex(0)
        self.actionVueEditeurToolBar.setChecked(True)
        self.actionVueBibliothequeToolBar.setChecked(False) 
        self.setComboBoxMash()

    def setComboBoxMash(self) :
        try :
            self.comboBoxMashProfiles.blockSignals(True)
            self.popMashCombo()
            self.comboBoxMashProfiles.blockSignals(False)
            if self.recipe.mash.name is not None :
                # self.comboBoxMashProfiles.setCurrentIndex(len(self.listMash)-1)
                self.comboBoxMashProfiles.addItem(self.recipe.mash.name + "*")
                self.comboBoxMashProfiles.setCurrentIndex(len(ImportBase().listeMashes))
            else :
                self.comboBoxMashProfiles.setCurrentIndex(-1)
        except :
            self.comboBoxMashProfiles.setCurrentIndex(-1)

              


    def importInLib (self):
        self.s = QtGui.QFileDialog.getOpenFileName(self, self.trUtf8("Ouvrir un fichier"), home_dir,
                                                   self.trUtf8("All (*);;BeerXML (*.xml);;BeerSmith 2 (*.bsmx)"))
        errors = Errors()
        try:
            filename = os.path.basename(self.s)
            if filename.endswith('.bsmx'):
                recipe = Recipe.parse(self.s, 'bsmx')
            # By default BeerXML is used
            else:
                recipe = Recipe.parse(self.s, 'beerxml')
            finalDest = recettes_dir + "/" + recipe.name.replace('/', ' ') + ".xml"
            if os.path.exists(finalDest):
                logger.debug("Le fichier existe déjà dans la bibliothèque")
                errors.warningExistingFile()
            else:
                self.recipe = recipe
                self.enregistrerRecette(finalDest)
        except (TypeError, SyntaxError, AttributeError):
            logger.debug("Fichier incompatible. L'importation a échoué")
            errors.warningXml()
            
        self.listdir(recettes_dir)
        self.showLib()
     
        
       
    def cancelRecipe(self):
        self.listdir(recettes_dir) 
        self.showLib()
        
    def okRecipe(self):
        self.enregistrer()
        if self.fileSaved :
            self.listdir(recettes_dir)
            self.showLib()
            
        else :
            pass

             
    def initRep(self) :   
        home = QtCore.QDir(home_dir)
        config = QtCore.QDir(config_dir)
        logger.debug (config)
        if not config.exists() :
            home.mkpath (config_dir)
        else :
            pass
        database = QtCore.QFile(database_file)
        if not database.exists() :
            database.copy(database_root, database_file)
        else :
            pass
        recettes = QtCore.QFile(recettes_dir)
        if not recettes.exists() :
            try :
                shutil.copytree(samples_dir, samples_target)
            except :
                home.mkpath(recettes_dir)
        mash  = QtCore.QFile(mash_file)
        if not mash.exists() :
            mash.copy(mash_root, mash_file)
        else :
            pass
        journal  = QtCore.QFile(journal_file)
        if not journal.exists() :
            journal.copy(journal_root, journal_file)
        else :
            pass
        
        # on configure des valeurs par défaut
        if not settings.conf.contains("BoilOffRate") :
            settings.conf.setValue("BoilOffRate", 10)
        if not settings.conf.contains("CoolingLoss") :
            settings.conf.setValue("CoolingLoss", 5)
        if not settings.conf.contains("GrainTemp") :
            settings.conf.setValue("GrainTemp", 20)
        if not settings.conf.contains("FudgeFactor") :
            settings.conf.setValue("FudgeFactor", 1.7)
        if not settings.conf.contains("GrainRetention") :
            settings.conf.setValue("GrainRetention", 1)
        if not settings.conf.contains("Menus") :
            settings.conf.setValue("Menus", "button")


    def prefReload(self) :
        if platform == 'win32':
            recettes_dir = settings.conf.value("pathWin32")
        else :
            recettes_dir = settings.conf.value("pathUnix")
        self.initRep()
        self.listdir(recettes_dir)
        self.showLib()
        print(settings.conf.value("pathUnix"))

        
    def switchToEditor(self) :
        self.stackedWidget.setCurrentIndex(0)
       

    @QtCore.pyqtSlot()    
    def switchToLibrary(self) :
        self.stackedWidget.setCurrentIndex(1)        
        # self.viewRecipeLib(self.s)

 
    def switchToNotes(self) :
        self.stackedWidget.setCurrentIndex(3)        

        
    def switchToMash(self) :
        self.stackedWidget.setCurrentIndex(4)        



    def pageChanged(self, newIndex):
        self.previousPage.append(newIndex)
        if len(self.previousPage) > 2:
            del self.previousPage[0]

    def switchToPreviousPage(self):
        self.stackedWidget.setCurrentIndex(self.previousPage[0])

    def restoreDataBase(self) :
        home = QtCore.QDir(home_dir)
        config = QtCore.QDir(config_dir)
        database = QtCore.QFile(database_file)
        confirmation = QtGui.QMessageBox.question(self,
                                    self.trUtf8("Remplacer la base ?"),
                                    self.trUtf8("La base des ingrédients actuelle va être effacée et remplacée par la base originale. Toutes vos modifications vont être effacées. Un redémarrage de l'application sera nécessaire.<br> Continuer ?"),
                                    QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
        if (confirmation == QtGui.QMessageBox.Yes):
            database.remove(database_file)
            database.copy(database_root, database_file)
        else :
            
            pass

    def modeleProportion (self) :
        #Cette fonction est appelée chaque fois que la quantité, les AA ou les temps sont modifiés, via un signal émit par les classes Delegate.
        #Cette fonction met à jour les données du modèle Qt
        recipeView = RecipeView(self.recipe)
        for i in range(self.modele.rowCount()):
            data = self.modele.item(i, 5).data(view.constants.MODEL_DATA_ROLE)
            if isinstance(data, Fermentable):
                self.modele.setItem(i, 5, recipeView.QStandardItem_for_fermentable_proportion(data))
            elif isinstance(data, Hop):
                self.modele.setItem(i, 5, recipeView.QStandardItem_for_hop_ibu(data))
        self.displayProfile()

    # cette fonction est appelee chaque fois que les donnees du modele changent
    def reverseMVC(self, item) :
        #logger.debug("item:%s %s %s", item, item.data(view.constants.MODEL_DATA_ROLE), item.data(QtCore.Qt.EditRole))
        row = item.row()
        column = item.column()
        modelInstance = item.data(view.constants.MODEL_DATA_ROLE)
        newValue = item.text()

        #Update Hop item
        if isinstance(modelInstance, Hop):
            logger.debug("Model update at [row=%d,column=%d] for Hop:%s; newValue=%s", row, column, modelInstance, newValue)
            hopLabels = HopViewLabels()
            if column == 1:
                #Update Hop amount value
                try:
                    modelInstance.amount = HopView.display_to_amount(newValue)
                except ValueError as e:
                    logger.warn("Can't set Hop amount value to:'%s' %s", newValue, e)
                    item.setData(HopView.amount_to_display(modelInstance.amount), QtCore.Qt.DisplayRole)
            if column == 2:
                #Update Hop time value
                try:
                    modelInstance.time = HopView.display_to_time(newValue)
                except ValueError:
                    logger.warn("Can't set Hop time value to:'%s'", newValue)
                    item.setData(HopView.time_to_display(modelInstance.time), QtCore.Qt.DisplayRole)
            if column == 3:
                #Update Hop alpha value
                try:
                    modelInstance.alpha = HopView.display_to_alpha(newValue)
                except ValueError:
                    logger.warn("Can't set Hop alpha value to:'%s'", newValue)
                    item.setData(HopView.alpha_to_display(modelInstance.alpha), QtCore.Qt.DisplayRole)
            elif column == 4:
                #Update Hop form
                for (k,v) in hopLabels.formLabels.items():
                    if newValue == v:
                        modelInstance.form = k
                        break
            elif column == 6:
                #Update form use
                for (k,v) in hopLabels.useLabels.items():
                    if newValue == v:
                        modelInstance.use = k
                        break

        #Update Fermentable item
        if isinstance(modelInstance, Fermentable):
            logger.debug("Model update at [row=%d,column=%d]for Fermentable:%s; newValue=%s", row, column, modelInstance, newValue)
            fermentableLabels = FermentableViewLabels()
            if column == 1:
                #Update amount value
                try:
                    modelInstance.amount = FermentableView.display_to_amount(newValue)
                except ValueError as e:
                    logger.warn("Can't set Fermentable amount value to:'%s' %s", newValue, e)
                    item.setData(FermentableView.amount_to_display(modelInstance.amount), QtCore.Qt.DisplayRole)
            if column == 6:
                #Update form use
                if newValue == fermentableLabels.useLabels[model.constants.FERMENTABLE_USE_BOIL]:
                    modelInstance.useAfterBoil = False
                elif newValue == fermentableLabels.useLabels[model.constants.FERMENTABLE_USE_AFTER_BOIL]:
                    modelInstance.useAfterBoil = True

        #Update Misc item
        if isinstance(modelInstance, Misc):
            logger.debug("Model update at [row=%d,column=%d] for Misc:%s; newValue=%s", row, column, modelInstance, newValue)
            miscLabels = MiscViewLabels()
            if column == 1:
                #Update Misc amount value
                try:
                    modelInstance.amount = MiscView.display_to_amount(newValue)
                except ValueError as e:
                    logger.warn("Can't set Misc amount value to:'%s' %s", newValue, e)
                    item.setData(MiscView.amount_to_display(modelInstance.amount), QtCore.Qt.DisplayRole)
            if column == 2:
                #Update Misc time value
                try:
                    modelInstance.time = MiscView.display_to_time(newValue)
                except ValueError:
                    logger.warn("Can't set Misc time value to:'%s'", newValue)
                    item.setData(MiscView.time_to_display(modelInstance.time), QtCore.Qt.DisplayRole)
            if column == 6:
                #Update form use
                for (k,v) in miscLabels.useLabels.items():
                    if newValue == v:
                        modelInstance.use = k
                        break
        #Dump updates for debugging
        #for h in self.recipe.listeHops:
        #    logger.debug(h)
        #for h in self.recipe.listeFermentables:
        #    logger.debug(h)
        #for h in self.recipe.listeMiscs:
        #    logger.debug(h)

    def clearModele(self):
        count = self.modele.rowCount()
        ret = self.modele.removeRows(0, count)
           
    def initModele(self) :
        if self.recipe is not None:
            self.displayProfile()
            self.clearModele()
            recipeView = RecipeView(self.recipe)
            
            for f in self.recipe.listeFermentables:
                fView = FermentableView(f)
                items = list()
                items.append( fView.QStandardItem_for_name() )
                items.append( fView.QStandardItem_for_amount() )
                items.append( QtGui.QStandardItem('') )
                items.append( QtGui.QStandardItem('') )
                items.append( fView.QStandardItem_for_type() )
                items.append( recipeView.QStandardItem_for_fermentable_proportion(f) )
                items.append( fView.QStandardItem_for_use() )
                self.modele.appendRow(items)

            for h in self.recipe.listeHops:
                hView = HopView(h)
                items = list()
                items.append( hView.QStandardItem_for_name() )
                items.append( hView.QStandardItem_for_amount() )
                items.append( hView.QStandardItem_for_time() )
                items.append( hView.QStandardItem_for_alpha() )
                items.append( hView.QStandardItem_for_form() )
                items.append (recipeView.QStandardItem_for_hop_ibu(h) )
                items.append( hView.QStandardItem_for_use() )
                self.modele.appendRow(items)

            for m in self.recipe.listeMiscs:
                mView = MiscView(m)
                items = list()
                items.append( mView.QStandardItem_for_name_type() )
                items.append( mView.QStandardItem_for_amount() )
                items.append( mView.QStandardItem_for_time() )
                items.append( QtGui.QStandardItem('') )
                items.append( QtGui.QStandardItem('') )
                items.append( QtGui.QStandardItem('') )
                items.append( mView.QStandardItem_for_use() )
                self.modele.appendRow(items)

            for y in self.recipe.listeYeasts:
                yView = YeastView(y)
                items = list()
                items.append( yView.QStandardItem_for_detail() )
                items.append( QtGui.QStandardItem('') )
                items.append( QtGui.QStandardItem('') )
                items.append( QtGui.QStandardItem('') )
                items.append( QtGui.QStandardItem('') )
                items.append( QtGui.QStandardItem('') )
                items.append( QtGui.QStandardItem('') )
                self.modele.appendRow(items)
                
    def editGrains(self) :
        self.dlgEditG.setModal(True)
        self.dlgEditG.setModel()
        self.dlgEditG.show()
        
    def editHoublons(self) :
        self.dlgEditH.setModal(True)
        self.dlgEditH.setModel()
        self.dlgEditH.show()
        
    def editDivers(self) :
        self.dlgEditD.setModal(True)
        self.dlgEditD.setModel()
        self.dlgEditD.show()   
    
    def editLevures(self) :
        self.dlgEditY.setModal(True)
        self.dlgEditY.setModel()
        self.dlgEditY.show()     

    @QtCore.pyqtSlot(float, float, float, float)  
    def preBoilCheck(self,volPreBoil,preBoilSg,GU,volume) :
        self.dlgPreBoil = DialogPreBoil(self)
        self.dlgPreBoil.setData(volPreBoil,preBoilSg,GU,volume)
        self.dlgPreBoil.setModal(True)
        self.dlgPreBoil.show()

        
    def dialogPreferences (self) :
        self.dlgPref.setModal(True)
        self.dlgPref.show()
    
       
    def purge (self) :
        self.clearModele()
        self.s = 0
        self.nouvelle()

    @QtCore.pyqtSlot()    
    def newRecipeFromLibrary (self) :
        self.switchToEditor()
        self.purge()
            
    def ajouterF(self) :
        comboText = self.comboBox.currentText()
        #Find selected Fermentable in database and copy it in recipe as new Fermentable
        try:
            fBase = [f for f in ImportBase().listeFermentables if f.name == comboText][0]
            newFermentable = fBase.copy()
            newFermentable.amount = 1000
            newFermentable.useAfterBoil = False
            self.recipe.listeFermentables.append(newFermentable)
            #Refill listView model
            self.initModele()
        except IndexError as e:
            logger.error("Problème dans la base de données des Fermentables :%s", e)
        
    def ajouterH(self) : 
        comboText = self.comboBoxH.currentText()
        #Find selected Hop in database and copy it in recipe as new Hop
        try:
            hBase = [h for h in ImportBase().listeHops if h.name == comboText][0]
            newHop = hBase.copy()
            newHop.amount = 0
            newHop.time = 0.0
            self.recipe.listeHops.append(newHop)
            self.initModele()
        except IndexError as e:
            logger.error("Problème dans la base de données des Houblons :%s", e)
    
    def ajouterM(self) :
        comboText = self.comboBoxM.currentText()
        #Find selected Misc in database and copy it in recipe as new Misc object
        try:
            mBase = [m for m in ImportBase().listeMiscs if m.name == comboText][0]
            newMisc = mBase.copy()
            self.recipe.listeMiscs.append(newMisc)
            self.initModele()
        except IndexError as e:
            logger.error("Problème dans la base de données des Divers :%s", e)

    def ajouterY(self) :
        comboText = self.comboBoxY.currentText()
        #Find selected Misc in database and copy it in recipe as new Misc object
        yBase = None
        for y in ImportBase().listeYeasts :
            yView = YeastView(y)
            if yView.yeastDetailDisplay() == comboText:
                yBase = y
        if yBase == None:
            logger.error("Problème dans la base de données des Levures ...")
        else:
            newYeast = yBase.copy()
            self.recipe.listeYeasts.append(newYeast)
            self.initModele()
        
    def enlever(self) :
        selection = self.tableViewF.selectionModel()
        data = None
        logger.debug("Nb de lignes sélectionnées :%d", len(selection.selectedRows()))
        logger.debug("Nb de colonnes sélectionnées :%d", len(selection.selectedColumns()))
        for index in selection.selectedRows():
            logger.debug("data=%s", index.data(view.constants.MODEL_DATA_ROLE))
            data = index.data(view.constants.MODEL_DATA_ROLE)
            if data is not None:
                break

        logger.debug("selection=%s data=%s",selection, data)
        if data is not None:
            if isinstance(data, Hop):
                tailleAvant = len(self.recipe.listeHops)
                self.recipe.listeHops.remove(data)
                tailleApres = len(self.recipe.listeHops)
                logger.debug("%d houblon supprimé", (tailleAvant-tailleApres))
            elif isinstance(data, Fermentable):
                tailleAvant = len(self.recipe.listeFermentables)
                self.recipe.listeFermentables.remove(data)
                tailleApres = len(self.recipe.listeFermentables)
                logger.debug("%d fermentable supprimé", (tailleAvant-tailleApres))
            elif isinstance(data, Yeast):
                tailleAvant = len(self.recipe.listeYeasts)
                self.recipe.listeYeasts.remove(data)
                tailleApres = len(self.recipe.listeYeasts)
                logger.debug("%d levure supprimé", (tailleAvant-tailleApres))
            elif isinstance(data, Misc):
                tailleAvant = len(self.recipe.listeMiscs)
                self.recipe.listeMiscs.remove(data)
                tailleApres = len(self.recipe.listeMiscs)
                logger.debug("%d divers supprimé", (tailleAvant-tailleApres))
            else :
                logger.warn("Impossible de supprimer un ingrédient de type: %s", type(data))
            self.initModele()

    def importBeerXML(self) :
        fichierBeerXML = self.s
        try:
            self.recipe = Recipe.parse(fichierBeerXML)
            self.lineEditRecette.setText(self.recipe.name)
            self.lineEditGenre.setText(self.recipe.style)
            self.doubleSpinBox_2Volume.setValue(self.recipe.volume)
            self.doubleSpinBoxRendemt.setValue(self.recipe.efficiency)
            self.spinBoxBoil.setValue(self.recipe.boil)
            
            if self.recipe.type == model.constants.RECIPE_TYPE_ALL_GRAIN :
                self.comboBoxType.setCurrentIndex(0)
            elif self.recipe.type == model.constants.RECIPE_TYPE_PARTIAL_MASH :
                self.comboBoxType.setCurrentIndex(2)
            elif self.recipe.type == model.constants.RECIPE_TYPE_EXTRACT :
                self.comboBoxType.setCurrentIndex(1)
            else :
                self.comboBoxType.setCurrentIndex(0)

            self.lineEditBrewer.setText(self.recipe.brewer)
            self.displayProfile()
            
            self.currentRecipeMash = self.recipe.mash

        except :
            errors = Errors()
            errors.warningXml()
            
    def displayProfile(self) : 
        self.colorPreview()    
        self.labelOGV.setText("%.3f" %(self.recipe.compute_OG()))
        self.labelFGV.setText("%.3f" %(self.recipe.compute_FG() ))
        self.labelEBCV.setText("%.0f" %(self.recipe.compute_EBC() ))
        self.labelIBUV.setText("%.0f" %(self.recipe.compute_IBU() ))
        self.labelAlcv.setText("%.1f%%" %(self.recipe.compute_ABV() ))
        self.labelRatioBuGu.setText("%.1f" %(self.recipe.compute_ratioBUGU()))
        
    def openRecipeFile(self,filePath):
        self.s = filePath
        self.nouvelle()
        self.importBeerXML()
        self.initModele()
        self.switchToEditor()

    def about(self) : 
        about = DialogAbout(self)
        about.show()
                  
    def rendemt_changed(self) :
        if self.checkBoxIng.isChecked() :
            try:
                ratio = self.recipe.efficiency/self.doubleSpinBoxRendemt.value()
                for f in self.recipe.listeFermentables:
                    if f.type != model.constants.FERMENTABLE_TYPE_EXTRACT:
                        f.amount *= ratio
                self.recipe.efficiency = self.doubleSpinBoxRendemt.value()
            except ZeroDivisionError:
                pass
        else :
            self.recipe.efficiency = self.doubleSpinBoxRendemt.value()
        self.initModele()                    
            
    def volume_changed(self) :
        if self.checkBoxIng.isChecked() :
            try:
                ratio = self.doubleSpinBox_2Volume.value()/float(self.recipe.volume)
                for x in itertools.chain(self.recipe.listeFermentables, self.recipe.listeHops, self.recipe.listeMiscs):
                    x.amount *= ratio
                self.recipe.volume = self.doubleSpinBox_2Volume.value()
            except ZeroDivisionError:
                pass
        else :
            self.recipe.volume = self.doubleSpinBox_2Volume.value()
        self.initModele()                    
            
    def typeChanged (self) :
        if self.recipe is not None:
            if self.comboBoxType.currentIndex() == 0 :
                self.recipe.type = model.constants.RECIPE_TYPE_ALL_GRAIN
                self.comboBoxMashProfiles.setEnabled(True)
                self.pushButtonMashDetails.setEnabled(True)
            if self.comboBoxType.currentIndex() == 1 :   
                self.recipe.type = model.constants.RECIPE_TYPE_EXTRACT
                self.comboBoxMashProfiles.setEnabled(False)
                self.comboBoxMashProfiles.setCurrentIndex(-1)
                self.pushButtonMashDetails.setEnabled(False)
            if self.comboBoxType.currentIndex() == 2 :
                self.recipe.type = model.constants.RECIPE_TYPE_PARTIAL_MASH
                self.comboBoxMashProfiles.setEnabled(True)
                self.pushButtonMashDetails.setEnabled(True)
            self.initModele()                    

    def enregistrerRecette(self, destination):
        recipeFile = QtCore.QFile(destination)
        if recipeFile.open(QtCore.QIODevice.WriteOnly):
            try:
                stream = QtCore.QTextStream(recipeFile)
                stream.setCodec("UTF-8")
                stream << self.recipe.export("beerxml")
            finally:
                recipeFile.close()
        else:
            # TODO : Prévenir l'utilisateur en cas d'échec de l'enregistrement
            pass  
        self.fileSaved = True    

               
    def enregistrer (self) :
        if self.recipe.name != self.lineEditRecette.text() :
            self.nameChanged = True       
        else :
            self.nameChanged = False

        self.recipe.name = self.lineEditRecette.text()
        self.recipe.style = self.lineEditGenre.text()
        self.recipe.brewer = self.lineEditBrewer.text()
        self.recipe.boil = self.spinBoxBoil.value()
        if not self.s:
            destination = recettes_dir + "/" + self.recipe.name.replace('/', ' ') + ".xml"
            if os.path.exists(destination) :
                errors=Errors()
                errors.warningExistingPath()
                self.fileSaved = False
            else :
                self.s = destination
                self.enregistrerRecette(destination)
        else :
            self.enregistrerRecette(self.s)

        
        
  
    def enregistrerSous (self) :
        self.s = QtGui.QFileDialog.getSaveFileName (self,
                                                    self.trUtf8("Enregistrer dans un fichier"),
                                                    recettes_dir + "/" + self.recipe.name.replace('/', ' ') + ".xml",
                                                    "BeerXML (*.xml)")
        self.enregistrerRecette(self.s)

    def exporterHtml (self) :
        self.recipe.name = self.lineEditRecette.text()
        self.recipe.style = self.lineEditGenre.text()
        fichier = QtGui.QFileDialog.getSaveFileName (self,
                                                    self.trUtf8("Enregistrer dans un fichier"),
                                                    self.recipe.name+".html",
                                                    "HTML (*.html)")
        fileHtml = QtCore.QFile(fichier)
        if fileHtml.open(QtCore.QIODevice.WriteOnly):
            try:
                stream = QtCore.QTextStream(fileHtml)
                stream.setCodec("UTF-8")
                stream << self.recipe.export("html-legacy")
            finally:
                fileHtml.close()
        else:
            # TODO : Prévenir l'utilisateur en cas d'échec de l'export
            pass
    
    def copierBbcode (self):
        app.clipboard().setText(self.recipe.export("bbcode"))

    def modifierStyle (self) :
        if self.pushButtonChangerStyle.isChecked () :
            self.comboBoxStyle.show()
        else :
            self.comboBoxStyle.hide()   


    def nouvelle(self) :
        self.recipe = Recipe()
        self.recipe.name = self.trUtf8('Nouvelle Recette')
        self.recipe.efficiency = 75
        self.recipe.volume = 10
        self.recipe.boil = 60
        self.recipe.style = self.trUtf8('''Générique''')
        self.recipe.recipeNotes =''

        self.lineEditBrewer.setText('')
        self.comboBoxType.setCurrentIndex(0)
        self.lineEditRecette.setText(self.recipe.name)
        self.lineEditGenre.setText(self.recipe.style)
        self.doubleSpinBox_2Volume.setValue(self.recipe.volume)
        self.doubleSpinBoxRendemt.setValue(self.recipe.efficiency)
        self.spinBoxBoil.setValue(self.recipe.boil)
            
        self.currentMash = None
        self.dicMashDetail = {}
        self.mashName=None
        self.popMashCombo()
        self.comboBoxMashProfiles.setCurrentIndex(-1)
        self.brewdayLock = 0
        
        
    def recharger(self) :
        if not self.s :
            pass
        else :
            self.clearModele()
            self.initModele()

    def importIng(self):
        s = QtGui.QFileDialog.getOpenFileName(self,
            self.trUtf8("Ouvrir un fichier"),
            home_dir,
            )
        if not s :
            pass
        else :
            self.importIngList = ImportIng()
            self.importIngList.parseFile(s)
            self.baseReload
                    
    def addStyle(self) :
        self.lineEditGenre.setText(self.comboBoxStyle.currentText())
        
    def recipeNotesClicked (self) :
        self.switchToNotes()
        self.textEditRecipeNotes.setText(self.recipe.recipeNotes)
    
    def recipeNotesAccepted (self) :
        self.switchToEditor()
        self.recipe.recipeNotes = self.textEditRecipeNotes.toPlainText()
        
    def recipeNotesRejected (self) :
        self.switchToEditor()
        
    def popMashCombo (self):
        self.comboBoxMashProfiles.clear() 
        for mash in ImportBase().listeMashes :
           self.comboBoxMashProfiles.addItem(mash.name)
           
    def mashComboChanged (self) :
        #on remet le verrou à 0, il va falloir recalculer en repassant en brewday mode
        self.brewdayLock = 0
        try :
            i =self.comboBoxMashProfiles.currentIndex()
            self.currentMash = ImportBase().listeMashes[i]
        except :
            self.currentMash = self.currentRecipeMash
        if i == -1 :
            self.currentMash = Mash()
        self.recipe.mash = self.currentMash
        
    def seeMash(self) :
        self.switchToMash()
        index = self.listWidgetMashProfiles.currentRow()
        i = self.listWidgetSteps.currentRow()
        self.listWidgetMashProfiles.clear()
        self.listWidgetSteps.clear()

        self.numMash = len(ImportBase().listeMashes)
        #self.numSteps = self.mashProfilesBase.numSteps
        self.popMashList()
        self.pushButtonMashEdit.setEnabled(False)
        self.pushButtonRemoveProfile.setEnabled(False)
        self.pushButtonStepRemove.setEnabled(False)
        self.pushButtonStepEdit.setEnabled(False)
        self.listWidgetMashProfiles.setCurrentRow(index)
        self.listWidgetSteps.setCurrentRow(i)

    def popMashList(self) :
        self.listWidgetMashProfiles.clear() 
        for mash in ImportBase().listeMashes :
           self.listWidgetMashProfiles.addItem(mash.name)    
            
    def mashClicked(self) :
        self.listWidgetSteps.clear()         
        index = self.listWidgetMashProfiles.currentRow()
        if index > -1:
            mash = ImportBase().listeMashes[index]
            for step in mash.listeSteps :
                self.listWidgetSteps.addItem(step.name)

            self.labelStepName.setTextFormat(QtCore.Qt.RichText)
            self.labelMashName.setText("<b>" + mash.name + "</b>")
            self.labelMashPh.setText("%.1f" %float(mash.ph))
    #        self.labelMashGrainTemp.setText("%.1f" %float(self.dicMashDetail['grainTemp']))
    #        self.labelMashTunTemp.setText("%.1f" %float(self.dicMashDetail['tunTemp']))
            try :
                self.labelMashSpargeTemp.setText("%.1f" %float(mash.spargeTemp))
            except :
                pass
            try :
                self.listWidgetSteps.setCurrentRow(0)
            except :
                pass
    #        print(self.dicMashDetail)
            self.pushButtonMashEdit.setEnabled(True)
            self.pushButtonRemoveProfile.setEnabled(True)
            
    def mashDetails(self) :
        self.dlgMashDetail = DialogMashDetail(self)
        self.dlgMashDetail.setModal(True)
        self.dlgMashDetail.show()
        self.dlgMashDetail.setFields(self.currentMash)
        self.dlgMashDetail.setAttribute( QtCore.Qt.WA_DeleteOnClose, True ) 

        
    def stepDetails(self) :
        index = self.listWidgetMashProfiles.currentRow()
        if index > -1:
            selected_mash = ImportBase().listeMashes[index]
            i = self.listWidgetSteps.currentRow()
            if i > -1:
                try:
                    selected_step = selected_mash.listeSteps[i]
                    self.labelStepName.setTextFormat(QtCore.Qt.RichText)
                    self.labelStepName.setText("<b>" + selected_step.name +"</b>")
                    self.labelStepType.setText(selected_step.type)
                    self.labelStepTemp.setText(MashStepView.temp_to_display(selected_step.temp))
                    self.labelStepTime.setText(MashStepView.time_to_display(selected_step.time))
                    self.pushButtonStepRemove.setEnabled(True)
                    self.pushButtonStepEdit.setEnabled(True)
                except:
                    pass
        
        
    def stepEdit(self) :
        index = self.listWidgetMashProfiles.currentRow()
        if  index > -1:
            selected_mash = ImportBase().listeMashes[index]
            i = self.listWidgetSteps.currentRow()
            if i > -1:
                selected_step = selected_mash.listeSteps[i]

                self.dlgStep.show()
                self.dlgStep.fields (selected_step)
    
    def stepReload(self, step) :
        index = self.listWidgetMashProfiles.currentRow()
        if index > -1:
            selected_mash = ImportBase().listeMashes[index]
            i = self.listWidgetSteps.currentRow()
            if i > -1:
                selected_step = selected_mash.listeSteps[i]

                selected_step.name = step.name
                selected_step.type = step.type
                selected_step.temp = step.temp
                selected_step.time = step.time
                self.seeMash()
                self.stepDetails()
                self.listWidgetMashProfiles.setCurrentRow(index)
                self.listWidgetSteps.setCurrentRow(i)
        
    def removeStep(self) :
        index = self.listWidgetMashProfiles.currentRow()
        if index > -1:
            selected_mash = ImportBase().listeMashes[index]
            i = self.listWidgetSteps.currentRow()
            if i > -1:
                item = self.listWidgetSteps.currentItem()
                del selected_mash.listeSteps[i]
                # self.listWidgetSteps.clearSelection()
                #self.listWidgetSteps.takeItem(item)
                #On force la sélection sur la ligne précédente
                self.listWidgetSteps.setCurrentRow(i-1)
                self.seeMash()
        
    def addStep(self) :
        index = self.listWidgetMashProfiles.currentRow()
        selected_mash = ImportBase().listeMashes[index]
        i = self.listWidgetSteps.currentRow()
        step = MashStep()
        step.name = 'Nouveau palier'
        step.type = 'Infusion'
        step.time = '0'
        step.temp = '0'
        step.vol = '0'
        selected_mash.listeSteps.append(step)

        self.listWidgetMashProfiles.setCurrentRow(index)
        self.seeMash()
        self.stepDetails()      
        self.listWidgetMashProfiles.setCurrentRow(index)
        # self.listWidgetSteps.setCurrentRow(i-1)
        # self.stepEdit()
        
    def mashEdit(self) :
        index = self.listWidgetMashProfiles.currentRow()
        selected_mash = ImportBase().listeMashes[index]
        self.dlgMash.show()
        self.dlgMash.fields(selected_mash)
        
    def mashReload(self,mash) :
        #on remet le verrou à 0, il va falloir recalculer en repassant en brewday mode
        self.brewdayLock = 0
        
        f = self.listWidgetMashProfiles.currentRow()
        selected_mash = ImportBase().listeMashes[f]
        selected_mash.name = mash.name
        selected_mash.ph = mash.ph
        selected_mash.grainTemp = 20
        selected_mash.tunTemp = 20
        selected_mash.spargeTemp = mash.spargeTemp
        self.popMashList()
        self.listWidgetMashProfiles.setCurrentRow(f)
        
#        print(self.dicMashDetail)

    def addMash(self) :
        new_mash = Mash()
        new_mash.name = 'Nouveau profil'
        new_mash.grainTemp = '0'
        new_mash.tunTemp = '0'
        new_mash.spargeTemp = '78'
        new_mash.ph = 5.4
        new_step = MashStep()
        new_step.name = 'Nouveau Palier'
        new_step.type = 'Infusion'
        new_step.time = '0'
        new_step.temp = '0'
        new_mash.listeSteps.append(new_step)
        ImportBase().listeMashes.append(new_mash)
        self.seeMash()
        self.listWidgetMashProfiles.setCurrentRow(len(ImportBase().listeMashes)-1)
        
    def removeMash(self) :
        i = self.listWidgetMashProfiles.currentRow()
        del ImportBase().listeMashes[i]
        self.seeMash()
        self.listWidgetSteps.clear() 
        
    def mashRejected (self) :
        self.switchToPreviousPage()

    def saveProfile(self) : 
        self.mashProfileExport.export(ImportBase().listeMashes)
        self.mashProfileExport.enregistrer(mash_file)
               
        
    def printRecipe (self) :
        printer=QtGui.QPrinter()
        dialog = QtGui.QPrintDialog(printer)
        dialog.setModal(True)
        dialog.setWindowTitle("Print Document" )
        if dialog.exec_() == True:
            # self.webViewBiblio.print(printer)
            document=QtGui.QTextDocument()
            stringHtml=self.recipe.export("print")
            document.setHtml(stringHtml)
            document.print(printer)
    

    @QtCore.pyqtSlot()
    def printBrewday(self) :
        printer=QtGui.QPrinter()
        dialog = QtGui.QPrintDialog(printer)
        dialog.setModal(True)
        dialog.setWindowTitle("Print Document" )
        if dialog.exec_() == True:
            self.webViewBrewday.print(printer)
            # document = self.webViewBrewday.page().currentFrame().toHtml()
            # document.print(printer)
        

                

# from plugins import PluginManager
# from plugins.ExtensionPoints import AppLifecycleExtensionPoint

if __name__ == "__main__":

    initLogging()

    logger = logging.getLogger(__name__)

    # for p in AppLifecycleExtensionPoint.plugins:
    #     p().startup()

    logger.debug("Initializing UI");
    QtCore.QTextCodec.setCodecForCStrings(QtCore.QTextCodec.codecForName("utf-8"))
    app = QtGui.QApplication(sys.argv)
    
    locale = QtCore.QLocale.system().name()
    translator=QtCore.QTranslator ()
    #~ translator.load(("qt_") +locale, QtCore.QLibraryInfo.location(QtCore.QLibraryInfo.TranslationsPath))
    translator.load('joliebulle_' + locale)
    app.installTranslator(translator)

    translatorQt = QtCore.QTranslator ()
    translatorQt.load('qt_' + locale)
    app.installTranslator(translatorQt)

    main_window = AppWindow()
    #main_window = MainWindow()
    # main_window.show()
    main_window.showMaximized()

    logger.debug("UI initialized");

    app.exec_()

    # for p in AppLifecycleExtensionPoint.plugins:
    #     p().shutdown()

