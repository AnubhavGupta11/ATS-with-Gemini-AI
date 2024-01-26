from dotenv import load_dotenv

load_dotenv()

import streamlit as st
import os
import io
import base64
from PIL import Image
import pdf2image
import google.generativeai as genai


genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


def get_gemini_response(input, pdf_content,prompt):
    model=genai.GenerativeModel('gemini-pro-vision')
    response=model.generate_content([input, pdf_content[0],prompt])
    return response.text

def input_pdf_setup(uploaded_file):
    #convert pdf to image
    if uploaded_file is not None:
        image=pdf2image.convert_from_bytes(uploaded_file.read())
        first_page=image[0]

        #convert to bytes
        img_byte_arr=io.BytesIO()
        first_page.save(img_byte_arr,format='JPEG')
        img_byte_arr=img_byte_arr.getvalue()

        pdf_parts=[
            {
                "mime_type" : "image/jpeg",
                "data": base64.b64encode(img_byte_arr).decode() #encode to base64
            }
        ]
        return pdf_parts
    else:
        raise FileNotFoundError("No File Uploaded")
    

#Steamlit App
    
st.set_page_config(page_title="ATS Resume Expert")
st.header("ATS Tracking System")
input_text=st.text_area("Job Description",key="input")
uploaded_file=st.file_uploader("upload your resume(pdf)...",type=["pdf"])


if uploaded_file is not None:
    st.write("PDF uploaded successfully")

submit1 =st.button("Tell me about the Resume")

submit2= st.button("Percentage match")

input_prompt1="""
you are an experienced HR with Tech Experience in the field of any one job role from Data Science, Full Stack Web developer, Big Data Engineering,
DevOps, Data Analyst, your task is to review the provided resume against the job description for these profiles.
Please share your professional evaluation on whether the candidate's profile aligns with the role. With the Highlights the strenghts 
and weakness of the application in the relation to the specified job 
"""
input_prompt2="""
you are an skilled ATS (Application Tracking system) scanner with a deep understanding of any one job role Data Science, Full Stack Web developer, 
Big Data Engineering, DevOps, Data Analyst, and deep ATS funcationality. your task is to evaluate the resume against the job description.
Please give me percentage of the match if the resume matches with the job description. First the output should come 
as a percentage and then the keywords missing and last final thoughts.
"""

if submit1:
    if uploaded_file is not None:
        pdf_content=input_pdf_setup(uploaded_file)
        response=get_gemini_response(input_prompt1,pdf_content,input_text)
        st.subheader("The Response is:")
        st.write(response)
    else:
        st.write("Please upload the resume")

elif submit2:
    if uploaded_file is not None:
        pdf_content=input_pdf_setup(uploaded_file)
        response=get_gemini_response(input_prompt2,pdf_content,input_text)
        st.subheader("The Response is:")
        st.write(response)
    else:
        st.write("Please upload the resume")






