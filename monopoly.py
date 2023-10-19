#! /usr/bin/python3

import random
import time

isDouble = lambda x: x[0] == x[1]
genRoll = lambda : (random.randint(1, 7), random.randint(1, 7))


class Square:
    def __init__(self, name):
        self.name = name
        self.landedOn = {}
        self.rentsCharged = {}
        self.isStation = False
        self.isUtility = False

    def land(self, player, roll, mult = 1):
        try:
            self.landedOn[player] += 1
            self.rentsCharged[player] += mult
        except KeyError:
            self.landedOn[player] = 1
            self.rentsCharged[player] = mult

    def __repr__(self):
        return "\n".join([
                self.name + ":",
                "\t- Station?: " + str(self.isStation),
                "\t- Utility?: " + str(self.isUtility),
                "\t- Times Landed On: " + str(self.landedOn),
                "\t- Rents Charged: " + str(self.rentsCharged)
                ])

class Chance(Square):
    def land(self, player, roll, mult = 1):
        super().land(player, roll, mult)
        
        num = random.randint(0, 16)
        if num == 0:
            player.give(150)
        elif num == 1:
            player.give(50)
        elif num == 2:
            player.charge(15)
        elif num == 3:
            player.chargePerHouse(25)
            player.chargePerHotel(100)
        elif num == 4:
            player.chargePerOpponent(50)
        elif num == 5:
            player.moveTo(lambda x: x == kingsCross, roll)
        elif num == 6:
            player.moveTo(lambda x: x == go, roll)
        elif num == 7:
            player.moveTo(lambda x: x == trafalgar, roll)
        elif num in [8, 9]:
            player.moveTo(lambda x: x.isStation, roll, mult = 2)
        elif num == 10:
            player.jailCount = 0
            player.square = jail
        elif num == 11:
            player.moveTo(lambda x: x == mayfair, roll)
        elif num == 12:
            player.moveTo(lambda x: x.isUtility, genRoll(), mult = 10)
        elif num == 13:
            player.moveTo(lambda x: x == pallMall, roll)
        elif num == 14:
            player.moveBack(3, roll)
        elif num == 15:
            player.getOutFreeCount += 1

class Chest(Square):
    def land(self, player, roll, mult = 1):
        super().land(player, roll, mult)
        
        num = random.randint(0, 16)
        if num == 0:
            player.givePerOpponent(10)
        elif num == 1:
            player.give(50)
        elif num == 2:
            player.give(25)
        elif num in [3, 4, 5]:
            player.give(100)
        elif num == 6:
            player.give(10)
        elif num == 7:
            player.give(20)
        elif num == 8:
            player.give(200)
        elif num in [9, 10]:
            player.charge(50)
        elif num == 11:
            player.charge(100)
        elif num == 12:
            player.chargePerHouse(40)
            player.chargePerHotel(115)
        elif num == 13:
            player.moveTo(lambda x: x == go, roll)
        elif num == 14:
            player.jailCount = 0
            player.square = jail
        elif num == 15:
            player.getOutFreeCount += 1

class Station(Square):
    def __init__(self, name):
        super().__init__(name)
        self.isStation = True

class Utility(Square):
    def __init__(self, name):
        super().__init__(name)
        self.isUtility = True
        self.income = 0
        self.incomePerMult = {}

    def land(self, player, roll, mult = 1):
        super().land(player, roll, mult)
        self.income += mult * (roll[0] + roll[1])
        try:
            self.incomePerMult[mult] += roll[0] + roll[1]
        except KeyError:
            self.incomePerMult[mult] = roll[0] + roll[1]

    def __repr__(self):
        return "\n".join([
                super().__repr__(),
                "\t- Income Gained: " + str(self.income),
                "\t- Income Per Multiplier: " + str(self.incomePerMult)
                ])

class GoToJail(Square):
    def land(self, player, roll, mult = 1):
        super().land(player, roll, mult)
        player.jailCount = 0
        player.square = jail


go              = Square("Go")
oldKent         = Square("Old Kent Road")
chest1          = Chest("Community Chest")
whitechapel     = Square("Whitechapel")
incomeTax       = Square("Income Tax")
kingsCross      = Station("King's Cross Station")
angel           = Square("The Angel, Islington")
chance1         = Chance("Chance")
euston          = Square("Euston")
pentonville     = Square("Pentonville Road")
justVisiting    = Square("Just Visiting")
pallMall        = Square("Pall Mall")
electric        = Utility("Electric Company")
whitehall       = Square("Whitehall")
northumberland  = Square("Northumberland Avenue")
marylebone      = Station("Marylebone Station")
bowStreet       = Square("Bow Street")
chest2          = Chest("Community Chest")
marlborough     = Square("Marlborough Street")
vineStreet      = Square("Vine Street")
freeParking     = Square("Free Parking")
strand          = Square("Strand")
chance2         = Chance("Chance")
fleetStreet     = Square("Fleet Street")
trafalgar       = Square("Trafalgar Square")
fenchurch       = Station("Fenchurch Street Station")
leicester       = Square("Leceister Square")
coventry        = Square("Coventry Street")
waterWorks      = Utility("Water Works")
piccadilly      = Square("Piccadilly")
goToJail        = GoToJail("Go To Jail")
regent          = Square("Regent Street")
oxford          = Square("Oxford Street")
chest3          = Chest("Community Chest")
bond            = Square("Bond Street")
liverpool       = Station("Liverpool Street Station")
chance3         = Chance("Chance")
parkLane        = Square("Park Lane")
superTax        = Square("Super Tax")
mayfair         = Square("Mayfair")

