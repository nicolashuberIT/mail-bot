# mail-bot
 
automated mailings (attachments, tls connection)

essential directories
* attachments/
* contacts/
* includes/

This python application was developed with a rather simple user experience in mind. To use the mail-bot you only need need basic programming skills and can just follow this guide.

First of all: never post critical information in the source code itself. For example, password strings etc. could be inputted in command line interactions!

How to use the program:
1) download the most recently published code as .zip
2) Install Python IDE like Pycharm or Visual Studio Code and setup project, which is simple as the provided folder is preconfigured in the correct manner.
3) setup virtual environment in order to run the program. Make sure you chose the main.py document as the primary program.
4) Configure the constants to your needs (open includes/constants.py and change the values according to your needs):
  * event (is also written into mail subject later on)
  * event_info (link event page)
  * admin_key (provide individual admin password)
  * program_key (enter individual start command)
  * root (make sure to enter the root of your virtual environment so it can locate essential documents like the contacts) 
    - you can determine the root working directory as follows:
    - import os
    - print(os.getcwd());
  * response_mail (determine a response mail adress)
  * sender_mail (enter a sender mail adress)
  * attachment_name (define the name of the attachments so they can be found. Make sure to name these XYZ_n (whilste n is a natural number, beginning at 1 and growing to infinity) Keep in mind, that there must be an attachment for every list item in the csv.)
  * courtesy (0 = normal, 1 = courtesy form)
  * mail_systemProtocol (sends protocoll to this adress)
  * attachment_systemProtocol (name of system protocol pdf)
5) Also setup a custom message! To do this, open includes/mailing.py and check line 44. There you can enter a custom message. Youse f'string in order to print individual messages. You can even define a courtesy message if you'd like to.

To run the programm there are two possibilities:
1) setup a venviv to run main.py as standard
2) run main.py

As a final step to initialize the mailing process you're asked to setup the server after having started the main.py script.

A lot of issues that you may encounter when using this program can be solved with stackoverflow or github. Good luck! :-)
