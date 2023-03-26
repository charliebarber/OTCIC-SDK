import random as r
import os
import time
import otcic



# word syllable count
SYL_MIN = 1
SYL_MAX = 2 #6

# sentence word count
WORD_MIN = 1 #4
WORD_MAX = 2 #8

# book sentence/line count
LINES_MIN = 2 #40
LINES_MAX = 3 #400

BOOKS_MAX = 32
INTERVAL = 100



vowels = "aeiou"
consonants = "bcdfghjklmnpqrstvwxyz"



def pick_letter(letters: str) -> str:
    return letters[r.randint(0, len(letters) - 1)]

def make_word() -> str:
    return "".join([
        pick_letter(consonants) + pick_letter(vowels)
        for i in range(r.randint(SYL_MIN, SYL_MAX))
        ])

@otcic.ram_trace
def make_sentence(words: list | None = None) -> str:
    if not words:
        words = [make_word() for i in range(r.randint(WORD_MIN, WORD_MAX))]
    return "".join([" ".join(words), ". "])



@otcic.ram_trace
def read_book(name: str) -> list[list[str]]:
    book = []
    with open("books/" + name + ".txt") as file:
        book = [[word for word in line.strip().strip(".\n").split(" ")] for line in file]

    return book

@otcic.ram_trace
def write_book(name: str, book: list[list[str]] = None):
    if not book:
        book_lines = [make_sentence() for i in range(r.randint(LINES_MIN, LINES_MAX))]
    else:
        book_lines = [make_sentence(line) for line in book]
    book_str2 = "".join(book_lines)

    with open("books/" + name + ".txt", "w") as file:
        file.write(book_str2)



books = []

def get_book() -> str:
    return books[r.randint(0, len(books) - 1)]

@otcic.ram_trace
def main():
    if len(books) < BOOKS_MAX:
        for i in range(r.randint(1, BOOKS_MAX - len(books))):
            name = make_word()
            while name in books:
                name = make_word()
            write_book(name)
            books.append(name)
    
    modified_books = []
    for i in range(r.randint(1, len(books))):
        selected = get_book()
        while selected in modified_books:
            selected = get_book()
        modified_books.append(selected)

        book_content = read_book(selected)
        for i in range(len(book_content)):
            line = book_content[i]
            for _ in range(r.randint(1, max(1, int(len(line) // 2)))):
                line[r.randint(0, len(line) - 1)] = make_word()
        
        write_book(selected, book_content)


def startup():
    print("Book Writer Startup")
    filenames = []
    for path, dirs, files in os.walk("/books"):
        filenames = files
        break

    for filename in filenames:
        books.append(filename.strip(".txt"))

    count = 1
    while True:
        print("Book Writer Main Loop:", count)
        main()
        time.sleep(0.1)
        count = (count + 1) % INTERVAL
        if count == 0:
            print("Book Writer Waiting...")
            time.sleep(10)



otcic.setup("book-writer")
startup()