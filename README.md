# Prj_GenTaxydromikh

This is a personal project, that covers the need for a faster and more reliable,
updating process by email, when urgent consignment is required between 2 warehouses.
It uses the logged Outlook account to send the emails.

### BUGS:
* When clicked, the voucher label field, positions the cursor to the middle, thus
making it unresponsive to input. A crude solution is to press the "Home" button.

* Both the script(or the app) and the Outlook application must run with the same
privileges elevation. Otherwise an 'Operation Unavailable', followed by a 
'Server execution failed', error will occur.<br>
[stackoverflow.com/questions/41611383/](https://stackoverflow.com/questions/41611383/how-to-connect-to-a-running-instance-of-outlook-from-python)

## v-0.0.0
*     Except the unfilled email dict's and lists, for security reasons, 
      everything is ready for this application to run in a "Windows" environment.

## v-0.0.1
*     A logger has been added.
*     The gui can be executed on a "linux" environment, without an Import error.
      All the subsequent errors, since is designed for a "Windows" environment 
      will be logged.

## v-0.1.0
*     It is now possible to execute even when Outlook is instantiated.      
*     The application colours have a slight change.
*     