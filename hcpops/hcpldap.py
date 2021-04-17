import ldap

allowed_groups = ["Phase2ControlledUsers", "Phase2OpenUsers", "HCPDBUsers"]


class UsernameNotFound(Exception):
    pass


class HcpLdap:
    def __init__(self, uri, password):
        self.ldap = None
        self.uri = uri
        self.reconnect(password)

    def reconnect(self, password):
        bind_dn = "cn=HCPDB Read Write,ou=Service Accounts,ou=HCP Users,dc=hcp,dc=mir"
        ldap.set_option(ldap.OPT_X_TLS_REQUIRE_CERT, ldap.OPT_X_TLS_NEVER)
        ldap_object = ldap.initialize(self.uri)

        ldap_object.protocol_version = ldap.VERSION3
        ldap_object.set_option(ldap.OPT_REFERRALS, 0)

        ldap_object.bind_s(bind_dn, password)
        print("Successfully connected to LDAP.")
        self.ldap = ldap_object

    def find_user(self, username):
        results = self.ldap.search_s(
            base="dc=hcp,dc=mir",
            scope=ldap.SCOPE_SUBTREE,
            filterstr="(name={})".format(username),
            attrlist=None,
        )
        try:
            return results[-4]
        except:
            raise UsernameNotFound(username)

    def get_groups(self, username):
        try:
            me = self.find_user(username)
            groups = [g.decode().split(",", 1)[0][3:] for g in me[1]["memberOf"]]
            return groups
        except:
            return []

    def add_to_group(self, username, group="Phase2ControlledUsers"):
        if group not in allowed_groups:
            raise Exception(
                "That group %s is not allowed option. (allowed: %s)"
                % (group, allowed_groups)
            )
        group_dn = "CN=%s,OU=Web Security Groups,OU=HCP Users,DC=hcp,DC=mir" % group
        user = self.find_user(username)[0].encode("ascii", "ignore")

        try:
            self.ldap.modify_s(group_dn, [(ldap.MOD_ADD, "member", user)])
            return True
        except ldap.ALREADY_EXISTS:
            return True
        return False

    def get_groups_n(self, username):
        groups = self.get_groups(username)
        bitfield_labels = ("HCPDBUsers", "Phase2OpenUsers", "Phase2ControlledUsers")

        result = 0
        for gi, gname in enumerate(bitfield_labels):
            if gname in groups:
                result += 1 << gi
        return result
