# import pandas as pd
def psql_dtp_df(df):
    def psql_dtype(col:list):
        from natsort import natsorted as nt
        def int_convertible(col):
            try:
                [int(str(x)) for x in col]
                return True
            except (ValueError, IndexError):
                return False
        # validating integer types 
        def get_int(num):
            num = str(num)
            try:
                num = int(num)
                if num >= -32768 and num <= 32767:
                    return "SMALLINT"
                elif num >= -2147483648 and num <= 2147483647:
                    return "INTEGER"
                elif num >= -9223372036854775808 and num <= 9223372036854775807:
                    return "BIGINT"
                else:
                    return num
            except ValueError:
                return num
        # validating numeric type
        def get_float(num):
            num = str(num)
            if num.count(".") == 1:
                try:
                    num = float(num)
                    return "NUMERIC"
                except ValueError:
                    return num
            else:
                return num
        # validating date type 
        def get_date(x:str):
            import datetime as dt
            x = str(x).strip()
            try:
                x = dt.datetime.strptime(x, '%Y-%m-%d')
                return "DATE"
            except ValueError:
                return x
        # validating time type 
        def get_time(x:str):
            import datetime as dt
            x = str(x).strip()
            try:
                x = dt.datetime.strptime(x, '%H:%M:%S')
                return "TIME"
            except ValueError:
                return x
            
        # validating timestamp 
        def get_timestamp(x:str):
            import datetime as dt
            x = str(x).strip()
            try:
                x = dt.datetime.strptime(x, '%Y-%m-%d %H:%M:%S')
                return "TIMESTAMP"
            except ValueError:
                return x
        if col:
            max_col = nt(col)[-1]
            max_dtyp = get_int(max_col)
            col_float = [get_float(x) for x in col]
            col_float = [get_int(x) for x in col_float]
            col_date = [get_date(x) for x in col]
            col_time = [get_time(x) for x in col]
            col_dt = [get_timestamp(x) for x in col]
            col_bool_float =  [True if x == "NUMERIC"
                            or x == "BIGINT"  
                            or x == "INTEGER"
                            or x == "SMALLINT" else
                            False for x in col_float]
            col_bool_date = [True if x == "DATE" else
                            False for x in col_date]
            col_bool_time = [True if x == "TIME" else
                            False for x in col_time]
            col_bool_dt = [True if x == "TIMESTAMP" else
                            False for x in col_dt]
            # Boolean type check 
            chk_bool = list(set([str(x).lower() for x in col]))
            if len(chk_bool) == 2 and ('t' in chk_bool and 'f' in chk_bool):
                return "BOOL"
            elif len(chk_bool) == 2 and ('1' in chk_bool and '0' in chk_bool):
                return "BOOL"
            elif len(chk_bool) == 2 and ('true' in chk_bool and 'false' in chk_bool):
                return "BOOL"
            elif len(chk_bool) == 2 and ('y' in chk_bool and 'n' in chk_bool):
                return "BOOL"
            elif len(chk_bool) == 2 and ('on' in chk_bool and 'off' in chk_bool):
                return "BOOL"
            elif len(chk_bool) == 2 and ('yes' in chk_bool and 'no' in chk_bool):
                return "BOOL"
            elif int_convertible(col) and max_dtyp == "SMALLINT":
                return "SMALLINT"
            elif int_convertible(col) and max_dtyp == "INTEGER":
                return "INTEGER"
            elif int_convertible(col) and max_dtyp == "BIGINT":
                return "BIGINT"
            elif all(col_bool_float):
                return "NUMERIC"
            elif all(col_bool_date):
                return "DATE"
            elif all(col_bool_time):
                return "TIME"
            elif all(col_bool_dt):
                return "TIMESTAMP"

            else:
                return "TEXT"
        else:
            return "TEXT"

    dtyp_ls = []
    for x in df:
        f = df[x]
        d = [tt for tt in f if tt != '']
        if len(d) == 0:
            dtyp_ls.append("TEXT")
        else:
            dtyp_ls.append(psql_dtype(d))
    return dtyp_ls


def mysql_dtp_df(df):
    def mysql_dtype(col):
        from natsort import natsorted as nt
        def int_convertible(col):
            try:
                [int(str(x)) for x in col]
                return True
            except (ValueError, IndexError):
                return False
        # validating integer types 
        def get_int(num):
            num = str(num)
            try:
                num = int(num)
                if num >= -32768 and num <= 32767:
                    return "SMALLINT"
                elif num >= -2147483648 and num <= 2147483647:
                    return "INTEGER"
                elif num >= -9223372036854775808 and num <= 9223372036854775807:
                    return "BIGINT"
                else:
                    return num
            except ValueError:
                return num
        # validating numeric type
        def get_float(num):
            num = str(num)
            if num.count(".") == 1:
                try:
                    num = float(num)
                    return "NUMERIC"
                except ValueError:
                    return num
            else:
                return num
        # validating date type 
        def get_date(x:str):
            import datetime as dt
            x = str(x).strip()
            try:
                x = dt.datetime.strptime(x, '%Y-%m-%d')
                return "DATE"
            except ValueError:
                return x
        # validating time type 
        def get_time(x:str):
            import datetime as dt
            x = str(x).strip()
            try:
                x = dt.datetime.strptime(x, '%H:%M:%S')
                return "TIME"
            except ValueError:
                return x
            
        # validating timestamp 
        def get_timestamp(x:str):
            import datetime as dt
            x = str(x).strip()
            try:
                x = dt.datetime.strptime(x, '%Y-%m-%d %H:%M:%S')
                return "TIMESTAMP"
            except ValueError:
                return x
        if col:
            max_col = nt(col)[-1]
            max_dtyp = get_int(max_col)
            col_float = [get_float(x) for x in col]
            col_float = [get_int(x) for x in col_float]
            col_date = [get_date(x) for x in col]
            col_time = [get_time(x) for x in col]
            col_dt = [get_timestamp(x) for x in col]
            col_bool_float =  [True if x == "NUMERIC"
                            or x == "BIGINT"  
                            or x == "INTEGER"
                            or x == "SMALLINT" else
                            False for x in col_float]
            col_bool_date = [True if x == "DATE" else
                            False for x in col_date]
            col_bool_time = [True if x == "TIME" else
                            False for x in col_time]
            col_bool_dt = [True if x == "TIMESTAMP" else
                            False for x in col_dt]
            # Boolean type check 
            chk_bool = list(set([str(x).lower() for x in col]))
            if len(chk_bool) == 2 and ('1' in chk_bool and '0' in chk_bool):
                return "TINYINT"
            # elif len(chk_bool) == 2 and ('true' in chk_bool and 'false' in chk_bool):
            #     return "TINYINT"
            elif int_convertible(col) and max_dtyp == "SMALLINT":
                return "SMALLINT"
            elif int_convertible(col) and max_dtyp == "INTEGER":
                return "INTEGER"
            elif int_convertible(col) and max_dtyp == "BIGINT":
                return "BIGINT"
            elif all(col_bool_float):
                return "REAL"
            elif all(col_bool_date):
                return "DATE"
            elif all(col_bool_time):
                return "TIME"
            elif all(col_bool_dt):
                return "TIMESTAMP"

            else:
                return "TEXT"
        else:
            return "TEXT"    
        

    dtyp_ls = []
    for x in df:
        f = df[x]
        d = [tt for tt in f if tt != '']
        if len(d) == 0:
            dtyp_ls.append("TEXT")
        else:
            dtyp_ls.append(mysql_dtype(d))
    return dtyp_ls
