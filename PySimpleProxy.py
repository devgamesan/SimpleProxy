import click
from flask import Flask, request, Response
import requests
import os
import json
import datetime

DIR_NAME = "data"
request_index = 1

# proxy server
app = Flask(__name__)
@app.route('/<path:path>', methods=['GET', 'POST', 'PATCH', 'DELETE', "OPTIONS", "PUT"])
def proxy(path):
   # save  a http request content to file
   save_request(request)
   response = requests.request(
      method=request.method,
      url=request.url,
      headers=request.headers,
      data=request.data
  )

   # save a http response content to file
   save_response(response)
   return Response(
      response=response.content,
      status=response.status_code,
      headers=dict(response.headers)
  )

# show the contents of a specific request.
def show_request(id):
   with open(os.path.join(DIR_NAME, str(id), "request.json"), "r") as f:
      request_data = json.load(f)
   print(json.dumps(request_data, indent=2))

# show the contents of a specific respose.
def show_response(id):
   with open(os.path.join(DIR_NAME, str(id), "response.json"), "r") as f:
      response_data = json.load(f)
   print(json.dumps(response_data, indent=2))
      
# save a http request content to file     
def save_request(request):
   now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

   output_dir = os.path.join(DIR_NAME, str(request_index))
   os.mkdir(output_dir)

   if "Content-Type" in request.headers:
      body = request.get_data().decode("utf-8", "ignore")
      request_data = {
         "datetime" : now,
         "ipaddress" :  request.remote_addr,
         "method" : request.method,
         "url": request.url,
         "headers" : dict(request.headers),
         "body" : body
      }
   else:
      request_data = {
         "method" : request.method,
         "url": request.url,
         "headers" : dict(request.headers)
      }

   with open(os.path.join(output_dir, "request.json"), "w") as f:
         json.dump(request_data, f, indent=2)

# save a http response content to file
def save_response(response):
   global request_index
   body = response.content.decode("utf-8", "ignore")
   response_data = {
      "status" : response.status_code,
      "headers" : dict(response.headers),
      "body" : body
   }
   with open(os.path.join(DIR_NAME, str(request_index), "response.json"), "w") as f:
         json.dump(response_data, f, indent=2)
   request_index += 1

def get_directory_names():
   directories = [entry for entry in os.listdir(DIR_NAME) if os.path.isdir(os.path.join(DIR_NAME, entry))]
   def to_int(str):
      return int(str)
   return sorted(directories, key=to_int)

# list http requests/responses
def list_all():
   sorted_directories = get_directory_names()

   for dir_no in sorted_directories:
      request_data = {}
      with open(os.path.join(DIR_NAME, str(dir_no), "request.json"), "r") as f:
         request_data = json.load(f)

      response_data = {}
      response_data_file = os.path.join(DIR_NAME, str(dir_no), "response.json")
      if os.path.exists(response_data_file):
         with open(response_data_file, "r") as f:
            response_data = json.load(f)  
      
      print("{:>5} {:>16} [{}] {} {:>6} {}".format(
         dir_no,
         request_data["ipaddress"],
         request_data["datetime"],
         response_data.get("status", "no"),
         request_data["method"],
         request_data["url"]))

# CLI
@click.group()
def PySimpleProxy():
   # initialize

   global request_index
   # make dir
   if not os.path.exists(DIR_NAME):
      os.mkdir(DIR_NAME)

   # dir
   dir_entries = os.listdir(DIR_NAME)
   directories = [entry for entry in dir_entries if os.path.isdir(os.path.join(DIR_NAME, entry))]
   
   def to_int(str):
      return int(str)

   sorted_directories = sorted(directories, key=to_int)
   if len(sorted_directories) == 0:
      request_index = 1
   else:
      request_index = int(sorted_directories[-1]) + 1

@PySimpleProxy.command()
@click.option('--port', help='Specify the proxy port', default=8080, type=int)
def start(port):
    app.run(host="0.0.0.0", port=8080)

@PySimpleProxy.command()
def list():
   list_all()

@PySimpleProxy.command()
@click.option('--id', help='Specify the id', type=int, required=True)
def showreq(id):
    show_request(id)

@PySimpleProxy.command()
@click.option('--id', help='Specify the id', type=int, required=True)
def showres(id):
    show_response(id)

if __name__ == "__main__":
    PySimpleProxy()