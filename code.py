from collections import Counter
import re


def open_file(filename):
    # function for work with file
    try:
        # open file,default mode is read
        file = open(filename, 'r')
        #  read file line by line and convert all text to lowercase
        text = file.read().lower()
        #   delete '\n' characters
        formatted = "".join(text.splitlines())
        file.close()
        return formatted
    except IOError:
        print("Error: File does not appear to exist.")


def text_processing(text):
    # function for separate words from text file
    regex = r'[\w]+[^\s]+'
    result = re.findall(regex, text)
    return result


def output(processed_text):
    # function for count quantity of words

    # initialize counter
    cnt = Counter()
    # add words and their quantities to counter
    for word in processed_text:
        cnt[word] += 1
    # convert counter object to dictionary
    word_dict = dict(cnt)
    # sort dictionary in alphabetical order
    sorted_dict = dict(sorted(word_dict.items(), key=lambda x: x[0].lower()))
    return sorted_dict
