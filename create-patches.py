#!/usr/bin/python3

import argparse
import subprocess
import shutil
import os

def parse_cover_letter_txt(cover_letter_path):
    if not os.path.isfile(cover_letter_path):
        raise Exception(f"{cover_letter_path} does not exist")

    with open(cover_letter_path, 'r') as file:
        subject = file.readline()
        subject = subject.strip()

        file.readline()

        body = file.read()
        body = body.rstrip()

        return subject, body

def update_cover_letter(cover_letter_path, subject, body):
    with open(cover_letter_path, 'r') as file:
        filedata = file.read()

    filedata = filedata.replace('*** SUBJECT HERE ***', subject)
    filedata = filedata.replace('*** BLURB HERE ***', body)

    with open(cover_letter_path, 'w') as file:
        file.write(filedata)

def main():
    parser = argparse.ArgumentParser(description='Generate patch files')
    parser.add_argument('-v', metavar='SERIES_VERSION', type=int, help = 'version of patch series')
    parser.add_argument('-c', metavar='COVER_LETTER', type=str, help = 'cover letter text file')
    parser.add_argument('start_commit', type=int, help = 'Starting commit')
    parser.add_argument('num_commits', type=int, help = 'Number of commits including and after start commit to turn into patch files')
    args = parser.parse_args() 
    
    cmd = ['git', 'format-patch', '--cover-letter']
    if args.v is not None:
        cmd.append('-v' + str(args.v))

    end_commit = args.start_commit - args.num_commits
    cmd.append('HEAD~'+str(args.start_commit) + '..' + 'HEAD~'+str(end_commit))

    if args.c is not None:
       subject, body = parse_cover_letter_txt(args.c) 

    
    result = subprocess.run(cmd)
    if result.returncode != 0:
        print(f"Error: git format-patch command failed.")
        exit(result.returncode)

    if args.c is not None:
        current_cover_letter_path = "0000-cover-letter.patch"
        if args.v is not None:
            current_cover_letter_path = "v"+str(args.v)+"-" + current_cover_letter_path
        update_cover_letter(current_cover_letter_path, subject, body)

main()
