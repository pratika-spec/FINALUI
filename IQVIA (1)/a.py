# import streamlit as st
# import json
# import PyPDF2
# from pdf2image import convert_from_path
# from pytesseract import image_to_string 
# import pytesseract
# # import re
# # import requests
# import openai
# import fitz
# # import time
# # import uuid

# openai.api_key="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"
# pytesseract.pytesseract.tesseract_cmd = r"C:\\Users\\pratika.karna\\Downloads\\combine_app (1)\\combine_app\\Tesseract-OCR\\tesseract.exe"


# # Title and instructions


# # Sidebar with three buttons
# with st.sidebar:
#     st.write("Sidebar")
#     selected_option = st.selectbox("Select an option", ["Language_Convertor", "Pdf_Convertor", "Research Paper"])


# # File uploader widget

# # Display content based on button clicks


# # Check if a file was uploaded
# # if uploaded_file is not None:
# #     # Display some information about the uploaded file
# #     st.write("File name:", uploaded_file.name)
# #     st.write("File size:", uploaded_file.size, "bytes")

# if selected_option=="Language_Convertor":
#     uploaded_file = st.file_uploader("Choose a PDF file", type=["pdf"])
#     if uploaded_file is not None:
#     # Display some information about the uploaded file
#         st.write("File name:", uploaded_file.name)
#         st.write("File size:", uploaded_file.size, "bytes")

#         def get_completion(prompt, model="gpt-4o", temperature=0):
#             messages = [{"role": "user", "content": prompt}]
#             response = openai.ChatCompletion.create(
#                 model=model,
#                 messages=messages,
#                 temperature=temperature,
#             )
#             return response.choices[0].message["content"]

        
#         pdfFileObject = open(uploaded_file.name, 'rb')
# # creating a pdf reader object
#         pdfReader = PyPDF2.PdfReader(pdfFileObject)
#         text=[]

#         for i in range(0,len(pdfReader.pages)):
#         # creating a page object
#             pageObj = pdfReader.pages[i].extract_text()
#             pageObj= pageObj.replace('\t\r','')
#             pageObj= pageObj.replace('\xa0','')
#             # extracting text from page
#             text.append(pageObj)
                
#         # for i in range(len(text)):
#         prompt =f"""Data is converted into english "

#         ```{text}```
#             """
#         try:
#                 response = get_completion(prompt)
#         except:
#                 response = get_completion(prompt)
#         prompt1 =f"""
#         Your task is to convert the data into json format. 
#         Check if the details are related to each other for example someone's details,
#         which can inlcude name, date of birth, age, gender, weight, height etc then those should be included as a sub dict.' 
#         Entire json format should be editable as this is a pdf editable form.

#         ```{response}``
#         """
#         response1 = get_completion(prompt1)
#         json_data = json.loads(response1)

#         st.write("Output:")
#         st.json(json_data)
        


#         # Function to ask questions and get answers from the chatbot API
        
        


        
       

# if selected_option=="Pdf_Convertor":
#     uploaded_file = st.file_uploader("Choose a PDF file", type=["pdf"])
#     if uploaded_file is not None:
#         st.write("File name:", uploaded_file.name)
#         st.write("File size:", uploaded_file.size, "bytes")
#     # Display some information about the uploaded file
#         def convert_pdf_to_img(pdf_file):
#           return convert_from_path(pdf_file, poppler_path=r'C:\\Users\\pratika.karna\\OneDrive - Thermo Fisher Scientific\\Desktop\\combine_app (1)\\combine_app\\poppler-24.08.0\\Library\\bin')


#         def convert_image_to_text(file):
        
            
#             text = image_to_string(file)
#             return text


#         def get_text_from_any_pdf(pdf_file):
        
#             images = convert_pdf_to_img(pdf_file)
#             final_text = ""
#             for pg, img in enumerate(images):
                
#                 final_text += convert_image_to_text(img)
#                 #print("Page n°{}".format(pg))
#                 #print(convert_image_to_text(img))
            
#             return final_text



#         def get_completion(prompt, model="gpt-3.5-turbo-16k"):
#             messages = [{"role": "user", "content": prompt}]
#             response = openai.ChatCompletion.create(
#             model=model,
#             messages=messages,
#             temperature=0, # this is the degree of randomness of the model's output
#         )
#             return response

#         ext_text = get_text_from_any_pdf(uploaded_file.name) 


#         input_text = f""" Your task is to convert the data into json format. 
#         Check if the details are related to each other for example someone's details,
#                         if the data contains any boxes, do create the proper check boxes for someone to tick or untick it.' 
#         which can inlcude name, date of birth, age, gender, weight, height etc then those should be included as a sub dict
#         Entire json format should be editable as this is a pdf editable form.
                
                
#                 Context: {ext_text}
            

            
#             """
#         response = get_completion(input_text)
#         with open("response2.json", "w") as f:
#             f.write(response)
# if selected_option=="Research Paper":
#     uploaded_file = st.file_uploader("Choose a PDF file", type=["pdf"])
#     if uploaded_file is not None:
#         def get_completion(prompt, model="gpt-3.5-turbo-16k"):
#             messages = [{"role": "user", "content": prompt}]
#             response = openai.ChatCompletion.create(
#                 model=model,
#                 messages=messages,
#                 temperature=0.7,
#             )
#             return response

#         def extract_text_from_pdf(pdf_path):
#             text = ""
#             with fitz.open(pdf_path) as pdf_document:
#                 for page_num in range(pdf_document.page_count):
#                     page = pdf_document.load_page(page_num)
#                     text += page.get_text()
#             return text
#         extracted_text = extract_text_from_pdf(uploaded_file.name)

        
        
        
                
    
#  # st.write("You can ask your questions here:")
#         user_input=("1- list of drugs prescribed to the patient"
#                     "2- What side effects were experienced by the patient after he started taking the drugs ? What was the diagnosis",
#                     "3- Which drug was responsible for this side effect? Which sentences demonstrate the causality between the drug and the side effect?",
#                     "4- Is Peripheral Neuropathy a listed / known side effect?"
#         )
#         prompt = f""" Mention all the  question and answer the question wise first question then give them answert
        

