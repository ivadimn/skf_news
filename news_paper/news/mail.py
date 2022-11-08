import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.audio import MIMEAudio
from email.mime.application import MIMEApplication
from email.mime.base import MIMEBase
from email import encoders
import mimetypes

vadimn = "WV2mrczR7jLirWjsmp1R"
pickup = "9NQsHFmqmeYCynFEf9QE"


class Mail:

    def __init__(self, sender: str):
        self.__sender = sender
        self.__server = smtplib.SMTP_SSL("smtp.mail.ru", 465)
        self.__message = None
        self.__attachment = []

    def prepare(self, subject: str, mbody: str, html_content: str) -> None:
        self.__message = MIMEMultipart()
        self.__message["From"] = self.__sender
        self.__message["Subject"] = subject
        self.__message.attach(MIMEText(html_content, "html"))

    def send(self, destinations: list) -> bool:
        try:
            self.__server.login(self.__sender, pickup)
            self.__message["To"] = ", ".join(destinations)
            self.__server.sendmail(self.__sender, destinations, self.__message.as_string())
            return True
        except Exception as ex:
            print(str(ex))
            return False
        finally:
            self.__server.quit()
