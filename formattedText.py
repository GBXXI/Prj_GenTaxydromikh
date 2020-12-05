
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

formattedText_Os = (
    "YOU ARE RUNNING THIS PROGRAMM IN AN NO WINDOWS MACHINE."
    "AFTER THIS MESSAGE IS CLOSED IT IS GOING TO BE TERMINATED."
)

formattedText_EmptyFields = (
    "Υπάρχουν κενά πεδία! \n"
    "Παρακαλώ συμπληρώστετα και προσπαθήστε ξανά!"
)

formattedText_Help = (
    "<html>\n"
        "\n"
        "    <head />\n"
        "\n"
        "    <body>\n"
        "        <ol style=\"margin-top: 0px; margin-bottom: 0px; margin-left: 0px; margin-right: 0px; -qt-list-indent: 1;\">\n"
        "            <li align=\"justify\"\n"
        "                style=\" margin-top:12px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">\n"
        "                Σε περίπτωση που ο κέρσορας στην γραμμή εισαγωγής των voucher <br />βρίσκεται στο μέσο του πεδίου, δεν\n"
        "                θα μπορέσει να εισάγει το <br />σκαναρισμένο barcode. Πιέστε το πλήκτρο Home, ώστε να μπορέσετε <br />να\n"
        "                σκανάρετε. <br /></li>\n"
        "            <li align=\"justify\"\n"
        "                style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">\n"
        "                Το όνομα του αποστολέα γίνεται δεκτό <u>μόνο με ελληνικούς κεφαλαίους</u></li>\n"
        "            <p align=\"justify\">χαρακτήρες και πρέπει να είναι της μορφής:</p>\n"
        "            <p align=\"justify\">Ο. ΕΠΩΝΥΜΟ </p>\n"
        "            <li align=\"justify\"\n"
        "                style=\" margin-top:0px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">\n"
        "                Για να γίνει επιτυχώς η αποστολή του e-mail, πρέπει ΟΛΑ τα στοιχεία<br />του πίνακα να είναι\n"
        "                συμπληρωμένα.</li>\n"
        "        </ol>\n"
        "    </body>\n"
        "\n"
    "</html>"
)

# -------------------------------"Dirty Testing"--------------------------------
if __name__ == '__main__':
    v_dict = {'key1':'value1', 'key2':'value2', 'key3':'value3'}
    v_list = [f'<li>{value}</li>' for value in v_dict.values()]
    v_gen = (f'<li>{value}</li>' for value in v_dict.values())
    k = formattedBody('evening', 321, 3, v_gen, 'John Doe')
    print(k)
    print(formattedText_Os)
