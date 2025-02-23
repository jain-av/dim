import base64
import math

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import utils
from cryptography.hazmat.backends import default_backend
from cryptography.exceptions import InvalidSignature


_file_privkey_rsa = """Private-key-format: v1.2
Algorithm: %(alg)d (%(algtxt)s)
Modulus: %(n)s
PublicExponent: %(e)s
PrivateExponent: %(d)s
Prime1: %(p)s
Prime2: %(q)s
Exponent1: %(dmp1)s
Exponent2: %(dmq1)s
Coefficient: %(u)s
"""


def _rsa2dnskey(key):
    """Get RSA public key in DNSKEY resource record format (RFC-3110)"""
    octets = b''
    e = key.public_numbers().e
    n = key.public_numbers().n
    explen = int(math.ceil(math.log(e, 2)/8))
    if explen > 255:
        octets = b"\x00"
    octets += (explen.to_bytes(1, 'big') +
               e.to_bytes(explen, 'big') +
               n.to_bytes(math.ceil(math.log(n, 2)/8), 'big'))
    return octets


def generate_RSASHA256_key_pair(bits):
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=bits,
        backend=default_backend()
    )
    public_key = private_key.public_key()
    pubkey = base64.b64encode(_rsa2dnskey(public_key))
    RSASHA256 = 8
    keydata = dict(alg=RSASHA256,
                   algtxt='RSASHA256')
    
    # Extract data for private key file format
    private_numbers = private_key.private_numbers()
    public_numbers = public_key.public_numbers()
    
    keydata['n'] = base64.b64encode(public_numbers.n.to_bytes(math.ceil(math.log(public_numbers.n, 2)/8), 'big')).decode('utf-8')
    keydata['e'] = base64.b64encode(public_numbers.e.to_bytes(math.ceil(math.log(public_numbers.e, 2)/8), 'big')).decode('utf-8')
    keydata['d'] = base64.b64encode(private_numbers.d.to_bytes(math.ceil(math.log(private_numbers.d, 2)/8), 'big')).decode('utf-8')
    keydata['p'] = base64.b64encode(private_numbers.p.to_bytes(math.ceil(math.log(private_numbers.p, 2)/8), 'big')).decode('utf-8')
    keydata['q'] = base64.b64encode(private_numbers.q.to_bytes(math.ceil(math.log(private_numbers.q, 2)/8), 'big')).decode('utf-8')
    keydata['dmp1'] = base64.b64encode(private_numbers.dmp1.to_bytes(math.ceil(math.log(private_numbers.dmp1, 2)/8), 'big')).decode('utf-8')
    keydata['dmq1'] = base64.b64encode(private_numbers.dmq1.to_bytes(math.ceil(math.log(private_numbers.dmq1, 2)/8), 'big')).decode('utf-8')
    keydata['u'] = base64.b64encode(private_numbers.iqmp.to_bytes(math.ceil(math.log(private_numbers.iqmp, 2)/8), 'big')).decode('utf-8')

    privkey = _file_privkey_rsa % keydata
    return (pubkey, privkey)
