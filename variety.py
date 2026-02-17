def num_to_words(a:int) -> str:
    """Convert a number to word

    Parameter
    ----------------------------
    a: int

    An integer from 1 to 99999999999999999999999999999999

    Returns
    ---------------------------------
    str

    The number in words

    Note
    --------------------------------
    Return None if the number is more than 99999999999999999999999999999999
    
    """
    def one_octillion(a):
        if a < 1:
            raise ValueError (f"{a} is not allowed")
        def one_septillion(a):
            def one_sextillion(a):
                def one_quintillion(a):        
                    def one_quadrillion(a):
                        def one_trillion(a):
                            def one_billion(a):
                                def one_million(a):
                                    def one_thou(a):
                                        def one_999(a):
                                            def one_99(a):
                                                # 1 - 99 
                                                # FUNCTION
                                                # STARTS HERE 
                                                # creating number 
                                                # and word dictionary 
                                                num_dict = {1: 'one',
                                                            2: 'two',
                                                            3: 'three',
                                                            4: 'four',
                                                            5: 'five',
                                                            6: 'six',
                                                            7: 'seven',
                                                            8: 'eight',
                                                            9: 'nine',
                                                            10: 'ten',
                                                            11: 'eleven',
                                                            12: 'twelve',
                                                            13: 'thirteen',
                                                            14: 'forteen',
                                                            15: 'fifteen',
                                                            16: 'sixteen',
                                                            17: 'seventeen',
                                                            18: 'eighteen',
                                                            19: 'nineteen',
                                                            20: 'twenty',
                                                            30: 'thirty',
                                                            40: 'forty',
                                                            50: 'fifty',
                                                            60: 'sixty',
                                                            70: 'seventy',
                                                            80: 'eighty',
                                                            90: 'ninety'}
                                                # membership check 
                                                if a in num_dict:
                                                    return num_dict[a]
                                                # checking the lenght of the digit 
                                                elif len(str(a)) == 2:
                                                    # join 0 to the first digit 
                                                    b = int(str(a)[0] + "0")
                                                    # obtain remainder 
                                                    c = a % b
                                                    # join the two number word with - 
                                                    return f"{num_dict[b]}-{num_dict[c]}"
                                                # 1 - 99 
                                                # FUNCTION
                                                # ENDS HERE 
                                            
                                            # 1 - 999 FUNCTION STARTS HERE
                                            # condition for hundred
                                            if len(str(a)) == 3:
                                                b = int(str(a)[0])
                                                # join two 0's to the first digit 
                                                c = a % int(str(b)+"0"*2)
                                                # applying the previous inner function conditionally
                                                if c != 0:
                                                    return f"{one_99(b)} hundred and {one_99(c)}"
                                                else:
                                                    return f"{one_99(b)} hundred"
                                            else:
                                                return one_99(a)
                                            # 1 - 999 FUNCTION ENDS HERE

                                        # 1 - 999,999 FUNCTION STARTS HERE
                                        # formating the digits with comma seperator 
                                        d = f"{a:,}"
                                        # condition for thousand 
                                        if d.count(",") == 1:
                                            # extracting the number before the first comma 
                                            b = int(d[0:d.find(",")])
                                            # join three 0's to the digit(s) before the first comma 
                                            c = a % int(str(b)+"0"*3)
                                            # applying the previous inner function conditionally 
                                            if c != 0 and 0 < c < 100:
                                                return f"{one_999(b)} thousand and {one_999(c)}"
                                            elif c != 0 and c > 100:
                                                return f"{one_999(b)} thousand, {one_999(c)}"
                                            else:
                                                return f"{one_999(b)} thousand"
                                        else:
                                            return one_999(a)
                                        # 1 - 999,999 FUNCTION ENDS HERE

                                    # 1 - 999,999,999 FUNCTION STARTS HERE
                                    # formating the digits with comma seperator 
                                    d = f"{a:,}"
                                    # condition for million
                                    if d.count(",") == 2:
                                        # extracting the number before the first comma 
                                        b = int(d[0:d.find(",")])
                                        # join six 0's to the digit(s) before the first comma 
                                        c = a % int(str(b)+"0"*6)
                                        # applying the previous inner function conditionally 
                                        if c != 0 and 0 < c < 100:
                                            return f"{one_thou(b)} million and {one_thou(c)}"
                                        elif c != 0 and c > 100:
                                            return f"{one_thou(b)} million, {one_thou(c)}"
                                        else:
                                            return f"{one_thou(b)} million"
                                    else:
                                        return one_thou(a)
                                    # 1 - 999,999,999 FUNCTION ENDS HERE


                                # 1 - 999,999,999,999 FUNCTION STARTS HERE
                                # formating the digits with comma seperator 
                                d = f"{a:,}"
                                # condition for billion
                                if d.count(",") == 3:
                                    # extracting the number before the first comma 
                                    b = int(d[0:d.find(",")])
                                    # join nine 0's to the digit(s) before the first comma 
                                    c = a % int(str(b)+"0"*9)
                                    # applying the previous inner function conditionally 
                                    if c != 0 and 0 < c < 100:
                                        return f"{one_million(b)} billion and {one_million(c)}"
                                    elif c != 0 and c > 100:
                                        return f"{one_million(b)} billion, {one_million(c)}"
                                    else:
                                        return f"{one_million(b)} billion"
                                else:
                                    return one_million(a)
                                # 1 - 999,999,999,999 FUNCTION ENDS HERE


                            # 1 - 999,999,999,999,999 FUNCTION STARTS HERE
                            # formating the digits with comma seperator 
                            d = f"{a:,}"
                            # condition for trillion
                            if d.count(",") == 4:
                                # extracting the number before the first comma 
                                b = int(d[0:d.find(",")])
                                # join twelve 0's to the digit(s) before the first comma 
                                c = a % int(str(b)+"0"*12)
                                # applying the previous inner function conditionally 
                                if c != 0 and 0 < c < 100:
                                    return f"{one_billion(b)} trillion and {one_billion(c)}"
                                elif c != 0 and c > 100:
                                    return f"{one_billion(b)} trillion, {one_billion(c)}"
                                else:
                                    return f"{one_billion(b)} trillion"
                            else:
                                return one_billion(a)
                            # 1 - 999,999,999,999,999 FUNCTION ENDS HERE

                        # 1 - 999,999,999,999,999,999 FUNCTION STARTS HERE
                        # formating the digits with comma seperator 
                        d = f"{a:,}"
                        # condition for quadrillion
                        if d.count(",") == 5:
                            # extracting the number before the first comma 
                            b = int(d[0:d.find(",")])
                            # join fiften 0's to the digit(s) before the first comma 
                            c = a % int(str(b)+"0"*15)
                            # applying the previous inner function conditionally 
                            if c != 0 and 0 < c < 100:
                                return f"{one_trillion(b)} quadrillion and {one_trillion(c)}"
                            elif c != 0 and c > 100:
                                return f"{one_trillion(b)} quadrillion, {one_trillion(c)}"
                            else:
                                return f"{one_trillion(b)} quadrillion"
                        else:
                            return one_trillion(a)
                        # 1 - 999,999,999,999,999,999 FUNCTION ends HERE


                    # 1 - 999,999,999,999,999,999,999 FUNCTION STARTS HERE
                    # formating the digits with comma seperator 
                    d = f"{a:,}"
                    # condition for quintillion
                    if d.count(",") == 6:
                        # extracting the number before the first comma 
                        b = int(d[0:d.find(",")])
                        # join eighteen 0's to the digit(s) before the first comma 
                        c = a % int(str(b)+"0"*18)
                        # applying the previous inner function conditionally 
                        if c != 0 and 0 < c < 100:
                            return f"{one_quadrillion(b)} quintillion and {one_quadrillion(c)}"
                        elif c != 0 and c > 100:
                            return f"{one_quadrillion(b)} quintillion, {one_quadrillion(c)}"
                        else:
                            return f"{one_quadrillion(b)} quintillion"
                    else:
                        return one_quadrillion(a)
                    # 1 - 999,999,999,999,999,999,999 FUNCTION ENDS HERE


                # 1 - 999,999,999,999,999,999,999,999 FUNCTION STARTS HERE
                # formating the digits with comma seperator 
                d = f"{a:,}"
                # condition for sextillion
                if d.count(",") == 7:
                    # extracting the number before the first comma 
                    b = int(d[0:d.find(",")])
                    # join twenty-one 0's to the digit(s) before the first comma 
                    c = a % int(str(b)+"0"*21)
                    # applying the previous inner function conditionally 
                    if c != 0 and 0 < c < 100:
                        return f"{one_quintillion(b)} sextillion and {one_quintillion(c)}"
                    elif c != 0 and c > 100:
                        return f"{one_quintillion(b)} sextillion, {one_quintillion(c)}"
                    else:
                        return f"{one_quintillion(b)} sextillion"
                else:
                    return one_quintillion(a)
               # 1 - 999,999,999,999,999,999,999,999 FUNCTION ENDS HERE


            # 1 - 999,999,999,999,999,999,999,999,999 FUNCTION STARTS HERE
            # formating the digits with comma seperator 
            d = f"{a:,}"
            # condition for septillion
            if d.count(",") == 8:
                # extracting the number before the first comma 
                b = int(d[0:d.find(",")])
                # join twenty-four 0's to the digit(s) before the first comma 
                c = a % int(str(b)+"0"*24)
                # applying the previous inner function conditionally 
                if c != 0 and 0 < c < 100:
                    return f"{one_sextillion(b)} septillion and {one_sextillion(c)}"
                elif c != 0 and c > 100:
                    return f"{one_sextillion(b)} septillion, {one_sextillion(c)}"
                else:
                    return f"{one_sextillion(b)} septillion"
            else:
                return one_sextillion(a)
            # 1 - 999,999,999,999,999,999,999,999,999 FUNCTION ENDS HERE


        # 1 - 999,999,999,999,999,999,999,999,999,999 FUNCTION STARTS HERE
        # formating the digits with comma seperator                    
        d = f"{a:,}"
        # condition for octillion
        if d.count(",") == 9:
            # extracting the number before the first comma 
            b = int(d[0:d.find(",")])
            # join twenty-seven 0's to the digit(s) before the first comma 
            c = a % int(str(b)+"0"*27)
            # applying the previous inner function conditionally 
            if c != 0 and 0 < c < 100:
                return f"{one_septillion(b)} octillion and {one_septillion(c)}"
            elif c != 0 and c > 100:
                return f"{one_septillion(b)} octillion, {one_septillion(c)}"
            else:
                return f"{one_septillion(b)} octillion"
        else:
            return one_septillion(a)
        # 1 - 999,999,999,999,999,999,999,999,999,999 FUNCTION ENDS HERE
    

    # 1 - 999,999,999,999,999,999,999,999,999,999,999 FUNCTION STARTS HERE
    # formating the digits with comma seperator
    if not isinstance(a,(int)):
        raise ValueError (f"{a} is not allowed")
    d = f"{a:,}"
    # condition for octillion
    if d.count(",") == 10:
        # extracting the number before the first comma 
        b = int(d[0:d.find(",")])
        # join thirty 0's to the digit(s) before the first comma 
        c = a % int(str(b)+"0"*30)
        # applying the previous inner function conditionally 
        if c != 0 and 0 < c < 100:
            return f"{one_octillion(b)} nonillion and {one_octillion(c)}"
        elif c != 0 and c > 100:
            return f"{one_octillion(b)} nonillion, {one_octillion(c)}"
        else:
            return f"{one_octillion(b)} nonillion"
    else:
        return one_octillion(a)
    


