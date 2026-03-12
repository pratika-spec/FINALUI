import json
from pdf2image import convert_from_path
import pytesseract
import re
import requests
import openai

openai.api_key = "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"
pytesseract.pytesseract.tesseract_cmd = 'C://Program Files//Tesseract-OCR//tesseract.exe'

# Function to convert PDF to Images (same as before)
def convert_pdf_to_img(pdf_file):
    images = convert_from_path(pdf_file, poppler_path=r'C://Users//Laptop//Downloads//Release-23.07.0-0 (2)//poppler-23.07.0//Library//bin')
    return images

# Function to extract text from an Image (same as before)
def extract_text_from_image(image):
    text = pytesseract.image_to_string(image)
    return text

# Function to get text from all pages of a PDF (same as before)
def get_text_from_any_pdf(pdf_file):
    images = convert_pdf_to_img(pdf_file)
    final_text = ""
    for pg, img in enumerate(images):
        final_text += extract_text_from_image(img)
    return final_text

# Function to ask questions and get answers from the chatbot API
def get_completion(prompt, model="gpt-4o"):
  messages = [{"role": "user", "content": prompt}]
  response = openai.ChatCompletion.create(
     model=model,
     messages=messages,
    
     temperature=0.7,
#      temperature=0, # this is the degree of randomness of the model's output
  )
  return response.choices[0].message["content"]
pdf=input("Enter a pdf name =")
pdf1=pdf.strip()
data = get_text_from_any_pdf(pdf1+'.pdf')
input_text = f"""
        YOUR TASK IS TO  translate this text from German to English language and
        if data is in table format then answer must be in table format 
        
        Context: {data}
       

        Answer: 
        """
response = get_completion(input_text)
with open("a_Language_Converted.txt", "w") as f:
    f.write(response)
# print("Chatbot=======================================", response)
# # print(data)

# while True:
#     user_input = input("User==========================================: ")
#     response1 = []

#     input_text = f"""
        
        
#         Context: {data}
#         Question: {user_input}

#         Answer: 
#         """

#     response = generate_response(input_text)
#     print("Chatbot=======================================", response)
