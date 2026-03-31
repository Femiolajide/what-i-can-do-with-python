import streamlit as st
import pandas as pd 
import io 
import re
from PIL import Image, ImageDraw, ImageFont
from charset_normalizer import from_bytes
import csv
st.title("Create a Customized Certificate at once")
st.write("This app allows you to get ....")
st.markdown("---")
def extention(x):
    import re
    return re.findall(r"\..+$",x)[0]
def validate_names(x):
    import re 
    if re.match()
encod = "utf-8"
data = ""
choice = st.selectbox("Choose an option",
             ["Enter the raw data","Upload the raw data"])
if choice == "Enter the raw data":
    data = pd.DataFrame(columns=["name","certification_date"])
    st.data_editor(data=data,
                hide_index=True,
                num_rows="dynamic",
                placeholder="Type here...",
                column_config={"certification_date":st.column_config.DateColumn(
                    help="Type the date of certification in **`dd/mm/yyyy`** format",
                    format="MMMM D, YYYY",
                    required=True
                ),
                "name":st.column_config.TextColumn(
                    max_chars=35,
                    help="Type the name(s) to be written on the certificate (not more than `35` characters)",
                    required=True,
                    validate="^[a-zA-Z]+\s?[a-zA-Z]+\s?[a-zA-Z]*$"
                )})
else:
    file = st.file_uploader("**Upload your data**",
                            help="Only csv, txt, tsv and excel file are supported",)
    if file:
        if re.search(r"\.tsv$|\.csv$|\.txt$|\.xlsx$|\.xls$",file.name):
            if re.search(r"\.tsv$|\.csv$|\.txt$",file.name):
                raw = file.getvalue()
                encod = from_bytes(raw).best().encoding
                sample_txt = raw .decode(encoding=encod,errors="ignore")
                delimiter = csv.Sniffer().sniff(sample_txt).delimiter
                data = pd.read_csv(file,encoding=encod,sep=delimiter)
            else:
                sheets = [*pd.read_excel(file,sheet_name=None).keys()]
                if len(sheets) == 1:
                    data = pd.read_excel(file)
                else:
                    sheet = st.selectbox("### Select the sheet you want to pick data from",
                                sheets)
                    data = pd.read_excel(file, sheet_name=sheet)
        else:
            st.error(f"ERROR: You can only upload csv, txt, tsv or excel file NOT '{extention(file.name)}' file")
        if not isinstance(data,str):
            with st.expander("Preview data"):
                st.dataframe(data.head())
            columns = [*data.columns]
            with st.expander("Select column for name and date"):
               col1, col2 = st.columns([5,3.5])
               with col1:
                   name = st.selectbox("Select a column for names",
                                    columns)
               with col2:
                   date = st.selectbox("Select a column for date",
                                columns)
            data = data[[name,date]]
        
