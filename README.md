# SimpleProxy
Simple Proxy for test/debug/development.
This program records the contents of HTTP requests and responses for debugging purposes during the development of web applications.


# How to use
## start proxy server

Start proxy server and set it to your browser.

```
python PySimpleProxy.py start

or 

python PySimpleProxy.py start --port 9999


note: default port is 8080
```

## list http requests/resonses
```
python PySimpleProxy.py list

    1     192.168.56.1 [2024-02-25 13:38:34] 200   POST http://localhost:9999/json
    2     192.168.56.1 [2024-02-25 13:38:36] 200   POST http://localhost:9999/html
    3     192.168.56.1 [2024-02-25 13:38:38] 200   POST http://localhost:9999/binary
    4     192.168.56.1 [2024-02-25 13:38:40] 200   POST http://localhost:9999/json
    5     192.168.56.1 [2024-02-25 13:38:42] 200   POST http://localhost:9999/html
    6     192.168.56.1 [2024-02-25 13:38:44] 200   POST http://localhost:9999/binary
```

## show http request details

```
python PySimpleProxy.py showreq --id 6

{
  "datetime": "2024-02-25 13:38:44",
  "ipaddress": "192.168.56.1",
  "method": "POST",
  "url": "http://localhost:9999/binary",
  "headers": {
    "Host": "localhost:9999",
    "User-Agent": "curl/7.81.0",
    "Accept": "*/*",
    "Proxy-Connection": "Keep-Alive",
    "Content-Type": "application/json",
    "Content-Length": "29"
  },
  "body": "{ \"name\": \"taro\", \"age\": 20 }"
}
```


## show http response details

```
python PySimpleProxy.py showres --id 6

{
  "status": 200,
  "headers": {
    "Server": "Werkzeug/3.0.1 Python/3.10.12",
    "Date": "Sun, 25 Feb 2024 04:38:46 GMT",
    "Content-Type": "application/octet-stream",
    "Content-Length": "13",
    "Connection": "close"
  },
  "body": "Hello, World!"
}
```
