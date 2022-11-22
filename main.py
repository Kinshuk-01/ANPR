import streamlit as st
import os
from PIL import Image
import cv2
import numpy as np
import pandas as pd
import pytesseract
from datetime import datetime, date

now = datetime.now()
current_time = now.strftime("%H:%M:%S")
download_path = "Downloads/"

st.set_page_config(
    page_title="Auto NPR",
    page_icon="✨",
    layout="centered",
    initial_sidebar_state="expanded",
)

pytesseract.pytesseract.tesseract_cmd="C:/Program Files/Tesseract-OCR/tesseract.exe"

cascade= cv2.CascadeClassifier("haarcascade_russian_plate_number.xml")
states={"AN":"Andaman and Nicobar",
    "AP":"Andhra Pradesh","AR":"Arunachal Pradesh",
    "AS":"Assam","BR":"Bihar","CH":"Chandigarh",
    "DN":"Dadra and Nagar Haveli","DD":"Daman and Diu",
    "DL":"Delhi","GA":"Goa","GJ":"Gujarat",
    "HR":"Haryana","HP":"Himachal Pradesh",
    "JK":"Jammu and Kashmir","KA":"Karnataka","KL":"Kerala",
    "LD":"Lakshadweep","MP":"Madhya Pradesh","MH":"Maharashtra","MN":"Manipur",
    "ML":"Meghalaya","MZ":"Mizoram","NL":"Nagaland","OD":"Odissa",
    "PY":"Pondicherry","PN":"Punjab","RJ":"Rajasthan","SK":"Sikkim","TN":"TamilNadu",
    "TR":"Tripura","UP":"Uttar Pradesh", "WB":"West Bengal","CG":"Chhattisgarh",
    "TS":"Telangana","JH":"Jharkhand","UK":"Uttarakhand"}

@st.cache(persist=True,allow_output_mutation=True,show_spinner=False,suppress_st_warning=True)
def download_success():
    st.balloons()
    st.success('✅ Download Successful !!')

def extract_num(img_filename):
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    today_date = date.today()
    img=cv2.imread(img_filename)
    
    #Img To Gray
    gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    nplate=cascade.detectMultiScale(gray,1.1,4)

    #crop portion
    for (x,y,w,h) in nplate:
        wT,hT,cT=img.shape
        a,b=(int(0.02*wT),int(0.02*hT))
        plate=img[y+a:y+h-a,x+b:x+w-b,:]

        #make the img more darker to identify LPR
        kernel=np.ones((1,1),np.uint8)
        plate=cv2.dilate(plate,kernel,iterations=1)
        plate=cv2.erode(plate,kernel,iterations=1)
        plate_gray=cv2.cvtColor(plate,cv2.COLOR_BGR2GRAY)
        (thresh,plate)=cv2.threshold(plate_gray,127,255,cv2.THRESH_BINARY)

        #read the text on the plate
        read=pytesseract.image_to_string(plate)
        read=''.join(e for e in read if e.isalnum())
        stat=read[0:2]
        cv2.rectangle(img,(x,y),(x+w,y+h),(51,51,255),2)
        cv2.rectangle(img,(x-1,y-40),(x+w+1,y),(51,51,255),-1)
        cv2.putText(img,read,(x,y-10),cv2.FONT_HERSHEY_SIMPLEX,0.9,(255,255,255),2)
        
        #Dislaying our Final image
        st.image(img, caption='This is how your final image looks like 😉')
        
        #Displaying Plate Info on SideBar
        st.sidebar.title("Number Plate Info")
        st.sidebar.subheader("Cropped Image of plate")
        st.sidebar.image(plate)
        if read: 
            st.sidebar.write("The number read by the machine is: ", read)
        else: 
            st.sidebar.subheader("Machine is not able to retrive the number")
        if stat in states:
            st.sidebar.write("The car belongs to state: ", states[stat])
        else:
            st.sidebar.subheader("The car dosn't belongs to India")    
            
        st.sidebar.write("The car enter at: ", current_time)
        st.sidebar.write("The car entered at date: ", date.today())
        st.sidebar.markdown("---")
        
        #Downloading our Final image
        downloaded_image = os.path.abspath(os.path.join(download_path,str("output_"+uploaded_file.name)))
        
        img_base64 = Image.fromarray(img)
        img_base64.save(downloaded_image, format="JPEG")
                    
        with open(downloaded_image, "rb") as file:
            if uploaded_file.name.endswith('.jpg') or uploaded_file.name.endswith('.JPG'):
                if st.download_button(
                                        label="Download Output Image 📷",
                                        data=file,
                                        file_name=str("output_"+uploaded_file.name),
                                        mime='image/jpg'
                                     ):
                    download_success()
            if uploaded_file.name.endswith('.jpeg') or uploaded_file.name.endswith('.JPEG'):
                if st.download_button(
                                        label="Download Output Image 📷",
                                        data=file,
                                        file_name=str("output_"+uploaded_file.name),
                                        mime='image/jpeg'
                                     ):
                    download_success()

            if uploaded_file.name.endswith('.png') or uploaded_file.name.endswith('.PNG'):
                if st.download_button(
                                        label="Download Output Image 📷",
                                        data=file,
                                        file_name=str("output_"+uploaded_file.name),
                                        mime='image/png'
                                     ):
                    download_success()

            if uploaded_file.name.endswith('.bmp') or uploaded_file.name.endswith('.BMP'):
                if st.download_button(
                                        label="Download Output Image 📷",
                                        data=file,
                                        file_name=str("output_"+uploaded_file.name),
                                        mime='image/bmp'
                                     ):
                    download_success()
                    
            st.markdown("---")
    

# ----------------- PROGRAM STARTS HERE ---------------
st.title(' Automatic Number Plate Recognition 🚘 🚙')

st.info('✨ Supports all popular image formats 📷 - PNG, JPG, BMP 😉')
uploaded_file = st.file_uploader("Upload Image of car's number plate 🚓", type=["png","jpg","bmp","jpeg"])

if uploaded_file is not None:
    with open(os.path.join(uploaded_file.name),"wb") as f:
        f.write((uploaded_file).getbuffer())
    with st.spinner(f"Working... 💫"):
        uploaded_image = os.path.abspath(os.path.join(uploaded_file.name))
        
    extract_num(uploaded_image)
    
    
else:
    st.warning('⚠ Please upload your Image 😯')
    
st.markdown("<center><strong> Made with ❤️ by: <strong> <br>Kinshuk Chauhan (20BCS4917) <br>Ashutosh Kumar (20BCS4960) <br>Harshit Gupta (20BCS4925) <br>Saket Singh (20BCS9299) </a></center><hr>", unsafe_allow_html=True)

    
