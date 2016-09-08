#!/usr/bin/env python3
"""
Simple twitter page fetcher.

A simple script which checks the twitter account of uberspace
(or any other twitter account as well) for messages containing
specific keywords.
"""

import hashlib
import html
import os
import re
import requests
import subprocess

RELEVANT_HOSTS = [
    'alpheca',
]
#NOTIFY_COMMAND = 'cat; echo subject: {}'
NOTIFY_COMMAND = 'mail -s "{}" $USER'
URL = 'https://twitter.com/ubernauten'

# hashes of all messages stored in STORE_FILE to prevent duplicates
STORE_FILE = os.path.join(os.getcwd(), 'notified')


def main():
    messages = get_messages()


def get_messages():
    """Get a list containing the plain-text messages."""
    page = requests.get(URL)
    pattern = re.compile(r'<div class="js-tweet-text-container">[^>]*>(.*?)</p>.*?</div>', re.DOTALL)
    messages = pattern.findall(page.text)

    # unescape
    messages = (clean_message(message) for message in messages)

    for message in messages:
        host = check_relevance(message)
        if host:
            send_notification(host, message)


def send_notification(host: str, message: str):
    """Send a notification message."""
    if check_for_done_notification(message):
        # notification has already been sent
        return
    subject = 'New message regarding {}'.format(host)
    subprocess.Popen(
        NOTIFY_COMMAND.format(subject), shell=True,
        stdin=subprocess.PIPE).communicate(message.encode())

def check_for_done_notification(message: str) -> bool:
    """Check whether a notification message has been sent already and store
    the hash."""
    hash = hashlib.sha256(message.encode()).hexdigest()
    if hash in get_stored_hashes():
        return True
    add_stored_hash(hash)
    return False


def add_stored_hash(hash: str):
    with open(STORE_FILE, 'a') as file:
        file.write('{}\n'.format(hash))


def get_stored_hashes() -> list:
    if not os.path.isfile(STORE_FILE):
        return []
    with open(STORE_FILE, 'r') as file:
        return file.read().split('\n')

def check_relevance(message: str) -> str:
    """Check if a message is relevant and return host."""
    for host in RELEVANT_HOSTS:
        if host in message:
            return host

def clean_message(message: str) -> str:
    """Html-unescape and strip html from a message."""
    message = html.unescape(message)
    pattern = re.compile(r'<[^>]*>')
    message = pattern.sub('', message)
    return message


if __name__ == '__main__':
    main()
