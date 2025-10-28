import os, time, random, pyautogui
from selenium import webdriver
from selenium.webdriver.common.by import By

#Set up web driver and options
driver =  webdriver.Chrome()
driver.get("https://www.nytimes.com/games/wordle/index.html")

options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors-spki-list')
options.add_argument('--ignore-ssl-errors')

#Set up the word list
WordList = []

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

WordList = open(".//WordleWords.txt").readlines()

Guesses = WordList.copy()
SafeLetters = []

#Enter the game
continue_button = driver.find_element(By.XPATH,'/html/body/div[2]/div[1]/div/div/div/div[2]/button[3]')
continue_button.click()
time.sleep(1)
x_button = driver.find_element(By.XPATH,'/html/body/div[2]/div/dialog/div/div/button')
x_button.click()
time.sleep(1)

#Perform a guess
def Guess(y):
    
    if len(Guesses) > 0:
        
        #If first guess, then use the word "Slate"; otherwise, use a random word from the possible winners
        if y == 1:
            guess_word = "slate\n"
        else:
            guess_word = random.choice(Guesses)
            Guesses.remove(guess_word)

        #Input the guess word
        pyautogui.write(guess_word)
        
        #Wait for the game to give grey/yellow/green letters
        time.sleep(2)

        #Remove all impossible options from the possible winners list
        for x in range (1,6):
            c_element = driver.find_element(By.XPATH,f'//*[@id="wordle-app-game"]/div[1]/div/div[{y}]/div[{x}]/div')
            letter = c_element.get_attribute('aria-label').split(",")[1].strip().lower()

            if c_element.get_attribute('aria-label').split(",")[2].strip() == "absent":
                if letter not in SafeLetters:
                    for item in Guesses[:]:
                        if letter in item:
                            Guesses.remove(item)
            elif c_element.get_attribute('aria-label').split(",")[2].strip() == "present in another position":
                SafeLetters.append(letter)
                for item in Guesses[:]:
                    if letter not in item or letter == item[(x - 1)]:
                        Guesses.remove(item)
            elif c_element.get_attribute('aria-label').split(",")[2].strip() == "correct":
                SafeLetters.append(letter)
                for item in Guesses[:]:
                    if letter != item[(x - 1)]:
                        Guesses.remove(item)
        time.sleep(1)
        print(Guesses)
    else:
        print("You won!")
        print(f"Guesses: {y - 1}")
        input('Press "Enter" to exit.')
        quit()

#Begin Guessing
#Guess 1
print(f'Words Possible: {len(Guesses)}')
Guess(1)
#Guess 2
print(f'Words Possible: {len(Guesses)}')
Guess(2)
#Guess 3
print(f'Words Possible: {len(Guesses)}')
Guess(3)
#Guess 4
print(f'Words Possible: {len(Guesses)}')
Guess(4)
#Guess 5
print(f'Words Possible: {len(Guesses)}')
Guess(5)
#Guess 6
print(f'Words Possible: {len(Guesses)}')
Guess(6)

if len(Guesses) <= 0:
    print("You won!")
    print(f"Guesses: 6")
    input('Press "Enter" to exit.')
    quit()
else:

    print("You lost.")
