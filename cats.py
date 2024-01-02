"""Typing test implementation"""

from utils import lower, split, remove_punctuation, lines_from_file
from ucb import main, interact, trace
from datetime import datetime


###########
# Phase 1 #
###########


def pick(paragraphs, select, k):
    """Return the Kth paragraph from PARAGRAPHS for which SELECT called on the
    paragraph returns True. If there are fewer than K such paragraphs, return
    the empty string.

    Arguments:
        paragraphs: a list of strings
        select: a function that returns True for paragraphs that can be selected
        k: an integer

    >>> ps = ['hi', 'how are you', 'fine']
    >>> s = lambda p: len(p) <= 4
    >>> pick(ps, s, 0)
    'hi'
    >>> pick(ps, s, 1)
    'fine'
    >>> pick(ps, s, 2)
    ''
    """
    # BEGIN PROBLEM 1
    all_true = []
    for _ in paragraphs:
        if select(_):
            all_true += [_]
    return '' if k > len(all_true) - 1 else all_true[k] #remember that len is one more than the possible indexes... will go out of bounds
    # END PROBLEM 1


def about(subject):
    """Return a select function that returns whether
    a paragraph contains one of the words in SUBJECT.

    Arguments:
        subject: a list of words related to a subject

    >>> about_dogs = about(['dog', 'dogs', 'pup', 'puppy'])
    >>> pick(['Cute Dog!', 'That is a cat.', 'Nice pup!'], about_dogs, 0)
    'Cute Dog!'
    >>> pick(['Cute Dog!', 'That is a cat.', 'Nice pup.'], about_dogs, 1)
    'Nice pup.'
    """
    assert all([lower(x) == x for x in subject]), 'subjects should be lowercase.'
    # BEGIN PROBLEM 2
    answ = False
    def pg_check(paragraph):
        for j in subject:
            answ = j in split(remove_punctuation(lower(paragraph)))
            if answ == True:
                return True
        return False
    return pg_check
    # END PROBLEM 2


def accuracy(typed, source):
    """Return the accuracy (percentage of words typed correctly) of TYPED
    when compared to the prefix of SOURCE that was typed.

    Arguments:
        typed: a string that may contain typos
        source: a string without errors

    >>> accuracy('Cute Dog!', 'Cute Dog.')
    50.0
    >>> accuracy('A Cute Dog!', 'Cute Dog.')
    0.0
    >>> accuracy('cute Dog.', 'Cute Dog.')
    50.0
    >>> accuracy('Cute Dog. I say!', 'Cute Dog.')
    50.0
    >>> accuracy('Cute', 'Cute Dog.')
    100.0
    >>> accuracy('', 'Cute Dog.')
    0.0
    >>> accuracy('', '')
    100.0
    """
    # if source is longer than typed, extra words in sourced = not counted in total
    # if typed is longer than source, extra words in typed = counted in total

    typed_words = split(typed)
    source_words = split(source)
    # BEGIN PROBLEM 3

    #special cases
    if len(typed_words) == 0 and len(source_words) == 0:
        return 100.0
    if len(typed_words) == 0 or len(source_words) == 0:
        return 0.0
    
    # as if both are the same length
    total = min(len(typed_words), len(source_words))
    difference = len(typed_words) - len(source_words)
    
    # to find count 
    count = 0
    for i in range(0, total):
        if typed_words[i] == source_words[i]:
            count += 1
            # note: need to check both at each indexes

    # adjusting for diff length
    if difference > 0: # typed is longer than source
        total = len(typed_words)

    return count / total * 100 
    # END PROBLEM 3


def wpm(typed, elapsed):
    """Return the words-per-minute (WPM) of the TYPED string.

    Arguments:
        typed: an entered string
        elapsed: an amount of time in seconds

    >>> wpm('hello friend hello buddy hello', 15)
    24.0
    >>> wpm('0123456789',60)
    2.0
    """
    assert elapsed > 0, 'Elapsed time must be positive'
    # BEGIN PROBLEM 4
    if typed == "": 
        return 0.0
    return (len(typed) / 5) * (60 / elapsed) # don't need / 60 bc its already asking per-minute
    # END PROBLEM 4


############
# Phase 2A #
############


