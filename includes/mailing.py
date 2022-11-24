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

    timestamp();

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

    f = open(f"{constants.root}/system/txt/{timestamp}_systemLog.txt", "x");
    f.write(f"msg: index, timestamp, email, name surname, category \n");

    limit = len(contacts.name);

    print("-- output --> feedback loop:");

    for i in range(0, limit, 1):

        timestamp_mailing = formatdate(localtime=True);

        if constants.courtesy == 0:
            message = f'Hallo {contacts.name[i]} \n\n Schön, dass du dich für den Skitag 2023 angemeldet hast! Wir freuen uns über deine Teilnahme. :-) \n\n Zur Kontrolle deine Kontaktangaben: \n - Vorname, Name: {contacts.name[i]} {contacts.surname[i]} \n - E-Mail: {contacts.mailbox[i]} \n - Kategorie: {contacts.team[i]} \n\n Wenn du einen Fehler feststellst, bitten wir dich um eine rasche Benachrichtigung, sodass wir diesen beheben können. \n\n Zur Nachverfolgung dieser Nachricht: \n -Timestamp: {timestamp_mailing} \n\n Gerne senden wir dir im Anhang deine personalisierte Rechnung ("{constants.attachment_name}_{i+1}.pdf"). Wir bitten dich, diese baldmöglichst zu begleichen. \n\n Bitte beachte, dass diese Nachricht automatisiert durch ein Python-Skript verschickt wurde. Reaktionen an {constants.sender_mail} können daher nicht beantwortet werden. Ausführliche Informationen zum Event finden sich weiterhin unter {constants.event_info}. Gerne sind wir für individuelle Fragen erreichbar. Du erreichst uns jederzeit unter {constants.response_mail}. \n\n Bis bald im Schnee! \n\n Herzliche Grüsse \n SO KZO \n\n _____________________________ \n Kantonsschule Zürcher Oberland \n\n SO KZO \n so@kzo.ch \n https://www.sorg.kzo.ch';

        else:
            message = f'Hallo! \n SO KZO \n\n _____________________________ \n Kantonsschule Zürcher Oberland \n\n SO KZO \n so@kzo.ch \n https://www.sorg.kzo.ch';

        msg = MIMEMultipart();
        msg['Subject'] = f'{constants.event} | SO KZO';
        msg['From'] = constants.sender_mail;
        msg['Date'] = timestamp_mailing;
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
                part.add_header('Content-Disposition', 'attachment', filename=fileformat)
                msg.attach(part)
        except Exception as e:
            print(f'------ error {str(e)}: --> {timestamp_mailing}: mail could not be sent to {contacts.mailbox[i]} and the following contacts as the attachment "{constants.attachment_name}_{i + 1}.pdf" could not be found. Please rerun the programm manually.');

            f.write(f"error: {i}, {timestamp_mailing}, {contacts.mailbox[i]}, {contacts.name[i]} {contacts.surname[i]}, {contacts.team[i]},{filename} \nerror: following contacts \n\nthe following error occured: {str(e)} \n");
            f.close();

            sendProtocol();

            quitServer(server.mailserver);
            exit();

        try:
            message_final = msg.as_string();
            server.mailserver.sendmail(constants.sender_mail, rcpt, message_final);
            f.write(f"Success: {i}, {timestamp_mailing}, {contacts.mailbox[i]}, {contacts.name[i]} {contacts.surname[i]}, {contacts.team[i]}, {filename}\n");
            print(f'------ email sent to (mail, captain, team, status): --> {contacts.mailbox[i]}, {contacts.name[i]} {contacts.surname[i]}, {contacts.team[i]}, successful');

        except Exception as error:
            print(f'------ error {str(error)}: --> {timestamp_mailing}: mail could not be sent to {contacts.mailbox[i]} and the following contacts as the attachment "{constants.attachment_name}_{i + 1}.pdf" could not be found. Please rerun the programm manually.');
            f.write(f"error: {i}, {timestamp_mailing}, {contacts.mailbox[i]}, {contacts.name[i]} {contacts.surname[i]}, Team {contacts.team[i]},{filename} \nerror: following contacts \n\nthe following error occured: {str(e)} \n");
            f.close();

            sendProtocol();

            quitServer(server.mailserver);
            exit();

    f.close();
    print("-- output --> mailing successfully executed! \n");

# --- sending system protocol ---

def sendProtocol():

    if constants.index_systemProtocol == 0:
        sendTXT(timestamp);
    else:
        sendPDF(timestamp);

