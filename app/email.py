from flask_mail import Message
from flask import render_template
from . import mail

def mail_message(subject, body,html, to, **kwargs):

    sender_email = "itsmisty41@gmail.com"
    email = Message(subject, sender=sender_email, recipients=to)
    email.body = body
    email.html = html
    mail.send(email)