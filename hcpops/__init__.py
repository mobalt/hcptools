from .hcpldap import HcpLdap, UsernameNotFound
from .email import send_email


def updatedb(session, firstname, lastname, email, status, username):
    n_to_status = {0: "No Account", 1: "No DUT", 3: "Access Granted"}
    status = n_to_status[status]

    data = dict(
        firstname=firstname,
        lastname=lastname,
        email=email,
        status=status,
        username=username,
    )

    return session.post("https://hcp-ops.humanconnectome.org/update_db", json=data)
