#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import random

repetitions = 3
quizSize = 10
wordList = []

encouragements = [ 
    "✌️  Victory is yours!",
    "✋  High five!",
    "💪  Going strong!",
    "👌  That's a-OK!",
    "👊  Fist bump!",
    "👏  Applause!",
    "🤘  Rock on!",
    "😎  Cool!" ]


def CSI(item):
    return '\033[' + item


def setCol(col):
    return CSI(str(col) + 'G')

def setRowCol(row, col):
    return CSI(str(row) + ';' + str(col) + 'H')


def readWordList(filename):
    wordList.extend(map(lambda line: tuple(line.split()),
                        open(filename, "r").readlines()))


def makeQuiz(wordList, count):
    uniqueWords = set(wordList)
    if len(uniqueWords) <= count:
        return list(uniqueWords)

    # Start with a weighted sample
    quiz = list(set(random.sample(wordList, count)))

    # Due to duplicates from the weighted list, we may have fewer words than
    # needed, so add more words from the unused words in the  unique list.
    quiz.extend(random.sample(list(uniqueWords.difference(set(quiz))),
                              count - len(quiz)))

    return quiz


def askOne(pair):
    print('');
    answer = raw_input(setCol(17) + pair[0] + setCol(41) + '? ')
    correct = answer == pair[1];
    if correct:
        print(CSI('F') + setCol(41) + '  ' + answer)
    else:
        print(CSI('F') + setCol(41) +
              CSI('31m') + '✗ ' + CSI('m') + answer 
                         + ' \t' + CSI('4m') + CSI('31m') + pair[1]) + CSI('m')
    return (pair, correct)


def takeQuiz(quiz):
    print(setRowCol(3, 20) + '     q⃣   u⃣   i⃣   z⃣     ')
    print('')
    result = [];
    for item in quiz:
        result.append(askOne(item))

    return result

def showStats(wordList, wordsToLearn):
    pctLearned = 100 - len(wordsToLearn) * 100 / (repetitions * len(wordList))
    print(setRowCol(2, 60) + '  Words: {:3d}'.format(len(wordList)))
    print(setRowCol(3, 60) + 'Learned: {:3.0f}%'.format(pctLearned))

def learnWords(wordList, wordsToLearn):
    while len(wordsToLearn):
        quiz = makeQuiz(wordsToLearn, quizSize)
        print(CSI('2J'))
        showStats(wordList, wordsToLearn)
        result=takeQuiz(quiz)
        perfect = all(item[1] for item in result)

        for item in result:
            if item[1]:
                wordsToLearn.remove(item[0])
            else:
                while item[0] in wordsToLearn:
                    wordsToLearn.remove(item[0])
                wordsToLearn.extend(repetitions * [item[0]])

        showStats(wordList, wordsToLearn)

        if not len(wordsToLearn):
            print(setRowCol(10 + quizSize * 2, 17) + '💯  Perfect!\n\n')
            break

        msg = (random.sample(encouragements, 1)[0] + " Enter to continue." 
               if perfect else 'Enter to continue or Ctrl-C to stop.')

        raw_input(setRowCol(10 + quizSize * 2, 17) + msg)


for file in (sys.argv[1:] if len(sys.argv) > 1 else ["wordList.txt"]):
    wordList = []
    readWordList(file)

wordList = list(set(wordList))
wordsToLearn = repetitions * wordList

try:
    learnWords(wordList, wordsToLearn)
except (KeyboardInterrupt, SystemExit):
    print(setRowCol(10 + quizSize * 2, 17) + '👋  Bye!' + CSI('K') + '\n')
