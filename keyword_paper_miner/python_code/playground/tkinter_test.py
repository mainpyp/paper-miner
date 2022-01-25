import keyword_paper_miner.python_code.backend.scholar_scraper as mst
import webbrowser
from PIL import ImageTk
from PIL import Image as IMG
from tkinter import *


root = Tk()
root.title("Keyword paper miner")
root.configure(background="lightgrey")


def change_label():
    key_word = key_word_field.get()
    if key_word == "Please enter a keyword":
        message = f"You did not enter a keyword"
        keyword_label.configure(text=message, bg="#910611", fg="#c2bebe")
    else:
        message = f"Keyword: {key_word}"
        keyword_label.configure(text=message, bg="#910611", fg="#c2bebe")


def get_paper():
    content = key_word_field.get()
    print(f"content: {content}")
    if content in ["", "Please enter a keyword", "Keyword: "]:
        key_word_field.configure(text="Please enter a keyword")
    else:
        fetched_papers = mst.search_for_papers([content], int(var_amount.get()))
        if len(fetched_papers) == 0:
            paper_label.configure(text=f"No suiting paper was found for {content}")
            return
        total_information = ""
        for interesting_paper in fetched_papers[content]:
            main_author = interesting_paper.bib['author'][0]
            if len(interesting_paper.bib['author']) > 1:
                second_author = interesting_paper.bib['author'][1]
                paper_information = f"Paper title: {interesting_paper.bib['title']}\n" \
                                    f"Main author: {main_author}\n" \
                                    f"Second author: {second_author}\n" \
                                    f"Citations: {interesting_paper.bib['cites']}"
            else:
                paper_information = f"Paper title: {interesting_paper.bib['title']}\n" \
                                    f"Main author: {main_author}\n" \
                                    f"Citations: {interesting_paper.bib['cites']}"
            total_information += f"\n\n{paper_information}"
        #print(paper_information)
        paper_label.configure(text=total_information)

    if var_url.get() == "yes":
        webbrowser.open(interesting_paper.bib['url'])


# create elements
key_word_field = Entry(root)
key_word_field.insert(INSERT, "Please enter a keyword")
keyword_label = Label(root)
paper_label = Label(root)
submit_keyword_button = Button(root, text="submit keyword", borderwidth=0, command=change_label)
search_paper_button = Button(root, text="search for paper", borderwidth=0, command=get_paper)
specification_label = Label(root, text="Optional specifications:", bg='lightgrey', borderwidth=0)
scrollbar = Scrollbar(root)
# logo
image_logo = IMG.open("../playground/logo/key_paper_miner.png")
image_logo.thumbnail((100, 400))
logo = ImageTk.PhotoImage(image_logo)
logo_panel = Label(root, image=logo)
# dropdown open url
url_label = Label(root, text="Open paper URL")
options = ['no', 'yes']
var_url = StringVar(root)
var_url.set(options[0])
url_dropdown = OptionMenu(root, var_url, *options)
# amount of found papers
amount_label = Label(root, text="Amount of papers")
options_amount = range(1, 7)
var_amount = StringVar(root)
var_amount.set(options_amount[0])
amount_dropdown = OptionMenu(root, var_amount, *options_amount)

# adjust style
key_word_field.configure(background="lightgrey")
keyword_label.configure(background="lightgrey")
paper_label.configure(background="lightgrey")
submit_keyword_button.configure(background="lightgrey")
search_paper_button.configure(background="lightgrey")
specification_label.configure(background="lightgrey")
scrollbar.configure(background="lightgrey")
# logo
logo_panel.configure(background="lightgrey")
# dropdown open url
url_label.configure(background="lightgrey")
url_dropdown.configure(background="lightgrey")
# amount of found papers
amount_label.configure(background="lightgrey")
amount_dropdown.configure(background="lightgrey")


# adds elements to root
keyword_label.grid(row=0, column=0, padx=10, pady=5)
paper_label.grid(row=1, column=0, padx=10, pady=5)
key_word_field.grid(row=2, column=0, padx=10, pady=5)
submit_keyword_button.grid(row=3, column=0, padx=10, pady=5)
search_paper_button.grid(row=4, column=0, padx=10, pady=5)
specification_label.grid(row=5, column=0, padx=10, pady=5)
url_label.grid(row=6, column=1, pady=5)
url_dropdown.grid(row=6, column=0, padx=10, pady=5)
amount_label.grid(row=7, column=1, pady=5)
amount_dropdown.grid(row=7, column=0, padx=10, pady=5)
logo_panel.grid(row=0, column=1, rowspan=5, padx=10)

if __name__ == '__main__':
    root.mainloop()
