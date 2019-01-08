from tkinter import *
import tkinter.scrolledtext
from tkinter.filedialog import *
from PIL import Image,ImageTk
import PyPDF2,shelve
from tkinter.ttk import Progressbar

#file path of folder
path = os.path.dirname(os.path.realpath(sys.argv[0]))

iconpath = path+r"\pdfsummaryicon.ico"
findIMAGEpath = path+r"\findIMAGE.png"

"""
SCROLLEDTEXT
 self.summaryScroll = tkinter.scrolledtext.ScrolledText(self, width = 50)
 
        #INSERTING TEXT
        self.summaryScroll.insert('insert', "3gdgfd0gfdg")
        self.summaryScroll.insert('insert', "90w530439uiefhdoiafhsdaof")
        
        
        #####REPLACING ALL TEXT ('1.0','end',(Text))
        self.summaryScroll.replace('1.0','end',"fdkljfds")

        self.summaryScroll.grid(row = 3, column = 2, columnspan = 2)

"""


class Page():
    #constructor
    def __init__(self):
        self.pageNumber = -1

        self.dictionary_words = {}
        self.page_raw = ""
        self.sorted_words = []


        self.removable = [",",".","!","$","#","@","^","&","*","-","_","+","-","/","(",")",":",";","?"]
        self.filler_words = ["and","than", "the", "there", "from", "you",
                                    "your", "their", "why", "his", "her", "I", "is", "are", "was", "were", "that",
                                    "the", "this","when","how","its","dont","which","but","also"]

    #distinguishes words and inserts them into the dictionary of words (NOT THE SORTED WORDS)
    def PullWords(self):
        new_word = ""

        for letter in self.page_raw:
            letter = letter.lower() #lowers the letter to make it easier to identify

            #keeps creating the word as it goes through each letter
            if(letter.isspace()==False and letter.isdigit()==False and letter not in self.removable):
                new_word = new_word+letter

            else:
                if(len(new_word)>2 and new_word not in self.filler_words):
                    if new_word not in self.dictionary_words:
                        self.dictionary_words[new_word] = 1
                    else:
                        count = self.dictionary_words[new_word]
                        count +=1
                        self.dictionary_words[new_word] = count
                new_word = ""

    def takeSecond(self,elem):
        return elem[1]

    #sorts the dictionary of words (LARGEST TO SMALLEST)
    def SortWords(self):
        sortedlist = self.dictionary_words.items()
        sortedlist = sorted(sortedlist,key=self.takeSecond,reverse=True)
        self.sorted_words = sortedlist

    def printWords(self):
        print(self.dictionary_words)


    def returnSummary(self,numberofwords):
        summary = "Most Occuring Words:\n"

        try:
            for i in range(numberofwords):
                word = self.sorted_words[i][0]
                summary = summary + str(i+1) +") "+ word + "\n"
            return summary
        except:
            return summary




