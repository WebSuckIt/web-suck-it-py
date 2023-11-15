import argparse
import json
import pprint
from typing import Optional

from config import logging
from sockit import Suckit, standalone_receive


def main():
    """
    Main function.
    """
    parser = argparse.ArgumentParser(description="WebSocket Client")
    # Create a mutually exclusive group for uri and user-related arguments
    group = parser.add_mutually_exclusive_group(required=False)
    parser.add_argument(
        "uri",
        type=Optional[str],
        help="WebSocket endpoint URI",
        default=None,
        nargs="?",
    )
    group.add_argument("--user-id", type=str, help="User ID")
    group.add_argument("--public-key", type=str, help="Public key")
    group.add_argument("--channel-name", type=str, help="Channel name")
    group.add_argument("--user-access-key", type=str, help="User access key")
    args = parser.parse_args()
    ws_uri = (
        args.uri
        if args.uri
        else Suckit(
            user_id=args.user_id,
            public_key=args.public_key,
            channel_name=args.channel_name,
            access_key=args.user_access_key,
        ).get_uri()
    )  # If URI is not provided, user-related arguments are required
    # If URI is provided, user-related arguments are not allowed
    logging.debug(f"[*] Connecting to {ws_uri}")
    socket_generator = standalone_receive(ws_uri)
    logging.info("[*] Connected to websocket")
    # processing the received data from the socket generator as json
    for data in socket_generator:
        logging.info("[*] Data Received: \n")
        pprint.pprint(json.loads(data))
        logging.info("[*] Waiting for data")


if __name__ == "__main__":
    main()
