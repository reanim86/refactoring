import email
import smtplib
import imaplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class Mail():
    def __init__(self, gmail_login, gmail_pass):
        self.gmail_login = gmail_login
        self.gmail_pass = gmail_pass
        self.gmail_smtp = "smtp.gmail.com"
        self.gmail_imap = "imap.gmail.com"

    def send_message(self, mail_recipients, mail_subject, mail_message):
        msg = MIMEMultipart()
        msg['From'] = self.gmail_login
        msg['To'] = ', '.join(mail_recipients)
        msg['Subject'] = mail_subject
        msg.attach(MIMEText(mail_message))
        ms = smtplib.SMTP(self.gmail_smtp, 587)
        ms.ehlo()
        ms.starttls()
        ms.ehlo()
        ms.login(self.gmail_login, self.gmail_pass)
        ms.sendmail(self.gmail_login, self.gmail_pass)
        msg.as_string()
        ms.quit()
        return

    def recieve_message(self, mail_header):
        mail = imaplib.IMAP4_SSL(self.gmail_imap)
        mail.login(self.gmail_login, self.gmail_pass)
        mail.list()
        mail.select("inbox")
        criterion = '(HEADER Subject "%s")' % mail_header if mail_header else 'ALL'
        result, data = mail.uid('search', None, criterion)
        assert data[0], 'There are no letters with current header'
        latest_email_uid = data[0].split()[-1]
        result, data = mail.uid('fetch', latest_email_uid, '(RFC822)')
        raw_email = data[0][1]
        email_message = email.message_from_string(raw_email)
        mail.logout()
        return

if __name__ == '__main__':
    login = 'login@gmail.com'
    password = 'qwerty'
    subject = 'Subject'
    recipients = ['vasya@email.com', 'petya@email.com']
    message = 'Message'
    header = None
    mail = Mail(login, password)
    mail.send_message(recipients, subject, message)
    mail.recieve_message(header)

