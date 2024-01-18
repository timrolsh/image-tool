import streamlit as st
import mainScript as ms

st.set_page_config(page_title="Image Tool")
st.write('# Skim Image Tool!')

st.write(' --- ')


left_column, middle_column, right_column = st.columns(3)

counter = 0
with left_column:
    st.write('###  *Instructions*  ')
    st.write('Step 1: Click setting')
    st.write('Step 2: Put image files in the newly created input folder')
    st.write('Step 3: Run setting again')
    st.write("Step 4: Put in what settings you want in the newly created Input_setting.xlsx file and save (Ctrl+S) when you're done")
    st.write(
        'Step 5: Click the Run button under Setting and images will be in the output folder!')


setting = right_column.button('Setting')
run = right_column.button('Run')

if setting:
    right_column.write(ms.Setting())

if run:
    right_column.write(ms.Run())
