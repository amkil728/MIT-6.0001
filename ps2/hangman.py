#!python
# Problem Set 2, hangman.py
# Name: aayush


# TODO:
# - Easy and hard modes (?)
# - Warning system (?)
# - Time taken (?)
# - Print high scores (?)


import random, string, time, os
from collections import Counter
from string import ascii_lowercase


LETTERS = ascii_lowercase         # String of all lowercase letters
WORDLIST_FILENAME = "words.txt"   # File to load words from
DASHES = '-' * 10 + '\n'          # String of dashes to print for screen break
GUESSES = 6                       # Number of guesses initially available to user
SCORES_FILE = 'scores.dat'         # File to save scores to



def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print("Loading word list...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # line: string
    line = inFile.readline()
    # wordlist: list of strings
    wordlist = line.split()
    #print("  ", len(wordlist), "words loaded.")
    time.sleep(0.5)
    os.system('cls')
    return wordlist



def choose_word(wordlist, min_letters, max_letters):
    """
    wordlist (list): list of words (strings)
    
    Returns string, random word from wordlist of length between min_letters
            and max_letters
    """

    while True:
        word = random.choice(wordlist)

        if min_letters <= len(word) <= max_letters:
            return word


# Load the list of words into the constant WORDLIST
# so that it can be accessed from anywhere in the program
WORDLIST = load_words()


def is_word_guessed(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing; assumes all letters are
      lowercase
    letters_guessed: list (of letters), which letters have been guessed so far;
      assumes that all letters are lowercase
    returns: boolean, True if all the letters of secret_word are in letters_guessed;
      False otherwise
    '''

    for letter in secret_word:
        if letter not in letters_guessed:
            return False

    return True



def get_guessed_word(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string, comprised of letters, underscores (_), and spaces that represents
      which letters in secret_word have been guessed so far.
    '''

    guessed_word = str() # string representing letters that have been guessed

    # For each letter in the word
    for letter in secret_word:
        # If letter has been guessed, add it to string
        if letter in letters_guessed:
            guessed_word += letter
        # Otherwise, add underscore, representing an unguessed letter
        else:
            guessed_word += ' _ '

    return guessed_word



def get_available_letters(letters_guessed):
    '''
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string (of letters), comprised of letters that represents which letters have not
      yet been guessed.
    '''

    available_letters = str()

    # For each lowercase letter
    for letter in LETTERS:
        # If letter has not been guessed yet
        if letter not in letters_guessed:
            # Add it to available letters
            available_letters += letter

    return available_letters



def calculate_score(secret_word, guesses_remaining):
    '''
    Calculates the score obtained by the player, according to the formula:
        score = guesses_remaining * number of unique letters in secret word

    Arguments:
    - secret_word: string, secret word guessed by player
    - guesses_remaining: int, number of guesses remaining
    
    Returns: int, score obtained by player
    '''

    # First, get number of unique letters in word

    # Start count at 0
    letter_count = 0

    # Keep track of letters already found in word
    found_letters = list()

    # For each letter in word
    for letter in secret_word:
        # If letter has been found, do nothing
        if letter in found_letters:
            continue

        # Add it to list of letters found, and increment count
        found_letters.append(letter)
        letter_count += 1

    # Score is letter_count * guesses_remaining
    return letter_count * guesses_remaining



def get_letter(available_letters, prompt, not_available_message):
    '''
    Prompts the user to enter a letter from the list of available letters.
    Keeps repeating until they enter a letter which is in the list.

    Arguments:
    - available_letters: list of letters available to user
    - prompt: string, prompt to display to user

    Returns: letter entered by user
    '''

    while True:
        # Prompt user to enter letter
        ch = input(prompt)

        # If nothing was entered
        if not ch:
            print("Oops! You didn\'t enter anything at all. Try again.")
            continue

        # If user typed a space after letter
        if ch.endswith(' '):
            print(f'I think you accidentaly put a space after {ch.strip()}.')
            print('Please try again.')
            continue

        # If user typed space before letter
        if ch.startswith(' '):
            print(f'I think you accidentaly put a space before {ch.strip()}')
            print('Please try again.')
            continue

        # If multiple characters entered
        if len(ch) > 1:
            print('You have entered', len(ch), f"characters: '{ch}'.")
            print('Please enter only a single letter.')
            continue

        # If character is not a letter
        if not ch.isalpha():
            print('Sorry,', ch, 'is not a valid letter.')
            continue

        # Since character is letter, make it lowercase
        letter = ch.lower()

        # If letter is in list of available letters, return it
        if letter in available_letters:
            return letter

        # Otherwise, inform user, and loop again
        print(not_available_message)



def print_intro():
    '''Prints the introduction to the game.'''

    header = '''

  _    _                                         
 | |  | |                                        
 | |__| | __ _ _ __   __ _ _ __ ___   __ _ _ __  
 |  __  |/ _` | '_ \ / _` | '_ ` _ \ / _` | '_ \ 
 | |  | | (_| | | | | (_| | | | | | | (_| | | | |
 |_|  |_|\__,_|_| |_|\__, |_| |_| |_|\__,_|_| |_|
                      __/ |                      
                     |___/                       


    '''

    print(header)
    print('by Aayush'.rjust(100))
    print()
    print()
    print()
    print('Hello! You have started a new game of Hangman. Have fun!')
    input()


def hangman(secret_word):
    '''
    Argument:
    secret_word: string, the secret word to guess.

    Returns: int, score obtained by user if they guess the word,
                0 otherwise
    
    Starts up an interactive game of Hangman.
    
    * At the start of the game, let the user know how many 
      letters the secret_word contains and how many guesses s/he starts with.
      
    * The user should start with 6 guesses

    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.
    
    * Ask the user to supply one guess per round. Remember to make
      sure that the user puts in a letter!
    
    * The user should receive feedback immediately after each guess 
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the 
      partially guessed word so far.
    
    Follows the other limitations detailed in the problem write-up.
    '''

    # Start with number of guesses predefined in a constant
    guesses_remaining = GUESSES

    # Initially, all letters are available
    available_letters = LETTERS

    # Create list to store letters guessed by user
    letters_guessed = list()

    print('-' * 50)
    print()
    print('I am thinking of a word that is', end=' ')
    print(len(secret_word), 'letters long.')
    print('You start with', GUESSES, 'guesses.')

    input()

    # While user has remaining guesses
    while guesses_remaining:
        print(DASHES)
        
        # Print number of remaining guesses
        print('You have', guesses_remaining, 'guesses left.')

        # Get and print available letters and guessed letters
        available_letters = get_available_letters(letters_guessed)

        if letters_guessed:
            print('So far, you have guessed the letters:',
                  ' '.join(letters_guessed))

        print('Available letters:', ' '.join(available_letters))

        # Get guess from user
        guess = get_letter(available_letters, "Guess a letter: ",
                "Sorry, you've already guessed that letter. Please try again.")
        
        # If guess was wrong
        if guess not in secret_word:
            print(f'Sorry, the letter {guess} is not in the word.')
            # Decrement remaining guesses by one
            guesses_remaining -= 1
        else:
            print('Good guess!')

        # Add guess to list of guessed letters
        letters_guessed.append(guess)

        # Print word with guessed letters
        print('Letters guessed so far:', end=' ')
        print(get_guessed_word(secret_word, letters_guessed))

        print()

        # If user guessed word correctly
        if is_word_guessed(secret_word, letters_guessed):
            print(DASHES)

            # Tell user they have guessed the word
            print('Well done! You have guessed the word.')
            # Find and print user's score
            score = calculate_score(secret_word, guesses_remaining)
            print('Your score for this game is:', score)
                  
            # Return score and end the function
            return score

    # If no remaining guesses
    else:
        # Inform user, and print secret word
        print(DASHES)
        print('Sorry, you ran out of guesses.', end=' ')
        print(f'The word was {secret_word}.')

    print()

    return 0



def get_y_or_n(prompt):
    '''
    Repeatedly prompts the user to enter the letters 'y' or 'n'.

    Argument:
    - prompt: string, prompt to display to user

    Returns: bool, True if user enters 'y', False if user enters 'n'
    '''

    ch = input(prompt)

    while True:
        if ch == 'y':
            return True
        if ch == 'n':
            return False

        ch = input('Please enter one of the letters y or n. ')



if __name__ == "__main__":
    print_intro()

    # Keep track of score across several games
    total_score = 0

    # Main loop
    while True:
        # Get the secret word
        secret_word = choose_word(WORDLIST, min_letters=6, max_letters=8)

        # Run game and get users score
        score = hangman(secret_word)

        # Add score to running total
        total_score += score

        # Ask user if they want to play another game
        if get_y_or_n('Press y to play another game, and n to quit. '):
            # If entered 'y', go to next iteration
            print()
            continue

        # User entered 'n'
        # Ask user if they want to save their score
        if get_y_or_n('Save your score? (y/n) '):
            # If user entered 'y', ask for user name
            name = input('Please enter your user name: ')
            
            # Save name and score to scores file
            with open(SCORES_FILE, 'a') as outfile:
                line = name + ', ' + str(total_score) + '\n'
                outfile.write(line)


        # Print total score and end game
        print('Your total score is', total_score, '. Well done!')
        input('Press enter to end the game. ')
        break
