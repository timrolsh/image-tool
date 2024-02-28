import streamlit as st
import mainScript as ms
import create_excel as ce
import os


def mainPage():
    st.set_page_config(page_title="Image Tool")
    st.write("# Skim Image Tool!")
    st.write(" --- ")

    left_column, middle_column, right_column = st.columns(3)

    with left_column:
        with st.container(border=True):
            st.write("###  *Instructions*  ")
            st.write("Check which functions you want to use:")
            st.write("If resize/rename is checked, run the setting button")
            st.write(
                "When setting is run, it will create an excel with each file name and the current dimensions, with seperate boxes to adjust the name and target size"
            )

    with middle_column:
        with st.container(border=True):
            rembg = st.checkbox("Remove Background", value=True)
            crop_im = st.checkbox("Crop to Image", value=True)
            resize = st.checkbox("Resize", value=False)
            rename = st.checkbox("Rename", value=False)

    with right_column:
        kSize = st.slider("kSize", 1, 15, 7, 2)

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
        right_column.write(ms.Run(rembg, crop_im, resize, rename, kSize))
        show_im = st.button("See images here")
        if show_im:
            st.session_state.runpage = imagePage
            st.session_state.runpage()
            st.experimental_rerun()


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
