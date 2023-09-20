import streamlit as st
import fitz  # PyMuPDF
import io
import os
import zipfile

st.title('🔥 PDF Image Extractor by Yuval Avidani @HACKIT.CO.IL 🔥')

uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file:
    file_details = {"FileName": uploaded_file.name, "FileType": uploaded_file.type, "FileSize": uploaded_file.size}
    st.write(file_details)
    
    # Save the uploaded file to a temporary file
    temp_file_path = os.path.join(os.getcwd(), uploaded_file.name)
    with open(temp_file_path, "wb") as temp_file:
        temp_file.write(uploaded_file.read())
    
    if os.path.exists(temp_file_path):
        st.write("File has been uploaded successfully.")
        
        doc = fitz.open(temp_file_path)
        st.write("Extracted Images:")
        
        image_list = []
        zip_file_path = os.path.join(os.getcwd(), "extracted_images.zip")
        
        for i in range(len(doc)):
            for img in doc.get_page_images(i):
                base_image = doc.extract_image(img[0])
                image_data = base_image["image"]
                
                image_stream = io.BytesIO(image_data)
                st.image(image_stream, caption=f"Image from page {i+1}", use_column_width=True)
                
                # Adding image data to the list
                image_list.append(image_data)
        
        # Create a zip file containing all the images
        with zipfile.ZipFile(zip_file_path, 'w') as zipf:
            for i, img_data in enumerate(image_list):
                zipf.writestr(f'image_{i+1}.png', img_data)
        
        # Adding download all images button
        if st.button('Prepare ZIP with all the images'):
            with open(zip_file_path, 'rb') as f:
                st.download_button(
                    label="Download Zip File",
                    data=f,
                    file_name="extracted_images.zip",
                    mime="application/zip"
                )
        
        # Close the document and delete the temporary file after processing
        doc.close()
        os.remove(temp_file_path)
        if os.path.exists(zip_file_path):
            os.remove(zip_file_path)
    else:
        st.write("Failed to upload the file.")

st.markdown('## Create with ❤️‍🔥 by Yuval Avidani @HACKIT.CO.IL 🔥')
