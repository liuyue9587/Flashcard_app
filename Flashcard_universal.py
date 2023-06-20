import tkinter as tk
from tkinter import messagebox, ttk
import random
import json
import os
from gtts import gTTS
import tempfile
import pygame

if not os.path.exists('words.json'):
    with open('words.json', 'w') as f:
        json.dump({'english': [], 'chinese': []}, f)

class FlashCard:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title('Flash Card')

        try:
            with open('words.json', 'r') as f:
                data = json.load(f)
            self.english_words = data['english']
            self.chinese_words = data['chinese']
        except (FileNotFoundError, json.JSONDecodeError, KeyError):
            self.english_words = ["apple", "book", "car"]
            self.chinese_words = ["苹果", "书", "车"]

        self.current_word = None

        # Create three frames
        self.frame1 = tk.Frame(self.window, bd=2, relief='solid')
        self.frame2 = tk.Frame(self.window, bd=2, relief='solid')
        self.frame3 = tk.Frame(self.window, bd=2, relief='solid')
        self.frame4 = tk.Frame(self.window, bd=2, relief='solid')


        
        
        ###
        self.frame1.grid_rowconfigure(0, weight=1)
        self.frame1.grid_rowconfigure(1, weight=1)
        self.frame1.grid_columnconfigure(0, weight=1)
        ###
        
        
        self.frame1.grid(row=0, column=0, padx=10, pady=10, sticky='nswe', rowspan=4)
        self.frame2.grid(row=0, column=1, padx=10, pady=10, sticky='nswe', rowspan=2)
        self.frame3.grid(row=2, column=1, padx=10, pady=10, sticky='nswe', rowspan=2)
        self.frame4.grid(row=0, column=2, padx=10, pady=10, sticky='nswe', rowspan=4)


        # Section labels
        self.label1 = tk.Label(self.frame1, text="Section 1: Show a random Words\n(Randomly choose a word from your word list)")
        self.label2 = tk.Label(self.frame2, text="Section 2: Add Words\n(Add a word into your word list)")
        self.label3 = tk.Label(self.frame3, text="Section 3: List Words\n(Open your word list)")
        self.label4 = tk.Label(self.frame4, text="Section 4: Usage")
        self.label1.pack(anchor='center')
        self.label2.pack(anchor='center')
        self.label3.pack(anchor='center')
        
        self.label0 = tk.Label(self.frame3, text="\n\n\n")
        self.label0.pack()
        
        self.label4.pack()

        self.label1 = tk.Label(self.frame4, text="-----------------------------------------------\nReading Comprehension Practice\nPress 'Pick a sample from target language(text)'\nA random word from the list will appear\nRecall its meaning, if you don't remember, click on reveal for a hint\n-----------------------------------------------")
        self.label1.pack()

        self.label2 = tk.Label(self.frame4, text="Listening Comprehension Practice\nPress 'Pick a sample from target language(vocal)'\nA random word audio from the list will play\nIf you don't know, click on reveal\n-----------------------------------------------")
        self.label2.pack()

        self.label3 = tk.Label(self.frame4, text="Oral Expression Practice\nPress 'Pick a word from your own language'\nA random word from your own language in the list will appear\nRecall its expression in the your target language\n-----------------------------------------------")
        self.label3.pack()

        self.label4 = tk.Label(self.frame4, text="Spelling Practice\nPress 'Pick a word from your own language' (for writing practice)\nor 'Pick a sample from target language(vocal)(vocal)' (for listening and writing practice)\nAfter inputting the spelling of the word in the 'Spell the word' bar\nPress reveal to check\n-----------------------------------------------")
        self.label4.pack()

        self.label5 = tk.Label(self.frame4, text="Basic Usage Procedure\n1. Use section.2 to add words to your dictionary\n2. Practice using the four methods above\n-----------------------------------------------\nUse the list words in section.3\nYou can quickly review the word list\n-----------------------------------------------\n\nPlease contact us if you have any questions")
        self.label5.pack()

        
        self.text1 = tk.Text(self.frame4, height=1, width=25)
        self.text1.insert(tk.END, "tenri.coding@gmail.com")
        self.text1.configure(state="disabled")
        self.text1.pack()
        
        self.label6 = tk.Label(self.frame4, text="Good luck with your studies!")
        self.label6.pack()

        # label4
        # self.label4 = tk.Label(self.frame4, text="\n\n\n\n\n\n")
        # self.label4.pack()
        # self.label4.configure(padx=10, pady=10, font=('Arial', 12))
        
        # self.image_label.pack(padx=10, pady=10)

        # 或者添加图片
        # self.image = tk.PhotoImage(file="path/to/image.png")
        # self.image_label = tk.Label(self.frame4, image=self.image)
        # self.image_label.pack()

        # Rest of your code modified to place widgets in the right frames
        self.word_label = tk.Label(self.frame1, text="", font=('Arial', 18))
        self.word_label.configure(wraplength=170,height=8)
        self.word_label.pack(padx=20, pady=20)

        self.reveal_button = tk.Button(self.frame1, text="Reveal", command=self.reveal_word)
        self.reveal_button.pack(padx=20, pady=20)
        
        # spelling check
        self.spelling_entry = tk.Entry(self.frame1)
        self.spelling_entry.pack(padx=20, pady=20)
        # spell the word
        self.spelling_entry.insert(tk.END, "Spell the word")
        self.spelling_entry.configure(fg='gray', font=('Arial', 10, 'italic'))

        def on_spelling_entry_click(event):
            if self.spelling_entry.get() == "Spell the word":
                self.spelling_entry.delete(0, tk.END)
                self.spelling_entry.configure(fg='black', font=('Arial', 10, 'normal'))

        def on_spelling_entry_focusout(event):
            if self.spelling_entry.get() == "":
                self.spelling_entry.insert(tk.END, "Spell the word")
                self.spelling_entry.configure(fg='gray', font=('Arial', 10, 'italic'))

        self.spelling_entry.bind("<FocusIn>", on_spelling_entry_click)
        self.spelling_entry.bind("<FocusOut>", on_spelling_entry_focusout)

        self.english_sample_button = tk.Button(self.frame1, text="Pick a sample from target language(text)", command=lambda: self.pick_sample('en'))
        self.english_sample_button.pack(padx=20, pady=20)
        
        # vocal part
        self.english_sample_vocal_button = tk.Button(self.frame1, text="Pick a sample from target language(vocal)", command=self.pick_sample_vocal)
        self.english_sample_vocal_button.pack(padx=20, pady=20)  # position changed here

        self.chinese_sample_button = tk.Button(self.frame1, text="Pick a word from your own language", command=lambda: self.pick_sample('ch'))
        self.chinese_sample_button.pack(padx=20, pady=20)

        self.new_word_entry = tk.Entry(self.frame2)
        self.new_word_entry.pack(padx=20, pady=20)

        self.new_word_translation_entry = tk.Entry(self.frame2)
        self.new_word_translation_entry.pack(padx=20, pady=20)
        # gray
        self.new_word_entry.insert(tk.END, "word in target language")
        self.new_word_entry.configure(fg='gray', font=('Arial', 10, 'italic'))

        self.new_word_translation_entry.insert(tk.END, "word in your own language")
        self.new_word_translation_entry.configure(fg='gray', font=('Arial', 10, 'italic'))

        def on_new_word_entry_click(event):
            if self.new_word_entry.get() == "word in target language":
                self.new_word_entry.delete(0, tk.END)
                self.new_word_entry.configure(fg='black', font=('Arial', 10, 'normal'))

        def on_new_word_entry_focusout(event):
            if self.new_word_entry.get() == "":
                self.new_word_entry.insert(tk.END, "word in target language")
                self.new_word_entry.configure(fg='gray', font=('Arial', 10, 'italic'))

        def on_new_word_translation_entry_click(event):
            if self.new_word_translation_entry.get() == "word in your own language":
                self.new_word_translation_entry.delete(0, tk.END)
                self.new_word_translation_entry.configure(fg='black', font=('Arial', 10, 'normal'))

        def on_new_word_translation_entry_focusout(event):
            if self.new_word_translation_entry.get() == "":
                self.new_word_translation_entry.insert(tk.END, "word in your own language")
                self.new_word_translation_entry.configure(fg='gray', font=('Arial', 10, 'italic'))

        self.new_word_entry.bind("<FocusIn>", on_new_word_entry_click)
        self.new_word_entry.bind("<FocusOut>", on_new_word_entry_focusout)
        self.new_word_translation_entry.bind("<FocusIn>", on_new_word_translation_entry_click)
        self.new_word_translation_entry.bind("<FocusOut>", on_new_word_translation_entry_focusout)


        self.add_word_button = tk.Button(self.frame2, text="Add word", command=self.add_word)
        self.add_word_button.pack(padx=20, pady=20)

        self.list_words_button = tk.Button(self.frame3, text="List words", command=self.list_words)
        self.list_words_button.pack(padx=20, pady=20)
        

        # Set the minimum size of the window
        self.window.minsize(450, 450)  # Set this to whatever size you want

        # Get screen width and height
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()

        # Calculate position for centering the window
        x = (screen_width / 2) - (500 / 2)  # Assuming the window is 500px wide
        y = (screen_height / 2) - (500 / 2)  # Assuming the window is 500px high

        self.window.geometry("+%d+%d" % (x, y))
        
        pygame.mixer.init()



    def run(self):
        self.window.mainloop()

    def pick_sample(self, language):
        if language == 'en':
            idx = random.randint(0, len(self.english_words) - 1)
            self.current_word = (self.english_words[idx], self.chinese_words[idx])
            self.word_label.config(text=self.current_word[0])
        elif language == 'ch':
            idx = random.randint(0, len(self.chinese_words) - 1)
            self.current_word = (self.english_words[idx], self.chinese_words[idx])
            self.word_label.config(text=self.current_word[1])
        self.reveal_button.config(state="normal")
        
        self.spelling_entry.delete(0, 'end')  # Clear the spelling entry

    def reveal_word(self):
        if self.current_word is not None:
            user_spelling = self.spelling_entry.get()
            tts = gTTS(text=self.current_word[0], lang='en')
            if user_spelling:  # If the user has entered something in the spelling entry
                if user_spelling.lower() == self.current_word[0].lower():  # If the user spelling matches the current word
                    self.word_label.config(text=f'{self.current_word[0]} \n {self.current_word[1]} \nYour spelling\n"{user_spelling}"\nwas correct')
                    with tempfile.NamedTemporaryFile(delete=True) as fp:
                        tts.save(f"{fp.name}.mp3")
                        pygame.mixer.music.load(f"{fp.name}.mp3")
                        pygame.mixer.music.play()
                else:
                    self.word_label.config(text=f'{self.current_word[0]} \n {self.current_word[1]} \nYour spelling\n"{user_spelling}"\nwas incorrect')
                    with tempfile.NamedTemporaryFile(delete=True) as fp:
                        tts.save(f"{fp.name}.mp3")
                        pygame.mixer.music.load(f"{fp.name}.mp3")
                        pygame.mixer.music.play()
            else:  # If the user has not entered anything in the spelling entry
                self.word_label.config(text=f'{self.current_word[0]} \n {self.current_word[1]}')
                with tempfile.NamedTemporaryFile(delete=True) as fp:
                        tts.save(f"{fp.name}.mp3")
                        pygame.mixer.music.load(f"{fp.name}.mp3")
                        pygame.mixer.music.play()
            self.spelling_entry.delete(0, 'end')  # Clear the spelling entry after revealing the answer
    # def reveal_word(self):
    #     if self.current_word is not None:
    #         user_spelling = self.spelling_entry.get()
    #         if user_spelling:  # If the user has entered something in the spelling entry
    #             if user_spelling.lower() == self.current_word[0].lower():  # If the user spelling matches the current word
    #                 self.word_label.config(text=f'{self.current_word[0]} \n {self.current_word[1]} \nYour spelling\n"{user_spelling}"\nwas correct')
    #                 speak_text(self.current_word[0])
    #             else:
    #                 self.word_label.config(text=f'{self.current_word[0]} \n {self.current_word[1]} \nYour spelling\n"{user_spelling}"\nwas incorrect')
    #                 speak_text(self.current_word[0])
    #         else:  # If the user has not entered anything in the spelling entry
    #             self.word_label.config(text=f'{self.current_word[0]} \n {self.current_word[1]}')
    #             speak_text(self.current_word[0])
    #         self.spelling_entry.delete(0, 'end')  # Clear the spelling entry after revealing the answer


    def add_word(self):
        new_word = self.new_word_entry.get()
        new_word_translation = self.new_word_translation_entry.get()

        if not new_word or not new_word_translation:
            messagebox.showerror("Error", "Please input both languages")
            return

        if new_word in self.english_words:
            idx = self.english_words.index(new_word)
            existing_word_translation = self.chinese_words[idx]
            messagebox.showinfo("Word already exists", f"The word '{new_word}' already exists with translation \n'{existing_word_translation}'.")
            return

        self.english_words.append(new_word)
        self.chinese_words.append(new_word_translation)

        with open('words.json', 'w') as f:
            json.dump({'english': self.english_words, 'chinese': self.chinese_words}, f)

        self.new_word_entry.delete(0, 'end')
        self.new_word_translation_entry.delete(0, 'end')

        messagebox.showinfo("Success", "New word added successfully")

    def list_words(self):
        ListWordsWindow(self)
        
    def pick_sample_vocal(self):
        idx = random.randint(0, len(self.english_words) - 1)
        self.current_word = (self.english_words[idx], self.chinese_words[idx])
        tts = gTTS(text=self.current_word[0], lang='en')
        with tempfile.NamedTemporaryFile(delete=True) as fp:
            tts.save(f"{fp.name}.mp3")
            pygame.mixer.music.load(f"{fp.name}.mp3")
            pygame.mixer.music.play()
    # def pick_sample_vocal(self):
    #     idx = random.randint(0, len(self.english_words) - 1)
    #     self.current_word = (self.english_words[idx], self.chinese_words[idx])
    #     speak_text(self.current_word[0])


