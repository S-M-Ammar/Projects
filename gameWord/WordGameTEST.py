>>> from WordGame import *

>>> import random

############################# Final Project Rules #############################

You MUST WORK ON YOUR OWN on this project.
You are NOT allowed to COLLABORATE with others.
You MUST WRITE YOUR OWN CODE.

You MAY use any course materials or notes you like.
You MAY research on the existing material on internet, BUT

YOu MAY NOT solicit advice on the internet or from any source (other than the prof).
You MAY NOT POST code, questions, or problem descriptions anywhere.

You MAY ask the professor questions to clarify the assignment.

############################# Directions #############################

The goal of this assignment is to create a text based word guessing
game.  The project is completely described in this file,
WordGameTEST.py.  Follow these steps:

    1) download files to your working folder.  you will need the win.txt
    and lose.txt files as inputs    

    2) Create a file WordGame.py and add your solutions
    (functions/classes) to that file.    
    
    3) After you finish each section, run the doctest to check it.

    4) When you are finished submit your WordGame.py to
    d2l>submissions>FinalProject

If you finish, you can play the game (see the final section below).

#################### clean ####################

clean - Implement a function clean that accepts two str arguments, the
first a str of "bad" characters and the second a phrase.  clean
should then return a copy of the phrase where each character in the bad
str has been replaced by a single space character, " ".

>>> clean(".,?", 'Hello, how are you?')		      
'Hello  how are you '
>>> bad = '="0€%:@)795]”,(#-!3/;81?2&\'$.4*[6â'
>>> clean( bad, 'ACADEME, n. An ancient school where morality and philosophy were taught.')      
'ACADEME  n  An ancient school where morality and philosophy were taught '
>>> clean(bad, 'ACADEMY, n. [from ACADEME] A modern school where football is taught.')		      
'ACADEMY  n   from ACADEME  A modern school where football is taught '
>>> clean(bad, bad) == len(bad)*" "		      
True

##>>> biercetxt = clean(bad,open('Bierce.txt').read())
##>>> len(biercetxt)
##382251

#################### wordsByLength ####################

wordsByLength - Implement a function wordsByLength that accepts one str
argument, a phrase, and that returns a dictionary.  Each key in the
returned dictionary is a word length and the  value corresponding to
that key will be a list of the words in the phrase that have that
length.  Entries will be listed in the order encountered.

>>> wordsByLength('hello how are you')
{5: ['hello'], 3: ['how', 'are', 'you']}
>>> wordsByLength('Given a phrase this function will return a dictionary that lists those words by length')
{5: ['Given', 'lists', 'those', 'words'], 1: ['a', 'a'], 6: ['phrase', 'return', 'length'], 4: ['this', 'will', 'that'], 8: ['function'], 10: ['dictionary'], 2: ['by']}


##>>> wbl = wordsByLength(biercetxt)
##>>> [(k,len(wbl[k])) for k in sorted(wbl)]
##[(1, 4147), (2, 11333), (3, 13065), (4, 9680), (5, 6628), (6, 5106), (7, 4663), (8, 3253), (9, 2877), (10, 1891), (11, 970), (12, 488), (13, 252), (14, 116), (15, 33), (16, 10), (17, 7)]
##>>> wbl[17]
##['controversialists', 'controversialists', 'contradistinction', 'objectionableness', 'WHANGDEPOOTENAWAH', 'Whangdepootenawah', 'Whangdepootenawah']


#################### WordGame ####################

WordGame - Implement a class WordGame that is the basis for a guessing
game for words.  A WordGame object has a secret word inside.  The
letters can be guessed using the guess method and the game will keep
track of both the correct and incorrect guesses that have been made as
well as the state of the game, i.e., whether still playing, won or lost.

Implementation methods/details:

__init__ - accepts one str argument, the secret word.  Note that the
secret word can be given in any case but should be stored in UPPER case.
This method should create and initialize 3 attributes (ie., self.?????
):
    - str attribute to keep track of the secret word, initialized to the
    given secret word (but converted to UPPER case).
    
    - str attribute to keep track of correct/right guesses, initialized
    to an empty str.
    
    - str attribute to keep track of incorrect/wrong guesses,
     initialized to an empty str.

getSecret, getRight, getWrong – methods that return the stored str
attributes referred to above

