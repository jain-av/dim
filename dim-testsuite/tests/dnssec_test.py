import unittest
import hashlib
from dns.dnssec import dnskey_tag, make_ds

pubkey = 'AwEAAbJKLSzK2R+DpWt9Vudk02db2actR3NsS6TZhLBrs4ud5S4U9e/3Yz90YrQwcJC83seoAH942nTMOt+NlKfXWRjqVZUP+tkxWqFvwKU82UGg/TWmbqH4BQY/ZM6ybdo2Z2fkpWwpTpf6/37vnS7/Rq7TI/sFA7R81PHAvr1dN5AQYpYNB/RhRaQ0q+0k/kBVuReeffNVN36uO9ECpBDjiE1j3uMbEzwxI/ht/OyXJ3w7S8iE06qwS/44KzEYmkxYIUwhjyvWAMbfEzw4rE7fEHgvnQKoHXe4azamtLbyDTn/NZDwzBjU7ewZIUpANV/fUm7t5ksvAmXi2JsE3YZHshs=' # noqa
algorithm = 8
flags = 257
protocol = 3


class DNSKEYTest(unittest.TestCase):
    def test_dnskey_tag(self):
        assert dnskey_tag(flags, protocol, algorithm, pubkey.encode('ascii')) == 20842

    def test_ds_hash(self):
        dnskey = flags, protocol, algorithm, pubkey.encode('ascii')
        name = 'a.com'
        assert make_ds(name, dnskey, 'SHA1').digest.hex().upper() == \
            '91053B9A59B05FB08D5469472A5F1B588C5CA092'
        assert make_ds(name, dnskey, 'SHA256').digest.hex().upper() == \
            'FFB15B5EF961E0AE3474E7B868FBD3C8F7C861D3BEA4527382CBDA791D4B9FF4'
