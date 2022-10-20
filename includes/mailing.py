from includes import server, constants, contacts
from email.utils import formatdate
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.base import MIMEBase
import os
from email import encoders
from pathlib import Path

def final_check():
    print("-- output --> mailing overview");
    print(f'------ working directory: --> {os.getcwd()}')
    print(f'------ event: --> {constants.event}');
    print(f'------ event info: --> {constants.event_info}');
    print(f'------ sender mail: --> {constants.sender_mail}');
    print(f'------ response mail: --> {constants.response_mail}');
    print(f'------ attachments: --> "{constants.attachment_name}_i.pdf" \n');

    initialize = input("To start the mailing now, enter 'final'!\n -- input --> ")

    if initialize == "final":
        print("-- output --> The mailing is now being initialized! Almost done. :-)");

    else:
        print("-- output --> The program was quit unexpectedly.")
        server.mailserver.quit()
        exit()

print("Mailing process ongoing...");

def send():

    limit = len(contacts.name);

    print("-- output --> feedback loop:");


    for i in range(0, limit, 1):

        message = f'Hallo {contacts.name[i]}! \n\n Die Volleynight naht! Weil du dich bei der Anmeldung als Captain registriert hast, senden wir dir im Anhang die Rechnung für dein Team. Wir bitten dich, diese baldmöglichst zu begleichen. Selbstverständlich gilt dennoch eine Zahlungsfrist von 10 Tagen, weshalb der Zahlungsvorgang von der Teilnahme an der Volleynight entkoppelt ist. \n\n Zur Kontrolle deine Captain-Angaben: \n - Vorname, Name: {contacts.name[i]} {contacts.surname[i]} \n - E-Mail: {contacts.mailbox[i]} \n - Team: {contacts.team[i]} \n\n Im Anhang findest du: \n - "{constants.attachment_name}_{i+1}.pdf" \n\n Solltest du einen Fehler feststellen, wendest du dich bitte per Mail an {constants.response_mail}. Beachte auch, dass diese E-Mail automatisiert mit einem Python-Skript versendet wurde. Reaktionen an {constants.sender_mail} können daher nicht beantwortet werden. \n\n In den nächsten Tagen werden automatisiert Tickets mit QR-Code und Besucher-ID erstellt und an jeden/jede Teilnehmer/-in individuell versendet. \n\n Ausführliche Informationen zum Event finden sich weiterhin auf unserer Website unter {constants.event_info}. Gerne geben wir dir bei individuellen Fragen auch per E-Mail Auskunft. \n\n Wir freuen uns auf eine tolle Volleynight und bedanken uns für die Unterstützung bei der Abwicklung der Zahlung. \n\n Herzliche Grüsse \n SO KZO \n\n _____________________________ \n Kantonsschule Zürcher Oberland \n\n SO KZO \n so@kzo.ch \n https://www.sorg-kzo.ch';
        msg = MIMEMultipart();
        msg['Subject'] = f'{constants.event} | Team {contacts.team[i]} | SO KZO';
        msg['From'] = constants.sender_mail;
        msg['Date'] = formatdate(localtime=True);
        msg['To'] = contacts.mailbox[i];
        msg.attach(MIMEText(message))

        attachmentPath = rf'{os.getcwd()}/attachments/{constants.attachment_name}_{i+1}.pdf'
        filename = f'{constants.attachment_name}_{i+1}.pdf'
        #print(filename)

        #print(attachmentPath)
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
            print(str(e));

            if str(e) == f"[Errno 2] No such file or directory: '{attachmentPath}'":
                print(f'------ error: --> mail could not be sent to {contacts.mailbox[i]} and the following contacts as the attachment "{constants.attachment_name}_{i + 1}.pdf" could not be found. Please rerun the programm manually.');
                server.mailserver.quit()
                exit();

        message_final = msg.as_string();
        server.mailserver.sendmail(constants.sender_mail, contacts.mailbox[i], message_final);
        print(f'------ email sent to (mail, captain, team, status: --> {contacts.mailbox[i]}, {contacts.name[i]} {contacts.surname[i]}, Team {contacts.team[i]}, successful');

    print("-- output --> mailing successfully executed! ");

    server.mailserver.quit()
    print("-- output --> The server connection was automatically terminated.\n");
