from subprocess import check_output


def get_credentials(site):
    return (
        check_output(["pass", "show", f"{site}/username"]).decode().strip(),
        check_output(["pass", "show", f"{site}/password"]).decode().strip(),
    )
