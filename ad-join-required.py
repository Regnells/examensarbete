from pyad import *

# This program requires the computer to be joined to the domain


# Connect to AD
pyad.set_defaults(ldap_server="example.local", username="anna", password="Linux4Ever")
user = pyad.aduser.ADUser.from_cn("anna")
