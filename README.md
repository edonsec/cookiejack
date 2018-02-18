# CookieJack

I wrote this as a proof of concept and it is not to be used for for any illegitimate purposes.

CookieJack sniffs plaintext HTTP traffic for cookie related headers, it then injects them to awaiting listeners. 

The primary listener sends these to a WebSocket server, using the accompanying Chrome / Firefox extensions by connecting to the available WebSocket server it injects the cookies into the browser in real time.

## Installation

```
virtualenv venv
source ./venv/bin/activate
python setup.py install
```

## Usage:

First install one of the two browser extensions:

https://github.com/ecradock/chrome-extension-cookie-injector
https://github.com/ecradock/firefox-extension-cookie-injector

General usage:

Run cookiejack on all interfaces filtering port 80 tcp traffic, websocket server runs on port 127.0.0.1:9000:

```
cookiejack -v
```

Use a pcap file to load cookies to the websocket:

```
cookiejack -v -r path/to/traffic.pcap
```

Once running visit the browser extension's options page and configure the host and port (defaults to localhost:9000) - then simply click the icon and watch the cookies arrive.

Cookies are set with wildcarded tld and are by default set as session cookies so closing the browser will allow you to remove the cookies.

## Exit

Due to the nature of the processes running, to kill the process as root you must run the following:

```
cookiejack -k
```

TODO: 
Logging to file / db
Find a cleaner way to kill the service
