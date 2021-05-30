# 6.0001 Problem Set 3
#
# The 6.0001 Word Game
# Created by: Kevin Luu <luuk> and Jenna Wiens <jwiens>
#
# Name          : amkil728

# TO DO:
# Wildcards


import math, random, string, os


VOWELS = 'aeiou'                        # string containing all vowels
CONSONANTS = 'bcdfghjklmnpqrstvwxyz'    # string containing all consonants
LETTERS = VOWELS + CONSONANTS           # string containing all letters of the alphabet
HAND_SIZE = 10                          # size of hand dealt to user at start of game

# Values assigned to each letter for scoring words
LETTER_VALUES = {
    'a': 1, 'b': 3, 'c': 3, 'd': 2, 'e': 1, 'f': 4, 'g': 2, 'h': 4, 'i': 1,
    'j': 8, 'k': 5, 'l': 1, 'm': 3, 'n': 1, 'o': 1, 'p': 3, 'q': 10, 'r': 1,
    's': 1, 't': 1, 'u': 1, 'v': 4, 'w': 4, 'x': 8, 'y': 4, 'z': 10
}


WORDLIST_FILENAME = "words_v2.txt" # file to load words from


def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    
    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # wordlist: list of strings
    wordlist = []
    for line in inFile:
        wordlist.append(line.strip().lower())
    print("  ", len(wordlist), "words loaded.")
    os.system('cls')
    return wordlist


def get_frequency_dict(sequence):
    """
    Returns a dictionary where the keys are elements of the sequence
    and the values are integer counts, for the number of times that
    an element is repeated in the sequence.

    sequence: string or list
    return: dictionary
    """
    
    # freqs: dictionary (element_type -> int)
    freq = {}
    for x in sequence:
        freq[x] = freq.get(x,0) + 1
    return freq
	


def get_word_score(word, n):
    """
    Returns the score for a word. Assumes the word is a
    valid word.

    You may assume that the input word is always either a string of letters, 
    or the empty string "". You may not assume that the string will only contain 
    lowercase letters, so you will have to handle uppercase and mixed case strings 
    appropriately. 

	The score for a word is the product of two components:

	The first component is the sum of the points for letters in the word.
	The second component is the larger of:
            1, or
            7*wordlen - 3*(n-wordlen), where wordlen is the length of the word
            and n is the hand length when the word was played

	Letters are scored as in Scrabble; A is worth 1, B is
	worth 3, C is worth 3, D is worth 2, E is worth 1, and so on.

    word: string
    n: int >= 0
    returns: int >= 0
    """

    # Get letter values
    letter_values = (LETTER_VALUES[letter] for letter in word.lower())

    # Calculate sum of letter points
    letter_score = sum(letter_values)

    word_len = len(word)     # length of word

    # Calculate multiplier:

    # contribution of hand size to multiplier
    hand_size_factor = 3 * (n - word_len)

    # multiple of word length
    word_len_multiple = 7 * word_len

    # multiplier is maximum of word_len_multiple - hand_size_factor and 1
    multiplier = max(word_len_multiple - hand_size_factor, 1)

    # Score is product of letter score and multiplier
    return letter_score * multiplier


def display_hand(hand):
    """
    Displays the letters currently in the hand.

    For example:
       display_hand({'a':1, 'x':2, 'l':3, 'e':1})
    Should print out something like:
       a x x l l l e
    The order of the letters is unimportant.

    hand: dictionary (string -> int)
    """
    
    for letter in hand.keys():
        for j in range(hand[letter]):
             print(letter, end=' ')      # print all on the same line
    print()                              # print an empty line



def deal_hand(n):
    """
    Returns a random hand containing n lowercase letters.
    ceil(n/3) - 1 letters in the hand should be VOWELS, and 1 letter should
    be the wilcard, '*'.

    Hands are represented as dictionaries. The keys are letters and the values
    are the number of times the particular letter is repeated in that hand.

    n: int >= 0
    returns: dictionary (string -> int)
    """

    # Initialise hand as empty dict
    hand = dict()

    num_vowels = int(math.ceil(n / 3)) - 1

    # Deal vowels
    for i in range(num_vowels):
        x = random.choice(VOWELS)
        hand[x] = hand.get(x, 0) + 1

    # Deal wildcard
    hand['*'] = 1

    # Deal consonants
    for i in range(num_vowels + 1, n):    
        x = random.choice(CONSONANTS)
        hand[x] = hand.get(x, 0) + 1
    
    return hand