getHint – returns masked version of the secret word.  Only the letters
that have been guessed correctly are revealed, all others display as
‘?’.

getState – returns one of three str values:

    ‘won’ – if all letters have been guessed correctly (how do you know in terms of the three attributes)
    ‘lost’ – if there have been 6 (or more) incorrect guesses,
    ‘playing’ – otherwise

guess – accepts one argument, an letter.  Immediately converts the
letter to uppercase and then does the following:

    - if the game is already won or lost (can call getState to find
    out), do nothing (quit)

    - if the letter has already been guessed (right or wrong), do
    nothing (quit)

    - if the letter is in the secret word, add the letter to the
    correct/right guess attribute,

    - Otherwise (the letter is incorrect) so add it to the
    wrong/incorrect guess attribute.


# basic game play

>>> wg = WordGame('apple')
>>> wg.getSecret()
'APPLE'
>>> wg.getHint()
'?????'
>>> wg.getRight()
''
>>> wg.getWrong()
''
>>> wg.guess('p') # correct guess     
>>> wg.getHint()	     
'?PP??'
>>> wg.getRight()	     
'P'
>>> wg.getWrong()	     
''
>>> wg.guess('z') # incorrect guess	     
>>> wg.getHint()	     
'?PP??'
>>> wg.getRight()	     
'P'
>>> wg.getWrong()	     
'Z'

# a winning game, notice that repeated guesses are ignored

>>> wg = WordGame('apple')
>>> wg.getState(), wg.getHint(), wg.getRight(), wg.getWrong()
('playing', '?????', '', '')
>>> wg.guess('P')
>>> wg.getState(), wg.getHint(), wg.getRight(), wg.getWrong()
('playing', '?PP??', 'P', '')
>>> wg.guess('Q')
>>> wg.getState(), wg.getHint(), wg.getRight(), wg.getWrong()
('playing', '?PP??', 'P', 'Q')
>>> wg.guess('R')
>>> wg.getState(), wg.getHint(), wg.getRight(), wg.getWrong()
('playing', '?PP??', 'P', 'QR')
>>> wg.guess('L')
>>> wg.getState(), wg.getHint(), wg.getRight(), wg.getWrong()
('playing', '?PPL?', 'PL', 'QR')
>>> wg.guess('L')
>>> wg.getState(), wg.getHint(), wg.getRight(), wg.getWrong()
('playing', '?PPL?', 'PL', 'QR')
>>> wg.guess('A')
>>> wg.getState(), wg.getHint(), wg.getRight(), wg.getWrong()
('playing', 'APPL?', 'PLA', 'QR')
>>> wg.guess('E')
>>> wg.getState(), wg.getHint(), wg.getRight(), wg.getWrong()
('won', 'APPLE', 'PLAE', 'QR')
>>> wg.guess('X')
>>> wg.getState(), wg.getHint(), wg.getRight(), wg.getWrong()
('won', 'APPLE', 'PLAE', 'QR')

# some complete games

