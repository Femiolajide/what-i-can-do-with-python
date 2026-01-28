import streamlit as st
import fractions as frac
deci = st.number_input(label="Insert a number",
                placeholder="Type a number...",
                )
numi = frac.Fraction(deci).limit_denominator().numerator
deno = frac.Fraction(deci).limit_denominator().denominator
result = fr"\frac{{{numi}}}{{{deno}}}"
if numi > deno and numi % deno > 0:
    mixed_frac = st.toggle("Expressed as a mixed fraction")
    w_num = numi // deno
    up = numi % deno
    if mixed_frac:
        result = fr"{{\large{{{w_num}}}}}\frac{{{up}}}{{{deno}}}"
if deci != 0:
    st.latex(result)