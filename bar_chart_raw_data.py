import streamlit as st
import matplotlib.pyplot as plt 
import textwrap as tw
import seaborn as sns
import pandas as pd 
import random as rd 
import io
import datetime as dt
from charset_normalizer import from_bytes
import re
import csv 
def extention(x):
    import re
    return re.findall(r"\..+$",x)[0]

file = st.file_uploader("Upload your data",
                        help="Only csv, txt, tsv and excel file is supported",)
encod = "utf-8"
data = ""
if re.search(r"\.tsv$|\.csv$|\.txt$|\.xlsx$|\.xls$",file.name):
    if re.search(r"\.tsv$|\.csv$|\.txt$",file.name):
        raw = file.getvalue()
        encod = from_bytes(raw).best().encoding
        sample_txt = raw[:2048].decode(encoding=encod,errors="ignore")
        delimiter = csv.Sniffer().sniff(sample_txt).delimiter
        data = pd.read_csv(file,encoding=encod,sep=delimiter)
    else:
        data = pd.read_excel(file)
else:
    st.error(f"ERROR: You can only upload csv, txt, tsv or excel file NOT '{extention(file.name)}' file")
if not isinstance(data,str):
    if st.button("Preview data"):
        st.dataframe(data.head())



