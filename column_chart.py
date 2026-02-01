import streamlit as st
import matplotlib.pyplot as plt 
import textwrap as tw
import seaborn as sns
import pandas as pd 
import random as rd 
st.title("Create your bar chart manually")
st.data_editor(data=pd.DataFrame(columns=["Category","Value"]),
               num_rows="dynamic",
               use_container_width=True,
               st.column_config=("Category":st.column_config.TextColumn("Category"))
               )
