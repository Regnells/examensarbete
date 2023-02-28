from ldap3 import Server, Connection, ALL
from pyad import *

class ad_tools:
    def __init__(self):
        self.user_session = None
        self.useredited = None
        self.server = Server('172.16.1.36', get_info=ALL)

    def authenticate(self, username, password):

        # Set up formatting of username for later use in tool.
        self.useredited = username.replace(".", " ")

        # Looks pretty bad but it works.
        try:
            self.user_session = conn = Connection(self.server, user=f"{username}@examen.local", password=f"{password}", auto_bind=True)
            if conn.result['result'] == 0:
                return True
            else:
                pass
        except:
            pass

    # Gets all the groups the user is in
    def get_groups(self):
        conn = self.user_session
        conn.search(f'cn={self.useredited},ou=exusers,dc=examen,dc=local', '(objectClass=person)', attributes=['memberOf'])
        return conn.entries[0].memberOf.values

    def check_hr(self):
        conn = self.user_session
        conn.search(f'cn={self.useredited},ou=exusers,dc=examen,dc=local', '(objectClass=person)', attributes=['memberOf'])
        if "HR" in str(conn.entries[0].memberOf.values):
            return True
        else:
            return False
        
    def check_it(self):
        conn = self.user_session
        conn.search(f'cn={self.useredited},ou=exusers,dc=examen,dc=local', '(objectClass=person)', attributes=['memberOf'])
        if "IT" in str(conn.entries[0].memberOf.values):
            return True
        else:
            return False
    
    # All earlier functions are related to the login process, this one is for the admin tool.
    def find_user(self, username):
        conn = self.user_session
        conn.search(f'cn={username},ou=exusers,dc=examen,dc=local', '(objectClass=person)', attributes=['memberOf', 'cn'])
        groups = conn.entries[0].memberOf.values
        name = conn.entries[0].cn.value
        return name, groups
    
    def add_user(self, username, password):
        # This requires the PC to be domain joined.
        pyad.set_defaults(ldap_server="172.16.1.36", username="administrator", password="Linux4Ever")
        ou = pyad.adcontainer.ADContainer.from_dn("OU=exusers,DC=examen,DC=local")
        user = pyad.aduser.ADUser.create(username, ou, password)

# if __name__ == "__main__":
#     ad = ad_tools()
#     ad.authenticate('anna.jansson', 'Linux4Ever')
#     ad.add_user('test', 'Linux4Ever')

