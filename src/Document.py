

class Document(object):
    def __init__(self, id, title="", date="", author="", keys="", text="", link=""):
        self.document = dict()
        self.document["I"] = id #I
        self.document["T"] = title #T
        self.document["B"] = date   #B
        self.document["A"] = author #A
        self.document["K"] = keys #K
        self.document["W"] = text #W
        self.document["X"] = link #X

    def textXtoList(self):
        self.document["X"]=[int(line.split()[0]) for line in self.document["X"].split("\n") if line]

    #Renvoie le document avec sa representation complete
    def getDocument(self):
        return self.document

    # set value for key
    def setValue(self, key, value):
        self.document[key] = value

    # get value for key
    def getValue(self, key):
        return self.document[key]

    #getter sur Id->I
    def getId(self):
        return self.document.get('I')

    #getter sur titre ->T
    def getTitle(self):
        return self.document.get('T')

    #getter sur date->B
    def getDate(self):
        return self.document.get('B')

    #getter sur author->A
    def getAuthor(self):
        return self.document.get('A')

    #getter sur Keys->K
    def getKeys(self):
        return self.document.get('K')

    #getter sur text->W
    def getText(self):
        return self.document.get('W')

    #getter sur link->X
    def getLink(self):
        return self.document.get('X')

    #setter sur Id
    def setId(self, id):
        self.document["I"] = id

    #setter sur title
    def setTitle(self, title):
        self.document["T"] = title

    #setter sur date
    def setDate(self, date):
        self.document["B"] = date

    #setter sur author
    def setAuthor(self, author):
        self.document["A"] = author

    #setter sur keys
    def setKeys(self, keys):
        self.document["K"] = keys

    #setter sur text
    def setText(self, text):
        self.document["W"] = text

    #setter sur link
    def setLink(self, link):
        self.document["X"] = link

    def __str__(self):
        toString=""
        for key, value in self.document.items():
            if key == "I":
                toString += ".I " + str(value)+"\n"
            else :
                toString += "." + key + "\n" + value
        return toString


