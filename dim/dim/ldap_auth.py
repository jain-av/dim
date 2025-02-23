import logging

import ldap3
import ssl
from flask import current_app as app

def check_credentials(username: str, password: str):
    server_kwargs = {}
    tls_kwargs = app.config.get_namespace('LDAP_SERVER_TLS_')
    if app.config['LDAP_SERVER'].startswith('ldaps'):
        if 'validate' in tls_kwargs.keys() and tls_kwargs.get('validate'):
            tls_kwargs['validate'] = ssl.CERT_NONE
        else:
            tls_kwargs['validate'] = ssl.CERT_REQUIRED
        server_kwargs['tls'] = ldap3.Tls(**tls_kwargs)

    ldap_server = ldap3.Server(app.config['LDAP_SERVER'], **server_kwargs)

    user_dn = app.config['LDAP_USER_DN'] % username
    if app.config['LDAP_SEARCH_BASE']:
        user_dn += "," + app.config['LDAP_SEARCH_BASE']

    conn = ldap3.Connection(ldap_server, user=user_dn, password=password, client_strategy=ldap3.SAFE_SYNC)
    try:
        status = conn.bind()
    except ldap3.core.exceptions.LDAPBindError as e:
        status = False
        logging.info('LDAP login for user %s failed: %s', username, str(e))
    if not status:
        logging.info('LDAP login for user %s failed', username)
    return status
