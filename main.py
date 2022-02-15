class wordle():
    def __init__(self):
        file = open("words.txt", "r", encoding = "utf-8")
        self.finaldict = {"no": [], "odd": [], "right": []}
        self.lastguess = "crane"
        self.wordlist = [n.rstrip() for n in file]
        self.movesleft = 6

    def valuesparse(self,wordweird):
        for i in range(5):
            currentv = wordweird[i]
            currentl = self.lastguess[i]

            doneletters = self.finaldict["no"] + [i[0] for i in self.finaldict["odd"]] + [i[0] for i in self.finaldict["right"]]

            if currentv == "n" and currentl not in doneletters:
                self.finaldict["no"].append(currentl)
            if currentv == "o":
                self.finaldict["odd"].append([currentl,i])
                if currentl in self.finaldict["no"]:
                    self.finaldict["no"].remove(currentl)
            if currentv == "r":
                self.finaldict["right"].append([currentl,i])
                if currentl in self.finaldict["no"]:
                    self.finaldict["no"].remove(currentl)

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
        sum = 0

        def strength(word):
            letterdict = {"a": 2348, "b": 715, "c": 964, "d": 1181, "e": 3009, "f": 561, "g": 679, "h": 814, "i": 1592,
                          "j": 89, "k": 596, "l": 1586, "m": 843, "n": 1285, "o": 1915, "p": 955, "q": 53, "r": 1910,
                          "s": 3033, "t": 1585, "u": 1089, "v": 318, "w": 505, "x": 139, "y": 886, "z": 135}
            value = 0
            for i in word:
                value += letterdict[i]/((word.count(i))**2)
            return value

        alphabet = "abcdefghijklmnopqrstuvwxyz"
        letterstrength = {"a": 0, "b": 0, "c": 0, "d": 0, "e": 0, "f": 0, "g": 0, "h": 0, "i": 0,
                          "j": 0, "k": 0, "l": 0, "m": 0, "n": 0, "o": 0, "p": 0, "q": 0, "r": 0,
                          "s": 0, "t": 0, "u": 0, "v": 0, "w": 0, "x": 0, "y": 0, "z": 0}
        for i in alphabet:
            for j in self.wordlist:
                if j.find(i) != -1:
                    letterstrength[i] += 1

        def weirdstrength(word, letterstrength, goodletters):
            weirdstrength = 0
            letters = ""
            for i in goodletters:
                if goodletters.count(i) < len(self.wordlist):
                    letters += i
            for i in word:
                if i in letters:
                    weirdstrength += letterstrength[i]/word.count(i)
            #print(word)
            return weirdstrength

        for i in self.wordlist:
            sum += strength(i)
            if strength(i) >= strong:
                strongest = i
                strong = strength(i)

        print((strong - sum / len(self.wordlist)))
        if (strong - sum / len(self.wordlist))/len(self.wordlist) < 200 and 2<len(self.wordlist)<5 and self.movesleft > 1:
            goodletters = ""
            for i in self.wordlist:
                goodletters += i
            strong = 0
            f = open("words.txt", "r", encoding="utf-8")
            for i in [line.rstrip() for line in f]:
                if weirdstrength(i, letterstrength, goodletters) >= strong:
                    strongest = i
                    strong = weirdstrength(i, letterstrength, goodletters)
        self.lastguess = strongest
        return strongest

ask = ""
world = wordle()
print("*instructions* the word it suggests will pop up above the 'result:' prompt. type this into wordle.\n"
      " under the prompt, type in a five letter sequence based on the colors of the word on the game. \n"
      "green = 'r', yellow = 'o', grey = 'n'. based on that, it will give you another suggested word. keep doing this until the game ends.\n")
while ask != "done":
    print(world.lastguess)
    if world.lastguess in world.wordlist:
        world.wordlist.remove(world.lastguess)
    world.movesleft -= 1
    ask = input("result:\n")
    if len(ask) == 5:
        world.valuesparse(ask)
        print(world.finaldict)
        world.limiter(world.finaldict)
        print(world.wordlist)
        print(world.ranker())
    elif ask == "new":
        world = wordle()