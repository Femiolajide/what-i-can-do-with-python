import streamlit as st
import pandas as pd 
import io 
import re
from charset_normalizer import from_bytes
import csv
import datetime as dt
ts = dt.datetime.now().strftime("%y%m%d%H%M%S")

def extention(x):
    import re
    return re.findall(r"\..+$",x)[0]

def psql_script(df,table_name:str) -> str:
    def clean_name(txt:str):
        import re
        txt = txt.lower()
        txt = re.sub(r"\s{2,}"," ",txt)
        return re.sub(r"[^a-z0-9_]","_",txt)
    table_name = clean_name(table_name)
    def psql_val(df):
        import pandas as pd
        import polars as pl
        df = df.fillna("NULL")
        df = df.apply(lambda x: x.astype(str))
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
                        temp_txt = temp_txt + f"{q}, "
                    else:
                        temp_txt = temp_txt + f"'{q}'),\n"
                temp_txt_list.append(temp_txt)
            else:
                for p, q in enumerate(x,1):
                    if p != len(x) and q != 'NULL':
                        temp_txt = temp_txt + f"'{q}',"
                    elif p != len(x) and q == 'NULL':
                        temp_txt = temp_txt + f"{q},"
                    elif p == len(x) and q == 'NULL':
                        temp_txt = temp_txt + f"{q},"
                    elif p == len(x):
                        temp_txt = temp_txt + f"'{q}')"
                temp_txt_list.append(temp_txt)
        return  "VALUES " + """""".join(temp_txt_list)

    def psql_create(df,table_name:str):
        from pandas.io.sql import get_schema
        import re
        df = df.rename(columns=lambda x: clean_name(x))
        df = df.apply(lambda x: x.astype(str))
        script = get_schema(df,table_name) + ";\n\n"
        script_2 = re.sub(r"^CREATE TABLE","INSERT INTO",script)
        script_2 = re.sub(r' [A-Z]+(?=,)| [A-Z]+(?=\n\);)',"",script_2).rstrip("\n;") + "\n\n"
        script_update = script.replace("CREATE TABLE",
                                       "CREATE TABLE IF NOT EXISTS")
        return script_update + script_2
    return psql_create(df,table_name) + psql_val(df)




encod = "utf-8"
data = ""

file = st.file_uploader("**Upload your data**",
                        help="Only csv, txt, tsv and excel file are supported"
                        )

if file:
    if re.search(r"\.tsv$|\.csv$|\.txt$|\.xlsx$|\.xls$",file.name):
        table_name = re.sub(r"\.tsv$|\.csv$|\.txt$|\.xlsx$|\.xls$","",file.name)
        if re.search(r"\.tsv$|\.csv$|\.txt$",file.name):
            raw = file.getvalue()
            encod = from_bytes(raw).best().encoding
            sample_txt = raw.decode(encoding="utf-8",errors="ignore")
            delimiter = csv.Sniffer().sniff(sample_txt).delimiter
            if delimiter.strip() and delimiter != '\t':
                try:
                    data = pd.read_csv(file,encoding=encod,sep=delimiter)
                except:
                    st.error("ERROR! Check your file again, does it have proper table structure?")
            else:
                try:
                    data = pd.read_csv(file,encoding=encod,sep="\t")
                except:
                    st.error("ERROR! Check your file again, does it have proper table structure?")
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
            st.write(f"The data you uploaded has `{data.shape[0]:,}` row(s) and `{data.shape[1]:,}` column(s)")
        data_table = psql_script(data,table_name)
        data_table = """SET client_encoding = 'UTF8';\n\n""" + data_table
        st.download_button(
            "Download SQL data script",
            data=data_table.encode("utf-8",errors="replace").decode("utf-8"),
            mime="text/plain",
            file_name=f"sql_script_{ts}.txt")
    