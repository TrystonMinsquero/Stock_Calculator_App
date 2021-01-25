from Profile import *
from tkinter import *
from threading import Thread
from time import time


class App(Tk):
    columnHeaders = []
    table = []
    totals = []
    updateStocksThread: Thread
    updateStocksThread = None
    updateStocks = False
    profiles: list
    currentProfile: Profile
    currentProfile = None
    colWidth = [5, 5, 7, 7, 2, 7, 7, 7, 7, 7]

    def __init__(self):
        super().__init__()
        self.geometry("800x480")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def clear(self):
        for widget in self.winfo_children():
            widget.destroy()
        self.columnHeaders = []
        self.table = []
        self.totals = []
        self.updateStocks = False

    def select_profile(self, name):
        Label(self, text="Loading...", font="Bold").pack()
        self.currentProfile = Profile(name)
        self.show_stocks()

    # Changes the screen to the select profile screen, will move to stocks screen if a profile is selected
    def show_select_profile(self, profiles=None):
        if profiles is not None:
            self.profiles = profiles
        self.clear()
        self.title("Select a Profile")
        i = 0
        for name in self.profiles:
            Button(self, text=name, width=40, height=2, font='30', command=lambda x=name: self.select_profile(x)).pack()
            i += 1
        Button(self, text="+", width=40, height=2, font='30', command=self.show_make_profile).pack()

    # Changes the screen to the profile creation screen, will move to the stocks screen after
    def show_make_profile(self):
        self.title("Create a Profile")
        self.clear()

        def clearWarningLabel():
            warningLabel.config(text="")

        def onClick():
            name = nameInput.get()
            if not create_profile_directory(name):
                warningLabel.config(text="Profile name already exists!")
                warningLabel.after(3000, clearWarningLabel)
            else:
                self.select_profile(name)
                self.profiles.append(self.currentProfile.name)

        nameInput = Entry(self, text="Profile Name")
        warningLabel = Label(self, text="", fg="red")
        nameInput.pack()
        Button(self, text="Enter", command=onClick).pack()
        Button(self, text="Cancel", command=self.show_select_profile).pack()
        warningLabel.pack()

    def get(self, stock, item):

        if item == "\n":
            return ""
        if item == "Tag\n":
            return stock.tag
        if item == "Shares\n":
            return self.currentProfile.stocks[stock]
        if item == "Current\nPrice":
            return stock.get_current_price()
        if item == "Dividend\nYield":
            return stock.get_div_yield()
        if item == "Total\nPrice":
            return stock.get_current_price(self.currentProfile.stocks[stock])
        if item == "Yearly\nDividend":
            return stock.get_exp_yearly_yield(self.currentProfile.stocks[stock])
        if item == "Quarterly\nDividend":
            return stock.get_exp_quarterly_yield(self.currentProfile.stocks[stock])

    def get_total(self, item):
        if item == "\n":
            return ""
        if item == "Tag\n":
            return "TOTAL"
        if item == "Shares\n":
            return ""
        if item == "Current\nPrice":
            return ""
        if item == "Dividend\nYield":
            return ""
        if item == "Total\nPrice":
            return self.currentProfile.get_total_current_prices()
        if item == "Yearly\nDividend":
            return self.currentProfile.get_total_yearly_dividend()
        if item == "Quarterly\nDividend":
            return self.currentProfile.get_total_quarterly_dividend()

    def update_totals(self):
        for col in range(5, len(self.totals)):
            self.totals[col].config(text=self.get_total(self.columnHeaders[col]))

    # changes the current stock's row to the current stock's data
    def show_stock(self, stock):
        i = -1
        for stock2 in self.currentProfile.stocks:
            i += 1
            if stock.tag == stock2.tag:
                break

        for col in range(2, len(self.columnHeaders)):
            self.table[i][col].config(text=self.get(stock, self.columnHeaders[col]))

    def show_profile(self):
        self.currentProfile.print_data()

    # def show_stock_data(self, stock):
    #     print("Show Stock info for " + stock.tag + ":")
    #     print(stock)

    def show_add_stock(self):
        self.title("Add a Stock")
        self.clear()

        def clearEntries():
            tagInput.delete(0, "end")
            sharesInput.delete(0, "end")

        def clearWarningLabel():
            warningLabel.config(text="")

        def onAddClick():
            try:
                if int(sharesInput.get()) < 0:
                    warningLabel.config(text="Please enter a number greater than -1")
                    warningLabel.after(3000, clearWarningLabel)
                else:
                    self.currentProfile.add_stock(tagInput.get(), int(sharesInput.get()))
                    clearEntries()
                    self.clear()
                    self.show_stocks()
            except ValueError:
                warningLabel.config(text="Please enter an integer for shares")
                warningLabel.after(3000, clearWarningLabel)
            except "Stock price can't be found":
                warningLabel.config(text="Please enter a valid stock price")
                warningLabel.after(3000, clearWarningLabel)

        def onAddAnotherClick():
            try:
                self.currentProfile.add_stock(tagInput.get(), int(sharesInput.get()))
                clearEntries()
                self.clear()
                self.show_add_stock()
            except ValueError:
                warningLabel.config(text="Please enter a number for shares")
                warningLabel.after(3000, clearWarningLabel)

        def onCancelClick():
            clearEntries()
            self.show_stocks()

        tagLabel = Label(self, text="Tag Name:")
        tagInput = Entry(self, text="Tag")
        sharesLabel = Label(self, text="Number of Shares:")
        sharesInput = Entry(self, text="Shares")
        warningLabel = Label(self, text="", fg="red")
        enterButton = Button(self, text="Add", command=onAddClick)
        addAnotherButton = Button(self, text="Add Another", command=onAddAnotherClick)
        cancelButton = Button(self, text="Cancel", command=onCancelClick)

        items = [tagLabel, tagInput, sharesLabel, sharesInput, warningLabel, enterButton, addAnotherButton,
                 cancelButton]

        for item in items:
            item.pack()

    def show_edit_stocks(self):
        self.title("Edit Stock List")
        self.clear()

        def finish():
            self.show_stocks()

        def clearWarningLabel():
            warningLabel.config(text="")

        def edit_stock(stock):
            try:
                shares = int(sharesEntry.get())
                if shares < 0:
                    delete_stock(stock)
                else:
                    self.currentProfile.edit_stock(stock, shares)
            except ValueError:
                warningLabel.config(text="Please enter an integer for shares")
                warningLabel.after(3000, clearWarningLabel)

        def delete_stock(stock):
            self.currentProfile.delete_stock(stock)
            self.show_edit_stocks()

        def show_entries(stock):
            stockLabel.config(text="You are now editing: " + stock.tag)
            sharesEntry.delete(0, END)
            sharesEntry.insert(0, str(self.currentProfile.stocks[stock]))
            saveButton.config(command=lambda x=stock: edit_stock(x))
            deleteButton.config(command=lambda x=stock: delete_stock(x))
            for item in entryWidgets:
                item.pack()

        def onTagClick(stock):
            show_entries(stock)

        frame = Frame(self, borderwidth=1, relief=SOLID)
        frame.pack()
        Button(self, text="Done", command=finish).pack(pady=20)
        tagButtonsFrame = Frame(frame, borderwidth=1, relief=SOLID)
        tagButtonsFrame.grid(row=0, column=0)
        for thisStock in self.currentProfile.stocks:
            Button(tagButtonsFrame, text=thisStock.tag, width=self.colWidth[0],
                   command=lambda x=thisStock: onTagClick(x)).pack()

        entryFrame = Frame(frame, borderwidth=1, relief=SOLID)
        entryFrame.grid(row=0, column=1)
        stockLabel = Label(entryFrame, text="You are now editing: 00000", font="Bold")
        sharesLabel = Label(entryFrame, text="Shares:")
        sharesEntry = Entry(entryFrame, width=10)
        warningLabel = Label(entryFrame, text="", fg="red")
        buttonFrame = Frame(entryFrame)
        saveButton = Button(buttonFrame, text="Save")
        saveButton.pack(side=LEFT)
        deleteButton = Button(buttonFrame, text="Delete")
        deleteButton.pack(side=RIGHT)

        entryWidgets = [stockLabel, sharesLabel, sharesEntry, warningLabel, buttonFrame]
        for widget in entryWidgets:
            widget.pack()

        print(str(entryFrame.winfo_width()) + " " + str(entryFrame.winfo_height()))
        # entryFrame.config(width=entryFrame.winfo_width(), height=entryFrame.winfo_height())
        # entryFrame.pack_propagate(0)
        # for widget in entryWidgets:
        #     widget.pack_forget()

    def __make_column_header(self, title, col):
        row = 1
        Button(self, width=self.colWidth[col], height=2, borderwidth=1, relief="solid",
               state="disabled").grid(row=row, column=col)
        Label(self, text=title, width=self.colWidth[col]). \
            grid(row=row, column=col)
        return title

    def __make_stock_row(self, stock, row):
        tableRow = []
        col = 0
        for column in self.columnHeaders:
            if col == 0:
                label = Button(self, text=self.get(stock, column), width=self.colWidth[col], height=1,
                               borderwidth=1,
                               relief="ridge")
            else:
                Button(self, width=self.colWidth[col], height=1, borderwidth=1, relief="solid",
                       state="disabled").grid(row=row, column=col)
                label = Label(self, text=self.get(stock, column), width=self.colWidth[col])
            label.grid(row=row, column=col)
            tableRow.append(label)
            col += 1

        return tableRow

    def show_stocks(self):

        row = 0

        # on click of the start/stop button
        def start_stop():
            self.updateStocks = not self.updateStocks
            if self.updateStocks:
                startStopButton.config(text="Stop")
            else:
                startStopButton.config(text="Start")

            if self.updateStocksThread is None and self.updateStocks:
                self.updateStocksThread = Thread(target=lambda x=self: update_stocks(x), args=[])
                self.updateStocksThread.start()

        self.title(self.currentProfile.name)
        self.clear()
        # Top Buttons
        topButtonsFrame = Frame(self)
        topButtonsFrame.grid(row=0, column=0)
        padx = 2
        startStopButton = Button(topButtonsFrame, text="Start", width=self.colWidth[0] - 1, command=start_stop)
        startStopButton.grid(row=row, column=0, padx=padx)
        Button(topButtonsFrame, text="Add", width=self.colWidth[1] - 1, command=self.show_add_stock).grid(row=0,
                                                                                                          column=1,
                                                                                                          padx=padx)
        Button(topButtonsFrame, text="Edit", width=self.colWidth[2] - 1, command=self.show_edit_stocks).grid(row=0,
                                                                                                             column=2,
                                                                                                             padx=padx)
        Button(topButtonsFrame, text="Profiles", width=self.colWidth[3] - 1, command=self.show_select_profile).grid(
            row=0, column=3, padx=padx)
        row += 1
        # Column Headers
        self.columnHeaders = [
            self.__make_column_header("Tag\n", 0),
            self.__make_column_header("Shares\n", 1),
            self.__make_column_header("Current\nPrice", 2),
            self.__make_column_header("Dividend\nYield", 3),
            self.__make_column_header("\n", 4),
            self.__make_column_header("Total\nPrice", 5),
            self.__make_column_header("Yearly\nDividend", 6),
            self.__make_column_header("Quarterly\nDividend", 7),
        ]
        topButtonsFrame.grid(columnspan=len(self.columnHeaders))
        row += 1
        # Substance
        for stock in self.currentProfile.stocks:
            tableRow = self.__make_stock_row(stock, row)
            row += 1
            self.table.append(tableRow)
            self.show_stock(stock)
        # Totals
        col = 0
        for column in self.columnHeaders:
            Button(self, width=self.colWidth[col], height=1, borderwidth=1, relief="solid",
                   state="disabled").grid(row=row, column=col)
            totalLabel = Label(self, text=self.get_total(column), width=self.colWidth[col])
            totalLabel.grid(row=row, column=col)
            self.totals.append(totalLabel)
            col += 1
        self.update_totals()

    def on_closing(self):
        self.quit()


# Will update all stocks in currentProfile's stock list
def update_stocks(app):
    iterations = 0
    print("updating...")
    while app.updateStocks:
        for stock in app.currentProfile.stocks:
            if app.updateStocks:
                begin = time()
                stock.update()  # this operation takes roughly a second
                end = time()
                print("Found " + stock.tag + " in " + str(round(end-begin, 2)) + " seconds")
                app.show_stock(stock)
                app.update_totals()
        iterations += 1
        print("iterations: " + str(iterations))
    print("Stop updating")
    app.updateStocksThread = None