def sendTXT(timestamp):

    message = f"Hallo Admin! \n\n Es handelt sich hierbei um ein automatisch erstelltes Systemprotokoll, das der Kontrolle des vorangehenden Mailings dient. \n\n Angaben zum Mailing: \n- Datum: {formatdate(localtime=True)} \n - Event: {constants.event} \n\n Zur Nachverfolgung dieser Nachricht: \n - UNIX-Timestamp: {timestamp} \n\n Im Anhang findet sich daher: \n - {timestamp}_systemLog.txt \n\n Binäre Grüsse \n Computer :-) \n\n _____________________________ \n Kantonsschule Zürcher Oberland \n\n SO KZO \n so@kzo.ch \n https://www.sorg.kzo.ch";

    msg = MIMEMultipart();
    msg['Subject'] = f'Systemprotokoll {timestamp} | Mailing: {constants.event} | SO KZO';
    msg['From'] = constants.sender_mail;
    msg['Date'] = formatdate(localtime=True);
    msg['To'] = constants.mail_systemProtocol;
    msg.attach(MIMEText(message))

    attachmentPath = rf'{constants.root}/system/txt/{timestamp}_systemLog.txt'
    filename = f'{timestamp}_systemLog.txt'

    fileformat = filename.format(Path(attachmentPath).name)

    try:
        with open(attachmentPath, "rb") as attachment:
            part = MIMEBase('application', "octet-stream")
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', 'attachment', filename=fileformat)
            msg.attach(part)

    except Exception as e:
        print(f'------ error {str(e)}: --> mail could not be sent to {constants.mail_systemProtocol} as the attachment "{timestamp}_systemLog.txt" could not be found. Please rerun the programm manually.');
        server.mailserver.quit()
        exit();

    message_final = msg.as_string();
    server.mailserver.sendmail(constants.sender_mail, constants.mail_systemProtocol, message_final);
    print(f'-- output --> protocol sent to (timestamp, mail, status): {timestamp}, {constants.mail_systemProtocol}, successful');

def generateProtocol(timestamp):

    pdf_array = [];

    f = open(f"{constants.root}/system/txt/{timestamp}_systemLog.txt", "r");

    for line in f:
        pdf_array.append(line);

    limit = len(pdf_array);

    pdf = FPDF();
    pdf.add_page();

    pdf.set_font("Helvetica", f"", 12);
    pdf.cell(200, 10, f'Systemprotokoll {timestamp} | Mailing: {constants.event} | SO KZO', ln=1);

    for i in range(0, 1, 1) in f:
            pdf.set_font("Helvetica", "", 6);
            pdf.cell(220+10*i, 10, pdf_array[i]);

    # f = open(rf'{constants.root}/system/txt/{timestamp}_systemLog.txt', "r");

    f.close();

    pdf.output(rf'{constants.root}/system/pdf/{timestamp}_systemLog.pdf');

def sendPDF(timestamp):

    generateProtocol(timestamp);

    message = f"Hallo Admin! \n\n Es handelt sich hierbei um ein automatisch erstelltes Systemprotokoll, das zur Kontrolle des vorangehenden Mailings dient. \n\n Angaben zum Mailing: \n- Datum: {formatdate(localtime=True)} \n - Event: {constants.event} \n\n Zur Nachverfolgung dieser Nachricht: \n - UNIX-Timestamp: - {timestamp} \n\n Im Anhang findet sich daher: \n - {timestamp}_systemLog.pdf \n\n _____________________________ \n Kantonsschule Zürcher Oberland \n\n SO KZO \n so@kzo.ch \n https://www.sorg.kzo.ch";

    msg = MIMEMultipart();
    msg['Subject'] = f'Systemprotokoll {timestamp} | Mailing: {constants.event} | SO KZO';
    msg['From'] = constants.sender_mail;
    msg['Date'] = formatdate(localtime=True);
    msg['To'] = constants.mail_systemProtocol;
    msg.attach(MIMEText(message))

    attachmentPath = rf'{constants.root}/system/pdf/{timestamp}_systemLog.pdf'
    filename = f'{timestamp}_systemLog.pdf'

    fileformat = filename.format(Path(attachmentPath).name)

    try:
        with open(attachmentPath, "rb") as attachment:
            part = MIMEBase('application', "octet-stream")
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', 'attachment', filename=fileformat)
            msg.attach(part)

    except Exception as e:
        print(
            f'------ error {str(e)}: --> mail could not be sent to {constants.mail_systemProtocol} as the attachment "{timestamp}_systemLog.pdf" could not be found. Please rerun the programm manually.');

        if str(e) == f"[Errno 2] No such file or directory: '{attachmentPath}'":
            print(
                f'------ error {str(e)}: --> mail could not be sent to {constants.mail_systemProtocol} as the attachment "{timestamp}_systemLog.pdf" could not be found. Please rerun the programm manually.');
            server.mailserver.quit()
            exit();

    message_final = msg.as_string();
    server.mailserver.sendmail(constants.sender_mail, constants.mail_systemProtocol, message_final);
    print(f'-- output --> protocol sent to (mail, status): {timestamp}, {constants.mail_systemProtocol}, successful');

# --- terminate server connection ---

def quitServer(mailserver):
    mailserver.quit()
    print("-- output --> The server connection was automatically terminated.\n");