class ListWordsWindow:
    def __init__(self, app):
        self.app = app
        self.window = tk.Toplevel(self.app.window)
        self.window.title('Word List')

        self.treeview = ttk.Treeview(self.window, columns=('target language', 'your own language'), show='headings', height=30)  # Double the height
        self.treeview.column('target language', width=150)
        self.treeview.column('your own language', width=150)
        self.treeview.heading('target language', text='target language')
        self.treeview.heading('your own language', text='your own language')

        self.treeview.bind('<Double-1>', self.modify_word)

        for i in range(len(self.app.english_words)):
            self.treeview.insert('', 'end', values=(self.app.english_words[i], self.app.chinese_words[i]))

        self.treeview.grid(row=0, column=0, columnspan=3, padx=20, pady=20)  # changed pack() to grid()

        # list_num
        self.count_label = tk.Label(self.window, text=f'Total words: {len(self.app.english_words)}')
        self.count_label.grid(row=1, column=0, columnspan=3, padx=20, pady=20)  # changed pack() to grid()

        # search
        self.search_entry = tk.Entry(self.window)
        self.search_entry.grid(row=2, column=0, padx=20, pady=20)  # changed pack() to grid()

        self.search_button = tk.Button(self.window, text='Search', command=self.search_word)
        self.search_button.grid(row=2, column=1, padx=20, pady=20)  # changed pack() to grid()

        # randomize_list
        self.randomize_button = tk.Button(self.window, text='Randomize', command=self.randomize)
        self.randomize_button.grid(row=3, column=0, padx=20, pady=20)  # changed pack() to grid()

        self.delete_button = tk.Button(self.window, text='Delete', command=self.delete_word)
        self.delete_button.grid(row=3, column=1, padx=20, pady=20)  # changed pack() to grid()
        
        # Add cover buttons
        self.cover_english_button = tk.Button(self.window, text='Cover target word list', command=self.cover_english)
        self.cover_english_button.grid(row=4, column=0, padx=20, pady=20)  # changed pack() to grid()

        self.cover_chinese_button = tk.Button(self.window, text='Cover your own word list', command=self.cover_chinese)
        self.cover_chinese_button.grid(row=4, column=1, padx=20, pady=20)  # changed pack() to grid()
        self.is_english_covered = False
        self.is_chinese_covered = False




    # Add delete_word method here
    def delete_word(self):
        item_id = self.treeview.selection()[0]
        english, _ = self.treeview.item(item_id, 'values')

        idx = self.app.english_words.index(english)

        del self.app.english_words[idx]
        del self.app.chinese_words[idx]

        with open('words.json', 'w') as f:
            json.dump({'english': self.app.english_words, 'chinese': self.app.chinese_words}, f)

        self.treeview.delete(item_id)  # Delete the row from the treeview

        self.count_label.config(text=f'Total words: {len(self.app.english_words)}')  # Update the word count
        messagebox.showinfo("Success", "Word deleted successfully")

    
    def randomize(self):
        combined = list(zip(self.app.english_words, self.app.chinese_words))  
        random.shuffle(combined)  
        self.app.english_words, self.app.chinese_words = zip(*combined)  

        for i in self.treeview.get_children():
            self.treeview.delete(i)

        if self.is_english_covered:
            for chinese in self.app.chinese_words:
                self.treeview.insert('', 'end', values=("", chinese))
        elif self.is_chinese_covered:
            for english in self.app.english_words:
                self.treeview.insert('', 'end', values=(english, ""))
        else:
            for english, chinese in zip(self.app.english_words, self.app.chinese_words):
                self.treeview.insert('', 'end', values=(english, chinese))
        
        


    def modify_word(self, event):
        item_id = self.treeview.selection()[0]
        english, chinese = self.treeview.item(item_id, 'values')
        ModifyWordWindow(self, english, chinese)
        
    def search_word(self):
        search_word = self.search_entry.get()
        for item_id in self.treeview.get_children():
            english, _ = self.treeview.item(item_id, 'values')
            if english == search_word:
                self.treeview.selection_set(item_id)
                self.treeview.focus(item_id)
                self.treeview.see(item_id)  # 这会自动滚动到选定的项
                return
        messagebox.showinfo("Search result", "Word not found")
        
    def cover_english(self):
        if not self.is_english_covered:
            if self.is_chinese_covered:
                self.cover_chinese()  # 取消 "Cover Chinese" 的效果
            for i in self.treeview.get_children():
                self.treeview.delete(i)
            for chinese in self.app.chinese_words:
                self.treeview.insert('', 'end', values=("", chinese))
            self.is_english_covered = True
        else:
            for i in self.treeview.get_children():
                self.treeview.delete(i)
            for english, chinese in zip(self.app.english_words, self.app.chinese_words):
                self.treeview.insert('', 'end', values=(english, chinese))
            self.is_english_covered = False


    def cover_chinese(self):
        if not self.is_chinese_covered:
            if self.is_english_covered:
                self.cover_english()  # 取消 "Cover English" 的效果
            for i in self.treeview.get_children():
                self.treeview.delete(i)
            for english in self.app.english_words:
                self.treeview.insert('', 'end', values=(english, ""))
            self.is_chinese_covered = True
        else:
            for i in self.treeview.get_children():
                self.treeview.delete(i)
            for english, chinese in zip(self.app.english_words, self.app.chinese_words):
                self.treeview.insert('', 'end', values=(english, chinese))
            self.is_chinese_covered = False




