from bottle import get,post,delete,route,request,run,put,response,static_file
import bottle
import os
from gluster import gfapi
import types
from gluster.gfapi import File, Volume

volume = gfapi.Volume("192.168.132.42","VOL-2")
volume.mount()

def read_in_chunks(fileObject, chunk_size=1024):
    while True:
        data=fileObject.read(chunk_size)
        if not data:
           break
        yield data

@post('/create/<filename>')
def create(filename):
    with volume.fopen(filename,"a") as f:
	print filename
	print request.files['file'].file.read()
        for chunk in read_in_chunks(request.files['file'].file):
	    print chunk
    return "SUCCESS"

@get('/read/<filename>')
def read(filename):
    try:
        with volume.fopen(filename,"r") as f:
            with open(filename,"a") as f2:
                for chunk in read_in_chunks(f):
                    f2.write(chunk)
        return static_file(filename,root='./')
    finally:
        print "this is executing further"
        if os.path.isfile('./'+filename):
            os.remove('./'+filename)


@delete('/remove')
def remove(fileName):
    arr = request.files['toDelete'].file
    for file in arr:
        volume.remove(file)
    return "SUCCESS"

run(host='192.168.132.60', port=8082, debug=True)
