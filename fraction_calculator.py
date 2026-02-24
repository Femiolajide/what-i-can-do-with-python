import streamlit as st
import re
from fractions import Fraction as fra
st.title("Fraction Expression Calculator")
st.write(
    """This calculator evaluates mathematical expressions containing fractions only.
It accepts valid fraction expressions `(e.g., 3/4 + 5/6)` and returns the answer.
Note that :red[exponents] and :red[mixed fractions] are not currently supported."""
)
st.write("---")
st.write(":blue-background[**NOTE:**] Correct answer is guarantted but the proper \
representation of complex expressions is still work-in-progress!")
def parse_frac_num(x:str):
    x = x.strip()
    import re 
    p1 = re.compile(r"\d*\.?\d+/\d*\.?\d+")
    q = p1.findall(x)
    vv = []
    for c in q:
        y = c[:c.find("/")]
        z = c[c.find("/")+1:]
        zz = fr"\frac{{{y}}}{{{z}}}"
        vv.append(zz)
    for tt,yy  in zip(q,vv):
        x = x.replace(tt,yy)
    if "^(" in x and ")" in x:
        x = x.replace("^(","^{(").replace(")",")}").replace("{6","{{6").replace("6}","6}}")
    return x
    
exp = st.text_input("Enter Fraction Expression",
                    placeholder="e.g. 3/4 + 5/6 - 1/2")
if exp:
    exp2 = exp.replace("^","**")
    if re.search(r"[^0-9\-\+\/\* \^\.\(\)]",exp):
        st.error("Invalid entry",icon="❌")
    elif "//" in exp:
        st.error("Invalid entry",icon="❌")
    elif "**" in exp:
        st.error("Invalid entry",icon="❌")
    elif "^" in exp:
        st.error("Invalid entry",icon="❌")
    elif "/" not in exp:
        st.warning("There is no fraction in your expreesion",icon="🛑")
    else:
        frac_exp = parse_frac_num(exp)
        frac_exp = frac_exp.replace("*",r"\times")
        frac_exp = frac_exp.replace("/",r"\div")
        try:
            ans = eval(exp2)
        except:
            st.error("Invalid entry",icon="❌")
        else:
            num = fra(ans).limit_denominator().numerator
            den = fra(ans).limit_denominator().denominator
            if den == num:
                fn_ans = f"{frac_exp} = {1}"
                st.latex(fn_ans)
            elif den < num:
                if den != 1:
                    as_mixed = st.toggle("Express answer as mixed fraction")
                    if as_mixed:
                        w_num = num // den
                        remain = num % den
                        if remain != 0:
                            fn_ans = fr"{frac_exp} = {{\large{w_num}}} \frac{{{remain}}}{{{den}}}"
                            st.latex(fn_ans)
                        else:
                            fn_ans = fr"{frac_exp} = {num//den}"
                            st.latex(fn_ans)
                    elif den == 1:
                        fn_ans = fr"{frac_exp} = {num}"
                        st.latex(fn_ans)   
                    else:
                        fn_ans = fr"{frac_exp} = \frac{{{num}}}{{{den}}}"
                        st.latex(fn_ans)
                else:
                    fn_ans = f"{frac_exp} = {num}"
                    st.latex(fn_ans)
            else:
                fn_ans = fr"{frac_exp} = \frac{{{num}}}{{{den}}}"
                st.latex(fn_ans)