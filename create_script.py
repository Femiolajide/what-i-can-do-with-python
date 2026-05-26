import pandas as pd 
import sql_dtypes as sdtyp
def psql_script(df,table_name:str,guess_dtype:bool) -> str:
    def psql_create(df:pd.DataFrame,tb):
        if guess_dtype:
            df = df 
            tb = table_name
            script = f"""CREATE TABLE IF NOT EXISTS "{tb}" """
            cols_def = []
            for x,y in zip(df,sdtyp.psql_dtp_df(df)):
                cols_def.append(f'''"{x}" {y}''')
            return script + "(" + ",\n".join (cols_def) + " );\n\n"
        else:
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

def mysql_script(df,table_name:str,guess_dtype:bool) -> str:
    def mysql_create(df:pd.DataFrame,tb):
        if guess_dtype:
            df = df 
            tb = table_name
            script = f"""CREATE TABLE IF NOT EXISTS `{tb}` """
            cols_def = []
            for x,y in zip(df,sdtyp.mysql_dtp_df(df)):
                cols_def.append(f"`{x}` {y}")
            return script + "(" + ",\n".join (cols_def) + " );\n\n"
        else:
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

