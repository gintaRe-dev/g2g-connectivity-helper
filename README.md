# Tool to make it easier to connect eFTI gate

Inspired by testfest-tools eFTI repository used for testfest activities

<!-- TOC -->
  * [Requirements](#requirements)
  * [Adding a new Gate](#adding-a-new-gate)
  * [Generating PMode files and eDelivery truststores locally](#generating-pmode-files-and-edelivery-truststores-locally)
  * [GitHub Actions (GHA) artefacts](#github-actions-gha-artefacts)
<!-- TOC -->

## Requirements

* Python 3.9 or greater

## Adding a new Gate

To add a new Gate, create a folder under `gates/` with the name of your Gate.
Please note, that the name of the folder is also used to create the PModes and eDelivery truststores (AP + TLS).

Now, add the following files to the folder:

- `ap.pem` eDelivery Access Point (AP) public certificate
- `tls.pem` eDelivery TLS public certificate
- `endpoint-url.txt` eDelivery AP address, e.g., https://gate.testfest.eu/services/msh. **Do not** include anything else in
  the file!
- README.md for extra information like IP address for outgoing traffic
  from your gate, so other parties can set up their firewall rules

## Generating PMode files and eDelivery truststores locally

Run the following command to generate PMode file for each Gate:

```shell
python3 create-pmodes.py
```

And to generate new eDelivery AP and TLS truststores, run command:

```shell
python3 create-truststores.py
```

Generated files can be found from `build` directory.
Default password for truststores is `changeit`.

The generated files are:
* ap-truststore.p12 - The truststore eDelivery Access point uses for
  verifying the signatures
* ap-legacy-truststore.p12 - AP truststore for legacy environments
* tls-truststore.p12 - The struststore eDelivery AP uses for mTLS
* tls-legacy-truststore.p12 - TLS truststore for legacy environments

## GitHub Actions (GHA) artefacts

Generated files are also automatically uploaded as GHA artefacts.
You can download the files from GitHub by viewing one of the workflow runs.
