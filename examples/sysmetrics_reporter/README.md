# System Metrics Reporter Program

This is a Python program that gathers system metrics and sends them as JSON payloads to clients over Websuckit.

## Requirements

Python 3.6 or higher is required to run this program.

## Project Directory

The project directory contains the following files:

- `config.py`: Contains configuration settings for the program.
- `metrics.py`: Contains functions for gathering system metrics.
- `server.py`: Contains the System metric server implementation for gathering and sending json.
- `sockit.py`: Contains the Websocket and WebSuckit implementation.
- `client.py`: Contains the System metric client implementation for receiving and processing JSON payloads.

## Usage

Install the required dependencies by running `pip install -r requirements.txt`.

### Setting up the environment variables

```bash
    export WEBSUCKIT_USER_ID=123
    export WEB_SUCKIT_PUBLIC_KEY=abcdef
    export WEBSUCKIT_CHANNEL_NAME=my_channel
    export WEB_SUCKIT_USER_ACCESS_KEY=123
```

### Configuration

The following configuration settings are available in `config.py` : \
    `report_interval`: integer - The time interval for reporting\
    `verbose`: boolean - basic logging level \
    `websuckit_user_access_key`: string \
    `websuckit_user_id`: UUID \
    `websuckit_public_key`: string \
    `websuckit_channel_name`: string

### Server

To use this program, follow these steps:

1. Start the server by running `python server.py`.
2. The server will send JSON payloads containing system metrics over the WebSocket connection.

### Client

```bash
usage: client.py [-h] [--user-id USER_ID | --public-key PUBLIC_KEY | --channel-name CHANNEL_NAME | --user-access-key USER_ACCESS_KEY] [uri]

WebSocket Client

positional arguments:
  uri                   WebSocket endpoint URI

options:
  -h, --help            show this help message and exit
  --user-id USER_ID     User ID
  --public-key PUBLIC_KEY
                        Public key
  --channel-name CHANNEL_NAME
                        Channel name
  --user-access-key USER_ACCESS_KEY
                        User access key
```

1. **Providing uri** : \
Run the script with the following arguments:
`uri`

```bash
   python script.py wss://example.com/socket
```

2. **Providing user-related arguments** : \
Run the script with the following arguments:
`--user-id`
`--public-key`
`--channel-name`
`--user-access-key`

```bash
    python script.py --user-id 123 --public-key abcdef --channel-name my_channel --user-access-key 123
```

3. **Using environment variables** : \
Setup environment variable as described in the previous section and run the script without arguments

```bash
    python script.py
```

## Demo

![Alt Text](./artifacts/demo.gif)
