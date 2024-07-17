import streamlit as st
from authentificate import check_password
from utils import (project_indexes,flat_index_list)

########## APP start ###########
st.set_page_config(layout="wide")

# Authorise user
if not check_password():
    st.stop()

# Get input parameters
st.markdown('### Please select testing parameters ')

selected_index = None
search_option = st.radio(
    "Choose Specific Indexes if you want to search one or more different indexes, choose "
    "All Project Indexes to select all indexes within a project.",
    ['Specific Indexes', 'All Project Indexes'])

if search_option == 'Specific Indexes':
    selected_indexes = st.multiselect('Please choose one or more indexes', flat_index_list, default=None,
                                      placeholder="Select one or more indexes")
    if selected_indexes:
        selected_index = ",".join(selected_indexes)
        st.write(f"You've selected: {', '.join(selected_indexes)}")
    else:
        selected_index = None
else:
    project_choice = st.selectbox('Please choose a project', list(project_indexes.keys()), index=None,
                                  placeholder="Select project")
    if project_choice:
        selected_indexes = project_indexes[project_choice]
        selected_index = ",".join(selected_indexes)
        st.write(f"You've selected: {', '.join(selected_indexes)}")

threshold = st.number_input("Please input a threshold you'd like to test",
                            min_value=0.0,
                            max_value=1.0,
                            value=0.5,
                            step=0.05)
st.write("You've selected", threshold)

prompt = st.text_input("Input the prompt you'd like to test")
st.write("You've selected", prompt)

selected_start_date = st.date_input("Select start date for the timeframe you'd like to test:")
formatted_start_date = selected_start_date.strftime("%Y-%m-%d")
st.write("You've selected start date:", selected_start_date)
selected_end_date = st.date_input("Select end date for the timeframe you'd like to test:")
formatted_end_date = selected_end_date.strftime("%Y-%m-%d")
st.write("You've selected end date:", selected_start_date)


