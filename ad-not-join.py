from ms_active_directory import ADDomain

example_domain_dns_name = 'examen.local'
domain = ADDomain(example_domain_dns_name)
ldap_servers = domain.get_ldap_uris()
kerberos_servers = domain.get_kerberos_uris()

# re-discover servers in dns and sort them by RTT again at a later time to pick up changes
domain.refresh_ldap_server_discovery()
domain.refresh_kerberos_server_discovery()