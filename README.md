## Kleros REST API

This API is hosted at `https://api.kleros.io`

Endpoint documentation can be found in ENDPOINTS.md


## NOTES

This API is centralized. You can audit the source code here, but realize that
data served from these endpoints require a certain level of trust and may not necessarily
reflect what is on the blockchain at all times. To provide speed and to minimize the number of blockchain calls, much of the data will be cached for some period of time. For applications where real time data is critical we
recommend you get your data directly from a Ethereum node.

## DEV

We are happy to accept help on creating more endpoints to serve data that people find useful.
This application is built in python 3.x using Flask as the webserver.

### SETUP

- You will need to provide a RPC endpoint (e.g. Infura) as an environment variable

```
$ export PROVIDER_URI=https://mainnet.infura.io/v3/<api_key>
```

- We recommend installing and using a `virtualenv` with python3

```
$ virtualenv --python=/usr/local/bin/python3 .venv
$ source .venv/bin/activate
```

- Install dependencies with `pip`

```
(.venv)$ pip install -r requirements.txt
```

- Start the Flask dev server

```
(.venv)$ python run.py
```
