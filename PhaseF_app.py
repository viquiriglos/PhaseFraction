import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
from numpy import asarray
from pathlib import Path


#---- PATH SETTINGS---
current_dir = Path(__file__).parent if "__file__" in locals() else Path.cwd()
#css_file = current_dir/"styles"/"main.css"
example_pic = current_dir/"assets"/"example.jpg"

#---GENERAL SETTINGS----
PAGE_TITLE = "Phase Fraction App"
st.set_page_config(page_title=PAGE_TITLE)

#----LOAD CSS
#with open(css_file) as f:
#    st.markdown("<style>{}</style>".format(f.read()), unsafe_allow_html=True)

st.write("""
# Phase Fraction App
- This app allows to find out the percentage of dark and white areas in an image. 
- A threshold can be set in order to define the limit between which are considered 'dark' or 'light' areas.
- Eventhough it's not a real measure of the phase fraction it could provide an adequate value for this parameter given the proper conditions. 
- Be carefull to crop out regions of the image that don't belong to the sample itself like scale bars.
""")

#-----SideBar
st.sidebar.header('User Input File and Threshold')

# Collects user input file and options
uploaded_file = st.sidebar.file_uploader("Upload your image (png, jpg or tif)", type=["png", "jpg", "tif"])
threshold = st.sidebar.slider('Choose a threshold', 0, 255, 100)


#-----Main Panel
# Displays the user input features
st.subheader('Original and Filtered Images')
numpydata = np.array([])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Raw Image')
    numpydata = asarray(image)
else:
    image = Image.open(example_pic)
    st.image(image, caption='Example Raw Image')
    numpydata = asarray(image)

shape=numpydata.shape
pixels=shape[0]*shape[1]
photo_masked=np.where(numpydata>threshold,255,0)
st.image(photo_masked, caption='Filtered Image')
st.write("The threshold is ", threshold)

#--- Makes the calculation
photo_binary=np.where(numpydata<threshold,1,0) #if the color of the pixel is under the threshold it becomes equal to one=white, if not it's a zero=black
dark=np.sum(photo_binary)/3 # I add all the pixels equal to one and divide by 3 (the number of channels)
light=pixels-dark
light_fraction=light/pixels
dark_fraction=1-light_fraction

#--- Just to check the results are correct
   
#st.write("Number of Light pixels:", light)
#st.write("Number of Dark pixels:", dark)

# Shows the results
st.subheader('Phase Fraction')
df=pd.DataFrame([dark_fraction, light_fraction], ["Dark Areas","Light Areas"], columns=["Percentage"])
st.write(df)
st.write("Image shape (h,w) in px:", shape[0], shape[1])
st.write("Total number of pixels:", pixels)
st.write("""Note: in the case of an image having regions that don't belong to the specimen (like the one in the Example)
 the threshold can be adjusted to obtain the portion of the image that must not be taken into account for calculation. 
 In the example picture for a threshold of 200 the light area is 0.2091 which in pixels is 0.2191*132190
and this amount of pixels should be removed from the phase fraction computation.""")
#st.write("Total number of pixels:", pixels)


