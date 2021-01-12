import tkinter as tk
import Recipes as rec

j = 1


class Application(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self._frame = None
        self.switch_frame(startPage, None)
        self.geometry('1000x1000')

    # Deletes current frame and switches to new frame
    # If New frame takes input, make frame with that input
    def switch_frame(self, frame_class, input):
        new_frame = ""
        if input is None:
            new_frame = frame_class(self)
        else:
            new_frame = frame_class(self, input)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()


# Start Page links to all other pages
class startPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.pack()
        tk.Label(self, text="Welcome to the Restaurant Bot").grid(row=0, column=1)
        # Buttons for each different category
        recipes = tk.Button(self, height=2, width=12, command=lambda: master.switch_frame(allRecipes, None),
                            text="All Recipes", padx=20)
        recipes.grid(row=1, column=1)
        stockBtn = tk.Button(self, height=2, width=12, command=lambda: master.switch_frame(stock, None), text="Stock",
                             padx=20)
        stockBtn.grid(row=1, column=0)
        addBtn = tk.Button(self, height=2, width=12, command=lambda: master.switch_frame(addRecipeFrame, None),
                           text="Add a Recipe", padx=20)
        addBtn.grid(row=1, column=2)
        tk.Label(self, text="Recipes with").grid(row=2, column=1)
        i = 0
        # Make buttons to go to recipes with each individual ingredients
        stocKJSON = rec.importJSON("Stock.txt")
        col = 0
        row = 3
        for x in stocKJSON:
            z = tk.Button(self, height=2, width=12, command=lambda y=x: master.switch_frame(ingredientSpecific, y),
                          text=x)
            z.grid(row=int(row), column=col)
            col = col + 1
            if col >= 3:
                row = row + 1
                col = 0


# Displays all stock. Have button to edit stock for admins
class stock(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.pack()
        tk.Label(self, text="Stock Management").grid(row=0, column=1)
        self.button = tk.Button(self, height=2, width=12, command=lambda: master.switch_frame(startPage, None),
                                text="Home")
        self.button.grid(row=10, column=0)
        self.inp = rec.importJSON("Stock.txt")
        y = 1
        # Make all the entrys
        self.entry = []
        for x in self.inp:
            val = tk.StringVar(self, str(self.inp[x]["Quantity"]))
            tk.Label(self, height=2, width=12, text=x).grid(row=y)
            self.entry.append(tk.Entry(self, textvariable=val))
            self.entry[y - 1].grid(row=y, column=1)
            y = y + 1
        tk.Button(self, height=2, width=12, command=self.updateValues, text="Save").grid(row=10, column=2)

    def updateValues(self):
        r = 0
        for x in self.inp:
            self.inp[x]["Quantity"] = int(self.entry[r].get())
            r = r + 1
        print(self.inp)
        rec.updateFile("Stock.txt", self.inp)
        rec.makeMenu("Stock.txt", "Recipes.txt", "Menu.txt")


class addRecipeFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.pack()
        # Title
        tk.Label(self, text="Add Recipe").grid(row=0, column=1)
        nameOfItem = tk.Entry(self)
        nameOfItem.grid(row=1, column=1)
        tk.Label(self, text="Item Name:").grid(row=1, column=0)
        # Home Button
        self.button = tk.Button(self, height=2, width=12, command=lambda: master.switch_frame(startPage, None),
                                text="Home")
        self.button.grid(row=10, column=1)
        self.ingredientsOnScreen = 4
        tk.Button(self, text="Save and Quit", command=lambda: saveAndQuit()).grid(row=10, column=2)
        testOption = rec.importJSON("Stock.txt")
        # Make option menu for number of ingredient
        numOfIngredients = []
        optionMenuForEachIngredient = []
        for x in testOption:
            numOfIngredients.append(len(numOfIngredients) + 1)
        ingred = tk.StringVar(app)
        ingred.set(numOfIngredients[3])
        tk.Label(self, text="Number of Ingredients:").grid(row=2, column=0)
        tk.OptionMenu(self, ingred, *numOfIngredients).grid(row=2, column=1)
        # Auto update on edits to number of ingredients
        ingred.trace_add('write', lambda *args: changeNumOfIngredients(ingred.get()))
        row = 3
        stockList = []
        for x in testOption:
            stockList.append(x)
        var = []
        i = 0
        inputs = []
        # Option menus for each ingredients
        for x in testOption:
            var.append(tk.StringVar(app))
            var[i].set(stockList[0])
            optionMenuForEachIngredient.append(tk.OptionMenu(self, var[i], *stockList))
            optionMenuForEachIngredient[i].grid(row=row, column=0)
            inputs.append(tk.Entry(self))
            inputs[i].grid(row=row, column=1)

            row = row + 1
            var[i].trace_add('write', lambda *args, z=i: print(z))
            i = i + 1

        # Changes the number of option menus on screen
        def changeNumOfIngredients(z):
            num = int(ingred.get())
            while self.ingredientsOnScreen > num:
                optionMenuForEachIngredient[self.ingredientsOnScreen - 1].grid_forget()
                inputs[self.ingredientsOnScreen - 1].grid_forget()
                self.ingredientsOnScreen = self.ingredientsOnScreen - 1
            while self.ingredientsOnScreen < num:
                optionMenuForEachIngredient[self.ingredientsOnScreen].grid(row=self.ingredientsOnScreen + 3)
                inputs[self.ingredientsOnScreen].grid(row=self.ingredientsOnScreen + 3, column=1)
                self.ingredientsOnScreen = self.ingredientsOnScreen + 1

        def saveAndQuit():
            finalList = []
            for z in range(self.ingredientsOnScreen):

                a_dict = {}
                if inputs[z].get() == '':
                    print("Error")
                    continue
                if not inputs[z].get().isdigit():
                    print(inputs[z].get() + " is not a int")
                    continue
                intVal = int(inputs[z].get())
                a_dict[var[z].get()] = intVal
                finalList.append(a_dict)
            if len(finalList) is 0:
                print("Error No item Added")
            else:
                addRecipeFunction("Recipes.txt", nameOfItem.get(), finalList)
            master.switch_frame(startPage, None)


# Shows recipes with specified ingredients
class ingredientSpecific(tk.Frame):
    def __init__(self, master, ingredient):
        super().__init__(master)
        self.master = master
        self.pack()
        self.ingredient = ingredient
        self.create_widgets(master, ingredient)
        self.button = tk.Button(self, height=2, width=12, command=lambda: master.switch_frame(startPage, None),
                                text="Home")
        self.button.grid(row=10, column=2)

    def create_widgets(self, master, ingredient):
        global j
        menu = rec.importJSON("Menu.txt")
        tk.Label(self, text="Recipes with: " + self.ingredient).grid(row=0, column=2)
        row = 1
        col = 0
        order = []
        for x in menu:
            for b in x.get("Items"):

                if b.get(ingredient) is not None:
                    btn = tk.Button(self, height=2, width=12, command=lambda y=x.get("Name"): orderAndReset("Menu.txt",
                                                                                                            "Stock.txt",
                                                                                                            y,
                                                                                                            "Recipes.txt"),
                                    text=x.get("Name"))
                    btn.grid(row=row, column=col, padx=10, pady=10)
                    col = col + 1
                    if col > 5:
                        row = row + 1
                        col = 0


class allRecipes(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets(master)

    def create_widgets(self, master):
        global j
        menu = rec.importJSON("Menu.txt")
        tk.Label(self, text="All Recipes").grid(row=0, column=2)
        i = 0
        col = 0
        order = []
        for x in menu:
            order.append("")
            order[i] = tk.Button(self, height=2, width=12,
                                 command=lambda y=x.get("Name"): orderAndReset("Menu.txt", "Stock.txt", y,
                                                                               "Recipes.txt"),
                                 text=x.get("Name"))
            order[i].grid(row=j, column=col, padx=10, pady=10)
            i = i + 1
            col = col + 1
            if col > 5:
                j = j + 1
                col = 0
        button = tk.Button(self, height=2, width=12, command=lambda: master.switch_frame(startPage, None), text="Home")
        button.grid(row=j + 1, column=2)


##Takes recipe
def orderAndReset(fmenu, stock, item, recipes):
    rec.order(fmenu, stock, item, recipes)
    global j
    j = 1
    app.switch_frame(startPage, None)


def addRecipeFunction(fileName, itemName, ingredients):
    test = rec.importJSON(fileName).get("Recipes")
    test.append({"Name": itemName, "Items": ingredients})
    rec.updateFile(fileName, {"Recipes": test})
    rec.makeMenu("Stock.txt", "Recipes.txt", "Menu.txt")


app = Application()

# addRecipe("Recipes.txt", "Bmac Burger", [{"Lettuce":1}, {"Buns":3}, {"Patty":3}])

app.mainloop()
