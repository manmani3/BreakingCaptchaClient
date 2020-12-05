import pyautogui
import sys, time, os


class windowHandler:
    def __init__(self):
        self.iter = 3
        
    def click(self, coords):
        offset = [681,474]
        Bounds = [[95,95], [127,95],[190,95],[253,95],[285,95],[380,95],
                [95,127], [127,127],[190,127],[253,127],[285,127],[380,127],
                [95,190], [127,190],[190,190],[253,190],[285,190],[380,190],
                [95,253], [127,253],[190,253],[253,253],[285,253],[380,253],
                [95,285], [127,285],[190,285],[253,285],[285,285],[380,285],
                [95,380], [127,380],[190,380],[253,380],[285,380],[380,380]]

        print("Needs to click this cells : " + str(coords))
        
        cnt = 0
        for getCoords in coords:
            print (getCoords)
            if getCoords > 0:
                xy = Bounds[cnt]
                print (str(xy))
                pyautogui.click(int(xy[0]-15+offset[0]),int(xy[1])-15+offset[1])
                time.sleep(0.5)
            cnt = cnt + 1

                
        #okButton = []
        #okButton = findOkButton()

        #pyautogui.click(okButton[0],okButton[1])
        
    def checkCell(self, coords):
        offset = [681,474]
        Bounds = [[95,95], [127,95],[190,95],[253,95],[285,95],[380,95],
                [95,127], [127,127],[190,127],[253,127],[285,127],[380,127],
                [95,190], [127,190],[190,190],[253,190],[285,190],[380,190],
                [95,253], [127,253],[190,253],[253,253],[285,253],[380,253],
                [95,285], [127,285],[190,285],[253,285],[285,285],[380,285],
                [95,380], [127,380],[190,380],[253,380],[285,380],[380,380]]
        Bounds.reverse()
        Cells =[0,0,0,0,0,0,
                0,0,0,0,0,0,
                0,0,0,0,0,0,
                0,0,0,0,0,0,
                0,0,0,0,0,0,
                0,0,0,0,0,0]
        #print("Needs to click this cells : " + str(coords))
        for coord in coords:
            cell = 36
            coord = coord.split(",")
            for check in Bounds:
                if (int(check[0])+offset[0] > int(coord[0])) and (int(check[1])+offset[1] > int(coord[1])):
                    cell = cell -1
            Cells[cell] = 1

        return Cells
    
    
    # Will get list of masks with original input Image 
    def findObjectsXY(self, info):
        objectsXY =[]
        for value in info.values():
            for heigh in value:
                heigh_cnt = 0
                for weight in heigh:
                    weight_pixel = weight.tolist()
                    weight_cnt = 0
                    for weightCoords in weight_pixel:
                        if (weightCoords):
                            #print (str(weight_cnt) + " "  + str(heigh_cnt))
                            objectsXY.append(str(weight_cnt) + ", "  + str(heigh_cnt))
                        weight_cnt = weight_cnt + 1
                    heigh_cnt = heigh_cnt + 1
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
