import sys
import random
si = sys.stdin

# for winning
# sys.stdin = open('win.txt')

#for loosing
# sys.stdin = open(('lose.txt'))

def clean(string_bad , string_phrase):

    for x in string_bad:
        string_phrase = string_phrase.replace(x,' ')

    return string_phrase



def wordsByLength(string_arg):

    word_dict = {}
    words = string_arg.split()

    print(words)
    for x in words:
        length = len(x)
        if(length in word_dict):
            previous_list = word_dict[length]
            previous_list.append(x)
            word_dict[length] = previous_list
        else:
            word_dict[length] = [x]

    return word_dict

# dictt = wordsByLength(biercetxt)
# print([(k,len(dictt[k])) for k in sorted(dictt)])


class WordGame:

    def __init__(self,secret_word):
        self.sec_word = secret_word.upper()
        self.right_guess = ""
        self.wrong_guess = ""

    def getSecret(self):
        return self.sec_word

    def getRight(self):
        return self.right_guess

    def getWrong(self):
        return self.wrong_guess

    def getState(self):

        if(self.getHint() == self.sec_word):
            return "won"
        elif(len(self.wrong_guess) >= 6):
            return "lost"
        else:
            return "playing"

    def getHint(self):

        hint_string = ""
        count = 0

        for x in self.sec_word:
            hint_string += '?'

        if(self.right_guess==""):

            return hint_string

        else:

            hint_list = list(hint_string)

            for x in self.right_guess:

                for y in self.sec_word:


                    if(x.upper()==y):
                        hint_list[count] = x
                    count += 1


                count = 0

            hint_string = "".join(hint_list)
            return hint_string




    def guess(self,guess_string):

        guess_word = guess_string.upper()

        if(self.getState()=='won'):
            #do nothing
            pass

        elif(self.getState()=='lost'):
            #do nothing
            pass

        else:
            if(guess_word not in self.right_guess and guess_word in self.sec_word):
                self.right_guess += guess_word
            elif(guess_word not in self.sec_word):

                    if(guess_word not in self.wrong_guess):

                        self.wrong_guess += guess_word




def playWordGame(secretWord):

    wg_obj = WordGame(secretWord)
    while(wg_obj.getState()=='playing'):
        print("What is this word : ",wg_obj.getHint(),"\n")
        print("Right : ",wg_obj.getRight(),"\n")
        print("Wrong : ",wg_obj.getWrong(),"\n")
        guess_word = str(input("Guess a letter : "))
        wg_obj.guess(guess_word)
        print("\n\n")

    if(wg_obj.getState()=='won'):
        print("\n\nCongratulations, you guessed it!  The word is ",wg_obj.getSecret(),".")

    else:
        print("Sorry, you lose!  The secret word is ",wg_obj.getSecret(),".")



def play_game_using_bierce():

    biercetxt = clean('="0€%:@)795]”,(#-!3/;81?2&\'$.4*[6âï»¿', open('Bierce.txt').read())
    wbl = wordsByLength(biercetxt)
    playWordGame(random.choice(wbl[9]))


play_game_using_bierce()
# playWordGame("apple")



#following are the outputs to check the code. kindly uncomment and run them to see the output

#
# obj_wg = WordGame('apple')
# print(obj_wg.getSecret())
# print(obj_wg.getHint())
# print(obj_wg.getRight())
# print(obj_wg.getWrong())
# obj_wg.guess('p')
# print(obj_wg.getHint())
# print(obj_wg.getRight())
# print(obj_wg.getRight())
# print(obj_wg.getWrong())
# obj_wg.guess('z')
# print(obj_wg.getHint())
# print(obj_wg.getRight())
# print(obj_wg.getWrong())
# obj_wg.guess('p')
# obj_wg.guess('a')
# obj_wg.guess('z')
# obj_wg.guess('z')
# obj_wg.guess('z')
# obj_wg.guess('z')
#
# print(obj_wg.getRight())
#
# wg = WordGame('RAILROAD')
# print([(letter,wg.guess(letter), wg.getState(), wg.getHint(), wg.getRight(), wg.getWrong()) for letter in 'RQQOASFOYYUYUIRAILDTRE'])