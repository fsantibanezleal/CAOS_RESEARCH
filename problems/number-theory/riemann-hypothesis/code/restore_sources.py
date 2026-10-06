"""Restore locally cached source documents from their version-pinned manifest.

This downloader never publishes or re-licenses source PDFs. A byte/hash mismatch
fails closed and requires a newly documented source version.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from urllib.request import Request, urlopen


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--verify-only', action='store_true')
    args = parser.parse_args()
    context = Path(__file__).resolve().parents[1] / 'context'
    manifests = [
        json.loads(path.read_text())
        for path in sorted(context.glob('source-manifest*.json'))
    ]
    for row in (row for manifest in manifests for row in manifest['documents']):
        target = (context / row['cache_path']).resolve()
        if not target.is_relative_to((context / 'source-cache').resolve()):
            raise ValueError('Source path escapes its cache')
        if not target.exists() and not args.verify_only:
            request = Request(row['source_url'], headers={'User-Agent': 'CAOS-Research-SourceArchive/1.0'})
            with urlopen(request, timeout=90) as response:
                payload = response.read()
            if len(payload) != row['bytes'] or hashlib.sha256(payload).hexdigest() != row['sha256']:
                raise ValueError('Downloaded source differs: ' + row['filename'])
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(payload)
        payload = target.read_bytes()
        if len(payload) != row['bytes'] or hashlib.sha256(payload).hexdigest() != row['sha256']:
            raise ValueError('Cached source differs: ' + row['filename'])
        print('verified: ' + row['filename'], flush=True)
    for row in (row for manifest in manifests for row in manifest['repositories']):
        target = context / row['archive_path']
        if hashlib.sha256(target.read_bytes()).hexdigest() != row['sha256']:
            raise ValueError('Code snapshot differs: ' + row['archive_path'])
    print('All source hashes verified.', flush=True)


if __name__ == '__main__':
    main()
