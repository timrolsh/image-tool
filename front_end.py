import streamlit as st
import mainScript as ms
import create_excel as ce
import os


def mainPage():

    st.set_page_config(page_title="Image Tool", layout="wide")
    st.write("# Skim Image Tool!")
    st.write(" --- ")

    left_column, middle_column, right_column = st.columns(3)

    with left_column:
        with st.container(border=True):
            st.write("###  *Instructions*  ")
            st.write("Check which functions you want to use:")
            st.write(
                "If resize/rename is checked, run the Create Excel button to make an excel sheet in the same directory where you can see all your files, current names, and where to rename/resize the images"
            )
            st.write(
                "When setting is run, it will create an input folder in the current directory where you place your images, then you have to run it again to create the output folder, where the results will be placed."
            )
            st.write("Once that's all set, click run after checking your desired functions.")
            st.write(
                'When done, a new button "Show Images" will appear that will show at least three of the images submitted'
            )

    with middle_column:
        with st.container(border=True):
            rembg = st.checkbox("Remove Background", value=True)
            crop_im = st.checkbox("Crop to Image", value=True)
            resize = st.checkbox("Resize", value=False)
            rename = st.checkbox("Rename", value=False)

    with right_column:
        st.info( # make into button options
            'kSize can be thought of as the "strength" of the background removal, so bigger number, more of the image will be removed...'
        )
        kSize = st.slider("Removal Strength", 1, 15, 7, 2)

    with middle_column:
        if resize or rename:
            create_button = st.button("Create Excel Sheet")
            if create_button:
                ce.create_excel()

    setting = right_column.button("Setting")
    if setting:
        right_column.write(ms.Setting())
    run = right_column.button("Run")

    if run:
        with st.spinner("Please wait... Processing"):
            right_column.write(ms.Run(rembg, crop_im, resize, rename, (kSize, kSize)))
        st.balloons()
            # show_im = st.button("See images here")
            # if show_im:
            #     st.session_state.runpage = imagePage
            #     st.session_state.runpage()
            #     st.experimental_rerun()


def imagePage():
    st.set_page_config(page_title="Image Tool")
    go_back = st.button("# <-- Go Back")
    if go_back:
        st.session_state.runpage = mainPage
        st.session_state.runpage()
        st.experimental_rerun()
    st.write("# Skim Image Tool!")
    st.write(" --- ")

    output_images = os.listdir("output")

    st.write("# Here's what a few of the images look like:")
    st.image("output/New.png")


mainPage()
