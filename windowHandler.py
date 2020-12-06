import pyautogui
import sys, time, os


class windowHandler:
    def __init__(self,offset, okButton):
        self.iter = 3
        self.offset = offset
        self.okButton = okButton
        
    def click(self, coords):
        offset = self.offset
        Bounds = [[95,95], [127,95],[190,95],[253,95],[285,95],[380,95],
                [95,127], [127,127],[190,127],[253,127],[285,127],[380,127],
                [95,190], [127,190],[190,190],[253,190],[285,190],[380,190],
                [95,253], [127,253],[190,253],[253,253],[285,253],[380,253],
                [95,285], [127,285],[190,285],[253,285],[285,285],[380,285],
                [95,380], [127,380],[190,380],[253,380],[285,380],[380,380]]


        print("Needs to click this cells : " + str(coords))
        
        cnt = 0
        for getCoords in coords:
            #print (getCoords)
            if getCoords > 0:
                xy = Bounds[cnt]
                #print (str(xy))
                pyautogui.click(int(xy[0]+offset[0]-15),int(xy[1])+offset[1]+75-15)
                time.sleep(0.4)
            cnt = cnt + 1
                        
        okButton = self.okButton
        time.sleep(3)
        pyautogui.click(okButton[0]+20,okButton[1]-20)


        #pyautogui.click(okButton[0],okButton[1])
        
    def checkCell(self, coords):
        offset = self.offset
        Bounds = [[0,0,95,95], [95,0,127,95],[127,0,190,95],[190,0,253,95],[235,0,285,95],[285,0,380,95],
                [0,95,95,127], [95,95,127,127],[127,95,190,127],[190,95,253,127],[235,95,285,127],[285,95,380,127],
                [0,127,95,190], [95,127,127,190],[127,127,190,190],[190,127,235,190],[235,127,285,190],[285,127,380,190],
                [0,190,95,253], [95,190,127,253],[127,190,190,253],[190,190,253,253],[235,190,285,253],[285,190,380,253],
                [0,253,95,285], [95,253,127,285],[127,253,190,285],[190,253,253,285],[235,253,285,285],[285,253,380,285],
                [0,280,95,380], [95,280,127,380],[127,280,190,380],[190,285,253,380],[235,280,285,380],[285,285,380,380]]
        #Bounds.reverse()
        Cells =[0,0,0,0,0,0,
                0,0,0,0,0,0,
                0,0,0,0,0,0,
                0,0,0,0,0,0,
                0,0,0,0,0,0,
                0,0,0,0,0,0]
        #print("Needs to click this cells : " + str(coords))
        for coord in coords:
            cell = 0
            coord = coord.split(",")
            for check in Bounds:
                #if (int(check[0])+offset[0] > int(coord[0])) and (int(check[1])+offset[1]+60 > int(coord[1])):
                if ( int(coord[0]) > int(check[0]) and int(coord[0]) < int(check[2]) and int(coord[1]) > int(check[1]) and int(coord[1]) < int(check[3])):
                    Cells[cell] = 1
                cell = cell + 1

        return Cells
    
    
    # Will get list of masks with original input Image 
    def findObjectsXY(self, info):
        objectsXY =[]
        test = open("ObjectsXY.txt","w")
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
                            test.write(str(weight_cnt) + ", "  + str(heigh_cnt))
                        weight_cnt = weight_cnt + 1
                    heigh_cnt = heigh_cnt + 1
        test.close
        return objectsXY



# Test for clicking window with x,y coords in list format
'''
testXY = [ [500,300], [422,520]]
for test in testXY:
    pyautogui.click(test[0],test[1])'''