>>> wg = WordGame('RAILROAD')
>>> [(letter,wg.guess(letter), wg.getState(), wg.getHint(), wg.getRight(), wg.getWrong()) for letter in 'RQQOASFOYYUYUIRAILTRE']
[('R', None, 'playing', 'R???R???', 'R', ''), ('Q', None, 'playing', 'R???R???', 'R', 'Q'), ('Q', None, 'playing', 'R???R???', 'R', 'Q'), ('O', None, 'playing', 'R???RO??', 'RO', 'Q'), ('A', None, 'playing', 'RA??ROA?', 'ROA', 'Q'), ('S', None, 'playing', 'RA??ROA?', 'ROA', 'QS'), ('F', None, 'playing', 'RA??ROA?', 'ROA', 'QSF'), ('O', None, 'playing', 'RA??ROA?', 'ROA', 'QSF'), ('Y', None, 'playing', 'RA??ROA?', 'ROA', 'QSFY'), ('Y', None, 'playing', 'RA??ROA?', 'ROA', 'QSFY'), ('U', None, 'playing', 'RA??ROA?', 'ROA', 'QSFYU'), ('Y', None, 'playing', 'RA??ROA?', 'ROA', 'QSFYU'), ('U', None, 'playing', 'RA??ROA?', 'ROA', 'QSFYU'), ('I', None, 'playing', 'RAI?ROA?', 'ROAI', 'QSFYU'), ('R', None, 'playing', 'RAI?ROA?', 'ROAI', 'QSFYU'), ('A', None, 'playing', 'RAI?ROA?', 'ROAI', 'QSFYU'), ('I', None, 'playing', 'RAI?ROA?', 'ROAI', 'QSFYU'), ('L', None, 'playing', 'RAILROA?', 'ROAIL', 'QSFYU'), ('T', None, 'lost', 'RAILROA?', 'ROAIL', 'QSFYUT'), ('R', None, 'lost', 'RAILROA?', 'ROAIL', 'QSFYUT'), ('E', None, 'lost', 'RAILROA?', 'ROAIL', 'QSFYUT')]
>>> wg = WordGame('RAILROAD')
>>> [(letter,wg.guess(letter), wg.getState(), wg.getHint(), wg.getRight(), wg.getWrong()) for letter in 'RQQOASFOYYUYUIRAILDTRE']
[('R', None, 'playing', 'R???R???', 'R', ''), ('Q', None, 'playing', 'R???R???', 'R', 'Q'), ('Q', None, 'playing', 'R???R???', 'R', 'Q'), ('O', None, 'playing', 'R???RO??', 'RO', 'Q'), ('A', None, 'playing', 'RA??ROA?', 'ROA', 'Q'), ('S', None, 'playing', 'RA??ROA?', 'ROA', 'QS'), ('F', None, 'playing', 'RA??ROA?', 'ROA', 'QSF'), ('O', None, 'playing', 'RA??ROA?', 'ROA', 'QSF'), ('Y', None, 'playing', 'RA??ROA?', 'ROA', 'QSFY'), ('Y', None, 'playing', 'RA??ROA?', 'ROA', 'QSFY'), ('U', None, 'playing', 'RA??ROA?', 'ROA', 'QSFYU'), ('Y', None, 'playing', 'RA??ROA?', 'ROA', 'QSFYU'), ('U', None, 'playing', 'RA??ROA?', 'ROA', 'QSFYU'), ('I', None, 'playing', 'RAI?ROA?', 'ROAI', 'QSFYU'), ('R', None, 'playing', 'RAI?ROA?', 'ROAI', 'QSFYU'), ('A', None, 'playing', 'RAI?ROA?', 'ROAI', 'QSFYU'), ('I', None, 'playing', 'RAI?ROA?', 'ROAI', 'QSFYU'), ('L', None, 'playing', 'RAILROA?', 'ROAIL', 'QSFYU'), ('D', None, 'won', 'RAILROAD', 'ROAILD', 'QSFYU'), ('T', None, 'won', 'RAILROAD', 'ROAILD', 'QSFYU'), ('R', None, 'won', 'RAILROAD', 'ROAILD', 'QSFYU'), ('E', None, 'won', 'RAILROAD', 'ROAILD', 'QSFYU')]
>>>


#################### playWordGame ####################

playWordGame - Implement a function playWordGame that allows the user to
interactively play a round of the WordGame.  The function accepts a
single argument, the secret word.  It then asks the user for guesses
until the game is won or lost. This function is a WordGame client, i.e.,
it creates and manipulates a WordGame object.  See the following
interaction which specifies how the game is played.

DO NOT UNCOMMENT the following lines.  They are provided to indicate a
user interaction, but the doctest will actually read the input from the
files win.txt and lose.txt (see below). Note also that the printed lines
below should also be left-justified, they are listed here with extra
space only for readability.

##   # winning game

##   >>> playWordGame('apple')     
##   What is this word? ?????
##   Right: 
##   Wrong: 
##   Guess a letter: p
##   
##   What is this word? ?PP??
##   Right: P
##   Wrong: 
##   Guess a letter: p
##   
##   What is this word? ?PP??
##   Right: P
##   Wrong: 
##   Guess a letter: l
##   
##   What is this word? ?PPL?
##   Right: PL
##   Wrong: 
##   Guess a letter: w
##   
##   What is this word? ?PPL?
##   Right: PL
##   Wrong: W
##   Guess a letter: 
##   
##   What is this word? ?PPL?
##   Right: PL
##   Wrong: W
##   Guess a letter: a
##   
##   What is this word? APPL?
##   Right: PLA
##   Wrong: W
##   Guess a letter: e
##   
##   Congratulations, you guessed it!  The word is APPLE.