jail            = Square("Jail")

boardSquares = [
        go, oldKent, chest1, whitechapel, incomeTax, kingsCross,
        angel, chance1, euston, pentonville, justVisiting, pallMall,
        electric, whitehall, northumberland, marylebone, bowStreet,
        chest2, marlborough, vineStreet, freeParking, strand, chance2,
        fleetStreet, trafalgar, fenchurch, leicester, coventry,
        waterWorks, piccadilly, goToJail, regent, oxford, chest3,
        bond, liverpool, chance3, parkLane, superTax, mayfair
        ]
board = {}
for i in range(len(boardSquares) - 1):
    board[boardSquares[i]] = boardSquares[i + 1]
board[boardSquares[-1]] = boardSquares[0]
revBoardSquares = list(boardSquares)
revBoardSquares.reverse()
revBoard = {}
for i in range(len(revBoardSquares) - 1):
    revBoard[revBoardSquares[i]] = revBoardSquares[i + 1]
revBoard[revBoardSquares[-1]] = revBoardSquares[0]


class Player:
    def __init__(self, name, square = go):
        self.name = name
        self.square = square
        self.jailCount = 0
        self.getOutFreeCount = 0

        self.laps = 0

        self.income = 0
        self.incomePerOpponent = 0
        self.incomePerHouse = 0
        self.incomePerHotel = 0

        self.expenses = 0
        self.expensesPerOpponent = 0
        self.expensesPerHouse = 0
        self.expensesPerHotel = 0

    def inJail(self):
        return self.square == jail

    def roll(self, roll = None, canDouble = True):
        if roll == None:
            roll = genRoll()

        if self.inJail():
            self.escapeJail(roll)
            return

        for doubles in range(2):
            self.move(roll[0] + roll[1], roll)

            if (not isDouble(roll)) or (not canDouble) or self.inJail():
                return
            roll = genRoll()

        if isDouble(roll):
            self.square = jail
            return

        self.move(roll[0] + roll[1], roll)

    def escapeJail(self, roll):
        self.jailCount += 1

        if isDouble(roll):
            self.jailCount = 0
            self.square = justVisiting
            self.roll(roll, canDouble = False)
            return
        elif self.jailCount == 2 and self.getOutFreeCount > 0:
            self.getOutFreeCount -= 1
            self.jailCount = 0
            self.square = justVisiting
            self.roll()
            return
        elif self.jailCount == 3:
            self.charge(50)
            self.jailCount = 0
            self.square = justVisiting
            self.roll(roll)
            return

    def step(self):
        self.square = board[self.square]
        if self.square == go:
            self.laps += 1

    def move(self, num, roll, mult = 1):
        for i in range(num):
            self.step()
        self.square.land(self, roll, mult)

    def moveTo(self, destCond, roll, mult = 1):
        while (not destCond(self.square)):
            self.step()
        self.square.land(self, roll, mult)

    def moveBack(self, num, roll, mult = 1):
        for i in range(num):
            self.square = revBoard[self.square]
        self.square.land(self, roll, mult)

    def give(self, cost):
        self.income += cost

    def givePerOpponent(self, cost):
        self.incomePerOpponent += cost

    def givePerHouse(self, cost):
        self.incomePerHouse += cost

    def givePerHotel(self, cost):
        self.incomePerHotel += cost

    def charge(self, cost):
        self.expenses += cost

    def chargePerOpponent(self, cost):
        self.expensesPerOpponent += cost

    def chargePerHouse(self, cost):
        self.expensesPerHouse += cost

    def chargePerHotel(self, cost):
        self.expensesPerHotel += cost

if __name__ == "__main__" and False:
    p1 = Player("Aaron", piccadilly)
    p1.roll((3, 4))
    print(p1.square.name)
    print("\n\n\n")
    print("Laps: " + str(p1.laps))
    print("Income:")
    print("\t- General: " + str(p1.income))
    print("\t- Per Opponent: " + str(p1.incomePerOpponent))
    print("\t- Per House: " + str(p1.incomePerHouse))
    print("\t- Per Hotel: " + str(p1.incomePerHotel))
    print("Expenses:")
    print("\t- General: " + str(p1.expenses))
    print("\t- Per Opponent: " + str(p1.expensesPerOpponent))
    print("\t- Per House: " + str(p1.expensesPerHouse))
    print("\t- Per Hotel: " + str(p1.expensesPerHotel))
    print("\n\n\n")
    
    for square in boardSquares:
        print()
        print(square.name)
        print(square.landedOn)

if __name__ == "__main__" and True:
    print(time.time())
    p1 = Player("Aaron")
    limit = 10 ** 9
    currentPower = 0
    interval = int(limit // 20)
    for i in range(limit):
        if i == (10 ** currentPower):
            print(str(i) + (" " * (20 - len(str(i)))) + str(time.time()))
            currentPower += 1
        elif i % interval == 0:
            print(str(i) + (" " * (20 - len(str(i)))) + str(time.time()))
        #print(p1.square.name)
        p1.roll()
    
    print(p1.square.name)
    print("\n\n\n")
    print(p1.laps)
    print("\n\n\n")

    print(p1.income)
    print(p1.incomePerOpponent)
    print(p1.incomePerHouse)
    print(p1.incomePerHotel)
    print(p1.expenses)
    print(p1.expensesPerOpponent)
    print(p1.expensesPerHouse)
    print(p1.expensesPerHotel)
    print("\n\n\n")
    
    for square in boardSquares:
        print()
        print(square)
