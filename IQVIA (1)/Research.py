import openai
import PyPDF2
import os
import pandas as pd
import time


openai.api_key  = "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"
def get_completion(prompt, model="gpt-3.5-turbo-16k"):
  messages = [{"role": "user", "content": prompt}]
  response = openai.ChatCompletion.create(
     model=model,
     messages=messages,
    
     temperature=0.7,
#      temperature=0, # this is the degree of randomness of the model's output
  )
  return response.choices[0].message["content"]

pdfFileObject = open('operationen-prozeduren-5231401217014-pages-4.pdf', 'rb')
# creating a pdf reader object
pdfReader = PyPDF2.PdfReader(pdfFileObject)
text=[]
summary=' '

for i in range(0,len(pdfReader.pages)):
  # creating a page object
  pageObj = pdfReader.pages[i].extract_text()
  # pageObj= pageObj.replace('\t\r','')
  # pageObj= pageObj.replace('\xa0','')
  # extracting text from page
  

  input_text = f"""
        YOUR TASK IS TO  translate this text from German to English language and
        if data is in table format then answer must be in table format
        
        Context: {pageObj}
       

        Answer: 
        """

  response = get_completion(input_text)
  with open("Language1_Converted.txt", "a") as f:
    f.write(response)
    
# for i in range(len(text)):











# while True:
#     que=input("Ask a question...")
#     prompt =f"""Provide two solutions for this question having the same context   

#                 question:```{que}```
#                 document: ```{text}```
#                 """""
#     # Question and answer
#     # should be in json format like if user ask multiple questions then make json  key value pair for each question and answer
#     try:
#             response = get_completion(prompt)
#     except:
#             response = get_completion(prompt)
#     print(response)
   
    
    