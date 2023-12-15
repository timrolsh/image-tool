import streamlit as st
import mainScript as ms

    
st.write('# Skim Image Tool!')
    

st.write(' --- ')

left_column, middle_column, right_column = st.columns(3)
with left_column:    
    st.write('###  *Instructions*  ')
    st.write('Step 1: Run setting')
    st.write('Step 2: Put image files in the newly created input folder')
    st.write('Step 3: Run setting again')
    st.write("Step 4: Put in what settings you want in the newly created Input_setting.xlsx file and save (Ctrl+S) when you're done")
    st.write('Step 5: Click the Run button under Setting and images will be in the output folder!')


if right_column.button('Setting'):
    ms.Setting()
if right_column.button('Run'):
    ms.Run()