class ModifyWordWindow:
    def __init__(self, parent, english, chinese):
        self.parent = parent
        self.window = tk.Toplevel(self.parent.window)
        self.window.title('Modify Word')

        tk.Label(self.window, text='English:').grid(row=0, column=0, padx=20, pady=20)
        tk.Label(self.window, text='Chinese:').grid(row=1, column=0, padx=20, pady=20)

        self.english_entry = tk.Entry(self.window)
        self.english_entry.insert(0, english)
        self.english_entry.grid(row=0, column=1, padx=20, pady=20)

        self.chinese_entry = tk.Entry(self.window)
        self.chinese_entry.insert(0, chinese)
        self.chinese_entry.grid(row=1, column=1, padx=20, pady=20)

        tk.Button(self.window, text='Save', command=self.save_word).grid(row=2, column=0, columnspan=2, padx=20, pady=20)

    def save_word(self):
        old_english, old_chinese = self.english_entry.get(), self.chinese_entry.get()
        new_english, new_chinese = self.english_entry.get(), self.chinese_entry.get()

        idx = self.parent.app.english_words.index(old_english)

        self.parent.app.english_words[idx] = new_english
        self.parent.app.chinese_words[idx] = new_chinese

        with open('words.json', 'w') as f:
            json.dump({'english': self.parent.app.english_words, 'chinese': self.parent.app.chinese_words}, f)

        for i in self.parent.treeview.get_children():
            self.parent.treeview.delete(i)

        for i in range(len(self.parent.app.english_words)):
            self.parent.treeview.insert('', 'end', values=(self.parent.app.english_words[i], self.parent.app.chinese_words[i]))
            
        self.parent.count_label.config(text=f'Total words: {len(self.parent.app.english_words)}')
        self.window.destroy()

if __name__ == "__main__":
    app = FlashCard()
    app.run()


# 看，听，说，写(拼)
# 手机上使用时选中单词可以有一个添加到list的选项，且会自动补全中文释义
# spelling part not finish yet.