#!/usr/bin/python3

import argparse
import subprocess
import shutil
import os

def main():
    parser = argparse.ArgumentParser(description='Send patches')
    parser.add_argument('-t', action='append', metavar='EMAIL', type=str, help='extra recipients')
    parser.add_argument('-c', action='append', metavar='EMAIL', type=str, help='extra carbon copies')
    parser.add_argument('patch', nargs='+', type=str, help='patch files')
    args = parser.parse_args()
   
    patches = ' '.join(args.patch)
    to_cmd = f"--to-cmd=./scripts/get_maintainer.pl --norolestats -nol {patches}"
    cc_cmd = f"--cc-cmd=./scripts/get_maintainer.pl --norolestats -nom {patches}"

    cmd = ['git', 'send-email', to_cmd, cc_cmd]

    if args.t is not None:
        for mail_addr in args.t:
            cmd.append('--to')
            cmd.append(mail_addr)

    if args.c is not None:
        for mail_addr in args.c:
            cmd.append('--cc')
            cmd.append(mail_addr)

    for patch in args.patch:
        cmd.append(patch)
    
    result = subprocess.run(cmd)
    exit(result.returncode)
    
main()
