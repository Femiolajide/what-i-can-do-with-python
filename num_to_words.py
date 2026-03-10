import streamlit as st
from variety import num_to_words
st.title("NUMBER TO WORDS")
st.write("""
---

         
This web app allows you to convert number to words.  
Read more about it [here](https://github.com/Femiolajide/Python-Functions-Playground#1-num_to_words)    
         

---

""")
num_enrered = st.text_input(label="**Enter a number**",
                placeholder="Type an integer from 1 - 999,999,999,999,999,999,999,999,999,999,999",
                max_chars=43
                ).replace(",","_")
if num_enrered:
    try:
        num_enrered = int(num_enrered)
    except ValueError:
        val_err = ValueError(f"**Invalid Entry:** :orange-background[{num_enrered}] is not allowed")
        st.error(val_err)
    else:
        if num_enrered < 1 or num_enrered > 999_999_999_999_999_999_999_999_999_999_999:
            range_err = ValueError(f"**Out of Range:** :orange-background[{num_enrered}] is not within 1 - 999,999,999,999,999,999,999,999,999,999,999")
            st.error(range_err)
        else:
            st.success(f"**{num_enrered:,}** = :blue-background[{num_to_words(num_enrered)}]")

