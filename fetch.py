#!/usr/bin/env python3
"""
Simple twitter page fetcher.

A simple script which checks the twitter account of uberspace
(or any other twitter account as well) for messages containing
specific keywords.
"""

import html
import re
import requests
import subprocess

RELEVANT_HOSTS = [
    'alpheca',
]
#NOTIFY_COMMAND = 'cat; echo subject: {}'
NOTIFY_COMMAND = 'mail -s "{}" $USER'
URL = 'https://twitter.com/ubernauten'


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
    subject = 'New message regarding {}'.format(host)
    subprocess.Popen(
        NOTIFY_COMMAND.format(subject), shell=True,
        stdin=subprocess.PIPE).communicate(message.encode())



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
