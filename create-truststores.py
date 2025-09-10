#!/usr/bin/env python3

from pathlib import Path
import subprocess

BUILD_PATH = Path("build")

def generate_truststore(gates, truststore_type):
    truststore_path = BUILD_PATH / ("%s-truststore.p12" % truststore_type)
    truststore_path.unlink(missing_ok=True)

    for g in gates:
        subprocess.run(["keytool",
                        "-import",
                        "-noprompt",
                        "-alias", g.name,
                        "-keystore", truststore_path,
                        "-file", g / ("%s.pem" % truststore_type),
                        "-storepass", "changeit"
                        ])

def make_legacy_ts(truststore_type):
    truststore_path = BUILD_PATH / ("%s-truststore.p12" % truststore_type)
    legacy_ts_path = BUILD_PATH / ("%s-legacy-truststore.p12" % truststore_type)

    subprocess.run(["keytool",
                    "-J-Dkeystore.pkcs12.legacy",
                    "-importkeystore",
                    "-srckeystore", truststore_path,
                    "-destkeystore", legacy_ts_path,
                    "-srcstoretype", "PKCS12",
                    "-deststoretype", "PKCS12",
                    "-srcstorepass", "changeit",
                    "-deststorepass", "changeit"
                    ])

def main():
    gates = [ f for f in Path("gates").iterdir() if f.is_dir() ]

    print('Generating eDelivery truststores for Gates:')
    for g in gates:
        print('  * %s' % g.name)

    BUILD_PATH.mkdir(exist_ok=True)
    generate_truststore(gates, "ap")
    generate_truststore(gates, "tls")

    make_legacy_ts("ap")
    make_legacy_ts("tls")

if __name__ == '__main__':
    main()