#         que:```{user_input}``` 
#         data: '''{extracted_text}'''
#         """
#         response = get_completion(prompt)
#         st.write(response)
#         # st.write(response.choices[0].message['content'])


# import streamlit as st
# import json
# import PyPDF2
# from pdf2image import convert_from_path
# from pytesseract import image_to_string 
# import pytesseract
# import openai
# import fitz

# openai.api_key = "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"
# pytesseract.pytesseract.tesseract_cmd = "C:\\Users\\pratika.karna\\Downloads\\combine_app (1)\\combine_app\\Tesseract-OCR\\tesseract.exe"

# st.title("PDF Processing App")

# with st.sidebar:
#     st.write("Sidebar")
#     selected_option = st.selectbox("Select an option", ["Language_Convertor", "Pdf_Convertor", "Research Paper"])


# # ─────────────────────────────────────────────
# # SHARED HELPER
# # ─────────────────────────────────────────────
# def get_completion(prompt, model="gpt-4o", temperature=0):
#     try:
#         messages = [{"role": "user", "content": prompt}]
#         response = openai.ChatCompletion.create(
#             model=model,
#             messages=messages,
#             temperature=temperature,
#         )
#         content = response.choices[0].message["content"]
#         if not content or content.strip() == "":
#             return None
#         return content
#     except openai.error.InvalidRequestError as e:
#         st.error(f"OpenAI API Error: {e}")
#         return None
#     except openai.error.AuthenticationError:
#         st.error("Invalid API key. Please check your OpenAI API key.")
#         return None
#     except openai.error.RateLimitError:
#         st.error("Rate limit exceeded. Please wait a moment and try again.")
#         return None
#     except Exception as e:
#         st.error(f"Unexpected error calling OpenAI: {e}")
#         return None


# def clean_json_response(raw: str) -> str:
#     """Strip markdown fences and whitespace from GPT response."""
#     cleaned = raw.strip()
#     # Remove ```json ... ``` or ``` ... ```
#     if cleaned.startswith("```"):
#         cleaned = cleaned.split("```", 2)[-1] if cleaned.count("```") == 1 else cleaned
#         lines = cleaned.split("\n")
#         # Remove first line if it's 'json' or empty
#         if lines[0].strip().lower() in ("json", ""):
#             lines = lines[1:]
#         # Remove last ``` if present
#         if lines and lines[-1].strip() == "```":
#             lines = lines[:-1]
#         cleaned = "\n".join(lines).strip()
#     return cleaned


# def safe_parse_json(raw: str):
#     """Try to parse JSON, return (json_data, error_message)."""
#     if not raw:
#         return None, "Empty response received from API."
#     cleaned = clean_json_response(raw)
#     if not cleaned:
#         return None, "Response was empty after cleaning."
#     try:
#         return json.loads(cleaned), None
#     except json.JSONDecodeError as e:
#         return None, f"JSON parse error: {e}\n\nRaw response:\n{cleaned[:500]}"


# # ─────────────────────────────────────────────
# # 1. LANGUAGE CONVERTER
# # ─────────────────────────────────────────────
# if selected_option == "Language_Convertor":
#     uploaded_file = st.file_uploader("Choose a PDF file", type=["pdf"])

#     if uploaded_file is not None:
#         st.write("File name:", uploaded_file.name)
#         st.write("File size:", uploaded_file.size, "bytes")

#         try:
#             # Save uploaded file temporarily
#             temp_path = f"temp_{uploaded_file.name}"
#             with open(temp_path, "wb") as f:
#                 f.write(uploaded_file.read())

#             pdfReader = PyPDF2.PdfReader(temp_path)
#             text = []

#             for i in range(len(pdfReader.pages)):
#                 pageObj = pdfReader.pages[i].extract_text()
#                 if pageObj:
#                     pageObj = pageObj.replace('\t\r', '').replace('\xa0', '')
#                     text.append(pageObj)

#             if not text:
#                 st.error("No text could be extracted from the PDF.")
#             else:
#                 full_text = " ".join(text)

#                 # Truncate if needed
#                 MAX_CHARS = 60000
#                 if len(full_text) > MAX_CHARS:
#                     st.warning(f"Document is large. Truncating to {MAX_CHARS} characters.")
#                     full_text = full_text[:MAX_CHARS]

#                 st.info(f"Extracted {len(full_text)} characters.")

#                 with st.spinner("Step 1/2 — Converting to English..."):
#                     prompt_english = f"""Convert the following data into English. 
# Return only the translated/converted text, no extra commentary.

# Data:
# {full_text}
# """
#                     response_english = get_completion(prompt_english)

#                 if not response_english:
#                     st.error("Failed to get a response from the API in Step 1.")
#                 else:
#                     with st.spinner("Step 2/2 — Converting to JSON..."):
#                         prompt_json = f"""Your task is to convert the following data into valid JSON format.
# - Group related fields as nested objects (e.g., patient details: name, dob, age, gender, weight, height).
# - Represent checkboxes as boolean fields (true/false).
# - The JSON must be editable as a PDF form.
# - Return ONLY raw valid JSON. Do NOT wrap in markdown code fences. Do NOT add any explanation.

# Data:
# {response_english}
# """
#                         response_json = get_completion(prompt_json)

#                     if not response_json:
#                         st.error("Failed to get a response from the API in Step 2.")
#                     else:
#                         json_data, err = safe_parse_json(response_json)
#                         if err:
#                             st.error(f"Failed to parse JSON: {err}")
#                             st.subheader("Raw API Response:")
#                             st.text(response_json)
#                         else:
#                             st.success("Successfully converted to JSON!")
#                             st.subheader("Output:")
#                             st.json(json_data)

