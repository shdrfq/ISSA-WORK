import streamlit as st
import fitz  # PyMuPDF for PDF processing
from PIL import Image
import os
import re
import google.generativeai as genai

# Configure Gemini API
genai.configure(api_key="AIzaSyCnRo7z_mSe-518MqQcp18qV0QaXeTmsIE")

def extract_text(file_path, file_type):
    """Extract text from a PDF or image file."""
    if file_type == "application/pdf":
        text = ""
        with fitz.open(file_path) as doc:
            for page in doc:
                text += page.get_text("text")
        return text
    else:
        image = Image.open(file_path)
        # Use pytesseract for OCR if needed, but ensure it's installed and configured
        # return pytesseract.image_to_string(image)
        return "OCR functionality not implemented in this example."

def extract_bill_details(text):
    """Extracts NAME & ADDRESS, DUE DATE, and PAYABLE WITHIN DUE DATE from the text."""
    details = {"Name & Address": "Not Found", "Due Date": "Not Found", "Payable Within Due Date": "Not Found"}
    
    # Extract Name & Address
    match = re.search(r'NAME & ADDRESS\s*([A-Z .]+\n[A-Z .]+\n[A-Z0-9 -]+)', text)
    if match:
        details["Name & Address"] = match.group(1).strip().replace('\n', ', ')
    
    # Extract Due Date (corrected regex for table format)
    match = re.search(r'DUE DATE\s*(\d{2} [A-Z]{3} \d{2})', text)
    print(match)
    if match:
        details["Due Date"] = match.group(1).strip()

    
    # Extract Payable Within Due Date
    match = re.search(r'PAYABLE WITHIN DUE DATE\s*(\d+)', text)
    if match:
        details["Payable Within Due Date"] = match.group(1).strip()
    
    return details

def chatbot_response(prompt):
    """Get response from Gemini LLM."""
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt)
    return response.text if response else "No response from the chatbot."

def main():
    st.title("FESCO Electricity Bill Chatbot")
    st.write("Upload your electricity bill (PDF or Image), and the chatbot will extract relevant details.")
    
    uploaded_file = st.file_uploader("Upload Bill (PDF or Image)", type=["pdf", "png", "jpg", "jpeg"])
    
    if uploaded_file:
        file_path = os.path.join("temp", uploaded_file.name)
        os.makedirs("temp", exist_ok=True)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        extracted_text = extract_text(file_path, uploaded_file.type)
        bill_details = extract_bill_details(extracted_text)
        
        st.subheader("Extracted Details:")
        for key, value in bill_details.items():
            st.write(f"**{key}:** {value}")
        
        prompt = (f"Provide a brief response regarding the electricity bill for {bill_details['Name & Address']}. "
                  f"The due date is {bill_details['Due Date']}, and the payable amount within the due date is {bill_details['Payable Within Due Date']}.")
        response = chatbot_response(prompt)
        
        st.subheader("Chatbot Response:")
        st.write(response)

if __name__ == "__main__":
    main()