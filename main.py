class wordle():
    def __init__(self):
        file = open("words.txt", "r", encoding = "utf-8")
        self.finaldict = {"no": [], "odd": [], "right": []}
        self.lastguess = "crane"
        self.wordlist = [n.rstrip() for n in file]

    def valuesparse(self,wordweird):
        for i in range(5):
            currentv = wordweird[i]
            currentl = self.lastguess[i]

            doneletters = self.finaldict["no"] + [i[0] for i in self.finaldict["odd"]] + [i[0] for i in self.finaldict["right"]]

            if currentv == "n" and currentl not in doneletters:
                self.finaldict["no"].append(currentl)
            if currentv == "o":
                self.finaldict["odd"].append([currentl,i])
            if currentv == "r":
                self.finaldict["right"].append([currentl,i])

        return (self.finaldict)

    def limiter(self,finaldict):
        f = open("words.txt", "r", encoding="utf-8")
        def nolimit(finaldict,f):
            banned = finaldict["no"]
            addvar = True
            possible = []

            for line in f:
                addvar = True
                for i in banned:
                    if line.find(i) != -1:
                        addvar = False
                        break
                if addvar:
                    possible.append(line)

            return possible

        def oddlimit(finaldict,f):
            letters = finaldict["odd"]
            addvar = True
            possible = []

            for line in f:
                addvar = True
                for i in letters:
                    if line.find(i[0]) in [i[1],-1]:
                        addvar = False
                        break
                if addvar:
                    possible.append(line)

            return possible

        def rightlimit(finaldict,f):
            letters = finaldict["right"]
            addvar = True
            possible = []

            for line in f:
                addvar = True
                for i in letters:
                    if line[i[1]] != i[0]:
                        addvar = False
                        break
                if addvar:
                    possible.append(line)

            return possible

        self.wordlist = oddlimit(finaldict, rightlimit(finaldict, nolimit(finaldict,self.wordlist)))

    def ranker(self):
        strong = 0
        strongest = ""

        def strength(word):
            letterdict = {"a": 2348, "b": 715, "c": 964, "d": 1181, "e": 3009, "f": 561, "g": 679, "h": 814, "i": 1592,
                          "j": 89, "k": 596, "l": 1586, "m": 843, "n": 1285, "o": 1915, "p": 955, "q": 53, "r": 1910,
                          "s": 3033, "t": 1585, "u": 1089, "v": 318, "w": 505, "x": 139, "y": 886, "z": 135}
            value = 0
            for i in word:
                value += letterdict[i]/((word.count(i))**2)
            return value

        for i in self.wordlist:
            if strength(i) >= strong:
                strongest = i
                strong = strength(i)
        self.lastguess = strongest
        return strongest

ask = ""
world = wordle()
print("*instructions* the word it suggests will pop up above the 'result:' prompt. type this into wordle.\n"
      " under the prompt, type in a five letter sequence based on the colors of the word on the game. \n"
      "green = 'r', yellow = 'o', grey = 'n'. based on that, it will give you another suggested word. keep doing this until the game ends.\n")
while ask != "done":
    print(world.lastguess)
    ask = input("result:\n")
    if len(ask) == 5:
        world.valuesparse(ask)
        print(world.finaldict)
        world.limiter(world.finaldict)
        print(world.wordlist)
        print(world.ranker())
    elif ask == "new":
        world = wordle()
