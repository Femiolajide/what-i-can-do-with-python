import streamlit as st
import pandas as pd 
import io 
import re
from PIL import Image, ImageDraw, ImageFont
from charset_normalizer import from_bytes
import csv
import zipfile as zp
import datetime as dt
ts = dt.datetime.now().strftime("%y-%m-%d %H:%M:%S")
st.title("Automated Certificate Creator")
st.write("This app allows you to generate personalized certificates instantly. Enter names manually or upload a file for bulk processing and download all certificates in one ZIP file.")
st.markdown("---")
def extention(x):
    import re
    return re.findall(r"\..+$",x)[0]
def validate_names(x):
    import re
    x = str(x)
    if re.match(r"^[a-zA-Z]+\s?[a-zA-Z]+\s?[a-zA-Z]*$",x) and len(x) <= 35:
        return True
    else:
        return False
def validate_dates(x):
    x = str(x)
    import pandas as pd
    try:
        pd.to_datetime(x,errors="raise")
        return True
    except:
        return False

encod = "utf-8"
data = ""
choice = st.selectbox("Choose an option",
             ["Enter the raw data","Upload the raw data"])
if choice == "Enter the raw data":
    data = pd.DataFrame(columns=["name","certification_date"])
    data = st.data_editor(data=data,
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
                                set(columns)-{name})
            data = data[[name,date]]
            data = data.fillna("missing   value")
            invalid_name_id = [x for x, y in
                               enumerate(data.iloc[:,0]) if validate_names(
                                   y
                               ) == False]
            
            invalid_date_id = [x for x, y in
                               enumerate(data.iloc[:,-1]) if validate_dates(
                                   y
                               ) == False]
            invalid_rows = invalid_name_id + invalid_date_id
            invalid_rows = list(set(invalid_rows))
            if invalid_rows:
                st.error("WARNING: Some dates or names are invalid in your data")
                with st.expander("Show invalid name/date"):
                    st.info(f"There are {len(invalid_rows)} records with invalid name or dates in your data")
                    with st.expander("Click here to check"):
                        st.warning("The folowing record will not appear in your certificate!!!")
                        invalid_rec = data.iloc[invalid_rows,:]
                        invalid_rec.index = range(1,len(invalid_rec) + 1)
                        st.table(invalid_rec)
            data = data.filter(
                items=set(data.index) - set(invalid_rows),
                axis=0)
if not isinstance(data,str):
    data.columns = ["name","date"]
    data["name"] = data["name"].astype(str)
    data["date"] = data["date"].astype(str)
    data["date"] = pd.to_datetime(
        data["date"],format="mixed"
    ).dt.strftime("%B %d, %Y")
    data["name"] = data["name"].str.upper().str.strip()
    data = data.sort_values(by="name",ascending=False)
    if not data.empty:
        zip_byte = io.BytesIO()
        st.write(f"##### There are `{len(data)}` certificate to be proccessed")
        click = st.button("Generate certificates")
        if click:
            progress_bar = st.progress(0)
            status_text = st.empty()
            total = len(data)
            with zp.ZipFile(zip_byte,"w") as zfile:
                for n,d,i in zip(data["name"], data["date"],range(1,len(data)+1)):
                    img = Image.open("CERTIFICATE_TEMPLATE.png")
                    draw = ImageDraw.Draw(img)
                    if len(n) <= 23:
                        font = ImageFont.truetype("Groovify-Demo.ttf",150)
                        draw.text((1650 - len(n)*35,
                                1290 
                                ),n,"black",font)
                    elif 24 <= len(n) <= 27:
                        font = ImageFont.truetype("Groovify-Demo.ttf",135)
                        draw.text((1700 - len(n)*35,
                                1300 
                                ),n,"black",font)

                    elif 27 <= len(n) <= 31:
                        font = ImageFont.truetype("Groovify-Demo.ttf",110)
                        draw.text((1930 - len(n)*35,
                                1330 
                                ),n,"black",font)
                        
                    elif 32 <= len(n) <= 35:
                        font = ImageFont.truetype("Groovify-Demo.ttf",100)
                        draw.text((2025 - len(n)*35,
                                1350 
                                ),n,"black",font)
                    else:
                        pass
                    date_font = ImageFont.truetype("arial.ttf",size=66)
                    draw.text((315 + len(d)*3 - 20,
                            2080),d,font=date_font,fill="black")
                    img_byte = io.BytesIO()
                    img.save(img_byte,"JPEG")
                    img_byte.seek(0)
                    zfile.writestr(f"{n}_{i}.png", img_byte.getvalue(),
                                   compress_type=zp.ZIP_STORED)
                    progress = i/total
                    progress_bar.progress(progress)
                    status_text.text(f"Processing {i/total:.2%}")
                    zip_byte.seek(0)
            status_text.success("Done! Click the Download button below")
            st.download_button("Download",data=zip_byte.getvalue(),
                               file_name="bulk_certificate_"+ts+".zip",
                               mime="Application/ZIP")
        

