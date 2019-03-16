#Trung Nguyen
#16 March 2019
#GUI NoDictionary Latin Parser

import gi
from gi.repository import Gtk
import bs4
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup

class MainWindow(Gtk.Window):
    def __init__(self):
        Gtk.Widget.__init__(self)
        Gtk.Window.__init__(self, title="Nihil Dictum")
        self.set_border_width(10)
        self.set_size_request(550,100)

        # Layout
        Vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        self.add(Vbox)

        # Title
        self.title = Gtk.Label("Project Nihil Dictum")
        Vbox.pack_start(self.title, True, True, 0)

        # Url
        self.url = Gtk.Entry()
        self.url.set_text("Url from nodictinaries.com i.e. http://nodictionaries.com/vergil/aeneid-1/1-7")
        Vbox.pack_start(self.url, True, True, 0)

        # Document
        self.doc = Gtk.Entry()
        self.doc.set_text("File Name to be saved as .docx i.e. Met.1.1-4")
        Vbox.pack_start(self.doc, True, True, 0)

        # Parse Button
        self.button = Gtk.Button(label="Parse")
        self.button.connect("clicked", self.success_dialog)
        Vbox.pack_start(self.button, True, True, 0)

        # Exit Button
        self.exit = Gtk.Button(label="Exit")
        self.exit.connect("clicked", Gtk.main_quit)
        Vbox.pack_start(self.exit, True, True, 0)

    #Dialog to confirm successful parse
    def success_dialog(self, widget):
        self.parse(self)
        success = Gtk.MessageDialog(self, 0, Gtk.MessageType.INFO, Gtk.ButtonsType.OK, "Success")
        success.format_secondary_text("File has been stored in the same directory as the program.")
        success.run()
        success.destroy()

    #Dialog to inform user to erroneous url
    def url_error_dialog(self, widget):
        error = Gtk.MessageDialog(self, 0, Gtk.MessageType.ERROR, Gtk.ButtonsType.CANCEL, "Url Error")
        error.format_secondary_text("There is an error with the url entered.")
        error.run()
        error.destroy()

    #Dialog to inform user to erroneous file name
    def doc_error_dialog(self, widget):
        error = Gtk.MessageDialog(self, 0, Gtk.MessageType.ERROR, Gtk.ButtonsType.CANCEL, "File Name Error")
        error.format_secondary_text("File name cannot contain:   /, \, ?, %, *, :, |, \", <, >, .")
        error.run()
        error.destroy()

    #Algorithm to parse through NoDictionaries' Latin literature
    def parse(self, widget):
        my_url = self.url.get_text()
        try:
            uClient = uReq(my_url)
        except:
            self.url_error_dialog(self)

        page_html = uClient.read()
        uClient.close()

        #file I/O
        filename = self.doc.get_text() + ".docx"
        try:
            f = open(filename, "w")
        except:
            self.doc_error_dialog(self)

        #html parser
        page_soup = soup(page_html, "html.parser")

        #grabs the title
        title = page_soup.h1.text.split()
        title_str = ' '.join(title[2:])
        # print("\n" + title_str)
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

            f.write("\n" + text + "\n\n")

            verify_counter = 0 #keeps count of the last two words
            counter = 0 #keeps track of each word

            #iterates through every word in line (IMPERFECT)
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

                    f.write(word + ": " + definition + "\n")
                    word_count += 1
                    counter += 1

window = MainWindow()
window.connect("delete-event", Gtk.main_quit)
window.show_all()
Gtk.main()
