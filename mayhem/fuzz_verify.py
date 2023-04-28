#!/usr/bin/env python3
import os.path
import atheris
import sys

import random

from PyPDF2.errors import PdfReadError
from cryptography.hazmat import backends
from cryptography.hazmat.primitives.serialization import pkcs12

with atheris.instrument_imports(include=['endesive']):
    from endesive.email import sign
    from endesive.email import verify


def TestOneInput(input_data):
    fdp = atheris.FuzzedDataProvider(input_data)
    ran = fdp.ConsumeInt(fdp.ConsumeIntInRange(0, 4))
    try:
        if ran == 0:
            hash_alg = 'sha1'
            dct = {
                'sigflags': 3,
                'contact': 'jake@mayhem.com',
                'location': 'Elsewhere',
                'signingdate': '01-' + ran + '-2023',
                'reason': 'For Mayhem',
            }
        elif ran == 1:
            hash_alg = 'sha256'
            dct = {
                'sigflags': 3,
                'contact': 'jake@mayhem.com',
                'location': 'Elsewhere',
                'signingdate': '01-' + ran + '-2023',
                'reason': 'For Mayhem',
            }
        elif ran == 2:
            hash_alg = 'sha384'
            dct = {
                'sigflags': 3,
                'contact': 'jake@mayhem.com',
                'location': 'Elsewhere',
                'signingdate': '01-' + ran + '-2023',
                'reason': 'For Mayhem',
            }
        else:
            hash_alg = 'sha512'
            dct = {
                'sigflags': 3,
                'contact': 'jake@mayhem.com',
                'location': 'Elsewhere',
                'signingdate': '01-' + ran + '-2023',
                'reason': 'For Mayhem',
            }
        consumed_bytes = fdp.ConsumeBytes(fdp.remaining_bytes())
        b = sign(consumed_bytes,
                 dct,
                 p12[0],
                 p12[1],
                 p12[2],
                 hash_alg)
        verify(b.decode('utf8'))
    except AssertionError:
        return -1
    except Exception:
        if random.random() > 0.99:
            raise
        return -1

def main():
    atheris.Setup(sys.argv, TestOneInput)
    atheris.Fuzz()


if __name__ == "__main__":
    path = os.path.dirname(os.path.abspath(__file__))
    with open(path + '/demo2_user1.p12', 'rb') as fp:
        p12 = pkcs12.load_key_and_certificates(fp.read(), b'1234', backends.default_backend())
    main()