class MainScreen(Frame):
    # METHODS -----------------------------------------------------------------

    def createSave(self):
        ""

    def takeSecond(self,elem):
        return elem[1]

    #returns a list of n number of words (only pulls different words not same word)
    def pullSummaryWords(self, inputlist):
        returnlist = []

        for i in inputlist:
            if i[0] not in returnlist:
                returnlist.append(i[0])

        return returnlist




    #creates the summary of the full pdf (pulls the most occurring words and picks the top 10)
    def createAllSummary(self):
        numberofwords = 5 #the number of words to pull from each page (pulls the most occurring words)

        #goes through each page's list of sorted words and pulls the top occurring words and
        #adds them into the summary list
        for page in self.dictofpages:
            if len(self.dictofpages[page].sorted_words)<numberofwords:
                self.fullSummary = self.fullSummary+self.dictofpages[page].sorted_words
            else:
                #pulls out the top occurring words from the sorted list if its larger/equal to desired number of words to pull
                self.fullSummary = self.fullSummary+ self.dictofpages[page].sorted_words[0:numberofwords]

        #sorts the self.fullSummary
        self.fullSummary = sorted(self.fullSummary,key = self.takeSecond, reverse= True)

        self.fullSummary = self.pullSummaryWords(self.fullSummary)



    def allSummary(self):
        self.resetSummaryBox()

        #adding text to summary box
        summary = "Most Occurring Words:\n"
        for i in range(self.numberofSummaryWords):
            try:
                summary = summary + str(i+1)+")" + str(self.fullSummary[i])+ "\n"
            except:
                print("could not add to summary")

        self.updateSummaryText(summary)





    def findWord(self, word):
        foundstring = ""
        iswordfound = False
        ispartialfound = False

        #try:
        for page in self.dictofpages:
            partial_count = 0 #keeps track of how many times the partial word appears
            phrasestring = "("

            #print(foundstring)
            keys = self.dictofpages[page].dictionary_words.keys()

            for key in keys:
                #if the word requested is in the current page
                if word in key and len(word) == len(key):
                    iswordfound = True

                    #number of times the word is within the page
                    found_count = self.dictofpages[page].dictionary_words[word]

                    if found_count == 1:
                        foundstring = foundstring + "PAGE " + str(self.dictofpages[page].pageNumber) + "|Found " + str(
                            found_count) + " time.\n\n"
                    else:
                        foundstring = foundstring + "PAGE " + str(self.dictofpages[page].pageNumber) + "|Found " + str(
                            found_count) + " times.\n\n"

                elif word in key:#self.dictofpages[page].dictionary_words:
                    #print("TRUE")
                    ispartialfound = True
                    partial_count +=1
                    phrasestring = phrasestring + '"'+key+'",'


            if(ispartialfound and partial_count>0):
                phrasestring = phrasestring+")"

                if partial_count ==1:
                    foundstring = foundstring + "PAGE " + str(self.dictofpages[page].pageNumber) + "|Found Partial " + str(partial_count) + " time.\n" + phrasestring +"\n\n"
                else:
                    foundstring = foundstring + "PAGE " + str(
                        self.dictofpages[page].pageNumber) + "|Found Partial " + str(
                        partial_count) + " times.\n" + phrasestring + "\n\n"

        """
        except:
            self.resetSummaryBox()
            self.updateSummaryText("ERROR")
            print("ERROR")
            return"""

        """
        if(isnotfound and word not in self.filler_words):
            self.resetSummaryBox()
            self.updateSummaryText("Did not find inputted word.")
            self.summaryScroll.update()
            self.after(1000)
            self.resetSummaryBox()
            return
        """

        self.resetSummaryBox() #removes all previous text
        self.updateSummaryText(foundstring) #updates the summaryscroll box text

    def updateSummaryText(self,text):
        self.summaryScroll.replace('1.0','end',text)

    def resetSummaryBox(self):
        self.summaryScroll.replace('1.0','end',"")

    def resetfindEntry(self):
        self.findENTRY.delete(0,END)


    def resetTextStorages(self):
        # elements
        self.PDFasString = ""
        self.numberofpages = 0  # default
        self.numberofSummaryWords = 10  # default

        # NEW---12/25/18
        self.dictofpages = {}

    def resetTextBoxes(self):
        self.percentageReadLabel.config(text = "")
        self.percentageReadLabel.update()

        self.inputtedPageNumber.delete(0, END)
        self.inputtedNumberofSummaryWords.delete(0, END)
        self.resetSummaryBox()
        self.resetfindEntry()



    #takes in a filelocation and returns the filename as a string
    def getArticleName(self,inputtedname):
        articlename = ""
        for letter in inputtedname:
            if letter == "/":
                articlename = ""
            else:
                articlename = articlename+letter

        return articlename

    #Lets the user pick the PDF file location
    def retrieveFileLocation(self):
        FileString = askopenfilename(title = "Choose PDF file", filetypes = (("pdf files", ".pdf"), ("all files", "*.*")))
        self.FileLocationString = FileString
        #print(self.FileLocationString)
        #print(self.getArticleName(self.FileLocationString))

        #sets label text GUI to the location of the file
        self.selectedFileLabel.config(text = self.FileLocationString)


        self.percentageReadLabel.config(text="")
        self.percentageReadLabel.update()
        self.percentageReadLabel.update_idletasks()



    # -----------------------------------------------------------------

    #Once user picks PDF, they click "Retrieve PDF" Button; program retrieves
    #all page text and adds to self.summaryperpagelist[]
    def retrievePDF(self):

        #NEW----------------12/22/18 (resets the labels and the lists holding the page text)
        self.resetTextStorages()
        self.resetTextBoxes()


        self.summaryALL = ""
        self.summaryperpagelist = []
        self.pagesALLclean = ""
        self.pagesALL = ""
        self.dictionaryofWordsALL = {}
        self.listofwordsALL = []

        #retrieves pdf file location
        pdfFile = open(r""+self.FileLocationString,'rb')

        #turns the filelocation to a readable file
        pdfreader = PyPDF2.PdfFileReader(pdfFile) #turns pdf file location (pdf) into a PyPDF2 object (to use methods such as numPages)
        self.numberofpages = pdfreader.numPages #gets the number of total pages of PDF
        self.getPageLabel.config(text = "Page Number:\n("+str(self.numberofpages)+" pages)") #displays label with # of pages


        blanklist = ["",] #temp list; Raw Page text are added to it
        percentageread = 0 #indicates when computer finished (reached 100%)
        self.percentageReadLabel.config(text = "Calculating..") #changes text once done pulling page text
        self.percentageReadLabel.update_idletasks()
        self.percentageReadLabel.update()



        #goes through each page of PDF and pulls the text; adds each text to blanklist[]
        for i in range(self.numberofpages):

            #deals with updating percentage label (does not work well)
            percentageread = i/self.numberofpages
            percentageread *= 100
            percentageread =int(percentageread)
            self.percentageReadLabel.config(text = str(percentageread)+"%")
            self.percentageReadLabel.update()

            pdfobj = pdfreader.getPage(i) #creates a string of the full page at i


            #NEW---------(places all text into a string)
            self.PDFasString = self.PDFasString+ pdfobj.extractText()


            #OLD------------------
            #blanklist.append(pdfobj.extractText()) #places the fullstring page at index i


            #12/25/18
            temp_page = Page()
            temp_page.page_raw = pdfobj.extractText() #pulls raw text out
            temp_page.PullWords()
            #temp_page.printWords()
            temp_page.SortWords()
            temp_page.pageNumber = i+1
            self.dictofpages[str(i+1)] = temp_page
            #print(self.dictofpages[str(i+1)].page_raw)


        #once finished, changes percentageread to 100 to indicate it finished
        percentageread = 100

        self.createAllSummary()

        self.summaryperpagelist = blanklist #adds Pages to self.summaryperpagelist[]
        self.percentageReadLabel.config(text=str(percentageread) + "% Complete")
        self.percentageReadLabel.update()
        self.percentageReadLabel.update_idletasks()

    # -----------------------------------------------------------------

    #RUN function; every 100ms updates/checks

    def run(self):
        while True:

            try:
                self.after(100)
                self.update_idletasks()
                self.update()
            except:
                ""


            try:
                if((len(self.inputtedNumberofSummaryWords.get())>3 and self.inputtedNumberofSummaryWords!="max") and (self.inputtedNumberofSummaryWords.get().isdigit()==False or self.inputtedNumberofSummaryWords!="max")):
                    self.inputtedNumberofSummaryWords.delete(0,END)
                    self.inputtedNumberofSummaryWords.insert(0,"10")
                    self.numberofSummaryWords = 10
                else:
                    if(self.inputtedNumberofSummaryWords.get()=="max"):
                        self.numberofSummaryWords = len(self.dictionaryofWords)
                        #print(self.dictionaryofWords)
                    else:
                        self.numberofSummaryWords = int(self.inputtedNumberofSummaryWords.get())
            except:
                ""

            try:
                if(int(self.inputtedPageNumber.get())<1 and len(self.summaryperpagelist)>0):
                    self.inputtedPageNumber.delete(0,END)
                    self.inputtedPageNumber.insert(0,"1")
            except:
                ""

            try:
                #if user inputted and kept input
                if(self.findENTRY.get()==self.oldfindentry and self.findENTRY.get()!="" and self.isUserFinding):
                    ""
                elif(len(self.findENTRY.get())==0 and self.isUserFinding):
                    self.resetSummaryBox()
                    self.summaryScroll.update()
                    self.isUserFinding= False
                    self.after(50)
                elif(self.findENTRY.get()!=self.oldfindentry):
                    self.resetSummaryBox()
                    self.isUserFinding = True
                    self.oldfindentry = self.findENTRY.get()
                    self.findWord(self.findENTRY.get())


            except:
                ""

    # -----------------------------------------------------------------

    #MAIN function that summarizes PDF by page or "all"
    def retrievePageSummary(self):
        #attributes (only declared not initialized)
        inputtedString = ""  #what the user typed in inputtedPageNumber Entry
        pagenumber = 0  #currently set to 0; takes inputted string later and turns to page number
        summary = ""

        #Checks if user typed "all" rather than a number (to get all article summary)
        if (self.inputtedPageNumber.get() == "all" and self.summaryALL == ""):
            allPages = "" #string which is going to hold all text pages as ONE string]


            #NEW-----------(does all the above but without a for loop)
            self.pagesALLclean.strip("\n")

            #if the user did not select to have a summary for ALL
            if (self.summaryCheckBoxValue.get() == False):
                #print("entered summarycheck ALL")
                self.summaryScroll.replace('1.0', 'end', "")  # makes the summary text blank
                try:
                    #OLD---------
                    #self.summaryScroll.insert('insert', self.pagesALL)

                    #NEW---------
                    self.summaryScroll.insert('insert', self.PDFasString)
                    return None
                except:
                    self.summaryScroll.insert('insert', "Page Does Not Exist")
                    print("error inserting pagenumber")
                    return None

            elif (self.summaryCheckBoxValue.get()):
                self.allSummary()


