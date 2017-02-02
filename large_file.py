# Download file from Django
# Python Generator
# Python Subprocess

from django.http import StreamingHttpResponse
import os, subprocess, datetime, csv
import logging
import csv

logging.basicConfig(filename='/logs/file_download.log', level=logging.INFO)

class Echo(object):
    """An object that implements just the write method of the file-like
    interface.
    """
    def write(self, value):
        """Write the value by returning it, instead of storing in a buffer."""
        return value

def read_in_chunks(file_object, chunk_size=4096):
    while True:
        data = file_object.read(chunk_size)
        logging.info("reading Data %s %s" %(datetime.datetime.now(), data))
        if not data:
            break
        yield data

def execute_popen_command():
    try:
        cmd = "/usr/bin/sudo /usr/bin/zip - /logs/my.csv"
        file_write("Cmd %s" %cmd)
        file_write("%s %s" %(datetime.datetime.now(), cmd))
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr = subprocess.PIPE, shell=True)
        while True:
            output = process.stdout.read(4096)
            if not output and process.poll() != None:
                break
            if output != "":
                yield output

        if process.stdout:
            process.stdout.close()
        if process.stderr:
            process.stderr.close()
        return_code = process.wait()
    except Exception, ex:
        logging.error("Exception while closing stdout pipe %s" %ex)
        
        
class MyClass(APIView):

    def download_simple_file(self):
        file_full_path = "/logs/my.csv"
        pseudo_buffer = Echo()
        writer = csv.writer(pseudo_buffer)
        response = StreamingHttpResponse((writer.writerow(row) for row in read_in_chunks(f)), content_type="text/csv")
        return response
        
    def download_zip_file(self, request, format=None):
        file_full_path = "/logs/my.csv"
        response = StreamingHttpResponse(execute_popen_command(), content_type="application/zip")
        response['Content-Disposition'] = 'attachment; filename=test1.zip'
        response['Content-Length'] = os.path.getsize(file_full_path)
        return response
