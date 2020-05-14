from flask_mail import Message
from flask import render_template
from . import mail

def mail_message(subject, body,html, to, **kwargs):

    