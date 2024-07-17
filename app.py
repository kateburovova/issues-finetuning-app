import os
import streamlit as st
import time

import plotly.express as px
import streamlit.components.v1 as components

from langchain import hub
from datetime import datetime
from langchain import callbacks
from elasticsearch import Elasticsearch
from elasticsearch import BadRequestError
from elasticsearch.exceptions import NotFoundError
from angle_emb import AnglE, Prompts
from langchain_openai import ChatOpenAI
from authentificate import check_password
from utils import (display_distribution_charts,populate_default_values, project_indexes,
                   populate_terms,create_must_term, create_dataframe_from_response,flat_index_list,
                   search_elastic_below_threshold)
#
#
# # Init Langchain and Langsmith services
# os.environ["LANGCHAIN_TRACING_V2"] = "true"
# os.environ["LANGCHAIN_PROJECT"] = f"streamlit_app : issues_finetuning : development"
# os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"
# os.environ["LANGCHAIN_API_KEY"] = st.secrets['ld_rag']['LANGCHAIN_API_KEY']
# os.environ["LANGSMITH_ACC"] = st.secrets['ld_rag']['LANGSMITH_ACC']


# # Init openai model
# OPENAI_API_KEY = st.secrets['ld_rag']['OPENAI_KEY_ORG']
# llm_chat = ChatOpenAI(temperature=0.0, openai_api_key=OPENAI_API_KEY,
#              model_name='gpt-4-1106-preview')

es_config = {
    'host': st.secrets['ld_rag']['ELASTIC_HOST'],
    'port': st.secrets['ld_rag']['ELASTIC_PORT'],
    'api_key': st.secrets['ld_rag']['ELASTIC_API']
}

########## APP start ###########
st.set_page_config(layout="wide")

# description
st.markdown('App relies on data, collected and enriched by our team and provides citations for all sources used for '
            'answers. \n'
            'If you are running this app from a mobile device, tap on any '
            'empty space to apply changes to input fields. '
            'If you experience any technical issues, please [submit the form](https://docs.google.com/forms/d/e/1FAIpQLSfZTr4YoXXsjOOIAMVGYCeGgXd6LOsCQusctJ7hZODaW5HzGQ/viewform?pli=1) by selecting "LD app Technical Issue" for '
            'the type of request. To give feedback for request output, '
            'please use the feedback form at the end of the page.')

# Authorise user
if not check_password():
    st.stop()

# Get input parameters
st.markdown('### Please select search parameters ')

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

