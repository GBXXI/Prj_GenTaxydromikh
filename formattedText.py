
def formattedBody(greeting, consNum, boxes, voucherNum, sender_name):
    formattedText_style = """
    <style>
        tab1 {
            padding-left: 2em;
        }

        ol {
            padding-left: 4em;
            list-style-type: decimal;
        }

        p {
            font-family: Arial, Helvetica, sans-serif;
        }
    </style>
    """
    formattedText_Body = f"""
    <div>
        
        <p>
            {greeting} σας,<br>    
        </p>
        
        <p>
            <tab1>
                Μόλις αναχώρησε από την αποθήκη μας η αποστολή με <br>
                <strong> <u>
                    αρ. Δελτίου: 27TA09-{consNum}
                </u></strong> ,<br>
            </tab1>

            <strong><u>
                ποσότητα Κιβωτίων: {boxes}
            </u></strong> <br>
        καθώς και τους ακόλουθους <strong><u>αριθμούς voucher</u></strong>:
            
            <ol>
               {(' ').join(voucherNum)} 
            </ol>
        </p>

        <p>
            {sender_name}
        </p>

    </div>
    """
    # print(formattedText_style, formattedText_Body)
    return formattedText_style + '\n' + formattedText_Body

formattedText_Os = \
"""YOU ARE RUNNING THIS PROGRAMM IN AN
NO WINDOWS MACHINE. AFTER THIS MESSAGE IS CLOSED IT
IS GOING TO BE TERMINATED.
"""    

# -------------------------------"Dirty Testing"--------------------------------
if __name__ == '__main__':
    v_dict = {'key1':'value1', 'key2':'value2', 'key3':'value3'}
    v_list = [f'<li>{value}</li>' for value in v_dict.values()]
    v_gen = (f'<li>{value}</li>' for value in v_dict.values())
    k = formattedBody('evening', 321, 3, v_gen, 'John Doe')
    print(k)
    print(formattedText_Os)