#ALL ends------------now checks if the user typed in a number rather than ALL to get a specific page to summarize/read------------------------------------------

        try:
            inputtedString = self.inputtedPageNumber.get() #turns what the user typed into a string

            #checks if the inputtedString is a number(page number) or else states to type in a page number
            if (inputtedString.isdigit() == False and inputtedString !="all"):
                self.resetSummaryBox()
                self.summaryScroll.insert('insert', "Input a Page Number")
                inputtedString = ""
        except:
            print("error in page")

        #turns the inputted string into the page number user wants
        try:
            pagenumber = int(inputtedString)
        except:
            print("ERROR PAGE NUMBER")
            return

        if(pagenumber<1 or pagenumber>self.numberofpages):
            self.summaryScroll.replace('1.0','end', "")
            self.summaryScroll.insert('insert', "Page Does Not Exist.")
            return

        #if its a valid page, selectedpage = userselected page
        selectedpage = self.dictofpages[str(pagenumber)]

        #if the user selects no Summary, gives the full page
        if(self.summaryCheckBoxValue.get()==False):
            self.summaryScroll.replace('1.0','end', "") #makes the summary text blank
            try:
                #OLD-------------------
                #self.summaryScroll.insert('insert', self.summaryperpagelist[pagenumber])

                self.summaryScroll.insert('insert',selectedpage.page_raw)
            except:
                self.summaryScroll.insert('insert',"Page Does Not Exist")
                print("error inserting pagenumber")

        else:
            #NEW-----------12/25/18
            # Places the text in summary box scroll (SHOULD BE DONE LAST)
            self.resetSummaryBox()
            self.summaryScroll.insert('insert', selectedpage.returnSummary(self.numberofSummaryWords))

