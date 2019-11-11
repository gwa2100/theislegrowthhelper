#!/usr/bin/python

"""
    The Isle Management Console
    Version 0.1.5
    By: Timothy Carlisle
    Description:
        This script is meant to simplify the creation and modification
        of user files via FTP for The Isle game server administrators.
    TIMC.py is the main starting point for The Isle Management Console.
    Licensed under the GPLv3
    This product is copyrighted by Timothy Carlisle.
    Contact gwa2100@gmail.com with any questions.
"""
__title__ = 'The Isle Management Console'
__all__ = ['The Isle', 'console']
__version__ = '0.1.5'
__author__ = 'Timothy Carlisle (gwa2100)'

import ftplib
import json
import tkinter
from tkinter import ttk
import os
import random


class Console:
    def __init__(self):
        self.dinoList = [
            "Anky",
            "AnkyJuv",
            "Austro",
            "AustroJuv",
            "Ava",
            "AvaJuv",
            "Camara",
            "Oro",
            "Taco",
            "Puerta",
            "PuertaJuv",
            "Shant",
            "ShantJuv",
            "Stego",
            "StegoJuv",
            "Theri",
            "TheriJuv",
            "Acro",
            "AcroJuv",
            "Albert",
            "Bary",
            "BaryJuv",
            "Herrera",
            "HerreraJuv",
            "Spino",
            "SpinoJuv",
            "Velo",
            "DiabloAdultS",
            "DiabloJuvS",
            "DiabloHatchS",
            "DryoAdultS",
            "DryoJuvS",
            "DryoHatchS",
            "GalliAdultS",
            "GalliJuvS",
            "GalliHatchS",
            "MaiaAdultS",
            "MaiaJuvS",
            "MaiaHatchS",
            "PachyAdultS",
            "PachyHatchS",
            "PachyJuvS",
            "ParaAdultS",
            "ParaJuvS",
            "ParaHatchS",
            "TrikeAdultS",
            "TrikeSubS",
            "TrikeJuvS",
            "TrikeHatchS",
            "AlloAdultS",
            "AlloJuvS",
            "AlloHatchS",
            "CarnoAdultS",
            "CarnoSubS",
            "CarnoJuvS",
            "CarnoHatchS",
            "CeratoAdultS",
            "CeratoJuvS",
            "CeratoHatchS",
            "DiloAdultS",
            "DiloJuvS",
            "DiloHatchS",
            "GigaAdultS",
            "GigaSubS",
            "GigaJuvS",
            "GigaHatchS",
            "SuchoAdultS",
            "SuchoHatchS",
            "SuchoJuvS",
            "RexAdultS",
            "RexSubS",
            "RexJuvS",
            "UtahAdultS",
            "UtahJuvS",
            "UtahHatchS"]

        # Core Objects
        self.top = tkinter.Tk()
        self.top.protocol("WM_DELETE_WINDOW", self.CatchShutdown)
        self.top.title(__title__ + " v" + __version__)

        self.top.geometry('900x640')
        self.serverIPEntryLabel = tkinter.Label(self.top, text="FTP IP:")
        self.serverIPEntryLabel.grid(column=0, row=0)
        self.serverIPEntry = tkinter.Entry(self.top, width=10)
        self.serverIPEntry.grid(column=1, row=0)

        self.serverPortEntryLabel = tkinter.Label(self.top, text="PORT:")
        self.serverPortEntryLabel.grid(column=2, row=0)
        self.serverPortEntry = tkinter.Entry(self.top, width=5)
        self.serverPortEntry.insert(tkinter.END, "21")
        self.serverPortEntry.grid(column=3, row=0)

        self.serverUsernameEntryLabel = tkinter.Label(self.top, text="USER:")
        self.serverUsernameEntryLabel.grid(column=4, row=0)
        self.serverUsername = tkinter.Entry(self.top, width=20)
        self.serverUsername.grid(column=5, row=0)

        self.serverPasswordEntryLabel = tkinter.Label(self.top, text="PASS:")
        self.serverPasswordEntryLabel.grid(column=6, row=0)
        self.serverPassword = tkinter.Entry(self.top, width=20, show="*")
        self.serverPassword.grid(column=7, row=0)

        self.userIDEntryLabel = tkinter.Label(self.top, text="USER ID:")
        self.userIDEntryLabel.grid(column=0, row=1)

        self.userIDEntry = tkinter.Entry(self.top, width=20)
        self.userIDEntry.grid(column=1, row=1)

        self.getBtn = tkinter.Button(self.top, command=self.GetUserFile, text="Load User")
        self.getBtn.grid(column=2, row=1)

        self.userDinoEntryLabel = tkinter.Label(self.top, text="Dino:")
        self.userDinoEntryLabel.grid(column=0, row=2)

        self.userDinoVar = tkinter.StringVar()
        self.userDinoMenu = ttk.Combobox(self.top, textvariable=self.userDinoVar, values=self.dinoList)
        self.userDinoMenu.grid(column=1, row=2)

        self.userGrowthSliderLabel = tkinter.Label(self.top, text="Growth: %")
        self.userGrowthSliderLabel.grid(column=2,row=2)

        self.userGrowthSlider = tkinter.Scale(self.top, from_=1, to = 100, orient=tkinter.HORIZONTAL)
        self.userGrowthSlider.grid(column=3,row=2)

        self.isMale = tkinter.BooleanVar()
        self.checkBoxMale = tkinter.Checkbutton(self.top, text="Female", variable=self.isMale)
        self.checkBoxMale.grid(column=0, row=3)

        self.isBrokenLegged = tkinter.BooleanVar()
        self.checkBoxBrokenLegs = tkinter.Checkbutton(self.top, text="Broken Legs", variable=self.isBrokenLegged)
        self.checkBoxBrokenLegs.grid(column=1, row=3)

        self.isResting = tkinter.BooleanVar()
        self.checkBoxResting = tkinter.Checkbutton(self.top, text="Resting", variable=self.isResting)
        self.checkBoxResting.grid(column=2, row=3)

        self.randomizeOn = tkinter.BooleanVar()
        self.checkBoxRandomizeSkin = tkinter.Checkbutton(self.top, text="Random Skin", variable=self.randomizeOn)
        self.checkBoxRandomizeSkin.grid(column=3, row=3)

        self.growUserBtn = tkinter.Button(self.top, command=self.GrowUser, text="Save User")
        self.growUserBtn.grid(column=2, row=4)

        self.errorText = ttk.Label(self.top)
        self.errorText["text"]= "No errors"
        self.errorText.place(x=0, y=175)

        # Configs
        self.ftpHostAddress = ""
        self.ftpHostPort = ""
        self.ftpUsername = ""
        self.ftpPassword = ""
        self.ftpUserFileDir = ""
        self.locations = [
            "Location_IslandV3",
            "Location_Thenyaw_Island",
            "DevTest"
        ]
        self.filesDownloaded = []

        # Startup check for ftp save file
        with open("config.dat", 'a+') as f:
            f.seek(0)
            try:
                data = json.load(f)
                self.ftpHostAddress = data['ftpHostAddress']
                self.ftpHostPort = data['ftpHostPort']
                self.ftpUsername = data['ftpUsername']
                self.ftpPassword = ""

                self.serverIPEntry.insert(tkinter.END, self.ftpHostAddress)
                self.serverPortEntry.insert(tkinter.END, self.ftpHostPort)
                self.serverPortEntry.delete(0,tkinter.END)
                if self.ftpHostPort == "":
                    self.serverPortEntry.insert(tkinter.END, "21")
                else:
                    self.serverPortEntry.insert(tkinter.END, self.ftpHostPort)
                self.serverUsername.insert(tkinter.END, self.ftpUsername)
            except TypeError:
                pass

            f.close()

        # Class-wide variables
        self.userID = ""
        self.userFileName = ""

    def MainLoop(self):
        self.top.mainloop()

    def ValidateInformation(self):
        if self.userFileName and self.ftpHostAddress and self.ftpHostPort and self.ftpUsername and self.ftpPassword:
            return True
        else:
            localErrorText = "Missing "
            if not self.userFileName:
                localErrorText += "UserID, "
            if not self.ftpHostAddress:
                localErrorText += " Host Address, "
            if not self.ftpHostPort:
                localErrorText += " Host Port, "
            if not self.ftpUsername:
                localErrorText += " Host Username, "
            if not self.ftpPassword:
                localErrorText += " Host Password, "
            self.errorText["text"] = localErrorText[0:-2]
            return False

    def ProcessEntries(self):

        self.userID = self.StripPrePostBlanks(str(self.userIDEntry.get()))
        self.userFileName = self.userID + '.json'
        self.ftpHostAddress = self.serverIPEntry.get()
        self.ftpHostPort = int(self.serverPortEntry.get())
        self.ftpUsername = self.serverUsername.get()
        self.ftpPassword = self.serverPassword.get()
        if self.ValidateInformation():
            return True
        else:
            return False

    def StripPrePostBlanks(self, pString):
        outmessage = ""
        for character in pString:
            if character != " ":
                outmessage += character
        return outmessage

    def GetUserFile(self):
        if self.ProcessEntries():
            ftpObject = ftplib.FTP()
            ftpObject.connect(self.ftpHostAddress, self.ftpHostPort)
            ftpObject.login(self.ftpUsername, self.ftpPassword)
            ftpObject.cwd(self.ftpUserFileDir)
            handle = open(self.userID + '.json', 'wb')
            ftpObject.retrbinary('RETR %s' % self.userFileName, handle.write)
            handle.close()
            with open(self.userFileName, 'r') as f:
                data = json.load(f)
                self.userDinoVar.set(data['CharacterClass'])
                self.isMale.set(data['bGender'])
                self.isBrokenLegged.set(data['bBrokenLegs'])
                self.isResting.set(data['bIsResting'])
                self.userGrowthSlider.set(str(float(data['Growth'])*100))
                self.randomizeOn.set('False')
                f.close()
            ftpObject.close()
            self.filesDownloaded.append(self.userFileName)
            self.errorText["text"] = "Operation Successful : File Loaded"
        return

    def PutUserFile(self, targetFileName):
        if self.ProcessEntries():
            ftpObject = ftplib.FTP()
            ftpObject.connect(self.ftpHostAddress, self.ftpHostPort)
            ftpObject.login(self.ftpUsername, self.ftpPassword)
            ftpObject.cwd(self.ftpUserFileDir)
            handle = open(targetFileName, 'rb')
            ftpObject.storbinary('STOR %s' % targetFileName, handle)
            handle.close()
            ftpObject.close()
            self.errorText["text"] = "Operation Successful : File Stored"
        else:
            return

    def GrowUser(self):
        data = ''
        with open(self.userFileName, 'rb+') as f:
            data = json.load(f)
            f.close()
        with open(self.userFileName, 'w+') as f:
            data['CharacterClass'] = self.userDinoVar.get()
            data['Health'] = 9999
            data['Hunger'] = 9999
            data['Thirst'] = 9999
            data['Stamina'] = 9999
            data['bGender'] = str(self.isMale.get())
            data['bBrokenLegs'] = str(self.isBrokenLegged.get())
            data['bIsResting'] = str(self.isResting.get())
            data['Growth'] = str(self.userGrowthSlider.get()/100)
            if self.randomizeOn.get():
                data['SkinPaletteSection1'] = random.randint(1, 32)
                data['SkinPaletteSection2'] = random.randint(1, 32)
                data['SkinPaletteSection3'] = random.randint(1, 32)
                data['SkinPaletteSection4'] = random.randint(1, 32)
                data['SkinPaletteSection5'] = random.randint(1, 32)
                data['SkinPaletteSection6'] = 254
                data['SkinPaletteVariation'] = str(float(random.randint(1, 6)))

            #Camera Fix
            data['CameraRotation_Thenyaw_Island'] = "P=0.000000 Y=-121.232460 R=0.000000"
            data['CameraDistance_Thenyaw_Island'] = "400.000000"


            json.dump(data, f, indent=4)
            f.close()
        self.PutUserFile(self.userFileName)

    def SaveConfig(self):
        cfgJson = {}
        cfgJson['ftpHostAddress'] = self.serverIPEntry.get()
        cfgJson['ftpHostPort'] = self.serverPortEntry.get()
        cfgJson['ftpUsername'] = self.serverUsername.get()
        print(self.ftpUsername)

        with open("config.dat", 'w+') as f:
            json.dump(cfgJson, f, indent=4)
            f.close()

    def Cleanup(self):
        try:
            for f in self.filesDownloaded:
                os.remove(f)
        except:
            pass

    def CatchShutdown(self):
        self.Cleanup()
        self.SaveConfig()
        self.top.destroy()


console = Console()
console.MainLoop()
