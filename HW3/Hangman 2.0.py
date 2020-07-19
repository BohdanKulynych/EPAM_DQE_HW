import typing
from collections import Counter
import itertools
import re


# This code was written by example of my lecturer in EPAM DQE LAB

def get_words(word_len: int, filename='words.txt') -> typing.List[str]:
    #get words with initial length
    """
    :param filename: name of file wth words
    :param word_len: len of user input word
    :return: list of words wth len = word_len
    """
    with open(filename, 'r') as word_list:
        words = word_list.read().splitlines()
        return [
            word.lower()
            for word in words
            if word_len == len(word)
        ]


def count_letters(selected_words: typing.List[str]) -> typing.Counter:

    # count quantity of every letter
    """
    :param selected_words: result of function get_words
    :return: counter of letters in word list
    """
    # divide our word set on letters
    letters = itertools.chain.from_iterable(selected_words)
    # count this letters
    letters_frequency: Counter = Counter(letters)

    return letters_frequency


def find_most_likely_letter(frequency: Counter) -> typing.Tuple[str, float]:
    '''

    :param frequency: result of count letters function
    :return:
    '''

    # choose only first pair (letter - quantitu)
    letter, letter_count = frequency.most_common(1)[0]

    probability = letter_count / sum(frequency.values()) * 100

    return letter, probability


def manipulate_word_list(words_set: typing.List[str], word: str, guessed_letters: str) -> typing.List[str]:

    # suggest the words which similar to current user input (update word list)
    '''

    :param words_set: list of word with const length
    :param word: input word
    :param guessed_letters: letters which user have guessed
    :return: list of word which correspond to the pattern
    '''


    # write pattern for find words using not guessed letters instead '_'
    guess: str = '.' if len(guessed_letters) == 0 else f"[^{guessed_letters}]"
    word_pattern: typing.Pattern = re.compile(f"{word.replace('_', guess)}")
    # if word match pattern write in into list
    words: typing.List = [word for word in words_set if word_pattern.match(word)]

    return words


def anticheat(initial_length: int, user_input: str, last_user_input: str, user_confirmed_letter: str) -> str:
    # don't allow cheating using some manipulations with word input

    corrected_input: str = user_input
    # check length of word
    length_check: bool = initial_length != len(corrected_input)
    while length_check:
        print(f'Please input the word length {initial_length}')
        corrected_input: str = input()
        # after corrected user's input check again
        length_check = initial_length != len(corrected_input)

    last_user_input = user_input if last_user_input == '_' * initial_length else last_user_input # don't think
    # that 1st input of word (___) it's cheating

    # check current and last user's inputs
    letters_order_check: bool = all(
        last_user_input[i] != corrected_input[i] for i, item in enumerate(last_user_input) if item != '_')

    while letters_order_check:
        print(f'Stop.Last input was {last_user_input} .Please change your input')
        corrected_input: str = input()
        #check again
        letters_order_check: bool = all(
            last_user_input[i] != corrected_input[i] for i, item in enumerate(last_user_input) if item != '_')


    # check if user input the letter has chosen by him
    letter_check: bool = all(
        [corrected_input[i] != user_confirmed_letter for i, item in enumerate(user_input)])

    while letter_check:
        print(f'Stop.The last letter was {user_confirmed_letter} .Please change your input')
        corrected_input: str = input()
        # again
        letter_check: bool = all(
            [corrected_input[i] != user_confirmed_letter for i, item in enumerate(corrected_input)])


    '''
    
    TOTAL CHECK 
    
    check if user don't manipulate with input of the comfirmed letter after the last check
    
    example the last input was a__c_ and missed letter s
    
    input s____ and get the new search by this pattern (in lecluter version)
    
    here the program return error and will offer the input of correct variant
    
    '''

    total_check: bool = all(
        [corrected_input[i] != user_confirmed_letter for i, item in enumerate(user_input)]) or all(
            last_user_input[i] != corrected_input[i] for i, item in enumerate(last_user_input) if item != '_')

    while total_check:
        print(f'Stop.Last input was {last_user_input} with letter {user_confirmed_letter} .Please change your input')
        corrected_input: str = input()
        total_check: bool = all(
        [corrected_input[i] != user_confirmed_letter for i, item in enumerate(user_input)]) or all(
            last_user_input[i] != corrected_input[i] for i, item in enumerate(last_user_input) if item != '_')

    return corrected_input


def play_hangman():

    # initialise all variables for word of game

    guessed_letters: str = ''

    guessed_word: str = input('Dear user.Input the word which has guessed in format _ (one underscore - one letter) \n')

    guessed_word_length: int = len(guessed_word) # need it for anticheat

    words = get_words(guessed_word_length) # get the 1st list of words with guessed_word_length

    game_continue: bool = True # if word will guess of not guessed game is over

    user_ask: bool = True

    while game_continue:

        words = manipulate_word_list(words, guessed_word, guessed_letters)

        print(f"Choose from {len(words)} words...")

        if len(words) <= 10:
            [print(word) for word in words]

        if len(words) == 0:
            print("I don't know this word")
            break

        if len(words) == 1:
            print(f"This word is {words[0]}")
            break

        letter_counter = count_letters(words)
        # offer the next letter in user_ask == no
        letter_counter = Counter({key: value for key, value in letter_counter.items() if key not in guessed_letters})

        likely_letter = find_most_likely_letter(letter_counter)

        print(f"I think that letter {likely_letter[0]} is into your word with probability "
              f"{likely_letter[1]:.2f}%")

        user_ask = input("Isn't it? (y/n) ").lower() == 'y'

        if user_ask:
            last_input: str = guessed_word
            guessed_word = input(f"Change _ in your word on the letter {likely_letter[0]}\n")
            guessed_word = anticheat(guessed_word_length, guessed_word, last_input, likely_letter[0])
            guessed_letters += likely_letter[0]

        guessed_letters += likely_letter[0]


play_hangman()
