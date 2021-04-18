import html.entities
from smtplib import SMTP

MESSAGES_BY_STATUS = {
    0: """
<p>
FYI, your request for access to restricted HCP data has been approved conditional 
on your additional acceptance of the HCP Open Access Data Use Terms.  On the ConnectomeDB 
website, I was unable to locate a ConnectomeDB account under your name or evidence 
that you have already accepted the Open Access Data Use Terms.  To fulfill the 
conditions of this approval, please take the following steps and respond to this 
email when completed:
</p>
<ol>
<li> Register for a ConnectomeDB account at <a href="https://db.humanconnectome.org">https://db.humanconnectome.org</a></li>
<li> Log into your account and read and accept the Open Access Data Use Terms that you are directed to by the site.</li>
</ol>
<p>
If you already have an account and have accepted the Open Access Data Use Terms, 
<u>please let me know the username</u> and I will grant access to that account.
</p><p>
As a reminder, because of the sensitivity of Restricted Data, please do not forward 
it to others in your laboratory; when their Restricted Access application is submitted 
and approved, they will be able to access the data themselves.
</p>
""",
    1: """
<p>
FYI, your request for access to restricted HCP data has been approved conditional 
on your additional acceptance of the HCP Open Access Data Use Terms.  On the 
ConnectomeDB website, I found an account '<b>{username}</b>' that appears to be yours, 
but the Open Access Data Use Terms had not been accepted.  To fulfill the conditions 
of this approval, please log into your account and read and accept the HCP Open 
Access Data Use Terms that you are directed to by the site.  If you are unable 
to access your account because the account hasn't been verified, please click the 
'<span style="font-family: monospace">Resend email verification</span>' link next to the '<span style="font-family: monospace;">Log In</span>' button.  Please let me know 
when you have accepted the Open Access terms and I will grant access to the restricted data.
</p><p>
As a reminder, because of the sensitivity of Restricted Data, please do not 
forward it to others in your laboratory; when their Restricted Access application 
is submitted and approved, they will be able to access the data themselves.
</p>
""",
    3: """
<p>
Per approval of your application for access to Restricted Access HCP data, I've 
granted access to restricted data to your '<b>{username}</b>' account on 
<a href="https://db.humanconnectome.org">https://db.humanconnectome.org</a>.
</p><p>
As a reminder, because of the sensitivity of Restricted Data, please do not forward 
it to others in your laboratory; when their Restricted Access application is 
submitted and approved, they will be able to access the data themselves.
</p><p>
Please feel free to contact me if you have any questions or are unable to access 
the restricted data.
</p>
""",
}
DEFAULT_EMAIL_FORMAT = """From: {sender_name} <{sender_email}>
To: {to}
CC: {cc}
MIME-Version: 1.0
Content-type: text/html
Subject: {subject}

<html>
<body>
<p>{title} {lastname},</p>

{body}

<br />
<p>
    Regards,<br />
    {sender_name}
</p>

</body></html>"""
DEFAULT_CC_LIST = {
    "scurtiss@brainvis.wustl.edu",
    "rlriney@wustl.edu",
    "hodgem@wustl.edu",
    "plenzini@wustl.edu",
    "moises@wustl.edu",
}
DEFAULT_SUBJECT = "Access to Restricted Data in ConnectomeDB"

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
