#!/usr/bin/env python3

from __future__ import annotations

import argparse
import mailbox
import math
import os
import sys
import tempfile
from datetime import datetime
from email.utils import parsedate_to_datetime

from jmapc import Blob, Client, MailboxQueryFilterCondition, Ref
from jmapc.methods import MailboxGet, MailboxGetResponse, MailboxQuery


def main() -> None:
    args = parse_args()

    # Validate mbox file
    if not os.path.isfile(args.mbox_file):
        print(f"Error: {args.mbox_file} is not a file", file=sys.stderr)
        sys.exit(1)

    # Create JMAP client
    client = Client.create_with_api_token(
        host=os.environ["JMAP_HOST"],
        api_token=os.environ["JMAP_API_TOKEN"],
    )

    # Get the destination mailbox ID
    mailbox_id = get_mailbox_id(client, args.mailbox)
    print(f"Found {args.mailbox} with ID: {mailbox_id!r}")

    # Open the mbox file
    print("Opening mbox file")
    mbox = mailbox.mbox(args.mbox_file)
    size = len(mbox)
    print("Iterating through", size, "message(s) for import")
    successful = 0

    for processed, message in enumerate(mbox):
        succeeded = import_message(
            client=client,
            mailbox_id=mailbox_id,
            message=message,
            dry_run=args.dry_run,
        )
        if succeeded:
            successful += 1
        if args.limit and processed >= args.limit:
            break

    if not args.dry_run:
        print(f"Successfully imported {successful} of {size} message(s).")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Import an mbox file into a JMAP-compatible server"
    )
    parser.add_argument("mbox_file", help="Path to the mbox file to import")
    parser.add_argument(
        "--mailbox",
        default="Inbox",
        help="Name of the destination mailbox (default: Inbox)",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=0,
        help="Max number of messages to import (default: 0 = no limit)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Don't actually import, just print what would happen",
    )
    return parser.parse_args()


def get_mailbox_id(client: Client, mailbox_name: str) -> str:
    """
    Find the mailbox ID for the given mailbox name.
    """
    methods = [
        MailboxQuery(filter=MailboxQueryFilterCondition(name=mailbox_name)),
        MailboxGet(ids=Ref("/ids")),
    ]
    results = client.request(methods)

    # Get the mailbox ID from the results
    # Cast the response to MailboxGetResponse
    response = results[1].response
    assert isinstance(response, MailboxGetResponse)

    if not (mailbox_data := response.data):
        raise ValueError(f"Mailbox {mailbox_name!r} not found on the server")

    mailbox_id = mailbox_data[0].id
    if mailbox_id is None:
        raise RuntimeError(f"Mailbox {mailbox_name!r} has no ID")

    return mailbox_id


def extract_received_at(message: mailbox.Message) -> str:
    """
    Extract the received date from the email message.
    """
    # Try to get the date from various headers
    for header in ["Date", "Received"]:
        try:
            date_value = message[header]
        except KeyError:
            continue

        # For Received header, extract the date part
        if header == "Received":
            # The date is typically at the end of the Received header
            date_value = date_value.split(";")[-1].strip()

        date = parsedate_to_datetime(date_value)
        return date.isoformat()

    # If we can't parse the date, use current time
    return datetime.now().isoformat()


def import_message(
    client: Client,
    mailbox_id: str,
    message: mailbox.Message,
    dry_run: bool = False,
) -> bool:
    """
    Import a single email message from the mbox file.

    Args:
        client: JMAP client
        mailbox_id: ID of mailbox to import to
        message: Email message from mailbox module
        dry_run: If True, just print what would be imported

    Returns:
        whether the import was successful
    """
    # Convert the message to bytes, using CRLF to be JMAP-compliant
    policy = message.policy.clone(linesep="\r\n")
    message_bytes = message.as_bytes(policy=policy)

    # Extract a few other bits of information we'll need
    received_at = extract_received_at(message)
    message_id = message.get("Message-ID")
    message_size = format_size(len(message_bytes))
    subject = message.get("Subject", "(No subject)")

    # For dry run, just print and return False (b/c we did not upload)
    if dry_run:
        print(
            f"Would import: {subject!r}",
            f"(size: {message_size},",
            f"received: {received_at})",
        )
        return False

    # Upload the message
    blob = upload_blob_data(client, message_bytes)

    # Import the blob as an email using Email/import
    result = client.import_email(
        blob_id=blob.id,
        mailbox_ids={mailbox_id: True},
        received_at=received_at,
    )

    if result.created:
        print(f"Imported: {subject!r} ({message_size})", message_id or "")
        return True

    print(
        f"Failed to import {message_id} ({message_size}): {result.not_created}"
    )
    return False


def format_size(num: int | float) -> str:
    if num == 0:
        return "0 bytes"
    elif num == 1:
        return "1 byte"
    units = ["bytes", "KB", "MB", "GB", "TB", "PB"]
    scale = int(math.floor(math.log(num, 1024)))
    rounded = round(num / (1024**scale))
    if not scale:
        return f"{rounded} {units[scale]}"
    return f"{rounded:.1f} {units[scale]}"


def upload_blob_data(client: Client, data: bytes) -> Blob:
    """
    Upload raw bytes as a blob.
    """
    with tempfile.NamedTemporaryFile() as temp:
        temp.write(data)
        temp_name = temp.name
        blob = client.upload_blob(temp_name)
        return blob


if __name__ == "__main__":
    main()
