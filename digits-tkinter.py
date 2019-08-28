import tkinter as tk
from PIL import ImageTk, Image, ImageOps, ImageEnhance
import os
from tkinter import filedialog, font
import keras
import numpy as np

height = 500
width = 600

model = keras.models.load_model('my_model.h5')

def uploadAction(event=None):
	filename = filedialog.askopenfilename()

	img = Image.open(filename)

	img_obrazek = img.resize((280,280),Image.ANTIALIAS)
	
	img_obliczenia = img.resize((28,28),Image.ANTIALIAS)
	img_obliczenia = ImageOps.grayscale(img_obliczenia)
	img_obliczenia = ImageEnhance.Brightness(img_obliczenia).enhance(1.3)
	img_obliczenia = ImageEnhance.Contrast(img_obliczenia).enhance(5)
	img_obliczenia = ImageOps.invert(img_obliczenia)

	pixels = list(img_obliczenia.getdata())
	width, height = img_obliczenia.size
	pixels = [pixels[i * width:(i+1)*width] for i in range(height)]

	df = np.stack(pixels, axis=0)
	df = df.reshape(-1,28,28,1)

	prediction = model.predict(df)
	prediction = np.argmax(prediction, axis=1)

	cyfra = tk.Label(canvas, text = prediction[0],font=myFont)
	cyfra.place(anchor = 'ne', relx=97/100,rely=6/25,height = 280, width = 280)

	img_obrazek = ImageTk.PhotoImage(img_obrazek)

	obrazek = tk.Label(canvas, image = img_obrazek)
	obrazek.image = img_obrazek
	obrazek.place(relx=3/100, rely=6/25)
	

root = tk.Tk()

myFont = font.Font(family = "Times New Roman", size = 80)

canvas = tk.Canvas(root, height = height, width = width)
canvas.pack()

button = tk.Button(canvas,text='Upload a file',bg='#a1bcc9', command = uploadAction)
button.place(anchor='n', relx=0.5,rely=2/25,relwidth=2/15, relheight=2/25)

root.mainloop()