#         except Exception as e:
#             st.error(f"An error occurred: {e}")


# # ─────────────────────────────────────────────
# # 2. PDF CONVERTER (OCR)
# # ─────────────────────────────────────────────
# elif selected_option == "Pdf_Convertor":
#     uploaded_file = st.file_uploader("Choose a PDF file", type=["pdf"])

#     if uploaded_file is not None:
#         st.write("File name:", uploaded_file.name)
#         st.write("File size:", uploaded_file.size, "bytes")

#         def convert_pdf_to_img(pdf_path):
#             return convert_from_path(
#                 pdf_path,
#                 poppler_path=r'C:\Users\pratika.karna\OneDrive - Thermo Fisher Scientific\Desktop\combine_app (1)\combine_app\poppler-24.08.0\Library\bin'
#             )

#         def convert_image_to_text(img):
#             return image_to_string(img)

#         def get_text_from_any_pdf(pdf_path):
#             images = convert_pdf_to_img(pdf_path)
#             final_text = ""
#             for img in images:
#                 final_text += convert_image_to_text(img)
#             return final_text

#         try:
#             # Save uploaded file temporarily
#             temp_path = f"temp_{uploaded_file.name}"
#             with open(temp_path, "wb") as f:
#                 f.write(uploaded_file.read())

#             with st.spinner("Extracting text via OCR..."):
#                 ext_text = get_text_from_any_pdf(temp_path)

#             if not ext_text or ext_text.strip() == "":
#                 st.error("No text could be extracted from the PDF via OCR.")
#             else:
#                 MAX_CHARS = 60000
#                 if len(ext_text) > MAX_CHARS:
#                     st.warning(f"Document is large. Truncating to {MAX_CHARS} characters.")
#                     ext_text = ext_text[:MAX_CHARS]

#                 st.info(f"Extracted {len(ext_text)} characters via OCR.")

#                 with st.spinner("Converting to JSON..."):
#                     input_text = f"""Your task is to convert the following data into valid JSON format.
# - Group related fields as nested objects (e.g., name, date of birth, age, gender, weight, height).
# - Represent any checkboxes or tick boxes as boolean fields (true/false).
# - The JSON must be editable as a PDF form.
# - Return ONLY raw valid JSON. Do NOT wrap in markdown code fences. Do NOT add any explanation.

# Data:
# {ext_text}
# """
#                     response = get_completion(input_text)

#                 if not response:
#                     st.error("Failed to get a response from the API.")
#                 else:
#                     json_data, err = safe_parse_json(response)
#                     if err:
#                         st.error(f"Failed to parse JSON: {err}")
#                         st.subheader("Raw API Response:")
#                         st.text(response)
#                     else:
#                         st.success("Successfully converted to JSON!")
#                         st.subheader("Output:")
#                         st.json(json_data)

#                         with open("response2.json", "w") as f:
#                             json.dump(json_data, f, indent=2)
#                         st.success("Saved to response2.json")

#         except Exception as e:
#             st.error(f"An error occurred: {e}")


# # ─────────────────────────────────────────────
# # 3. RESEARCH PAPER
# # ─────────────────────────────────────────────
# elif selected_option == "Research Paper":
#     uploaded_file = st.file_uploader("Choose a PDF file", type=["pdf"])

#     if uploaded_file is not None:
#         st.write("File name:", uploaded_file.name)
#         st.write("File size:", uploaded_file.size, "bytes")

#         def extract_text_from_pdf(pdf_path):
#             text = ""
#             with fitz.open(pdf_path) as pdf_document:
#                 for page_num in range(pdf_document.page_count):
#                     page = pdf_document.load_page(page_num)
#                     text += page.get_text()
#             return text

#         try:
#             # Save uploaded file temporarily
#             temp_path = f"temp_{uploaded_file.name}"
#             with open(temp_path, "wb") as f:
#                 f.write(uploaded_file.read())

#             with st.spinner("Extracting text from PDF..."):
#                 extracted_text = extract_text_from_pdf(temp_path)

#             if not extracted_text or extracted_text.strip() == "":
#                 st.error("No text could be extracted from the PDF.")
#             else:
#                 st.info(f"Extracted {len(extracted_text)} characters from the document.")

#                 MAX_CHARS = 100000
#                 if len(extracted_text) > MAX_CHARS:
#                     st.warning(f"Document is very large. Using first {MAX_CHARS} characters.")
#                     extracted_text = extracted_text[:MAX_CHARS]

#                 user_questions = """
# 1. List all drugs prescribed to the patient.
# 2. What side effects were experienced by the patient after starting the drugs? What was the diagnosis?
# 3. Which drug was responsible for the side effect? Which sentences from the document demonstrate the causality between the drug and the side effect?
# 4. Is Peripheral Neuropathy a listed or known side effect of the responsible drug?
# """

#                 prompt = f"""You are a medical document analyst. 
# Answer each of the following questions clearly and separately, based only on the document provided.
# Label each answer with its question number. Be concise and factual.

# Questions:
# {user_questions}

# Document:
# {extracted_text}
# """

#                 with st.spinner("Analyzing research paper with GPT-4o..."):
#                     response = get_completion(prompt, temperature=0.3)

#                 if not response:
#                     st.error("Failed to get a response from the API.")
#                 else:
#                     st.subheader("Analysis Results")
#                     st.write(response)

#         except Exception as e:
#             st.error(f"An error occurred: {e}")



import streamlit as st
import json
import PyPDF2
from pdf2image import convert_from_path
from pytesseract import image_to_string
import pytesseract
import openai
import fitz

st.set_page_config(
    page_title="DocuMind AI",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="expanded"
)

openai.api_key = "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"
pytesseract.pytesseract.tesseract_cmd = "C:\\Users\\pratika.karna\\Downloads\\combine_app (1)\\combine_app\\Tesseract-OCR\\tesseract.exe"

