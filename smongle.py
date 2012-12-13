#!/usr/bin/env python3
# A program to select a random assortment of students from a list.
# The trick is, if a student shows up in the list and is not called,
# they should go back in the list at the top next time...
# Okay, so the trick is we treat it like a stack of cards with two
# 'decks', each card bearing a student name.
# The 'unpicked' deck is initially shuffled, the 'picked' deck is
# empty.  
# You draw X students from the unpicked deck; those are teh ones
# who have to do the whiteboard exercise.  They go into your hand.
# If you try to draw a card and the unpicked deck is empty, you
# shuffle the picked deck and it becomes the unpicked one.
# If a student is absent, their card gets taken out of your hand
# and set aside.
# Once all that is done and you have your final student list,
# the cards in your hand go into the picked deck, the cards
# set aside get noted and put atop the unpicked deck, so they
# will get called again next time.

import random

class StudentList(object):
    def __init__(self):
        self.unpicked = loadStudentList('unpicked.list')
        self.picked = loadStudentList('picked.list')
        self.hand = []
        self.setAside = []
        self.absences = loadStudentList('absences.list')

    def drawStudent(self):
        if len(self.unpicked) == 0:
            self.reshufflePicked()
        self.hand.append(self.unpicked.pop())

    def reshufflePicked(self):
        self.unpicked = self.picked
        random.shuffle(self.picked)
        self.picked = []

    def revokeStudent(self, num):
        name = self.hand[num]
        self.hand.remove(name)
        self.setAside.append(name)
        self.absences.append(name)

    def saveStudents(self):
        self.picked = self.picked + self.hand
        self.unpicked = self.unpicked + self.setAside
        saveStudentList('unpicked.list', self.unpicked)
        saveStudentList('picked.list', self.picked)
        saveStudentList('absences.list', self.absences)

    def printHand(self):
        for i in range(len(self.hand)):
            person = self.hand[i]
            print("{0}: {1}".format(i, person))
            


def loadStudentList(filename):
    f = open(filename, 'r')
    lines = [l.strip() for l in f.readlines()]
    return lines

def saveStudentList(filename, lst):
    f = open(filename, 'w')
    f.writelines([str(l) + '\n' for l in lst])
    f.close()

def main():
    a = StudentList()
    try:
        count = int(input('Number of students to draw: '))
        for i in range(count): a.drawStudent()
        a.printHand()

        # Actually a perfect place for a do-while loop.  :-P
        resp = input('Enter number of any absent students, or enter for none: ')
        while resp != '':
            idx = int(resp)
            a.revokeStudent(idx)
            a.drawStudent()
            a.printHand()
            resp = input('Enter number of any absent students, or enter for none: ')
    finally:
        a.saveStudents()


if __name__ == '__main__':
    main()
