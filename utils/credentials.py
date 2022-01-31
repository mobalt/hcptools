from subprocess import check_output


def get_credentials(site):
    p = check_output(["pass", "show", site]).decode().strip()
    password, username = p.split("\n")
    username = username.split(" ")[1]
    return ( username, password)