def autocorrect(typed_word, word_list, diff_function, limit):
    """Returns the element of WORD_LIST that has the smallest difference
    from TYPED_WORD. If multiple words are tied for the smallest difference,
    return the one that appears closest to the front of WORD_LIST. If the
    difference is greater than LIMIT, instead return TYPED_WORD.

    Arguments:
        typed_word: a string representing a word that may contain typos
        word_list: a list of strings representing source words
        diff_function: a function quantifying the difference between two words
        limit: a number

    >>> ten_diff = lambda w1, w2, limit: 10 # Always returns 10
    >>> autocorrect("hwllo", ["butter", "hello", "potato"], ten_diff, 20)
    'butter'
    >>> first_diff = lambda w1, w2, limit: (1 if w1[0] != w2[0] else 0) # Checks for matching first char
    >>> autocorrect("tosting", ["testing", "asking", "fasting"], first_diff, 10)
    'testing'
    """
    # BEGIN PROBLEM 5
    if typed_word in word_list:
        return typed_word
    # if it gets here, exact word was not found in word_list, so need to find the closest word:
    closest_word = word_list[0] #initialize
    min_difference = diff_function(typed_word, word_list[0], limit)
    # need to define outside of func, or else resets every time
    for word in word_list:
        test = diff_function(typed_word, word, limit)
        # if len(word_list) == 1:
        #     return word
        if test < min_difference and test <= limit: # only updates if its less than... not if its the same
            min_difference = test
            closest_word = word
    if min_difference > limit: #needed to move this out ... 
        return typed_word
    return closest_word
    # END PROBLEM 5

    #ehh:
    # BEGIN PROBLEM 5
    if typed_word in word_list:
        return typed_word
    # if it gets here, exact word was not found in word_list, so need to find the closest word:
    closest_word = typed_word
    min_difference = limit
    loop = True
    # need to define outside of func, or else resets every time
    for word in word_list:
        test = diff_function(typed_word, word, limit)
        # if test > limit:
        #     return typed_word # returns typed_word bc lowest_difference is too big (> limit)
        # if test == 0:
        #     return word
        # if len(word_list) == 1:
        #     return word
        if test <= limit and (test < min_difference or loop): # only updates if its less than... not if its the same
            loop = False
            min_difference = test
            closest_word = word
    return closest_word
    # END PROBLEM 5


    # case thats failing: the exact same length, replace it with word
    


def feline_fixes(typed, source, limit):
    """A diff function for autocorrect that determines how many letters
    in TYPED need to be substituted to create SOURCE, then adds the difference in
    their lengths and returns the result.

    Arguments:
        typed: a starting word
        source: a string representing a desired goal word
        limit: a number representing an upper bound on the number of chars that must change

    >>> big_limit = 10
    >>> feline_fixes("nice", "rice", big_limit)    # Substitute: n -> r
    1
    >>> feline_fixes("range", "rungs", big_limit)  # Substitute: a -> u, e -> s
    2
    >>> feline_fixes("pill", "pillage", big_limit) # Don't substitute anything, length difference of 3.
    3
    >>> feline_fixes("roses", "arose", big_limit)  # Substitute: r -> a, o -> r, s -> o, e -> s, s -> e
    5
    >>> feline_fixes("rose", "hello", big_limit)   # Substitute: r->h, o->e, s->l, e->l, length difference of 1.
    5
    """
    # BEGIN PROBLEM 6
    if len(typed) == 0 or len(source) == 0:
        return max(len(typed), len(source))
    if typed[0] != source[0]: 
        if limit == 0:
            return 1
        return 1 + feline_fixes(typed[1:], source[1:], limit - 1)
    else:
        return feline_fixes(typed[1:], source[1:], limit) #only checking limit against INCORRECT characters
    # END PROBLEM 6


############
# Phase 2B #
############