# ─────────────────────────────────────────────
# GLOBAL CSS — Light theme for ALL modules
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:ital,wght@0,300;0,400;0,500;1,400&display=swap');

*, *::before, *::after { box-sizing: border-box; }

/* ── Global light background ── */
html, body,
[data-testid="stAppViewContainer"],
[data-testid="stMain"],
.main {
    background: #f4f6fb !important;
    font-family: 'DM Sans', sans-serif;
    color: #1a1a2e !important;
}

#MainMenu, footer, header { visibility: hidden; }
[data-testid="stToolbar"] { display: none; }
.block-container {
    padding: 2rem 3rem 4rem 3rem !important;
    max-width: 1200px !important;
    background: transparent !important;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: #ffffff !important;
    border-right: 1px solid #e5e7eb !important;
}
[data-testid="stSidebar"] > div { padding: 2rem 1.5rem !important; }

.sidebar-logo {
    text-align: center;
    padding: 1.5rem 0 2rem;
    border-bottom: 1px solid #e5e7eb;
    margin-bottom: 2rem;
}
.sidebar-logo .logo-icon {
    font-size: 2.5rem;
    display: block;
    margin-bottom: 0.5rem;
}
.sidebar-logo h1 {
    font-family: 'Syne', sans-serif;
    font-size: 1.5rem;
    font-weight: 800;
    color: #7c3aed;
    letter-spacing: -0.02em;
}
.sidebar-logo p {
    font-size: 0.7rem;
    color: #9ca3af;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    margin-top: 0.25rem;
}

.nav-label {
    font-size: 0.65rem;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: #9ca3af;
    margin-bottom: 0.75rem;
    font-weight: 600;
}

/* ── Selectbox ── */
[data-testid="stSelectbox"] label { display: none !important; }
[data-testid="stSelectbox"] > div > div {
    background: #f3f4f6 !important;
    border: 1px solid #e5e7eb !important;
    border-radius: 12px !important;
    color: #1a1a2e !important;
    font-family: 'DM Sans', sans-serif !important;
}
[data-testid="stSelectbox"] > div > div:hover {
    border-color: #c4b5fd !important;
    background: #faf5ff !important;
}

