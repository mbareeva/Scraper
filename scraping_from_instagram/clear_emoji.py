#!/usr/bin/env python3
import argparse
import json
import sys
import re

CLEAR_RE = re.compile(r'[^\u1f300-\u1f5ff\u1f900-\u1f9ff\u1f600-\u1f64f\u1f680-\u1f6ff\u2600-\u26ff\u2700-\u27bf\u1f1e6-\u1f1ff\u1f191-\u1f251\u1f004\u1f0cf\u1f170-\u1f171\u1f17e-\u1f17f\u1f18e\u3030\u2b50\u2b55\u2934-\u2935\u2b05-\u2b07\u2b1b-\u2b1c\u3297\u3299\u303d\u00a9\u00ae\u2122\u23f3\u24c2\u23e9-\u23ef\u25b6\u23f8-\u23fa]', re.UNICODE | re.IGNORECASE | re.MULTILINE)
M_SPACES = re.compile(r'[\n\r\t\u00A0]+')


def clear(s):
    global CLEAR_RE
    global M_SPACES
    # s = CLEAR_RE.sub(' ', s)
    s = s.encode("ascii", "ignore").decode()
    s = M_SPACES.sub(' ', s)
    return s

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('input_file', help='Input file')
    parser.add_argument('output_file', help='Output file')
    args = parser.parse_args()

    try:
        with open(args.input_file, 'rt') as f:
            data = json.load(f)
    except FileNotFoundError:
        sys.exit(f'File "args.input_file" not found.')

    for item in data:
        item['biography'] = clear(item['biography'])
        for media in item['latestMedia']:
            media['caption'] = clear(media['caption'])

    with open(args.output_file, 'wt') as f:
        json.dump(data, f, indent=4)
