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
ts = dt.datetime.now().strftime("%y-%m-%d %H:%M:%S")
st.write("---")
st.title("Create Your Bar Chart From Your Raw Data")
st.write("This web application allows you \
to manually create, customise, and download \
bar charts, but this version allows you to create the chart from your raw data.")
st.write("---")
def extention(x):
    import re
    return re.findall(r"\..+$",x)[0]
encod = "utf-8"
data = ""
tab1, tab3, tab4 = st.tabs(["Data Entry",
                                 "Default Graph","Edit Graph"])
with tab1:
    file = st.file_uploader("**Upload your data**",
                            help="Only csv, txt, tsv and excel file is supported",)
    if file:
        if re.search(r"\.tsv$|\.csv$|\.txt$|\.xlsx$|\.xls$",file.name):
            if re.search(r"\.tsv$|\.csv$|\.txt$",file.name):
                raw = file.getvalue()
                encod = from_bytes(raw).best().encoding
                sample_txt = raw[:2048].decode(encoding=encod,errors="ignore")
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
            if st.button("Preview data"):
                st.dataframe(data.head())
            else:
                pass
            columns = [*data.columns]
            var = st.selectbox("Select a column to plot in your bar chart",
                                columns)
            data = data[var].value_counts(sort=False).to_frame().reset_index()
            data = data.rename(columns={"count":"Frequency"})
            if not data.empty:
                with tab3:
                    f, a = plt.subplots(figsize=(8,5)) 
                    a.margins(.2)
                    data[var] = [tw.fill(x,20,) for x in data[var]]
                    tot = data["Frequency"].sum()
                    lab_typ = "n%"
                    y_axis = "n"
                    sns.barplot(data=data,
                                x=var,
                                y="Frequency",
                                width=.4,
                                # height= 5,
                                # aspect=1.8,
                                palette="colorblind",
                                ax=a
                                
                                )

                    ax = plt.gca()
                    for cont in ax.containers:
                        if lab_typ == "n%":
                            lab = [f"{int(x.get_height())}\n({int(x.get_height())/tot:.1%})" 
                                
                                for x in cont]
                            ax.bar_label(container=cont,labels=lab,padding=4,
                                        #  fontsize=12
                                        )
                        elif lab_typ == "%":
                            lab = [f"{int(x.get_height())/tot:.1%}" 
                                
                                for x in cont]
                            ax.bar_label(container=cont,labels=lab,padding=4,
                                        #  fontsize=12
                                        )
                        elif lab_typ == "n":
                            lab = [f"{int(x.get_height())}" 
                                
                                for x in cont]
                            ax.bar_label(container=cont,labels=lab,padding=4,
                                        #  fontsize=12
                                        )  
                        else:
                            pass
                    plt.xticks(fontsize=10)
                    plt.yticks(fontsize=10)
                    plt.ylabel("\nFrequency\n",fontsize=14,)
                    plt.xlabel("\n"+var+"\n",fontsize=14,)
                    plt.grid(which="both",axis="y",alpha=.3)
                    ax = plt.gca()
                    ax.set_axisbelow(True)
                    plt.title(f"\nFrequency Distribution of {var.capitalize()}",
                                fontsize=16,
                            fontweight="bold",pad=20)
                    sns.despine(ax=a,
                        top=True,
                        right=True,
                        # left=True
                                # offset=24
                                )
                    y_tik = ax.get_yticks()
                    if y_axis == "%":
                        plt.yticks(y_tik, [f"{x/tot:.0%}" for x in y_tik])
                    plt.tight_layout()
                    if not data.empty:
                        st.pyplot(f)
                    v_disk = io.BytesIO()
                    plt.savefig(v_disk,format="png")
                    v_disk.seek(0)

                    st.download_button(label="Download chart",
                                        data=v_disk,
                                        file_name="bar_chart_"+ts+".png",
                                        mime="image/png")

                with tab4:
                    st.subheader("Edit your graph")
                    with st.expander("Chart Settings",
                                    expanded=False):
                        st.write("Graph size (in inches)")
                        col1, col2 = st.columns(2)
                        with col1:
                            width = st.slider("width",3,30,8)
                        with col2:
                            height = st.slider("Height",3,30,5)            
                        title = st.text_input("Chart title",var)
                        col1, col2, col3, col4 = st.columns(4)
                        with col1:
                            title_size = st.slider("Font size",8,40,16)
                        with col2:
                            title_color = st.color_picker("Colour","#000000")
                        with col3:
                            title_bold = st.checkbox("Bold",True)
                    with st.expander("Axis settings"):
                        x_lab = st.text_input("X-axis Label",var)
                        col1, col2, col3, col4, col5 = st.columns(5)
                        with col1:
                            x_lab_size = st.slider("X label Font size",8,40,11)
                        with col2:
                            x_lab_colour = st.color_picker("X label Colour","#000000")
                        with col3:
                            x_lab_bold = st.checkbox("Bold",False)
                        with col4: 
                            x_lab_dat_size = st.slider("x data Font size",8,40,11)
                        with col5:
                            x_lab_data_colour = st.color_picker("x data Colour","#000000")
                        y_lab = st.text_input("Y-axis Label","Frequency")
                        col1, col2, col3, col4, col5, col6 = st.columns(6)
                        with col1:
                            y_lab_size = st.slider("Y label Font size",8,40,11)
                        with col2:
                            y_lab_colour = st.color_picker("Y label Colour","#000000")
                        with col3:
                            y_lab_bold = st.checkbox("bold",False)
                        with col4: 
                            y_lab_dat_size = st.slider("Y data Font size",8,40,11)
                        with col5:
                            y_lab_data_colour = st.color_picker("Y data Colour","#000000")
                        with col6:
                            y_ax_as_pct = st.toggle("Show y-axis as percentage of total")
                    with st.expander("Data Labels"):
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            data_label = st.selectbox("Select data label format",["None","n","%","n (%)"])
                        with col2:
                            data_label_color = st.color_picker("data label colour","#000000")
                        with col3:
                            data_label_size = st.slider("data label Font size",8,40,11)
                    with st.expander("Bar Options"):
                        col1, col2,col3  = st.columns(3)
                        with col1:
                            bar_width = st.slider("Bar width",.1,1.0,.4)
                        with col2:
                            bar_sort = st.selectbox("bar sort",["None","ascending","descending"])
                            max_cols =3
                        with st.expander("###### ***Pick a color for each of these category***"):
                            cat = data[var].unique()
                            clrs = {}
                            rows = [cat[i:i+max_cols] for i in range(0,len(cat),max_cols)] 
                            for x in rows:
                                cols = st.columns(len(x))
                            for col, kat in zip(cols,x):
                                with col:
                                    clrs[kat] = st.color_picker(f"{kat}",
                                                        "#2956a3")
                    if bar_sort == "ascending":
                        data = data.sort_values("Frequency",ascending=True)
                    elif bar_sort == "descending":
                        data = data.sort_values("Frequency",ascending=False)
                    else:
                        pass
                    f, a = plt.subplots(figsize=(width,height)) 
                    a.margins(.2)
                    data[var] = [tw.fill(x,12,) for x in data[var]]
                    tot = data["Frequency"].sum()
                    lab_typ = data_label
                    y_axis = y_ax_as_pct
                    sns.barplot(data=data,
                                x=var,
                                y="Frequency",
                                width=bar_width,
                                # height= 5,
                                # aspect=1.8,
                                hue=var,
                                palette=clrs.values(),
                                
                                # palette="colorblind",
                                ax=a
                                
                                )

                    ax = plt.gca()
                    for cont in ax.containers:
                        if lab_typ == "n (%)":
                            lab = [f"{int(x.get_height())}\n({int(x.get_height())/tot:.1%})" 
                                
                                for x in cont]
                            ax.bar_label(container=cont,labels=lab,padding=4,
                                        fontsize=data_label_size,
                                        color=data_label_color
                                        )
                        elif lab_typ == "%":
                            lab = [f"{int(x.get_height())/tot:.1%}" 
                                
                                for x in cont]
                            ax.bar_label(container=cont,labels=lab,padding=4,
                                        fontsize=data_label_size,
                                        color=data_label_color
                                        )
                        elif lab_typ == "n":
                            lab = [f"{int(x.get_height())}" 
                                
                                for x in cont]
                            ax.bar_label(container=cont,labels=lab,padding=4,
                                        fontsize=data_label_size,
                                        color=data_label_color
                                        )  
                        else:
                            pass
                    plt.xticks(fontsize=x_lab_dat_size,color=x_lab_data_colour)
                    plt.yticks(fontsize=y_lab_dat_size,
                                color=y_lab_data_colour)
                    f_wegt_y = "bold" if y_lab_bold else None
                    plt.ylabel("\n"+y_lab,fontsize=y_lab_size,fontweight=f_wegt_y,
                                color=y_lab_colour)
                    plt.xlabel(x_lab,
                                color=x_lab_colour,
                                fontsize=x_lab_size,
                                fontweight="bold" if x_lab_bold else None,)
                    plt.grid(which="both",axis="y",alpha=.3)
                    ax = plt.gca()
                    ax.set_axisbelow(True)
                    f_wegt_t = "bold" if title_bold else None
                    plt.title(f"\n{title}",
                                fontsize=title_size,
                            fontweight=f_wegt_t,pad=20,
                            color=title_color)
                    sns.despine(ax=a,
                        top=True,
                        right=True,
                        # left=True
                                # offset=24
                                )
                    y_tik = ax.get_yticks()
                    if y_ax_as_pct:
                        plt.yticks(y_tik, [f"{x/tot:.0%}" for x in y_tik])
                    plt.tight_layout()
                    if not data.empty:
                        st.pyplot(f)
                    v_disk = io.BytesIO()
                    plt.savefig(v_disk,format="png")
                    v_disk.seek(0)

                    st.download_button(label="Download edited chart",
                                        data=v_disk,
                                        file_name="bar_chart_"+ts+".png",
                                        mime="Image/png")


                            