.sidebar-info {
    margin-top: 2rem;
    padding: 1rem;
    background: #f9fafb;
    border: 1px solid #e5e7eb;
    border-radius: 12px;
}
.sidebar-info p { font-size: 0.75rem; color: #6b7280; line-height: 1.6; }
.sidebar-info .model-badge {
    display: inline-block;
    background: #ede9fe;
    border: 1px solid #c4b5fd;
    padding: 0.2rem 0.6rem;
    border-radius: 20px;
    font-size: 0.65rem;
    font-weight: 600;
    color: #6d28d9;
    letter-spacing: 0.05em;
    margin-bottom: 0.5rem;
}

/* ── Page header card ── */
.page-header {
    background: #ffffff;
    border: 1px solid #e5e7eb;
    border-radius: 16px;
    padding: 1.75rem 2rem;
    margin-bottom: 1.5rem;
    box-shadow: 0 2px 12px rgba(0,0,0,0.04);
}
.page-header .tag {
    display: inline-block;
    background: #ede9fe;
    color: #6d28d9;
    font-size: 0.65rem;
    font-weight: 700;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    padding: 0.25rem 0.75rem;
    border-radius: 20px;
    margin-bottom: 0.75rem;
}
.page-header h2 {
    font-family: 'Syne', sans-serif;
    font-size: 1.9rem;
    font-weight: 800;
    color: #1a1a2e !important;
    letter-spacing: -0.03em;
    margin-bottom: 0.4rem;
}
.page-header h2 span {
    color: #7c3aed;
}
.page-header p { font-size: 0.88rem; color: #6b7280; line-height: 1.6; }

/* ── Steps row ── */
.steps-row {
    display: flex;
    gap: 0.5rem;
    margin: 0 0 1.5rem;
    align-items: center;
}
.step-pill {
    display: flex;
    align-items: center;
    gap: 0.4rem;
    background: #f3f4f6;
    border: 1px solid #e5e7eb;
    border-radius: 20px;
    padding: 0.3rem 0.85rem;
    font-size: 0.72rem;
    font-weight: 500;
    color: #9ca3af;
}
.step-pill.active {
    background: #ede9fe;
    border-color: #c4b5fd;
    color: #6d28d9;
}
.step-pill .num {
    width: 16px; height: 16px;
    background: #c4b5fd;
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 0.6rem; font-weight: 700;
    color: #6d28d9;
}
.step-arrow { color: #d1d5db; font-size: 0.75rem; }

/* ── File uploader ── */
[data-testid="stFileUploader"] {
    background: #ffffff !important;
    border: 2px dashed #c4b5fd !important;
    border-radius: 16px !important;
    padding: 1rem !important;
    transition: all 0.2s ease !important;
}
[data-testid="stFileUploader"]:hover {
    border-color: #7c3aed !important;
    background: #faf5ff !important;
}
[data-testid="stFileUploader"] label {
    color: #7c3aed !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 600 !important;
}
[data-testid="stFileUploadDropzone"] { background: transparent !important; border: none !important; }
[data-testid="stFileUploadDropzone"] p { color: #9ca3af !important; font-size: 0.85rem !important; }
[data-testid="stFileUploadDropzone"] small { color: #c4b5fd !important; font-size: 0.75rem !important; }

/* ── File info card ── */
.file-info-card {
    display: flex;
    align-items: center;
    gap: 1rem;
    background: #faf5ff;
    border: 1px solid #e9d5ff;
    border-radius: 12px;
    padding: 1rem 1.25rem;
    margin: 1rem 0;
}
.file-icon { font-size: 1.8rem; }
.file-details h4 {
    font-family: 'Syne', sans-serif;
    font-size: 0.9rem;
    font-weight: 700;
    color: #1a1a2e;
    margin-bottom: 0.15rem;
}
.file-details p { font-size: 0.75rem; color: #9ca3af; }

/* ── Buttons ── */
.stButton > button {
    background: linear-gradient(135deg, #7c3aed, #a855f7) !important;
    color: white !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.85rem !important;
    letter-spacing: 0.05em !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 0.75rem 2rem !important;
    transition: all 0.2s ease !important;
    box-shadow: 0 4px 16px rgba(124,58,237,0.25) !important;
    width: 100% !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 24px rgba(124,58,237,0.35) !important;
}

/* ── Results header ── */
.results-header {
    display: flex; align-items: center; gap: 0.75rem;
    margin: 2rem 0 1rem;
}
.results-header .dot {
    width: 10px; height: 10px;
    background: #7c3aed;
    border-radius: 50%;
    box-shadow: 0 0 8px rgba(124,58,237,0.5);
    animation: pulse 2s ease-in-out infinite;
}
@keyframes pulse { 0%,100%{opacity:1;transform:scale(1)} 50%{opacity:0.5;transform:scale(1.3)} }
.results-header h3 {
    font-family: 'Syne', sans-serif;
    font-size: 1rem;
    font-weight: 700;
    color: #1a1a2e;
}

/* ── Success banner ── */
.success-banner {
    display: flex; align-items: center; gap: 0.75rem;
    background: #f0fdf4;
    border: 1px solid #86efac;
    border-radius: 12px;
    padding: 0.85rem 1.25rem;
    margin: 1rem 0;
}
.success-banner span { font-size: 1.2rem; }
.success-banner p { font-size: 0.85rem; color: #16a34a; font-weight: 500; }

/* ── JSON viewer ── */
[data-testid="stJson"] {
    background: #ffffff !important;
    border: 1px solid #e5e7eb !important;
    border-radius: 16px !important;
    padding: 1.5rem !important;
}

/* ── Alerts / info ── */
[data-testid="stAlert"] {
    border-radius: 12px !important;
    border: 1px solid #e5e7eb !important;
}

/* ── Progress bar ── */
[data-testid="stProgressBar"] > div { background: #7c3aed !important; border-radius: 8px !important; }

/* ── Spinner ── */
[data-testid="stSpinner"] { color: #7c3aed !important; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: #f4f6fb; }
::-webkit-scrollbar-thumb { background: #c4b5fd; border-radius: 3px; }

/* ── Doc ready badge ── */
.doc-ready {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    background: #f0fdf4;
    border: 1px solid #86efac;
    border-radius: 20px;
    padding: 0.3rem 0.9rem;
    font-size: 0.72rem;
    color: #16a34a;
    font-weight: 600;
    letter-spacing: 0.04em;
    margin-bottom: 0.75rem;
}
.dot-g {
    width: 7px; height: 7px;
    background: #22c55e;
    border-radius: 50%;
    box-shadow: 0 0 6px rgba(34,197,94,0.6);
    animation: gpulse 2s ease-in-out infinite;
    flex-shrink: 0;
}
@keyframes gpulse { 0%,100%{opacity:1;transform:scale(1)} 50%{opacity:0.5;transform:scale(1.3)} }

/* ── Section label ── */
.sec-lbl {
    font-size: 0.67rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #9ca3af;
    font-weight: 600;
    margin-bottom: 0.5rem;
}

/* ── Quick question chips ── */
.rp-chips .stButton > button {
    background: #ede9fe !important;
    color: #6d28d9 !important;
    border: 1px solid #c4b5fd !important;
    border-radius: 20px !important;
    font-size: 0.75rem !important;
    font-weight: 600 !important;
    padding: 0.4rem 0.8rem !important;
    box-shadow: none !important;
    letter-spacing: 0 !important;
    width: 100% !important;
}
.rp-chips .stButton > button:hover {
    background: #ddd6fe !important;
    border-color: #7c3aed !important;
    transform: none !important;
    box-shadow: 0 2px 8px rgba(124,58,237,0.15) !important;
}

/* ── Chat welcome box ── */
.chat-welcome-box {
    text-align: center;
    padding: 3rem 2rem;
    background: #ffffff;
    border: 1px solid #e5e7eb;
    border-radius: 16px;
    margin-bottom: 1rem;
    box-shadow: 0 2px 8px rgba(0,0,0,0.04);
}
.cw-icon { font-size: 2.5rem; margin-bottom: 0.75rem; }
.cw-title {
    font-family: 'Syne', sans-serif;
    font-size: 1rem;
    font-weight: 700;
    color: #4b5563;
    margin-bottom: 0.4rem;
}
.cw-sub { font-size: 0.82rem; color: #9ca3af; line-height: 1.7; }

/* ── Native st.chat_message light styling ── */
[data-testid="stChatMessage"] {
    background: transparent !important;
    border: none !important;
    padding: 0.2rem 0 !important;
}

/* AI message bubble */
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) {
    background: transparent !important;
}
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) > div:last-child {
    background: #f8f7ff !important;
    border: 1px solid #ede9fe !important;
    border-radius: 0 16px 16px 16px !important;
    padding: 0.85rem 1.1rem !important;
    box-shadow: 0 1px 4px rgba(0,0,0,0.05) !important;
}
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) p,
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) li {
    color: #1f2937 !important;
    font-size: 0.9rem !important;
    line-height: 1.7 !important;
}

/* User message bubble */
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) > div:last-child {
    background: linear-gradient(135deg, #7c3aed, #a855f7) !important;
    border-radius: 16px 0 16px 16px !important;
    padding: 0.85rem 1.1rem !important;
    box-shadow: 0 3px 12px rgba(124,58,237,0.2) !important;
}
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) p {
    color: #ffffff !important;
    font-size: 0.9rem !important;
    line-height: 1.6 !important;
}

/* Avatar icons */
[data-testid="chatAvatarIcon-assistant"] {
    background: #ede9fe !important;
    border: 1px solid #c4b5fd !important;
    color: #7c3aed !important;
}
[data-testid="chatAvatarIcon-user"] {
    background: linear-gradient(135deg, #7c3aed, #a855f7) !important;
}

/* ── Chat input light ── */
[data-testid="stChatInput"] > div {
    background: #ffffff !important;
    border: 1.5px solid #c4b5fd !important;
    border-radius: 14px !important;
    box-shadow: 0 2px 8px rgba(124,58,237,0.08) !important;
}
[data-testid="stChatInput"] textarea {
    color: #1a1a2e !important;
    font-size: 0.9rem !important;
    background: transparent !important;
}
[data-testid="stChatInput"] textarea::placeholder { color: #9ca3af !important; }
[data-testid="stChatInput"] button {
    background: linear-gradient(135deg, #7c3aed, #a855f7) !important;
    border-radius: 10px !important;
}

/* ── Clear button ── */
.clr-btn .stButton > button {
    background: #fff !important;
    color: #ef4444 !important;
    border: 1px solid #fca5a5 !important;
    border-radius: 10px !important;
    font-size: 0.78rem !important;
    font-weight: 600 !important;
    padding: 0.4rem 1rem !important;
    box-shadow: none !important;
    width: auto !important;
    letter-spacing: 0 !important;
}
.clr-btn .stButton > button:hover {
    background: #fef2f2 !important;
    transform: none !important;
    box-shadow: none !important;
}

/* ── No-doc placeholder ── */
.no-doc {
    text-align: center;
    padding: 4rem 2rem;
    background: #ffffff;
    border: 2px dashed #e5e7eb;
    border-radius: 16px;
    margin-top: 1rem;
}
.no-doc .icon { font-size: 3rem; margin-bottom: 0.75rem; }
.no-doc h4 { font-family: 'Syne', sans-serif; font-size: 1rem; color: #9ca3af; margin-bottom: 0.4rem; }
.no-doc p { font-size: 0.82rem; color: #d1d5db; line-height: 1.6; }

/* ── Steps row for research module ── */
.rp-steps { display:flex; gap:0.5rem; margin:0 0 1.5rem; align-items:center; }
.rp-step { display:flex; align-items:center; gap:0.4rem; background:#f3f4f6; border:1px solid #e5e7eb; border-radius:20px; padding:0.3rem 0.85rem; font-size:0.72rem; font-weight:500; color:#9ca3af; }
.rp-step.on { background:#ede9fe; border-color:#c4b5fd; color:#6d28d9; }
.rp-step .n { width:16px; height:16px; background:#c4b5fd; border-radius:50%; display:flex; align-items:center; justify-content:center; font-size:0.6rem; font-weight:700; color:#6d28d9; }
.rp-arr { color:#d1d5db; font-size:0.75rem; }

/* ── Research header card ── */
.rp-header {
    background: #ffffff;
    border: 1px solid #e5e7eb;
    border-radius: 16px;
    padding: 1.75rem 2rem;
    margin-bottom: 1.5rem;
    box-shadow: 0 2px 12px rgba(0,0,0,0.05);
}
.rp-tag {
    display: inline-block;
    background: #ede9fe;
    color: #6d28d9;
    font-size: 0.65rem;
    font-weight: 700;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    padding: 0.25rem 0.75rem;
    border-radius: 20px;
    margin-bottom: 0.75rem;
}
.rp-header h2 {
    font-family: 'Syne', sans-serif;
    font-size: 1.9rem;
    font-weight: 800;
    color: #1a1a2e;
    letter-spacing: -0.03em;
    margin-bottom: 0.4rem;
}
.rp-header h2 em { color: #7c3aed; font-style: normal; }
.rp-header p { font-size: 0.88rem; color: #6b7280; line-height: 1.6; }

/* ── Upload wrapper for research ── */
.rp-upload [data-testid="stFileUploader"] {
    background: #ffffff !important;
    border: 2px dashed #c4b5fd !important;
    border-radius: 14px !important;
}
.rp-upload [data-testid="stFileUploader"]:hover {
    border-color: #7c3aed !important;
    background: #faf5ff !important;
}
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
   
    st.markdown('<p class="nav-label">Select Module</p>', unsafe_allow_html=True)
    selected_option = st.selectbox(
        "Module", ["Language Converter", "PDF Converter (OCR)", "Case Report Analyser"],
        label_visibility="collapsed"
    )
    
    

# ─────────────────────────────────────────────
# SHARED HELPERS
# ─────────────────────────────────────────────
def get_completion(prompt, model="gpt-4o", temperature=0):
    try:
        messages = [{"role": "user", "content": prompt}]
        response = openai.ChatCompletion.create(model=model, messages=messages, temperature=temperature)
        content = response.choices[0].message["content"]
        return content if content and content.strip() else None
    except openai.error.InvalidRequestError as e:
        st.error(f"OpenAI Error: {e}"); return None
    except openai.error.AuthenticationError:
        st.error("Invalid API key."); return None
    except openai.error.RateLimitError:
        st.error("Rate limit exceeded."); return None
    except Exception as e:
        st.error(f"Unexpected error: {e}"); return None

def clean_json_response(raw):
    cleaned = raw.strip()
    if cleaned.startswith("```"):
        lines = cleaned.split("\n")
        if lines[0].strip().lower() in ("```json", "```", "json"): lines = lines[1:]
        if lines and lines[-1].strip() == "```": lines = lines[:-1]
        cleaned = "\n".join(lines).strip()
    return cleaned

def safe_parse_json(raw):
    if not raw: return None, "Empty response from API."
    cleaned = clean_json_response(raw)
    if not cleaned: return None, "Response empty after cleaning."
    try: return json.loads(cleaned), None
    except json.JSONDecodeError as e: return None, f"Parse error: {e}\n\nRaw:\n{cleaned[:500]}"

def save_temp(uploaded_file):
    temp_path = f"temp_{uploaded_file.name}"
    with open(temp_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return temp_path

def show_file_card(uploaded_file):
    size_kb = round(uploaded_file.size / 1024, 1)
    st.markdown(f"""
    <div class="file-info-card">
        <div class="file-icon">📄</div>
        <div class="file-details">
            <h4>{uploaded_file.name}</h4>
            <p>{size_kb} KB &nbsp;·&nbsp; PDF Document</p>
        </div>
    </div>""", unsafe_allow_html=True)

def show_results_header(label="Results"):
    st.markdown(f'<div class="results-header"><div class="dot"></div><h3>{label}</h3></div>', unsafe_allow_html=True)

def show_success(msg):
    st.markdown(f'<div class="success-banner"><span>✓</span><p>{msg}</p></div>', unsafe_allow_html=True)


# ═════════════════════════════════════════════
# MODULE 1 — LANGUAGE CONVERTER
# ═════════════════════════════════════════════
if selected_option == "Language Converter":
    st.markdown("""
    <div class="page-header">
        <div class="tag">Module 01</div>
        <h2>Language <span>Converter</span></h2>
        <p>Upload a PDF in any language. DocuMind will translate the content to English and convert it into a structured, editable JSON form.</p>
    </div>
    <div class="steps-row">
        <div class="step-pill active"><div class="num">1</div> Upload PDF</div>
        <div class="step-arrow">›</div>
        <div class="step-pill"><div class="num">2</div> Translate to English</div>
        <div class="step-arrow">›</div>
        <div class="step-pill"><div class="num">3</div> Generate JSON</div>
    </div>
    """, unsafe_allow_html=True)

    uploaded_file = st.file_uploader("Upload your PDF", type=["pdf"], key="lc_uploader")
    if uploaded_file is not None:
        show_file_card(uploaded_file)
        if st.button("✦  Translate & Convert to JSON", key="lc_btn"):
            try:
                temp_path = save_temp(uploaded_file)
                pdfReader = PyPDF2.PdfReader(temp_path)
                text = []
                for i in range(len(pdfReader.pages)):
                    p = pdfReader.pages[i].extract_text()
                    if p: text.append(p.replace('\t\r', '').replace('\xa0', ''))
                if not text:
                    st.error("No text could be extracted.")
                else:
                    full_text = " ".join(text)
                    if len(full_text) > 60000:
                        st.warning("Large document. Truncating to 60,000 characters.")
                        full_text = full_text[:60000]
                    with st.spinner("Translating to English..."):
                        r1 = get_completion(f"Convert the following data into English. Return only translated text.\n\n{full_text}")
                    if not r1:
                        st.error("Translation failed.")
                    else:
                        with st.spinner("Structuring into JSON..."):
                            r2 = get_completion(f"Convert the data below into valid JSON format. Group related fields as nested objects. Checkboxes as booleans. Return ONLY raw valid JSON, no markdown fences.\n\n{r1}")
                        if not r2:
                            st.error("JSON conversion failed.")
                        else:
                            jd, err = safe_parse_json(r2)
                            if err: st.error(err); st.text(r2)
                            else:
                                show_success("Document translated and converted to JSON.")
                                show_results_header("Structured JSON Output")
                                st.json(jd)
            except Exception as e:
                st.error(f"Error: {e}")


# ═════════════════════════════════════════════
# MODULE 2 — PDF CONVERTER (OCR)
# ═════════════════════════════════════════════
elif selected_option == "PDF Converter (OCR)":
    st.markdown("""
    <div class="page-header">
        <div class="tag">Module 02</div>
        <h2>PDF Converter <span>(OCR)</span></h2>
        <p>Upload a scanned or image-based PDF. DocuMind uses OCR to extract every character and converts it into a fully editable JSON structure.</p>
    </div>
    <div class="steps-row">
        <div class="step-pill active"><div class="num">1</div> Upload Scanned PDF</div>
        <div class="step-arrow">›</div>
        <div class="step-pill"><div class="num">2</div> OCR Extraction</div>
        <div class="step-arrow">›</div>
        <div class="step-pill"><div class="num">3</div> Generate JSON</div>
    </div>
    """, unsafe_allow_html=True)

    uploaded_file = st.file_uploader("Upload your scanned PDF", type=["pdf"], key="ocr_uploader")
    if uploaded_file is not None:
        show_file_card(uploaded_file)
        if st.button("✦  Run OCR & Convert to JSON", key="ocr_btn"):
            try:
                temp_path = save_temp(uploaded_file)
                with st.spinner("Running OCR..."):
                    images = convert_from_path(
                        temp_path,
                        poppler_path=r'C:\Users\pratika.karna\OneDrive - Thermo Fisher Scientific\Desktop\combine_app (1)\combine_app\poppler-24.08.0\Library\bin'
                    )
                    ext_text = ""
                    bar = st.progress(0, text="Processing pages...")
                    for idx, img in enumerate(images):
                        ext_text += image_to_string(img)
                        bar.progress((idx + 1) / len(images), text=f"Page {idx + 1} of {len(images)}...")
                    bar.empty()
                if not ext_text.strip():
                    st.error("No text extracted via OCR.")
                else:
                    if len(ext_text) > 60000:
                        st.warning("Large document. Truncating to 60,000 characters.")
                        ext_text = ext_text[:60000]
                    st.info(f"✓ Extracted {len(ext_text):,} characters from {len(images)} page(s).")
                    with st.spinner("Converting to JSON..."):
                        r = get_completion(
                            f"Convert the following OCR data into valid JSON format. Group related fields as nested objects. Checkboxes as booleans (true/false). Return ONLY raw valid JSON, no markdown fences.\n\n{ext_text}"
                        )
                    if not r:
                        st.error("JSON conversion failed.")
                    else:
                        jd, err = safe_parse_json(r)
                        if err: st.error(err); st.text(r)
                        else:
                            with open("response2.json", "w") as f: json.dump(jd, f, indent=2)
                            show_success(f"OCR complete. {len(images)} page(s) processed. Saved to response2.json")
                            show_results_header("Structured JSON Output")
                            st.json(jd)
            except Exception as e:
                st.error(f"Error: {e}")


# ═════════════════════════════════════════════
# MODULE 3 — RESEARCH PAPER CHATBOT
# ═════════════════════════════════════════════
elif selected_option == "Case Report Analyser":

    # ── Page Header ──
    st.markdown("""
    <div class="rp-header">
        <div class="rp-tag">Module 03</div>
        <h2>Case Report Analyser <em>Chatbot</em></h2>
        <p>Upload a clinical case report— then ask anything in natural conversation. Drugs, side effects, diagnoses, causality, and more.</p>
    </div>
    <div class="rp-steps">
        <div class="rp-step on"><div class="n">1</div> Upload Case Report</div>
        <div class="rp-arr">›</div>
        <div class="rp-step"><div class="n">2</div> AI Reads Document</div>
        <div class="rp-arr">›</div>
        <div class="rp-step"><div class="n">3</div> Ask Anything</div>
    </div>
    """, unsafe_allow_html=True)

    # ── Session state ──
    if "rp_doc_text" not in st.session_state: st.session_state.rp_doc_text = None
    if "rp_doc_name" not in st.session_state: st.session_state.rp_doc_name = None
    if "rp_messages" not in st.session_state: st.session_state.rp_messages = []

    # ── File uploader ──
    st.markdown('<div class="rp-upload">', unsafe_allow_html=True)
    uploaded_file = st.file_uploader(
        "Upload case report or research paper (PDF)",
        type=["pdf"], key="rp_uploader",
        help="Clinical papers, case studies, pharmacological reports"
    )
    st.markdown('</div>', unsafe_allow_html=True)

    # ── Auto-extract on upload ──
    if uploaded_file is not None and st.session_state.rp_doc_name != uploaded_file.name:
        with st.spinner("Reading and indexing document..."):
            try:
                temp_path = save_temp(uploaded_file)
                extracted_text = ""
                with fitz.open(temp_path) as pdf:
                    for page_num in range(pdf.page_count):
                        extracted_text += pdf.load_page(page_num).get_text()
                if len(extracted_text) > 100000:
                    extracted_text = extracted_text[:100000]
                st.session_state.rp_doc_text = extracted_text
                st.session_state.rp_doc_name = uploaded_file.name
                st.session_state.rp_messages = []
            except Exception as e:
                st.error(f"Failed to read PDF: {e}")

    # ── Chat interface ──
    if st.session_state.rp_doc_text:
        size_chars = len(st.session_state.rp_doc_text)

        st.markdown(f"""
        <div class="doc-ready">
            <div class="dot-g"></div>
            {st.session_state.rp_doc_name} &nbsp;·&nbsp; {size_chars:,} characters indexed
        </div>
        """, unsafe_allow_html=True)

        # Quick question chips
        st.markdown('<p class="sec-lbl">Quick Questions</p>', unsafe_allow_html=True)
        suggestions = [
            "List all drugs prescribed",
            "What side effects occurred?",
            "Which drug caused the side effect?",
            "Is Peripheral Neuropathy a known side effect?",
        ]
        chip_clicked = None
        st.markdown('<div class="rp-chips">', unsafe_allow_html=True)
        cols = st.columns(4)
        for col, s in zip(cols, suggestions):
            with col:
                if st.button(s, key=f"chip_{s[:18]}", use_container_width=True):
                    chip_clicked = s
        st.markdown('</div><br>', unsafe_allow_html=True)

        # ── Chat messages ──
        if not st.session_state.rp_messages:
            st.markdown("""
            <div class="chat-welcome-box">
                <div class="cw-icon">🔬</div>
                <div class="cw-title">Document ready. Ask your first question.</div>
                <div class="cw-sub">Use a quick question above or type in the box below to start your clinical analysis conversation.</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            for msg in st.session_state.rp_messages:
                with st.chat_message(msg["role"]):
                    st.markdown(msg["content"])

        # Chat input
        user_input = st.chat_input("Ask anything about the document...", key="rp_chat_input")
        question = chip_clicked if chip_clicked else user_input

        if question:
            st.session_state.rp_messages.append({"role": "user", "content": question})
            history_text = "\n".join(
                f"{'User' if m['role'] == 'user' else 'Assistant'}: {m['content']}"
                for m in st.session_state.rp_messages[:-1]
            )
            prompt = f"""You are a medical document analyst assistant.
Answer the user's question based ONLY on the document provided.
Be concise, factual, and reference specific parts when relevant.
If the answer is not in the document, say so clearly.

Previous conversation:
{history_text}

Document:
{st.session_state.rp_doc_text}

User's question: {question}
"""
            with st.spinner("Thinking..."):
                response = get_completion(prompt, temperature=0.3)

            st.session_state.rp_messages.append({
                "role": "assistant",
                "content": response if response else "Sorry, I couldn't generate a response. Please try again."
            })
            st.rerun()

        # Clear conversation button
        if st.session_state.rp_messages:
            st.markdown('<div class="clr-btn">', unsafe_allow_html=True)
            if st.button("🗑  Clear Conversation", key="clear_chat"):
                st.session_state.rp_messages = []
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

    else:
        st.markdown("""
        <div class="no-doc">
            <div class="icon">📋</div>
            <h4>No document uploaded yet</h4>
            <p>Upload a clinical case report or research paper above<br>to start your AI-powered analysis conversation.</p>
        </div>
        """, unsafe_allow_html=True)
