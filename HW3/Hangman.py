from collections import Counter
import itertools
import sys

file = open('words.txt', 'r')
words = file.read().lower().splitlines()

word = str(input())
encoded_word = len(word) * '_'

selected_words = []
if word not in words:
    print("Sorry.I don't know this word")
else:
    selected_words = [i for i in words if len(i) == len(word)]

letters = itertools.chain.from_iterable(selected_words)
frequency = Counter(letters)
most_likely_letter = max(frequency, key=frequency.get)

counter = 0
for i in range(len(frequency)):

    answer = str(input('Is letter ' + most_likely_letter + ' into your word?(yes/no)'))
    counter = counter + 1
    if answer == 'Yes' or answer == 'yes':
        print('Enter letter position:')
        position = int(input())
        encoded_word = encoded_word[:position - 1] + most_likely_letter + encoded_word[position:]
        selected_words = [i for i in words if len(i) == len(word) and i[position - 1] == most_likely_letter]
        letters = itertools.chain.from_iterable(selected_words)
        frequency = Counter(letters)
        most_likely_letter = max(frequency, key=frequency.get)

    elif answer == 'No' or answer == 'no':
        if most_likely_letter in word and most_likely_letter not in encoded_word:
            print("Don't lie me.")
            continue
        frequency.pop(most_likely_letter)
        most_likely_letter = max(frequency, key=frequency.get)

    while encoded_word == word:
        print('This word is ' + str(encoded_word) + ' .I guess it on ' + str(counter) + ' times')
        sys.exit(0)

