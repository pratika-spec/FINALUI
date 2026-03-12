import pytesseract
from pdf2image import convert_from_path
from pytesseract import image_to_string 
import openai
import json


openai.api_key  = "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"
pytesseract.pytesseract.tesseract_cmd = 'C://Program Files//Tesseract-OCR//tesseract.exe'

def convert_pdf_to_img(pdf_file):
   
    return convert_from_path(pdf_file, poppler_path=r'C://Program Files//poppler-23.07.0//Library//bin')


def convert_image_to_text(file):
   
    
    text = image_to_string(file)
    return text


def get_text_from_any_pdf(pdf_file):
   
    images = convert_pdf_to_img(pdf_file)
    final_text = ""
    for pg, img in enumerate(images):
        
        final_text += convert_image_to_text(img)
        #print("Page n°{}".format(pg))
        #print(convert_image_to_text(img))
    
    return final_text
pdf=input("Enter a pdf name = ")
pdf1=pdf.strip()
ext_text = get_text_from_any_pdf(pdf1+".pdf") 

def get_completion(prompt, model="gpt-3.5-turbo"):
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
     model=model,
     messages=messages,
     temperature=0, # this is the degree of randomness of the model's output
  )
    return response.choices[0].message["content"]


input_text = f""" Your task is to convert the data into json format. 
 Check if the details are related to each other for example someone's details,
                if the data contains any boxes, do create the proper check boxes for someone to tick or untick it.' 
which can inlcude name, date of birth, age, gender, weight, height etc then those should be included as a sub dict
Entire json format should be editable as this is a pdf editable form.
        
        
        Context: {ext_text}
      

       
       """
response = get_completion(input_text)
with open(pdf1+"_output.json", "w") as f:
    f.write(response)
# print(response)
