import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from news_paper.config import PICKUP


class Mail:

    def __init__(self, sender: str):
        self.__sender = sender
        self.__message = None
        self.__server = smtplib.SMTP_SSL("smtp.mail.ru", 465)
        self.__attachment = []

    def prepare_html(self, subject: str, html_content: str) -> None:
        self.__message = MIMEMultipart()
        self.__message["From"] = self.__sender
        self.__message["Subject"] = subject
        self.__message.attach(MIMEText(html_content, "html"))

    def prepare_text(self, subject: str, text_content: str) -> None:
        self.__message = MIMEMultipart()
        self.__message["From"] = self.__sender
        self.__message["Subject"] = subject
        self.__message.attach(MIMEText(text_content, "plain"))

    def send(self, destination: str) -> bool:
        try:
            self.__message["To"] = destination
            self.__server.sendmail(self.__sender, destination, self.__message.as_string())
            return True
        except Exception as ex:
            print(str(ex))
            return False

    def __enter__(self):
        self.__server.login(self.__sender, PICKUP)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__server.quit()

