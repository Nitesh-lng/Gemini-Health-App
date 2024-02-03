import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
from PIL import Image

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input_prompt, image):
    model = genai.GenerativeModel('gemini-pro-vision')
    response = model.generate_content([input_prompt, image[0]])
    return response.text

def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        image_parts = [
            {
                "mime_type": uploaded_file.type,
                
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError('NO file uploaded')

#inialize streamlit app
st.set_page_config(page_title='Gemini Health App')
uploaded_file=st.file_uploader("choose an image.....",type=["jpg","jpeg","png"])
image=""
if uploaded_file is not None:
    image=Image.open(uploaded_file)
    st.image(image,caption="Uploaded Image",use_column_width=True)

submit=st.button("Tell me about the total chlories")

input_prompt="""
You are an expert in nutritionist where you need to see the food itmems from the image
                  and calculate the total calories, also provide the details of every food items with
                   calories intake in below format
                   
                   1. Item 1- no. of calories
                   2. Item 2- No. of calories
                   
                   
        Finally you can also mention whether the food is healthy or not



"""
if submit:
    image_data=input_image_setup(uploaded_file)
    response = get_gemini_response(input_prompt , image_data)
    st.header("The Response is")
    st.write(response)