##   # losing game

##   >>> playWordGame('apple')	     
##   What is this word? ?????
##   Right: 
##   Wrong: 
##   Guess a letter: v
##   
##   What is this word? ?????
##   Right: 
##   Wrong: V
##   Guess a letter: e
##   
##   What is this word? ????E
##   Right: E
##   Wrong: V
##   Guess a letter: h
##   
##   What is this word? ????E
##   Right: E
##   Wrong: VH
##   Guess a letter: o
##   
##   What is this word? ????E
##   Right: E
##   Wrong: VHO
##   Guess a letter: q
##   
##   What is this word? ????E
##   Right: E
##   Wrong: VHOQ
##   Guess a letter: y
##   
##   What is this word? ????E
##   Right: E
##   Wrong: VHOQY
##   Guess a letter: u
##   
##   Sorry, you lose!  The secret word is APPLE.

actual doctest code below.  Note that it reads from the files win.txt
and lose.txt which must be in the current folder. (code below directs
input to be received from above should not cause an error.)

>>> import sys
>>> si = sys.stdin
>>> sys.stdin = open('win.txt')

>>> playWordGame('apple')
What is this word? ?????
Right: 
Wrong: 
Guess a letter: 
What is this word? ?PP??
Right: P
Wrong: 
Guess a letter: 
What is this word? ?PPL?
Right: PL
Wrong: 
Guess a letter: 
What is this word? ?PPL?
Right: PL
Wrong: 
Guess a letter: 
What is this word? ?PPL?
Right: PL
Wrong: 
Guess a letter: 
What is this word? ?PPL?
Right: PL
Wrong: V
Guess a letter: 
What is this word? ?PPL?
Right: PL
Wrong: VH
Guess a letter: 
What is this word? ?PPL?
Right: PL
Wrong: VHK
Guess a letter: 
What is this word? APPL?
Right: PLA
Wrong: VHK
Guess a letter: 
Congratulations, you guessed it!  The word is APPLE.

>>> sys.stdin = open('lose.txt')

>>> random.seed(2)
>>> playWordGame('WHANGDEPOOTENAWAH')
What is this word? ?????????????????
Right: 
Wrong: 
Guess a letter: 
What is this word? ??A??????????A?A?
Right: A
Wrong: 
Guess a letter: 
What is this word? ??A??????????A?A?
Right: A
Wrong: B
Guess a letter: 
What is this word? ??A??????????A?A?
Right: A
Wrong: BC
Guess a letter: 
What is this word? ??A??D???????A?A?
Right: AD
Wrong: BC
Guess a letter: 
What is this word? ??A??DE????E?A?A?
Right: ADE
Wrong: BC
Guess a letter: 
What is this word? ??A??DE????E?A?A?
Right: ADE
Wrong: BCF
Guess a letter: 
What is this word? ??A?GDE????E?A?A?
Right: ADEG
Wrong: BCF
Guess a letter: 
What is this word? ?HA?GDE????E?A?AH
Right: ADEGH
Wrong: BCF
Guess a letter: 
What is this word? ?HA?GDE????E?A?AH
Right: ADEGH
Wrong: BCFI
Guess a letter: 
What is this word? ?HA?GDE????E?A?AH
Right: ADEGH
Wrong: BCFIJ
Guess a letter: 
Sorry, you lose!  The secret word is WHANGDEPOOTENAWAH.

put stdin back to original, again, shouldnt cause error
>>> sys.stdin = si


#################### want to play? ####################

If you have finished the above, CONGRATULATIONS you are DONE!  If you
want to actually play the game for fun with a randomly selected (and
perhaps odd) word, run the following (which selects a random word of
length 9 from Bierce.txt) and runs your code!

##  >>> bad = '="0€%:@)795]”,(#-!3/;81?2&\'$.4*[6â'
##  >>> biercetxt = clean(bad,open('Bierce.txt').read())
##  >>> wbl = wordsByLength(biercetxt) 
##  >>> playWordGame( random.choice( wbl[9] )) # random word with length 9!














