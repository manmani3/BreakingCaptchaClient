import pyautogui
import sys, time, os


class windowHandler:
    def __init__(self):
        self.iter = 3
        
    def click(self, coords, offset):
        for cycle in len(self.iter):
            for getCoords in len(coords):
                pyautogui.click(getCoords[0],cogetCoordsords[1])
                sleep(0.2)
                
        okButton = []
        okButton = findOkButton(offset)

        pyautogui.click(okButton[0],okButton[1])
    
    # Will get list of masks with original input Image
    def findObjectsXY(self, inputImage, offset):
        objectsXY = []

        return objectsXY

    #Maybe hardcode this
    def findOkButton(self, offset):
        okButton = []
        return okButton


# Test for clicking window with x,y coords in list format
'''
testXY = [ [500,300], [422,520]]
for test in testXY:
    pyautogui.click(test[0],test[1])'''
