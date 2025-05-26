import pyttsx3
import PyPDF2
from tkinter.filedialog import askopenfilename
import time

book = askopenfilename()
pdfreader = PyPDF2.PdfReader(book)
pages = len(pdfreader.pages)

# Ask user for page(s) to read
page_input = input(f"Enter a page number or range (e.g., 5 or 3-7), or press Enter to read all {pages} pages: ").strip()

if page_input == "":
    pages_to_read = range(pages)  # read all pages
elif "-" in page_input:
    start, end = page_input.split("-")
    start = int(start) - 1
    end = int(end)
    pages_to_read = range(start, end)
else:
    page = int(page_input) - 1
    pages_to_read = [page]

speaker = pyttsx3.init()

# Slow down speech rate a bit for clarity
rate = speaker.getProperty('rate')
speaker.setProperty('rate', rate - 25)

speaker.setProperty('volume', 0.9)  # slightly quieter

# Choose voice (usually 0=male, 1=female on Windows)
voices = speaker.getProperty('voices')
speaker.setProperty('voice', voices[1].id)

for num in pages_to_read:
    if num < 0 or num >= pages:
        print(f"Page {num + 1} is out of range, skipping.")
        continue

    page = pdfreader.pages[num]
    text = page.extract_text()

    if text:
        print(f"Now reading: Page {num + 1}/{pages}")
        speaker.say(text)
        speaker.runAndWait()
        time.sleep(1)  # 1 second pause between pages
    else:
        print(f"Page {num + 1} has no text, skipping.")
