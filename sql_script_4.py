import streamlit as st
import pandas as pd 
import io 
import re
from charset_normalizer import from_bytes
import csv
import datetime as dt
import sql_dtypes as sdty
import create_script as cs
ts = dt.datetime.now().strftime("%y%m%d%H%M%S")
st.title("CSV/Excel to SQL Table Generator`(Multiple tables & Auto-detect data types)`")
st.write("This tool converts CSV and Excel files into ready-to-use **PostgreSQL/MySQL** table creation scripts. This tool has been updated to allow generation of multiple table at onces. Options for auto-detect datatype, table and column cleaning has been added for more data control...")
st.markdown("---")

# Function to extract file extension
def extention(x):
    import re
    return re.findall(r"\..+$",x)[0]

def clean_name(txt:str):
    import re
    txt = re.sub(r"\s{2,}"," ",txt)
    txt = re.sub(r"[^aA-zZ0-9_]","_",txt)
    for x in txt:
        if str(x).isupper():
            txt = txt.replace(x,f"_{x}")
    txt = txt.strip("_").lower()
    txt = re.sub(r'_{2,}','_',txt)
    return txt





encod = "utf-8"
data = ""

files = st.file_uploader("**Upload your data**",
                        help="Only csv, txt, tsv and excel file are supported",
                        type=['csv','tsv','xlsx','txt'],
                        accept_multiple_files=True
                        )

if files:
    st.subheader("Column and Datatype Options")
    with st.expander("Clean table and column name (convert to **snake_case**)"):
        col1, col2 = st.columns(2,border=True)
        with col1:
            clean_tb = st.toggle(":blue[Clean **table name**]")
        with col2:
            clean_cols = st.toggle(":blue[Clean **column name**]")
    with st.expander("Guess datatype"):
            guess_dtype = st.toggle(":blue[Auto-detect column **dataype**]")
            if guess_dtype:
                dtp = st.radio("Select database",
                         ['MySQL',"PostgreSQL"])
    # st.write("---")
    st.subheader("Table Preview")
    mysql_script_list_dtp = []
    psql_script_list_dtp = []
    psql_script_list = []
    mysql_script_list = []
    file_check = []
    for toggle_key, file in enumerate(files):
        file_check.append(re.sub(r"\.tsv$|\.csv$|\.txt$|\.xlsx$|\.xls$","",file.name))
        if len(set(file_check)) != len(file_check):
            # a = FileExistsError ("Duplicate is not allowed")
            st.warning("WARNING!!! You have a file with the same name")    
        if re.search(r"\.tsv$|\.csv$|\.txt$|\.xlsx$|\.xls$",file.name):
            table_name = re.sub(r"\.tsv$|\.csv$|\.txt$|\.xlsx$|\.xls$","",file.name)
            if clean_tb:
                table_name = clean_name(table_name)
            if re.search(r"\.tsv$|\.csv$|\.txt$",file.name):
                raw = file.getvalue()
                encod = from_bytes(raw).best().encoding
                sample_txt = raw.decode(encoding="utf-8",errors="ignore")
                delimiter = csv.Sniffer().sniff(sample_txt).delimiter
                if delimiter.strip() and delimiter != '\t':
                    try:
                        data = pd.read_csv(file,encoding=encod,sep=delimiter,na_filter=False)
                    except:
                        st.error("ERROR! Check your file again, does it have proper table structure?")
                else:
                    try:
                        data = pd.read_csv(file,encoding=encod,sep="\t",na_filter=False)
                    except:
                        st.error("ERROR! Check your file again, does it have proper table structure?")
            else:
                sheets = [*pd.read_excel(file,sheet_name=None).keys()]
                if len(sheets) == 1:
                    data = pd.read_excel(file,na_filter=False)
                else:
                    sheet = st.selectbox("### Select the sheet you want to pick data from",
                                sheets)
                    data = pd.read_excel(file, sheet_name=sheet,
                                        na_filter=False)
        else:
            st.error(f"ERROR: You can only upload csv, txt, tsv or excel file NOT '{extention(file.name)}' file")
        if not isinstance(data,str):
            if clean_cols:
                data = data.rename(
                    columns=lambda x: clean_name(x)
                )

        col_dtp = ["TEXT"] * data.shape[1]
        if guess_dtype:
            if dtp == 'MySQL':
                col_dtp = sdty.mysql_dtp_df(data)
            else:
                col_dtp = sdty.psql_dtp_df(data)

        with st.expander(f"Preview `{table_name}`"):
            kol = pd.MultiIndex.from_arrays(
                    [data.columns,col_dtp])
            data_head = data.head()
            bool_col = data_head.select_dtypes(bool).columns
            data_head[bool_col] = data_head[bool_col].astype(str)
            data_head.columns = kol
            data_head.index = [""]* data_head.shape[0]
            data_head.index.name = "DATATYPE"
            st.dataframe(data_head,hide_index=False)
            st.write(f"The data you uploaded has `{data.shape[0]:,}` row(s) and `{data.shape[1]:,}` column(s)")

            if guess_dtype and dtp == "PostgreSQL":
                psql_script_list_dtp.append(cs.psql_script(
                    data,table_name,guess_dtype=True
                ))
            elif guess_dtype and dtp == 'MySQL':
                mysql_script_list_dtp.append(cs.mysql_script(
                    data,table_name,guess_dtype=True
                ))
            else:
                psql_script_list.append(cs.psql_script(
                    data,table_name,guess_dtype=False
                ))
                mysql_script_list.append(cs.mysql_script(
                    data,table_name,guess_dtype=False
                ))
    
    if not guess_dtype:
        dbms = st.selectbox("Choose a database management system",
                            ["PostgreSQL","MySQL"])
        if dbms == "PostgreSQL":
            data_table = """SET client_encoding = 'UTF8';\n\n""" + "\n\n".join(psql_script_list)
            st.download_button(
                "Download as **`postgresql`** data script",
                data=data_table.encode("utf-8",errors="replace").decode("utf-8"),
                mime="text/plain",
                file_name=f"psql_script_{ts}.sql")
        else:
            data_table = """SET NAMES utf8mb4;\n\n""" + "\n\n".join(mysql_script_list)
            st.download_button(
                "Download as **`mysql`** data script",
                data=data_table.encode("utf-8",errors="replace").decode("utf-8"),
                mime="text/plain",
                file_name=f"mysql_script_{ts}.sql")  
    
    else:
        if dtp == "PostgreSQL":
            data_table = """SET client_encoding = 'UTF8';\n\n""" + "\n\n".join(psql_script_list_dtp)
            st.download_button(
                "Download as **`postgresql`** data script",
                data=data_table.encode("utf-8",errors="replace").decode("utf-8"),
                mime="text/plain",
                file_name=f"psql_script_{ts}.sql")
        else:
            data_table = """SET NAMES utf8mb4;\n\n""" + "\n\n".join(mysql_script_list_dtp)
            st.download_button(
                "Download as **`mysql`** data script",
                data=data_table.encode("utf-8",errors="replace").decode("utf-8"),
                mime="text/plain",
                file_name=f"mysql_script_{ts}.sql")  