def minimum_mewtations(typed, source, limit):
    """A diff function that computes the edit distance from TYPED to SOURCE.
    This function takes in a string TYPED, a string SOURCE, and a number LIMIT.
    Arguments:
        typed: a starting word
        source: a string representing a desired goal word
        limit: a number representing an upper bound on the number of edits
    >>> big_limit = 10
    >>> minimum_mewtations("cats", "scat", big_limit)       # cats -> scats -> scat
    2
    >>> minimum_mewtations("purng", "purring", big_limit)   # purng -> purrng -> purring
    2
    >>> minimum_mewtations("ckiteus", "kittens", big_limit) # ckiteus -> kiteus -> kitteus -> kittens
    3
    #added this 
    >>> minimum_mewtations("", "hello", 1)
    5
    """
    if len(typed) == 0 or len(source) == 0: # Base cases should go here, you may add more base cases as needed.
        # BEGIN
        return max(len(typed), len(source))
        # END

    # problem w/ like cache i think.... 
    # would return the max and that would be 
    # okay bc limit is just to to limit the number 
    # of recursie calls, in this case, would be min


    # Recursive cases should go below here
    if typed[0] == source[0]: # Feel free to remove or add additional cases
        return minimum_mewtations(source[1:], typed[1:], limit)
        # END
    else:
        if limit == 0:
            return 1 #adds 1 to the number of corrects which has become = to the limit (bc limit always goes down)
        add = 1 + minimum_mewtations(source[0] + typed[:], source, limit - 1) #need to write typed[:]
        remove = 1 + minimum_mewtations(typed[1:], source, limit - 1)
        substitute = 1 + minimum_mewtations(source[0] + typed[1:], source, limit - 1)
        # BEGIN
        return min(add, remove, substitute) #why add
        # END


def final_diff(typed, source, limit):
    """A diff function that takes in a string TYPED, a string SOURCE, and a number LIMIT.
    If you implement this function, it will be used."""
    assert False, 'Remove this line to use your final_diff function.'

FINAL_DIFF_LIMIT = 6 # REPLACE THIS WITH YOUR LIMIT


###########
# Phase 3 #
###########


def report_progress(typed, source, user_id, upload):
    """Upload a report of your id and progress so far to the multiplayer server.
    Returns the progress so far.

    Arguments:
        typed: a list of the words typed so far
        source: a list of the words in the typing source
        user_id: a number representing the id of the current user
        upload: a function used to upload progress to the multiplayer server

    >>> print_progress = lambda d: print('ID:', d['id'], 'Progress:', d['progress'])
    >>> # The above function displays progress in the format ID: __, Progress: __
    >>> print_progress({'id': 1, 'progress': 0.6})
    ID: 1 Progress: 0.6
    >>> typed = ['how', 'are', 'you']
    >>> source = ['how', 'are', 'you', 'doing', 'today']
    >>> report_progress(typed, source, 2, print_progress)
    ID: 2 Progress: 0.6
    0.6
    >>> report_progress(['how', 'aree'], source, 3, print_progress)
    ID: 3 Progress: 0.2
    0.2
    """
    num_correct = 0 
    for i in range(len(typed)): #rangeee
        if typed[i] == source[i]:
            num_correct += 1
        else:
            break # have to break after hitting the first incorrect word
    progress = num_correct / len(source)
    upload({'id': user_id, 'progress': progress})
    print(progress) #print at the end


def time_per_word(words, timestamps_per_player):
    """Given timing data, return a match data abstraction, which contains a
    list of words and the amount of time each player took to type each word.

    Arguments:
        words: a list of words, in the order they are typed.
        timestamps_per_player: A list of lists of timestamps including the time
                          the player started typing, followed by the time
                          the player finished typing each word.

    >>> p = [[75, 81, 84, 90, 92], [19, 29, 35, 36, 38]]
    >>> match = time_per_word(['collar', 'plush', 'blush', 'repute'], p)
    >>> get_all_words(match)
    ['collar', 'plush', 'blush', 'repute']
    >>> get_all_times(match)
    [[6, 3, 6, 2], [10, 6, 1, 2]]
    """
    times = []
    for i in range(len(timestamps_per_player)):
        x = []
        for j in range(len(timestamps_per_player[i])):
            if j == len(timestamps_per_player[i]) - 1:
                break
            x.append(abs(timestamps_per_player[i][j+1] - timestamps_per_player[i][j]))
        times.append(x)
    return match(words, times)


