# --- header files ---
import includes.mailing
from includes import server, constants, contacts
from email.utils import formatdate
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from pathlib import Path
from fpdf import FPDF
import calendar
import time
import os


# --- final check / final command to start mailing ---

def final_check():
    print("-- output --> mailing overview");
    print(f'------ working directory: --> {os.getcwd()}')
    print(f'------ event: --> {constants.event}');
    print(f'------ event info: --> {constants.event_info}');
    print(f'------ sender mail: --> {constants.sender_mail}');
    print(f'------ copy to: --> {constants.mail_BCC}');
    print(f'------ response mail: --> {constants.response_mail}');
    print(f'------ attachments: --> "{constants.attachment_name}_i.pdf"');
    print(f'------ courtesy: --> {constants.courtesy}\n')

    initialize = input("To start the mailing now, enter 'final'!\n -- input --> ")

    if initialize == "final":
        print("-- output --> The mailing is now being initialized! Almost done. :-)");

    else:
        print("-- output --> The program was quit unexpectedly.")
        server.mailserver.quit()
        exit()

# --- mailing ---

def timestamp():

    global timestamp;

    current_GMT = time.gmtime()
    timestamp = calendar.timegm(current_GMT)

    return timestamp;

def send():

    f = open(f"{constants.root}/system/txt/systemLog.txt", "w");

    limit = len(contacts.name);

    print("-- output --> feedback loop:");

    for i in range(0, limit, 1):

        timestamp = formatdate(localtime=True);

        if constants.courtesy == 0:
            message = f'Hallo! \n SO KZO \n\n _____________________________ \n Kantonsschule Zürcher Oberland \n\n SO KZO \n so@kzo.ch \n https://www.sorg.kzo.ch';

        else:
            message = f'Hallo! \n SO KZO \n\n _____________________________ \n Kantonsschule Zürcher Oberland \n\n SO KZO \n so@kzo.ch \n https://www.sorg.kzo.ch';

        msg = MIMEMultipart();
        msg['Subject'] = f'{constants.event} | Team {contacts.team[i]} | SO KZO';
        msg['From'] = constants.sender_mail;
        msg['Date'] = timestamp;
        msg['To'] = contacts.mailbox[i];
        msg['CC'] = constants.mail_BCC;
        rcpt = constants.mail_CC.split(",") + constants.mail_BCC.split(",") + [contacts.mailbox[i]];
        msg.attach(MIMEText(message))

        attachmentPath = rf'{constants.root}/attachments/{constants.attachment_name}_{i+1}.pdf'
        filename = f'{constants.attachment_name}_{i+1}.pdf'

        fileformat=filename.format(Path(attachmentPath).name)

        try:
            with open(attachmentPath, "rb") as attachment:
                part = MIMEBase('application', "octet-stream")
                part.set_payload(attachment.read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition',
                                'attachment', filename=fileformat)
                msg.attach(part)
        except Exception as e:
            print(f'------ error {str(e)}: --> {timestamp}: mail could not be sent to {contacts.mailbox[i]} and the following contacts as the attachment "{constants.attachment_name}_{i + 1}.pdf" could not be found. Please rerun the programm manually.');

            if str(e) == f"[Errno 2] No such file or directory: '{attachmentPath}'":
                f.write(f"error: {timestamp}, {contacts.mailbox[i]}, {contacts.name[i]} {contacts.surname[i]}, Team {contacts.team[i]},{filename} \nerror: following contacts \n");
                f.close();

                timestamp_e = includes.mailing.timestamp();

                generateProtocol(timestamp_e);
                sendProtocol(timestamp_e);

                quitServer(server.mailserver);
                exit();

        try:
            message_final = msg.as_string();
            server.mailserver.sendmail(constants.sender_mail, rcpt, message_final);
            f.write(f"Success: {timestamp}, {contacts.mailbox[i]}, {contacts.name[i]} {contacts.surname[i]}, Team {contacts.team[i]}, {filename}\n");
            print(f'------ email sent to (mail, captain, team, status): --> {contacts.mailbox[i]}, {contacts.name[i]} {contacts.surname[i]}, Team {contacts.team[i]}, successful');

        except Exception as error:
            print(f'------ error {str(error)}: --> {timestamp}: mail could not be sent to {contacts.mailbox[i]} and the following contacts as the attachment "{constants.attachment_name}_{i + 1}.pdf" could not be found. Please rerun the programm manually.');
            f.write(f"error: {timestamp}, {contacts.mailbox[i]}, {contacts.name[i]} {contacts.surname[i]}, Team {contacts.team[i]},{filename} \nerror: following contacts \n");
            f.close();

            timestamp_e = includes.mailing.timestamp();

            generateProtocol(timestamp_e);
            sendProtocol(timestamp_e);

            quitServer(server.mailserver);
            exit();

    f.close();
    print("-- output --> mailing successfully executed! \n");

