from ldap3 import Server, Connection, ALL

#Take input from user
# username = input("Enter your username: ")
# password = input("Enter your password: ")

server = Server('examen.local', get_info=ALL)
#conn = Connection(server, user=f"{username}", password=f"{password}", auto_bind=True)
conn = Connection(server, user="anna@examen.local", password="Linux4Ever", auto_bind=True)
#conn = Connection(server, 'uid=anna,ou=exusers,dc=examen,dc=local', 'Linux4Ever', auto_bind=True)

#print(type(conn))

conn.search('cn=anna jansson,ou=exusers,dc=examen,dc=local', '(objectClass=person)', attributes=['memberOf'])
#print(conn.entries)
for i in conn.entries:
    
    # Clunky string manipulation to get the group name. Wont work if user is in multiple groups
    # i = str(i.memberOf)
    # i = i[3:5]
    # if i == "HR":
    #     print("You are in the HR group")

    # Better way to get the group name
    if "HR" in str(i.memberOf):
        print("You are in the HR group")