#--------------------------------------------

    #takes in the string "back" or "next" to represent to increase the current
    # page number by 1 or decreate current page number by 1
    def gotoPage(self, BackorNext):
        self.resetfindEntry()

        if(self.inputtedPageNumber.get()==""):
            return None

        try:

            inputtedString = self.inputtedPageNumber.get() #turns what the user typed into a string

            #checks if the inputtedString is a number(page number) or else states to type in a page number
            if (inputtedString.isdigit() == False):
                self.resetSummaryBox()
                self.summaryScroll.insert('insert', "Input a Page Number")
                inputtedString = ""
        except:
            print("error in page")

        currentpage = int(inputtedString)
        nextpage = currentpage + 1
        backpage = currentpage - 1

        if(BackorNext=="next" and nextpage<=self.numberofpages):
            self.inputtedPageNumber.delete(0, END)
            self.inputtedPageNumber.insert(0, str(nextpage))
            self.retrievePageSummary()
        elif(BackorNext=="back" and backpage>=1):
            self.inputtedPageNumber.delete(0, END)
            self.inputtedPageNumber.insert(0, str(backpage))
            self.retrievePageSummary()
        else:
            return None


    def __init__(self):
        #Fields
        self.FileLocationString = "" #blanktobeginwith
        self.PDFasString = ""
        self.numberofpages = 0 #default
        self.numberofSummaryWords = 10  # default

        #NEW---12/25/18
        self.dictofpages = {} #stores all of the pages of pdf as Page objects within a dictionary

        self.filler_words = ["and", "than", "the", "there", "from", "you",
                             "your", "their", "why", "his", "her", "I", "is", "are", "was", "were", "that",
                             "the", "this", "when", "how", "its", "dont", "which", "but", "also"]

        #Find fields
        self.oldfindentry = ""
        self.isUserFinding = False

        #All fields
        self.fullSummary = [] #list of most occurring words (largest to smallest order)




        # root window
        root = Tk()
        root.title("PDFsummary1.3 - Miguel Zavala")
        root.iconbitmap(r""+iconpath)
        root.resizable(False,False)
        super().__init__(root)
        root.grid()








        #GUI
        self.Title = Label(self, text = "PDFsummary", fg = "red", font = "none 20 bold")
        self.Title.grid(row= 0, column = 2, columnspan = 2, pady= 20)

        self.selectFileLabel = Label(self, text= "Select PDF file:", font = "none 10 bold")
        self.selectFileLabel.grid(row = 1, column = 2)

        self.selectedFileLabel = Label(self, text = "", font = "none 10")
        self.selectedFileLabel.grid(row= 3, column= 2,columnspan=2)

        self.selectFileButton = Button(self, text = "Browse", font = "none 10", bg = "light gray" , width = 15, command = self.retrieveFileLocation)
        self.selectFileButton.grid(row = 2, column = 2)

        self.getPDFButton = Button (self, text = "Retrieve PDF", font = "none 10 bold", bg = "light gray", width = 20, command = self.retrievePDF)
        self.getPDFButton.grid(row = 2, column = 3)


        #find button
        self.findIMAGE = Image.open(findIMAGEpath)
        self.findIMAGE.thumbnail((25,25),Image.ANTIALIAS)
        self.findIMAGE = ImageTk.PhotoImage(self.findIMAGE)
        self.findButton = Button(self, image=self.findIMAGE, bg = "light gray", command = lambda: self.findWord(self.findENTRY.get()))
        self.findButton.grid(row = 0, column = 4, sticky = NE , pady = 5, padx= 5)

        #findentry
        self.findENTRY = Entry(self, width= 10)
        self.findENTRY.grid(row= 0 , column= 3, sticky= NE, pady=5)

        # progessbar
        #self.progress_bar = Progressbar(self, orient = HORIZONTAL, length= 10, mode = "indeterminate")
        #self.progress_bar.grid(row = 1, column = 3, pady= 5)

        self.percentageReadLabel = Label(self, text= "")
        self.percentageReadLabel.grid(row = 1, column =3, pady= 5)

        self.summaryScroll = tkinter.scrolledtext.ScrolledText(self, width = 60, height = 20)

        #SummaryFRAME --------------------------
        self.summaryLabelString = "Page Number:\n("+str(self.numberofpages)+" pages)"
        self.summaryFrame = Frame(self)
        self.summaryFrame.grid(row = 4, column = 2, columnspan = 2)

        self.getPageLabel = Label(self.summaryFrame, text = self.summaryLabelString)
        self.getPageLabel.grid(row= 0, column = 0, pady= 10)

        self.inputtedPageNumber = Entry(self.summaryFrame)
        self.inputtedPageNumber.grid(row=0, column=1, padx=5)

        self.enterNumberofWords = Label(self.summaryFrame,text = "                  Number of Summary Words\n(10 default)")
        self.enterNumberofWords.grid(row = 1, column = 0)

        self.inputtedNumberofSummaryWords = Entry(self.summaryFrame)
        self.inputtedNumberofSummaryWords.grid(row = 1, column = 1)
        self.inputtedNumberofSummaryWords.insert(0,str(self.numberofSummaryWords))

        self.summaryCheckBoxValue = BooleanVar()
        self.summaryCheckBoxValue.set(True)
        self.fullorsummaryCheckButton = Checkbutton(self.summaryFrame, text = "Summary?", variable = self.summaryCheckBoxValue)
        self.fullorsummaryCheckButton.grid(row= 0, column = 2)

        self.readButton = Button(self.summaryFrame, text = "Read", command = self.retrievePageSummary, width = 15, bg = "light gray", font = "none 10 bold")
        self.readButton.grid(row = 0, column = 3, padx = 30)

        self.HoldNextBackButtonsFrame = Frame(self.summaryFrame)
        self.HoldNextBackButtonsFrame.grid(row = 1, column = 3)
        self.NextButton = Button(self.HoldNextBackButtonsFrame, text = ">", font = "none 7 bold", width = 4, bg = "light gray", command = lambda: self.gotoPage("next"))
        self.NextButton.grid(row= 0, column = 1, padx = 5)
        self.BackButton = Button(self.HoldNextBackButtonsFrame, text="<", font="none 7 bold", width = 4,bg = "light gray", command = lambda: self.gotoPage("back"))
        self.BackButton.grid(row=0, column=0, padx = 5)
        #----------------------------------------

        #disables any editing
        #self.summaryScroll.config(state=DISABLED)

        self.summaryScroll.grid(row = 5, column = 2, columnspan = 2, pady = 10)



        self.grid()

        #Displays the root window
        self.run()



MainScreen()




