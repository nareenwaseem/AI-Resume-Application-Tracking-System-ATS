from dotenv import load_dotenv

load_dotenv()
import base64
import streamlit as st
import os
import io
from PIL import Image
import pdf2image
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input, pdf_content, prompt):
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content([input, pdf_content[0], prompt])
    return response.text

def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        # Convert the PDF to image
        images = pdf2image.convert_from_bytes(uploaded_file.read())

        first_page = images[0]

        # Convert to bytes
        img_byte_arr = io.BytesIO()
        first_page.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()

        pdf_parts = [
            {
                "mime_type": "image/jpeg",
                "data": base64.b64encode(img_byte_arr).decode()  # encode to base64
            }
        ]
        return pdf_parts
    else:
        raise FileNotFoundError("No file uploaded")

# Function to check relevance of the question
def is_question_relevant(question):
    relevant_keywords = [
        "resume", "job description", "skill", "experience", "education", "project",
        "achievement", "weakness", "strength", "ATS", "match", "improvement", "keyword"
    ]
    question_lower = question.lower()
    return any(keyword in question_lower for keyword in relevant_keywords)

# Streamlit App

st.set_page_config(page_title="ATS Resume Expert")
st.header("Application Tracking System(ATS)")
input_text = st.text_area("Job Description: ", key="input")
uploaded_file = st.file_uploader("Upload your resume (PDF)...", type=["pdf"])

if uploaded_file is not None:
    st.write("PDF Uploaded Successfully")


col1, col2 = st.columns(2)

with col1:
    submit1 = st.button("Percentage Match")
    submit2 = st.button("Identify Weakness")
    submit3 = st.button("Identify Strengths")
    submit4 = st.button("Detailed Skill Match")

with col2:
    submit5 = st.button("Resume Improvement Tips")
    submit6 = st.button("Keyword Analysis")
    submit7 = st.button("Experience Relevance")
    submit8 = st.button("Achievements and Projects")

input_prompt1 = """
You are an experienced ATS (Applicant Tracking System) scanner with a deep understanding of data science and ATS functionality.
Your task is to evaluate the resume against the provided job description and tell only the percentage match. Just percentage.
"""

input_prompt2 = """
You are an experienced Technical Human Resource Manager. Your task is to review the provided resume against the job description.
Please identify the weaknesses or missing keywords that reduce the chances of getting the job.
"""

input_prompt3 = """
You are an experienced Technical Human Resource Manager. Your task is to review the provided resume against the job description.
Please identify the strengths or present keywords that increase the chances of getting the job.
"""

input_prompt4 = """
You are an experienced ATS (Applicant Tracking System) scanner with a deep understanding of data science and ATS functionality.
Your task is to evaluate the resume against the job description and tell which specific skills listed in the job description are missing from the resume.
"""

input_prompt5 = """
You are an experienced Technical Human Resource Manager. Your task is to review the provided resume against the job description.
Please suggest ways to improve the resume to better match the job description.
"""

input_prompt6 = """
You are an experienced ATS (Applicant Tracking System) scanner with a deep understanding of data science and ATS functionality.
Your task is to evaluate the resume against the job description and tell which keywords from the job description are missing in the resume.
"""

input_prompt7 = """
You are an experienced Technical Human Resource Manager. Your task is to review the provided resume against the job description.
Please identify which of the candidate's past job experiences are most relevant to the job.
"""

input_prompt8 = """
You are an experienced Technical Human Resource Manager. Your task is to review the provided resume against the job description.
Please tell whether the achievements and projects are highlighted effectively in the resume.
"""

if submit1:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt1, pdf_content, input_text)
        st.subheader("The Response is")
        st.write(response)
    else:
        st.write("Please upload the resume")

elif submit2:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt2, pdf_content, input_text)
        st.subheader("The Response is")
        st.write(response)
    else:
        st.write("Please upload the resume")

elif submit3:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt3, pdf_content, input_text)
        st.subheader("The Response is")
        st.write(response)
    else:
        st.write("Please upload the resume")

elif submit4:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt4, pdf_content, input_text)
        st.subheader("The Response is")
        st.write(response)
    else:
        st.write("Please upload the resume")

elif submit5:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt5, pdf_content, input_text)
        st.subheader("The Response is")
        st.write(response)
    else:
        st.write("Please upload the resume")

elif submit6:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt6, pdf_content, input_text)
        st.subheader("The Response is")
        st.write(response)
    else:
        st.write("Please upload the resume")

elif submit7:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt7, pdf_content, input_text)
        st.subheader("The Response is")
        st.write(response)
    else:
        st.write("Please upload the resume")

elif submit8:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt8, pdf_content, input_text)
        st.subheader("The Response is")
        st.write(response)
    else:
        st.write("Please upload the resume")

# Chat bot input
st.subheader("Chat with ATS Expert")
chat_input = st.text_input("Ask any question related to your resume and job description:", key="chat_input")
chat_submit = st.button("Submit Question")

if chat_submit:
    if is_question_relevant(chat_input):
        if uploaded_file is not None:
            pdf_content = input_pdf_setup(uploaded_file)
            chat_response = get_gemini_response(chat_input, pdf_content, input_text)
            st.subheader("Chatbot Response")
            st.write(chat_response)
        else:
            st.write("Please upload the resume")
    else:
        st.write("The question seems to be irrelevant to your resume and job description. Please ask a relevant question.")