def update_hand(hand, word):
    """
    Does NOT assume that hand contains every letter in word at least as
    many times as the letter appears in word. Letters in word that don't
    appear in hand should be ignored. Letters that appear in word more times
    than in hand should never result in a negative count; instead, set the
    count in the returned hand to 0 (or remove the letter from the
    dictionary, depending on how your code is structured). 

    Updates the hand: uses up the letters in the given word
    and returns the new hand, without those letters in it.

    Has no side effects: does not modify hand.

    word: string
    hand: dictionary (string -> int)    
    returns: dictionary (string -> int)
    """

    temp = hand.copy()

    for char in word:
        letter = char.lower()
        
        if letter not in temp:
            continue

        if temp[letter] == 1:
            temp.pop(letter)

        else:
            temp[letter] -= 1

    return temp



def is_valid_word(word, hand, word_list):
    """
    Returns True if word is in the word_list and is entirely
    composed of letters in the hand. Otherwise, returns False.
    Does not mutate hand or word_list.
   
    word: string
    hand: dictionary (string -> int)
    word_list: list of lowercase strings
    returns: boolean
    """

    # Convert word to lowercase to compare it to word list
    word = word.lower()

    # If word is not in word list, it is not valid
    if word not in word_list:
        return False

    # Otherwise, need to check if word can be formed from letters in hand

    # Get letter frequencies for word
    word_letters = get_frequency_dict(word)

    # word is invalid if any letter occurs less in hand than in word
    for letter, freq in word_letters.items():
        if hand.get(letter, 0) < freq:
            return False

    # Otherwise, it is valid
    return True



def calculate_handlen(hand):
    """ 
    Returns the length (number of letters) in the current hand.
    
    hand: dictionary (string-> int)
    returns: integer
    """

    # Length of hand = sum of values for each letter
    return sum(hand.values())


def play_hand(hand, word_list):

    """
    Allows the user to play the given hand, as follows:

    * The hand is displayed.
    
    * The user may input a word.

    * When any word is entered (valid or invalid), it uses up letters
      from the hand.

    * An invalid word is rejected, and a message is displayed asking
      the user to choose another word.

    * After every valid word: the score for that word is displayed,
      the remaining letters in the hand are displayed, and the user
      is asked to input another word.

    * The sum of the word scores is displayed when the hand finishes.

    * The hand finishes when there are no more unused letters.
      The user can also finish playing the hand by inputing two 
      exclamation points (the string '!!') instead of a word.

      hand: dictionary (string -> int)
      word_list: list of lowercase strings
      returns: the total score for the hand
      
    """

    # Keep track of the total score
    total_score = 0

    # Keep track if user has entered any invalid words
    entered_invalid_word = False

    # As long as there are still letters left in the hand:
    while hand:
        # Display the hand
        print('Current hand:', end=' ')
        display_hand(hand)

        # Ask user for input
        word = input('Enter word, or "!!" to indicate that you are finished: ')

        # If the input is two exclamation points:
        if word == '!!':
            # End the game (break out of the loop)
            print()
            break


        # If the word is valid:
        if is_valid_word(word, hand, word_list):

            # Tell the user how many points the word earned,
            # and the updated total score
            score = get_word_score(word, calculate_handlen(hand))
            total_score += score

            print(f'{word}: {score} points. Total: {total_score} points.')

            # Update the user's hand by removing the letters of their inputted word
            hand = update_hand(hand, word)

        # Otherwise ,the word is not valid
        else:
            # Update the user's hand by removing the letters of their inputted word
            hand = update_hand(hand, word)

            # Reject invalid word (print a message)
            print(f'Sorry, {word} is not a valid word.', end='')
            if hand:
                print(' Please try again!')
            else:
                print()

            # Note that user entered invalid word
            entered_invalid_word = True

        

        print()

    # The hand is over (user entered '!!' or ran out of letters)
    if not hand:
        if entered_invalid_word:
            print("Run out of letters.")
        else:
            print('Good job! You used all the letters.')

    # Tell user the score
    print('Total score for this hand:', total_score)

    # Return the total score as result of function
    return total_score



