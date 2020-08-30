# coding=utf-8
import os
import cgi
import time
from http.server import BaseHTTPRequestHandler, HTTPServer
save_root_path = os.getcwd()
save_file_path = os.path.join(save_root_path,'data')
message_template = '<p>{filename}  <b>{info}</b></p>'
filename = ''
info = ''
class PostHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            self.send_response(200)
            self.end_headers()
            content = ''
            message = ''
            if os.path.isfile('index.html'):
                content = open('index.html').read()
            else:
                content = '<h1>Error: not found file index.html</h1>'
            self.wfile.write(bytes(content.format(message=message), encoding = "utf-8"))
        except IOError:
            self.send_error(404, 'File Not Found: %s' % self.path)

    def do_POST(self):
        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={'REQUEST_METHOD': 'POST', 'CONTENT_TYPE': self.headers['Content-Type']}
        )
        self.send_response(200)
        self.end_headers()
        content = ''
        message = ''
        for field in form.keys():
            info='Error.'
            field_item_list = form[field]
            if (type(field_item_list).__name__ != 'list'):
                field_item_list = [field_item_list]
            for field_item in field_item_list:
                filename = field_item.filename
                filevalue = field_item.value
                print(time.strftime('[%Y-%m-%d %H:%M:%S]',time.localtime(time.time())),filename,len(filevalue))
                with open(os.path.join(save_file_path,filename), 'wb') as f:
                    f.write(filevalue)
                    info='Success.'
                message = message + message_template.format(filename=filename,info=info)
            if os.path.isfile('index.html'):
                content = open('index.html').read()
            else:
                content = '<h1>Error: not found succes.html</h1>'
            self.wfile.write(bytes(content.format(message=message), encoding = "utf-8"))
            
        
        return

def StartServer():
    sever = HTTPServer(("", 9999), PostHandler)
    sever.serve_forever()
 
if __name__ == '__main__':
    StartServer()