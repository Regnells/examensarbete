from ldap3 import Server, Connection, ALL

#Take input from user
# username = input("Enter your username: ")
# password = input("Enter your password: ")

class ad_tools:
    def __init__(self):
        self.user_session = None
        self.useredited = None
        self.server = Server('172.16.1.36', get_info=ALL)

    def authenticate(self, username, password):

        # Edit username input for LDAP search
        self.useredited = useredited = username.replace(".", " ")
        self.user_session = conn = Connection(self.server, user=f"{username}@examen.local", password=f"{password}", auto_bind=True)

        try:
            if conn.result['result'] == 0:
                return True
            else:
                pass
        except:
            pass
        #conn.search(f'cn={useredited},ou=exusers,dc=examen,dc=local', '(objectClass=person)', attributes=['memberOf'])

    # Gets all the groups the user is in
    def get_groups(self):
        conn = self.user_session
        conn.search(f'cn={self.useredited},ou=exusers,dc=examen,dc=local', '(objectClass=person)', attributes=['memberOf'])
        return conn.entries[0].memberOf.values
    
        #return conn.response[0]['attributes']['memberOf']
        # for i in conn.entries:
        #     if "HR" in str(i.memberOf):
        #         print("You are in the HR group")
        #     else:
        #         print("You are not in the HR group")

        # print(useredited)

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
    

# if __name__ == "__main__":
#     ad = ad_tools()
#     ad.authenticate("bosse.blodtorstig", "Linux4Ever")
#     if ad.check_it():
#         print("IT")
#     else:
#         print("fail")


