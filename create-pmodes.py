#!/usr/bin/env python3

from pathlib import Path

TEMPLATE_PARTY_ENDPOINT = '''<party name="NAME" endpoint="URL">
    <identifier partyId="NAME" partyIdType="partyTypeUrn"/>
</party>'''
TEMPLATE_PARTY_INITIATOR = '''<initiatorParty name="NAME"/>'''
TEMPLATE_PARTY_RESPONDER = '''<responderParty name="NAME"/>'''

BUILD_PATH = Path("build")

def generate(party, parties):
    template = read_file_content(Path("pmode-template.xml"))

    endpoints_snippet = '\n'.join([TEMPLATE_PARTY_ENDPOINT
                                  .replace('NAME', p.name)
                                  .replace('URL', read_file_content(p / "endpoint-url.txt"))
                                   for p
                                   in parties])
    initiators_snippet = '\n'.join([TEMPLATE_PARTY_INITIATOR.replace('NAME', p.name) for p in parties])
    responder_snippet = '\n'.join([TEMPLATE_PARTY_RESPONDER.replace('NAME', p.name) for p in parties])

    pmode = (template
                .replace('PARTY_SELF', party.name)
                .replace('<!-- PARTY_ENDPOINTS -->', endpoints_snippet)
                .replace('<!-- PARTY_INITIATORS -->', initiators_snippet)
                .replace('<!-- PARTY_RESPONDERS -->', responder_snippet))

    return pmode


def read_file_content(path):
    return path.read_text(encoding='utf-8').rstrip()


def write_to_file(path, content):
    path.write_text(content, encoding='utf-8')


def main():
    parties = [ f for f in Path("gates").iterdir() if f.is_dir() ]

    print('Generating pmodes for parties:')
    for p in parties:
        print('  * %s' % p.name)

    BUILD_PATH.mkdir(exist_ok=True)
    for p in parties:
        write_to_file(BUILD_PATH / ("%s-pmode.xml" % p.name), generate(p, parties))


if __name__ == '__main__':
    main()
