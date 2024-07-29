# Kernel Dev Scripts
Just some python scripts to help with submitting patches to the Linux Kernel

## Creating Patch Files
`create-patches.py` is a wrapper around `git format-patch` however it allows
you to pass in a cover letter subject and blurb to overwrite the generated template
so you don't have to manually copy and paste

Here is an example how you can use the script to create patch files. Be sure to run
this in the root directory of the Linux Kernel

`<path/to/kernel-dev-scripts>/create-patches.py -v5 -c cover-letter.txt 2`


This command will create a version 5 patch series of the 2 top commits with a cover
letter patch based off of cover-letter.txt.

## Formatting a cover-letter.txt
The first line in cover-letter.txt is the subject line of the email.
The second line is skipped and should be left blank.
All the rest of the lines become the body of the cover letter.

Here is an example of a cover-letter.txt
```
This is the subject line

This is the body of the text!

This is also in the body of the text.
We are still in the body of the text!
```

This would produce a cover letter patch like the following:
```
From <COMMIT HASH> <DATE>
From: <NAME> <EMAIL>
Date: <DATE>
Subject: [PATCH 0/x] This is the subject line

This is the body of the text!

This is also in the body of the text.
We are still in the body of the text!

Signed-off-by: <NAME> <EMAIL>
---

<GIT DIFF INFO>

-- 
2.45.2

```

## Sending Patch Files
`send-patches.py` is a wrapper around `git send-email` but will
auto-magically set the recipients to the appropriate maintainers
based on the patch files passed in. It will also cc the appropriate
mailing lists.

Here is an example:

`send-patches.py -t example1@example.com -t example2@example.com -c example3@example.com
0000-cover-letter.patch 0001-example.patch 0002-example.patch`

This command will send out a patch series to the appropriate maintainers of the code modified in the specified patches.
It will also add two extra recepients (example1@example.com and example2@example.com) with an extra cc example3@example.com
