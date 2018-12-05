from tkinter import *
import tkinter
from tkinter.scrolledtext import ScrolledText

LABELS_DICT = {0: "1st options", 1: "2nd options", 2: "3rd options"}
class GUIInterface:
    def __init__(self):
        self.value = 0

    def add_text(self,message):
        message += " "
        self.scrolling_window.insert(END,message)

    def get_text(self, event):
        whole_text = self.scrolling_window.get(1.0,END)
        whole_text = whole_text.strip()
        word_wise = whole_text.split(" ")
        last_four = word_wise[-4:]
        print(whole_text)
        print(last_four)

    def handleGUI(self):
        main_window = Tk()
        # Creating scrolling window and adding callback
        self.scrolling_window = ScrolledText(main_window, width=100, height=20)
        self.scrolling_window.pack()
        main_window.wm_title("Categorized text predicter")
        #main_window.bind_all("<space>", lambda scrolling_window=scrolling_window: print_words(scrolling_window))
        main_window.bind_all("<space>", self.get_text)

        # Creating frames to keep buttons for suggestions
        options_frame = []
        messages = ["example", "example example", "example example example", "example example example example","example example example example example"]
        labels = []
        for j in range(0,3):
            options_frame.append(Frame(main_window))
            options_frame[j].pack()
            options =[]
            label = Label(options_frame[j], text=LABELS_DICT[j])
            label.pack()
            for i in range(0,5):
                options.append(tkinter.Button( options_frame[j], text = messages[i], command = lambda i=i: self.add_text(messages[i])))
                options[i].pack(side = LEFT)

        main_window.mainloop()


# For testing purposes
if __name__ == '__main__':
    g = GUIInterface()
    g.handleGUI()
