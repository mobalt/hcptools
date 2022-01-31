import html.entities
from smtplib import SMTP


HTML_TABLE = {k: "&{};".format(v) for k, v in html.entities.codepoint2name.items()}


def html_escape(text):
    return text.translate(HTML_TABLE)


def send_email(
    lastname,
    email,
    title="Dr.",
    status=0,
    username="",
    sender_name="Moises Baltazar",
    sender_email="moises@wustl.edu",
    subject=None,
    cc=None,
    email_format=None,
    host="localhost",
    port=1025,
):
    if cc is None:
        cc = DEFAULT_CC_LIST
    elif type(cc) is str:
        cc = {cc}
    if email_format is None:
        email_format = DEFAULT_EMAIL_FORMAT
    if subject is None:
        subject = DEFAULT_SUBJECT

    body = MESSAGES_BY_STATUS[status].format(username=html_escape(username))
    message = email_format.format(
        title=html_escape(title),
        lastname=html_escape(lastname),
        body=body,
        sender_name=sender_name,
        sender_email=sender_email,
        to=email,
        cc=", ".join(cc),
        subject=subject,
    ).encode("UTF-8")

    to_emails = cc | {email}

    with SMTP(host, port) as smtp:
        smtp.sendmail(sender_email, to_emails, message)