def fastest_words(match):
    """Return a list of lists of which words each player typed fastest.

    Arguments:
        match: a match data abstraction as returned by time_per_word.

    >>> p0 = [5, 1, 3]
    >>> p1 = [4, 1, 6]
    >>> fastest_words(match(['Just', 'have', 'fun'], [p0, p1]))
    [['have', 'fun'], ['Just']]
    >>> p0  # input lists should not be mutated
    [5, 1, 3]
    >>> p1
    [4, 1, 6]
    """
    
    player_indices = range(len(get_all_times(match)))
    word_indices = range(len(get_all_words(match)))
    #takeaways: how to break the prolem down into parts... write as pseudocode

    # 1. create a list of which player typed each word the fastest
    # will be the length of words
    words = get_all_words(match)
    times = get_all_times(match)
    min_times_list = [] # have to keep this outside
    for each_word in word_indices: #0 1 2     # for each word, need to find the min_time and which player got it (their index)
        min_player_index = 0            # what do you need to keep track of? 
        min_time = times[0][each_word]
        for each_player in player_indices: #0 1
            if times[each_player][each_word] < min_time:
                min_player_index = each_player #    need to update
                min_time = times[each_player][each_word]
        min_times_list.append(min_player_index)
        
    # 2. seperate that list --> lists for each player with what words they typed fastest
    final_list = [[] for num_players in player_indices]
    for i in range(len(min_times_list)): # for each word
        final_list[min_times_list[i]].append(get_word(match, i))
    return final_list



def match(words, times):
    """A data abstraction containing all words typed and their times.

    Arguments:
        words: A list of strings, each string representing a word typed.
        times: A list of lists for how long it took for each player to type
            each word.
            times[i][j] = time it took for player i to type words[j].

    Example input:
        words: ['Hello', 'world']
        times: [[5, 1], [4, 2]]
    """
    assert all([type(w) == str for w in words]), 'words should be a list of strings'
    assert all([type(t) == list for t in times]), 'times should be a list of lists'
    assert all([isinstance(i, (int, float)) for t in times for i in t]), 'times lists should contain numbers'
    assert all([len(t) == len(words) for t in times]), 'There should be one word per time.'
    return {"words": words, "times": times}


def get_word(match, word_index):
    """A utility function that gets the word with index word_index"""
    assert 0 <= word_index < len(get_all_words(match)), "word_index out of range of words"
    return get_all_words(match)[word_index]


def time(match, player_num, word_index):
    """A utility function for the time it took player_num to type the word at word_index"""
    assert word_index < len(get_all_words(match)), "word_index out of range of words"
    assert player_num < len(get_all_times(match)), "player_num out of range of players"
    return get_all_times(match)[player_num][word_index]

def get_all_words(match):
    """A selector function for all the words in the match"""
    return match["words"]

def get_all_times(match):
    """A selector function for all typing times for all players"""
    return match["times"]


def match_string(match):
    """A helper function that takes in a match data abstraction and returns a string representation of it"""
    return f"match({get_all_words(match)}, {get_all_times(match)})"

enable_multiplayer = True  # Change to True when you're ready to race.

##########################
# Command Line Interface #
##########################


def run_typing_test(topics):
    """Measure typing speed and accuracy on the command line."""
    paragraphs = lines_from_file('data/sample_paragraphs.txt')
    select = lambda p: True
    if topics:
        select = about(topics)
    i = 0
    while True:
        source = pick(paragraphs, select, i)
        if not source:
            print('No more paragraphs about', topics, 'are available.')
            return
        print('Type the following paragraph and then press enter/return.')
        print('If you only type part of it, you will be scored only on that part.\n')
        print(source)
        print()

        start = datetime.now()
        typed = input()
        if not typed:
            print('Goodbye.')
            return
        print()

        elapsed = (datetime.now() - start).total_seconds()
        print("Nice work!")
        print('Words per minute:', wpm(typed, elapsed))
        print('Accuracy:        ', accuracy(typed, source))

        print('\nPress enter/return for the next paragraph or type q to quit.')
        if input().strip() == 'q':
            return
        i += 1


@main
def run(*args):
    """Read in the command-line argument and calls corresponding functions."""
    import argparse
    parser = argparse.ArgumentParser(description="Typing Test")
    parser.add_argument('topic', help="Topic word", nargs='*')
    parser.add_argument('-t', help="Run typing test", action='store_true')

    args = parser.parse_args()
    if args.t:
        run_typing_test(args.topic)