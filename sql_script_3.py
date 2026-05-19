import streamlit as st
import pandas as pd 
import io 
import re
from charset_normalizer import from_bytes
import csv
import datetime as dt
ts = dt.datetime.now().strftime("%y%m%d%H%M%S")
st.title("CSV/Excel to SQL Table Generator`(Multiple tables)`")
st.write("This tool converts CSV and Excel files into ready-to-use **PostgreSQL/MySQL** table creation scripts. This tool has been updated to allow generation of multiple table at onces. Options for table and column cleaning has been added for more data control...")
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


def psql_script(df,table_name:str) -> str:
    def psql_create(df:pd.DataFrame,tb):
        df = df 
        tb = table_name
        script = f"""CREATE TABLE IF NOT EXISTS "{tb}" """
        cols_def = []
        for x in df:
            cols_def.append(f'''"{x}" TEXT''')
        return script + "(" + ",\n".join (cols_def) + " );\n\n"

    def psql_insert(df,tb):
        df = df 
        tb = table_name
        script = f"""INSERT INTO "{tb}" """
        cols_def = []
        for x in df:
            cols_def.append(f'''"{x}"''')
        return script + "(" + ",\n".join (cols_def) + " )\n\n"
    def psql_val(df:pd.DataFrame):
        import pandas as pd
        import polars as pl
        df = df.fillna("NULL")
        df = df.apply(lambda x: x.astype(str))
        df = df.replace({"":'NULL'})
        df = df.apply(lambda x: x.str.replace("'","''"))
        pl_df = pl.DataFrame(df)
        in_rows = pl_df.rows()
        temp_txt_list = []
        for y, x in enumerate(in_rows,1):
            temp_txt = """("""
            if y != len(in_rows):
                for p, q in enumerate(x,1):
                    if p != len(x) and q != 'NULL':
                        temp_txt = temp_txt + f"'{q}', "
                    elif p != len(x) and q == 'NULL':
                        temp_txt = temp_txt + f"{q}, "
                    elif p == len(x) and q == 'NULL':
                        temp_txt = temp_txt + f"{q}),\n"
                    elif p == len(x):
                        temp_txt = temp_txt + f"'{q}'),\n"
                temp_txt_list.append(temp_txt)
            else:
                for p, q in enumerate(x,1):
                    if p != len(x) and q != 'NULL':
                        temp_txt = temp_txt + f"'{q}',"
                    elif p != len(x) and q == 'NULL':
                        temp_txt = temp_txt + f"{q},"
                    elif p == len(x) and q == 'NULL':
                        temp_txt = temp_txt + f"{q})"
                    elif p == len(x):
                        temp_txt = temp_txt + f"'{q}')"
                temp_txt_list.append(temp_txt)
        return  "VALUES " + """""".join(temp_txt_list) + ";"

    return psql_create(df,table_name) + psql_insert(df,table_name) + psql_val(df)


# for mysql script 

def mysql_script(df,table_name:str) -> str:
    def mysql_create(df:pd.DataFrame,tb):
        df = df 
        tb = table_name
        script = f"""CREATE TABLE IF NOT EXISTS `{tb}` """
        cols_def = []
        for x in df:
            cols_def.append(f"`{x}` TEXT")
        return script + "(" + ",\n".join (cols_def) + " );\n\n"

    def mysql_insert(df,tb):
        df = df 
        tb = table_name
        script = f"""INSERT INTO `{tb}` """
        cols_def = []
        for x in df:
            cols_def.append(f"`{x}`")
        return script + "(" + ",\n".join (cols_def) + " )\n\n"
    
    def mysql_val(df:pd.DataFrame):
        import pandas as pd
        import polars as pl
        df = df.fillna("NULL")
        df = df.apply(lambda x: x.astype(str))
        df = df.replace({"":'NULL'})
        df = df.apply(lambda x: x.str.replace("'","\\'"))
        pl_df = pl.DataFrame(df)
        in_rows = pl_df.rows()
        temp_txt_list = []
        for y, x in enumerate(in_rows,1):
            temp_txt = """("""
            if y != len(in_rows):
                for p, q in enumerate(x,1):
                    if p != len(x) and q != 'NULL':
                        temp_txt = temp_txt + f"'{q}', "
                    elif p != len(x) and q == 'NULL':
                        temp_txt = temp_txt + f"{q}, "
                    elif p == len(x) and q == 'NULL':
                        temp_txt = temp_txt + f"{q}),\n"
                    elif p == len(x):
                        temp_txt = temp_txt + f"'{q}'),\n"
                temp_txt_list.append(temp_txt)
            else:
                for p, q in enumerate(x,1):
                    if p != len(x) and q != 'NULL':
                        temp_txt = temp_txt + f"'{q}',"
                    elif p != len(x) and q == 'NULL':
                        temp_txt = temp_txt + f"{q},"
                    elif p == len(x) and q == 'NULL':
                        temp_txt = temp_txt + f"{q})"
                    elif p == len(x):
                        temp_txt = temp_txt + f"'{q}');"
                temp_txt_list.append(temp_txt)
        return  "VALUES " + """""".join(temp_txt_list)
    return mysql_create(df,table_name) + mysql_insert(df,table_name) + mysql_val(df)





encod = "utf-8"
data = ""

files = st.file_uploader("**Upload your data**",
                        help="Only csv, txt, tsv and excel file are supported",
                        type=['csv','tsv','xlsx','txt'],
                        accept_multiple_files=True
                        )

if files:
    mysql_script_lists = []
    psql_script_list = []
    with st.expander("Clean table and column name (convert to **snake_case**)"):
        col1, col2 = st.columns(2,border=True)
        with col1:
            clean_tb = st.toggle(":blue[Clean **table name**]")
        with col2:
            clean_cols = st.toggle(":blue[Clean **column name**]")
    for toggle_key, file in enumerate(files):
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
            with st.expander(f"Preview `{table_name}`"):
                st.dataframe(data.head())
                st.write(f"The data you uploaded has `{data.shape[0]:,}` row(s) and `{data.shape[1]:,}` column(s)")
            psql_script_list.append(psql_script(
                data,table_name
            ))
            mysql_script_lists.append(
                mysql_script(
                    data,table_name
                )
            )
  



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
        data_table = """SET NAMES utf8mb4;\n\n""" + "\n\n".join(mysql_script_lists)
        st.download_button(
            "Download as **`mysql`** data script",
            data=data_table.encode("utf-8",errors="replace").decode("utf-8"),
            mime="text/plain",
            file_name=f"mysql_script_{ts}.sql")  
