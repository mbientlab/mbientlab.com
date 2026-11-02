#!/usr/bin/env python3
"""Fail if a firmware catalog references a file that is not in releases/.

The MetaWear apps and SDKs download https://mbientlab.com/releases/metawear/info2.json
(and info1.json for the legacy SDKs) and then fetch
<hardware>/<model>/<flavor>/<version>/<filename> relative to it. Shipped apps
cannot be updated to new URLs, so every referenced file must stay published.
"""
import json
import pathlib
import sys

ROOT = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else ".") / "releases" / "metawear"

# Referenced by the catalogs but already missing from the S3 bucket before
# the move to GitHub Pages. Remove an entry once its file is restored.
KNOWN_MISSING = {
    "0.1/8/bootloader/0.4.0/temp.zip",
    "0.2/99/vanilla/1.3.6/firmware.zip",
    "0.2/99/vanilla/1.3.7/firmware.zip",
    "0.2/99/vanilla/1.3.8/firmware.zip",
    "0.2/99/vanilla/1.4.0/firmware.zip",
    "0.2/99/vanilla/1.4.1/firmware.zip",
    "0.4/12/vanilla/1.20.112/firmware.zip",
    "0.4/5/bootloader/0.3.3/bl.zip",
    "0.5/5/bootloader/0.4.0/temp.zip",
}


def referenced(node, path=()):
    if isinstance(node, dict):
        for key, value in node.items():
            yield from referenced(value, path + (key,))
    elif isinstance(node, str) and node.endswith((".zip", ".bin", ".hex")):
        yield "/".join(path[:-1] + (node,))


def main():
    missing = []
    total = 0
    for catalog in ("info1.json", "info2.json"):
        data = json.loads((ROOT / catalog).read_text())
        for rel in sorted(set(referenced(data))):
            total += 1
            if not (ROOT / rel).is_file() and rel not in KNOWN_MISSING:
                missing.append(f"{catalog}: {rel}")
    if missing:
        print("Firmware files referenced by the catalog are missing:")
        print("\n".join(f"  {m}" for m in missing))
        sys.exit(1)
    print(f"OK: {total} catalog references checked under {ROOT}")


if __name__ == "__main__":
    main()