# --- generating system protocol ---
def generateProtocol(timestamp):

    pdf = FPDF();
    pdf.add_page();

    pdf.set_font("Helvetica", f"", 12);
    pdf.cell(200, 10, f'Systemprotokoll {timestamp} | Mailing: {constants.event} | SO KZO', ln=1);

    f = open(rf'{constants.root}/system/txt/systemLog.txt', "r");

    for x in f:
        pdf.set_font("Helvetica", "", 6);
        pdf.cell(220, 10, txt=x);



    pdf.output(rf'{constants.root}/system/pdf/{timestamp}_{constants.attachment_systemProtocol}.pdf');

# --- sending system protocol ---

def sendProtocol(timestamp):

    message = f"Hallo! \n\n Es handelt sich hierbei um ein automatisch erstelltes Systemprotokoll, das zur Kontrolle des vorangehenden Mailings dient. \n\n Angaben zum Mailing: \n- Datum: {formatdate(localtime=True)} \n - Event: {constants.event} \n\n Zur Nachverfolgung dieser Nachricht: \n - UNIX-Timestamp: {timestamp} \n\n Im Anhang findet sich daher: \n {timestamp}_'{constants.attachment_systemProtocol} \n\n _____________________________ \n Kantonsschule Zürcher Oberland \n\n SO KZO \n so@kzo.ch \n https://www.sorg.kzo.ch";

    msg = MIMEMultipart();
    msg['Subject'] = f'Systemprotokoll {timestamp} | Mailing: {constants.event} | SO KZO';
    msg['From'] = constants.sender_mail;
    msg['Date'] = formatdate(localtime=True);
    msg['To'] = constants.mail_systemProtocol;
    msg.attach(MIMEText(message))

    attachmentPath = rf'{constants.root}/system/pdf/{timestamp}_{constants.attachment_systemProtocol}.pdf'
    filename = f'{timestamp}_{constants.attachment_systemProtocol}.pdf'

    fileformat = filename.format(Path(attachmentPath).name)

    try:
        with open(attachmentPath, "rb") as attachment:
            part = MIMEBase('application', "octet-stream")
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', 'attachment', filename=fileformat)
            msg.attach(part)

    except Exception as e:
        print(f'------ error {str(e)}: --> mail could not be sent to {constants.mail_systemProtocol} as the attachment "{constants.attachment_systemProtocol}.pdf" could not be found. Please rerun the programm manually.');

        if str(e) == f"[Errno 2] No such file or directory: '{attachmentPath}'":
            print(f'------ error {str(e)}: --> mail could not be sent to {constants.mail_systemProtocol} as the attachment "{constants.attachment_systemProtocol}.pdf" could not be found. Please rerun the programm manually.');
            server.mailserver.quit()
            exit();

    message_final = msg.as_string();
    server.mailserver.sendmail(constants.sender_mail, constants.mail_systemProtocol, message_final);
    print(f'-- output --> protocol sent to (mail, status): {timestamp}, {constants.mail_systemProtocol}, successful');

def quitServer(mailserver):
    mailserver.quit()
    print("-- output --> The server connection was automatically terminated.\n");
