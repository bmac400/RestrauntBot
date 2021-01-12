import json
global cpos
#types = 0;
def moveTo(pos, cpos):
    if(cpos == -1):
        print("Calibrating, Moving all the way to the left")
        #Move to left most switch, then reset to point 0
        return moveTo(pos, 0)

    if(cpos == pos):
        print("In position: " + str(pos))
        return cpos
    if(pos > cpos):
        print("Moving Right")
        return moveTo(pos, cpos + 1)
    if(pos < cpos):
        print("Moving Left")
        return moveTo(pos, cpos - 1)



#Main Function Starts Here