# DERIVING ENGLISH WORDS FROM COMBINATION OF LETTERS.md
def derive_words(letters:str,min_letters:int,
                 max_letters=None) -> list:
    """Form a number of English words from group of letters
    
    Parameters
    -------------
    letters: str

        letters must be a string with only aphabeth from a to z
    
    min_letters: int

        Number of minimum letters to make up the derived 
        words from the letter provided

    max_letters: int (optional)

        Number of maximum letters to make up the derived 
        words from the letter provided   

    Returns
    -------------
        list

        Returns the list of words derived in ascending order
        or empty list if no match
        
    Raises
    ----------
        Raises ValueError if letters is not a string
        or if min_letters or max_letters is not an integer
        or if string has a character that is not with a to z
        or if min_letters is greater max_letters

    """
    # check if letters is a string 
    if not isinstance(letters,str):
        raise ValueError("Only string datatype is allowed")
    # update letters to its lower case version 
    letters = letters.lower()
    # importing regular expression module
    import re
    # validating characters that made up letters 
    # raise error if there is anything that is not 
    # within a to z in letters
    if re.search(r'[^aA-zZ]',letters):
        raise ValueError("Letters must be within a to z")
    # checking if min_letters is an integer
    if not isinstance(min_letters,int):
        raise ValueError("Only integer datatype is allowed")
    # checking if max_letters is an integer
    if not isinstance(max_letters,(int,type(None))):
        raise ValueError("Only integer datatype is allowed")
    if max_letters != None:
        if not (min_letters < max_letters):
            raise ValueError("min_letters > max_letters")
    # Importing permutation and combination tools 
    from itertools import permutations as pm, combinations as cb 
    # Accessing English dictionary words text files 
    with open(r"engmix.txt") as file:
        content = file.readlines()
    # removing the newlines ending each words 
    dict_words = [x.strip() for x in content]
    # creating a list to store the English words found in the file 
    combination_list = []
    # getting the possible combination of all the letters
    if max_letters != None:
        for x in range(min_letters,max_letters + 1):
            combination_list.extend(list(cb(letters,x)))
    else:
        combination_list.extend(list(cb(letters,min_letters)))
    # getting permutaion of all the letters combined
    permutation_list = []
    for x in combination_list:
        permutation_list.extend(list(pm(x)))
    permutation_list
    # turning the letters in tuple to word 
    word_list = ["".join(x) for x in permutation_list]
    word_list
    # deriving the dictionary words using set intersection
    eng_words = list(set(word_list) & set(dict_words))
    # return the matched words in ascending order 
    return list(sorted(eng_words))