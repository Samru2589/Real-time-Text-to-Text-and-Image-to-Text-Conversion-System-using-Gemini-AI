import streamlit as st
import os
import textwrap
from PIL import Image
import google.generativeai as genai

def to_markdown(text):
    text = text.replace('•', '  *')
    return textwrap.indent(text, '> ', predicate=lambda _: True)

# Set the GEMINI_API_KEY environment variable
os.environ['GEMINI_API_KEY'] = 'AIzaSyByW6OwuSnQ5oZoZuWgnpHWGsUfyDW5Qbs'
genai.configure(api_key=os.environ['GEMINI_API_KEY'])

# Function to get response from Gemini AI for text input or image upload
def get_gemini_response(input_type, input_data):
    model = genai.GenerativeModel('gemini-1.5-flash')
    if input_type == "Text Input":
        response = model.generate_content(input_data)
    elif input_type == "Image Upload":
        pil_image = Image.open(input_data)
        response = model.generate_content(pil_image)
    return response.text

# Initialize the Streamlit app
st.set_page_config(page_title="Gemini AI BOT Application")
st.header("Gemini AI BOT Application")

# Sidebar for selecting input type
input_type = st.sidebar.radio("Select input type:", ("Text Input", "Image Upload"))

# Display the appropriate input widget based on the user's choice
if input_type == "Text Input":
    input_text = st.text_input("Enter your text:", key="input_text")
elif input_type == "Image Upload":
    uploaded_image = st.file_uploader("Upload an image", type=["jpg", "png", "jpeg", "jfif"])

# Submit button
submit = st.sidebar.button("Submit")

# Handle the submit action
if submit:
    if input_type == "Text Input" and input_text:
        response_text = get_gemini_response(input_type, input_text)
        st.subheader("Response for Text Input:")
        st.write(to_markdown(response_text))

    if input_type == "Image Upload" and uploaded_image:
        # Display the uploaded image
        st.image(uploaded_image, caption='Uploaded Image', use_column_width=True)
        
        response_image_text = get_gemini_response(input_type, uploaded_image)
        st.subheader("Extracted Text from Image:")
        st.write(to_markdown(response_image_text))
