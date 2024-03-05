import nltk
import requests
from bs4 import BeautifulSoup
import os
import numpy as np
import cv2
import pyautogui
from PIL import Image
from pytesseract import pytesseract
from random import choice
import pyttsx3

def speech(words):
	engine = pyttsx3.init()

	engine.setProperty("voice", "com.apple.speech.syntheis.voice.samantha")
	engine.setProperty("rate", 180)

	engine.say(words)
	engine.runAndWait()

path_to_tesseract = r"D:\Tesseract\tesseract.exe"
image_path = r"D:\Python\Text To Image\image.png"

img = Image.open(image_path)

pytesseract.tesseract_cmd = path_to_tesseract

text = pytesseract.image_to_string(img)
text = text.replace("\n", "")

sentences = text.split(". ")[:-1]

for sentence in sentences:
    tokens = nltk.word_tokenize(sentence)
    tagged = nltk.pos_tag(tokens)

    tags = ["NNP", "VBZ", "VB", "NNS"]
    key_words = ""

    for tag in tagged:
        if tag[1] in tags:
            key_words += tag[0] + " "

    key_words = key_words[:-1]

    url = "https://www.google.com/search?q=%s&source=lnms&tbm=isch" % (key_words)
    response = requests.get(url)

    soup = BeautifulSoup(response.content, "html.parser")

    image_tags = soup.find_all("img")

    try:
        image_url = [img["src"] for img in image_tags][1]

        directory = "D:\Codes\Python\Text To Image"
        if not os.path.exists(directory):
            os.makedirs(directory)

        response = requests.get(image_url)
        with open(os.path.join(directory, "pic.png"), "wb") as f:
            f.write(response.content)

        img = cv2.imread("D:\Codes\Python\Text To Image\pic.png")
        img = cv2.resize(img, (800, 800))
        cv2.imshow("Image", img)

        cv2.waitKey(1)
        speech(sentence)
        cv2.destroyAllWindows()
    except:
        pass