def play_game(word_list):
    """
    Allow the user to play a series of hands.

    * Asks the user to input a total number of hands

    * Accumulates the score for each hand into a total score for the 
      entire series
 
    * For each hand, before playing, ask the user if they want to substitute
      one letter for another. If the user inputs 'yes', prompt them for their
      desired letter. This can only be done once during the game. Once the
      substitue option is used, the user should not be asked if they want to
      substitute letters in the future. (IN PROGRESS!)

    * For each hand, ask the user if they would like to replay the hand.
      If the user inputs 'yes', they will replay the hand and keep 
      the better of the two scores for that hand.  This can only be done once 
      during the game. Once the replay option is used, the user should not
      be asked if they want to replay future hands. Replaying the hand does
      not count as one of the total number of hands the user initially
      wanted to play.

            * Note: if you replay a hand, you do not get the option to substitute
                    a letter - you must play whatever hand you just had.
      
    * Returns the total score for the series of hands

    word_list: list of lowercase strings
    """

    # Ask user to input total number of hands
    number_of_hands = int(input('How many hands would you like to play? '))

    # Keep track of total score
    total_score = 0

    # Initially, player has option to replay hand and substitute a letter
    replay = substitute = True

    print()

    # While there are hands left
    while number_of_hands:
        # Deal hand
        hand = deal_hand(HAND_SIZE)

        # Display the hand
        print('New hand:', end=' ')
        display_hand(hand)
        print()

        # If player has substitute option
        if substitute:
            # Ask user if they want to substitute a letter
            option = input('Would you like to substitute a letter? ')

            # If yes
            if option == 'yes':
                # Ask which letter to substitute
                letter = input('Which letter would you like to replace? ')

                # Substitute letter
                hand, new_letter = substitute_hand(hand, letter)

                # Print substituted letter
                print(f'I have replaced {letter} with {new_letter}.')

                # User loses substitute option
                substitute = False

            print()

        # Play hand and get score
        hand_score = play_hand(hand, word_list)

        print_separator()

        # If user has replay option
        if replay:
            # Ask user if they would like to replay
            option = input('Would you like to replay the hand? ')

            # If yes
            if option == 'yes':
                print()
                
                # Play hand again, and get score
                new_score = play_hand(hand, word_list)

                # Score for hand is better of the two scores
                hand_score = max(hand_score, new_score)

                # Display final score for hand
                print_separator()
                print('Final score for this hand:', hand_score)

                # User loses replay option
                replay = False

            print_separator()

        # Update total score with score for this hand
        total_score += hand_score

        # Decrement number of hands
        number_of_hands -= 1

    # Print total score
    print('Total score for this game:', total_score)


def substitute_hand(hand, letter):
    """ 
    Allow the user to replace all copies of one letter in the hand (chosen by user)
    with a new letter chosen from the VOWELS and CONSONANTS at random. The new letter
    should be different from user's choice, and should not be any of the letters
    already in the hand.

    If user provide a letter not in the hand, the hand should be the same.

    Has no side effects: does not mutate hand.

    For example:
        substitute_hand({'h':1, 'e':1, 'l':2, 'o':1}, 'l')
    might return:
        {'h':1, 'e':1, 'o':1, 'x':2} -> if the new letter is 'x'
    The new letter should not be 'h', 'e', 'l', or 'o' since those letters were
    already in the hand.
    
    hand: dictionary (string -> int)
    letter: string
    returns: dictionary (string -> int), string
    """

    temp = hand.copy()

    while True:
        new_letter = random.choice(LETTERS)

        if new_letter not in hand:
            break

    if letter in temp:
        temp[new_letter] = temp[letter]
        temp.pop(letter)

    return temp, new_letter


def print_separator():
    '''Prints a separator: newline, 10 dashes, newline'''
    print()
    print('-' * 10)
    print()



# Build data structures used for entire session and play game
if __name__ == '__main__':
    word_list = load_words()

    print('Starting a new game.')
    print()
    play_game(word_list)
    print()
    print('Goodbye!')
    input()
