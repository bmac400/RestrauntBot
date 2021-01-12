import json
import MotorControl as motor

cpos = -1
##Take a json file name and import it as json object
def importJSON(fileName):
    f = open(fileName, "r")
    data = json.load(f)
    #print(json.dumps(data,indent=4))
    f.close()

    return data


# Clears old file and puts input(String) into it
def updateFile(fileName, input):
    f = open(fileName,"w")
    data = json.dumps(input, indent=4)
    f.truncate(0)
    f.write(data)
    f.close()



##Split it into individual menu items, returns linked list of acceptable items based off stock
def makeMenu(stock, recipes, menu):
     stock_Items = importJSON(stock)
     recipes_Items = importJSON(recipes)
     menuItems = []
     f = open(menu, "w")
     f.truncate(0)
     x = recipes_Items.get("Recipes")
     menuItems = []
     #Check each recipe
     for y in x:
         item = y.get("Items")
         makeAble = True
         #Ensure we have each item
         for z in item:
            for j in z:
                if(z.get(j) > stock_Items.get(j).get("Quantity")):
                    print("Not enough " + j + " to nake " + y["Name"])
                    makeAble = False
         if(makeAble == True):
             menuItems.append(y)
     json.dump(menuItems, f, indent=4)
     f.close()



#    return menu

##Allow for ordering of items, remove those items from inventory
def order(fmenu, stockFileName, itemName, recipes):
    stock = importJSON(stockFileName)
    menu = importJSON(fmenu)
    #Assume itemname is always in menu
    global cpos
    for i in menu:
        if(i.get("Name") == itemName):
            print("Making " + itemName)
            for j in i.get("Items"):
                for x in j:

                    stock[x]["Quantity"] = stock[x]["Quantity"] - j[x]
                    print("Getting: " + x)
                    cpos = motor.moveTo(stock.get(x).get("Position"), cpos)

    # Check each recipe
    f = open(stockFileName, "w")
    json.dump(stock, f, indent=4)
    f.close()
    makeMenu(stockFileName, recipes, fmenu)


