import requests
from bs4 import BeautifulSoup
import re
#import chardet
#from lxml import html

class Scrape:
    def __init__(self):
#        self.text_ldc = self.pullFromWebLDC()
#        self.text_burt = self.pullFromWebBurton()
        
        self.text_ldc = self.readFromFileLDC()
        self.text_burt = self.readFromFileBurt()
        
        self.foodList_ldc = self.breakFood(self.text_ldc)
        self.foodList_burt = self.breakFood(self.text_burt)
        
        self.stationsList_ldc = self.breakStations(self.text_ldc)
        self.stationsList_burt = self.breakStations(self.text_burt)
        
        self.cleanFoodList_ldc = self.cleanList(self.foodList_ldc)
        self.cleanFoodList_burt = self.cleanList(self.foodList_burt)
        
        self.menu_ldc = self.makeMenu(self.cleanFoodList_ldc, self.stationsList_ldc)
        self.menu_burt = self.makeMenu(self.cleanFoodList_burt, self.stationsList_burt)
        
        self.allTimes_ldc = self.mealTimes(self.menu_ldc)
        self.allTimes_burt = self.mealTimes(self.menu_burt)

    def pullFromWebLDC(self):
        # Get content of bon app web page (make request object)
        r_ldc = requests.get('http://carleton.cafebonappetit.com/cafe/east-hall/')
        
        # read HTML from r object
        soup_ldc = BeautifulSoup(r_ldc.content, "lxml")
        
        # Get the section of the HTML where the foods are contained
        food_section_ldc = soup_ldc.find_all("section", class_="panel panel-type-daypart panel-odd")
        
        text_ldc = str(food_section_ldc[0])
        
        self.writeToFileLDC(text_ldc)    
        return text_ldc
    
    def pullFromWebBurton(self):
        # Get content of bon app web page (make request object)
        r_burt = requests.get('http://carleton.cafebonappetit.com/cafe/burton/')

        # read HTML from r object
        soup_burt = BeautifulSoup(r_burt.content, "lxml")

        # Get the section of the HTML where the foods are contained
        food_section_burt = soup_burt.find_all("section", class_="panel panel-type-daypart panel-odd")

        text_burt = str(food_section_burt[0])

        self.writeToFileBurt(text_burt)    
        return text_burt

    def writeToFileLDC(self, text):
        f = open('src_ldc.txt', 'w')
        f.write(text)
        f.close()

    def writeToFileBurt(self, text):
        f = open('src_burt.txt', 'w')
        f.write(text)
        f.close()
        
    def readFromFileLDC(self):
        f = open('src_ldc.txt', 'r')
        text = f.read()
        f.close()
        return text
    
    def readFromFileBurt(self):
        f = open('src_burt.txt', 'r')
        text = f.read()
        f.close()
        return text

    def breakStations(self, text): 
        text = text.split('Bamco.menu_items = ')[1]
        text = text.split('Bamco.cor_icons = ')[0]

        stationList = []

        stations = text.split('"<strong>@')

        for i in range(1,len(stations)):
            tempStationList = stations[i].split("<\/strong>")
            stationList.append(tempStationList[0])
        
        return stationList

    def breakFood(self, text):
        text = text.split('Bamco.menu_items = ')[1]
        text = text.split('Bamco.cor_icons = ')[0]
        myList = text.split('"zero_entree"')

        for i in range(0, len(myList)-1):
            if '"sides"' in str(myList[i]):
                myList[i] = myList[i].split('"id":')[1]

        tempFoodList = []
        foodList = []

        for j in range(0, len(myList)-1):
            tempList = myList[j].split(',"description":"",')
            tempFoodList.append(tempList[0])

        for k in range (len(tempFoodList)):
            tempList = tempFoodList[k].rsplit(':', maxsplit=1)
            foodList.append(tempList[1])

        return foodList

    def makeMenu(self, food, stations):

        menuList = []

        for i in range(0, len(food)):
            menuList.append((food[i], stations[i]))

        return menuList

    def printList(self, list):
        print("\n")
        for item in list:
            print(item)
        print('\n')
    
    def mealTimes(self, menu):
        breakfastList = []
        brunchList = []
        lunchList = []
        dinnerList = []
        allTimes = []
        brunch = False
        lunch = False

        for i in range(0, len(menu)):
            if 'Breakfast' in menu[i][1]:
                breakfastList.append(menu[i])
            if 'Brunch' in menu[i][1]:
                brunchList.append(menu[i])
                brunch = True
            if 'Lunch' in menu[i][1]:
                lunchList.append(menu[i])
                lunch = True
            if 'Soup' in menu[i][1]:
                if brunch == True:
                    brunchList.append(menu[i])
                if lunch == True:
                    lunchList.append(menu[i])
                dinnerList.append(menu[i])
            if 'Cucina Pizza' in menu[i][1] or 'Cucina Pasta' in menu[i][1] or 'Thymes' in menu[i][1]:
                if brunch == True:
                    brunchList.append(menu[i])
                if lunch == True:
                    lunchList.append(menu[i])
                dinnerList.append(menu[i])
            if 'Grill' in menu[i][1] and 'Breakfast' not in menu[i][1]:
                if brunch == True:
                    brunchList.append(menu[i])
                if lunch == True:
                    lunchList.append(menu[i])
                dinnerList.append(menu[i])
            if 'Global' in menu[i][1] or 'American' in menu[i][1] or 'Chopsticks' in menu[i][1]:
                if lunch == True:
                    lunchList.append(menu[i])
                dinnerList.append(menu[i])
            if 'Dinner' in menu[i][1]:
                dinnerList.append(menu[i])
            if 'Cucina' in menu[i][1] and 'Pasta' not in menu[i][1] and 'Pizza' not in menu[i][1] and 'Brunch' not in menu[i][1]:
                dinnerList.append(menu[i])

        allTimes.append(breakfastList)
        allTimes.append(brunchList)
        allTimes.append(lunchList)
        allTimes.append(dinnerList)
        
        return allTimes

    def cleanList(self, foodList):
        editedList = []
        for item in foodList:
            editedItem = re.sub(r'\([^)]*\)', '', item)
            for num in range(10):
                editedItem = re.sub(str(num), '', editedItem)
            editedItem = editedItem.strip(' "\'\t\r\n ')
            editedList.append(editedItem)
        return editedList

    def getDataLDC(self):
        return self.allTimes_ldc
    
    def getDataBurt(self):
        return self.allTimes_burt
    