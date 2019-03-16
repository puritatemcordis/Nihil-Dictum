#Trung Nguyen
#15 March 2019
#Command Line NoDictionary Latin Parser

import bs4
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup

#downloads html of webpage
my_url = input("Enter url from NoDictionaries.com: ")
uClient = uReq(my_url) 
page_html = uClient.read()
uClient.close()

#file I/O
file_name = input("Enter document name: ")
filename = file_name + ".docx"
f = open(filename, "w")

#html parser
page_soup = soup(page_html, "html.parser")

#grabs the title
title = page_soup.h1.text.split()
title_str = ' '.join(title[2:])
print("\n" + title_str)
f.write(title_str + "\n")

#grabs each line of latin
latin = page_soup.findAll("div",{"class":"subpassage-line-text"})

#grabs each term/word
terms = page_soup.findAll("span", {"class":"gloss"})


word_count = 0
#iterates through every line of latin and translated english word
for line in latin:
    text = line.text
    text_array = text.split()
    text_array_sub = text_array[-2:] #stores last two words
    last_words = [word[:2].lower() for word in text_array_sub] #stores first two letters of last words
    
    print(text + "\n\n")
    f.write("\n" + text + "\n\n")

    verify_counter = 0 #keeps count of the last two words
    counter = 0 #keeps track of each word
    while(True):        
            verify_bool = False    

            #exception handling if at end of vocabulary list
            try:
                word = terms[word_count].i.text

            except IndexError:
                break
            
            except AttributeError:
                word_count += 1
                continue


            word_array = word.split(',')
            #only verify last two words and number of words greater than the length of the list - 2
            if (word_array[0][0:2] in last_words) and (counter >= (len(text_array) - 2)):
                #considers if word has finally reached the last word in line
                if(word_array[0][0:2] in last_words[1]):
                    verify_counter += 1
                    verify_bool = True

            #if the last word of the line was passed, break
            if (not verify_bool) and (verify_counter > 0):
                break

            definition = terms[word_count].findAll("span",{"class":"english"})[0].text

            print(word + ":" + definition)
            f.write(word + ": " + definition + "\n")
            word_count += 1
            counter += 1

    print("\n")

print("The Word Document has been placed in the same directory as the program!")
