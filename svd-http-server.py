import cgi
import os
import http.server
import json
import urllib.parse
import zipfile
import glob
import shutil
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse

data = {'result': 'this is a result','test': 'this is a test'}
# host = ("localhost", 8000) # local testing
host = ("0.0.0.0", 8000) # deployment
data_json = json.dumps({'key1':'value1','key2':'value2'})   # dumps：将python对象解码为json数据
img_path = os.getcwd()

def achive_folder_to_zip(sFilePath, startDate, endDate):
    """
    input : Folder path and name
    output: using zipfile to ZIP folder
    """
    zf = zipfile.ZipFile(img_path + '/images/img.zip', 'w', zipfile.ZIP_DEFLATED)
    # os.chdir(sFilePath)
    print("%s%s" % (img_path, '/images/img.zip'))

    sDateStart = list(startDate)
    sDateEnd = list(endDate)

    glob_arg = "{}/images/*[{}-{}][{}-{}][{}-{}][{}-{}]-[{}-{}][{}-{}]-[{}-{}][{}-{}] *.jpg".format(
        img_path, 
        sDateStart[0], sDateEnd[0],
        sDateStart[1], sDateEnd[1],
        sDateStart[2], sDateEnd[2],
        sDateStart[3], sDateEnd[3],
        sDateStart[4], sDateEnd[4],
        sDateStart[5], sDateEnd[5],
        sDateStart[6], sDateEnd[6],
        sDateStart[7], sDateEnd[7]
    )

    file_names = glob.glob(glob_arg)

    for file_name in file_names:
        new_path = file_name.split("/")[-1]
        zf.write(file_name, new_path)
    # file_names = glob.glob(os.path.join(img_path + '/images', "*.jpg"))
    # file_count = 0
    # for file_name in file_names:
    #     new_path = file_name.split("/")[-1]
    #     zf.write(file_name, new_path)
    #     file_count = file_count + 1
    #     if file_count == int(file_no):
    #         break
    zf.close()

class WebRequestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        print(self)
        parsed_result=urlparse(self.path)
        queries = parsed_result.query.split("&")
        datestart = ""
        dateend = ""

        for query in queries:
            pra, value = query.split("=")
            if pra == "start_date":
                datestart = value
            elif pra == "end_date":
                dateend = value
        achive_folder_to_zip(img_path, datestart, dateend)

        ZIP_FILEPATH = img_path + "/images/img.zip"

        with open(ZIP_FILEPATH, 'rb') as f:
            self.send_response(200)
            self.send_header("Content-Type", 'application/octet-stream')
            self.send_header("Content-Disposition", 'attachment; filename="{}"'.format(os.path.basename(ZIP_FILEPATH)))
            fs = os.fstat(f.fileno())
            self.send_header("Content-Length", str(fs.st_size))
            self.end_headers()
            shutil.copyfileobj(f, self.wfile)
    # def do_GET(self):
    #     print("Request for '%s' received." % self.path)
    #     self.send_response(200)
    #     self.send_header('Content-type', 'application/json')
    #     self.end_headers()
    #     self.wfile.write(json.dumps(data).encode())
    def do_POST(self):
        enc = "UTF-8"
        path = str(self.path)
        # 获取POST请求的一种方式，首先受到length，然后通过self.rfile里读出该长度的数据
        # length = int(self.headers["content-length"])  # 获取除头部后的请求参数的长度
        # datas = urllib.parse.parse_qs(self.rfile.read(length), keep_blank_values=1)  # 获取请求参数数据，请求数据为json字符串
        # print(datas)
        if path == "/data":
            # pass（可以添加对参数的逻辑处理）
            # 以下是返回报文
            self.send_response(200)  # 返回状态码
            self.send_header("Content-type", "text/html;charset=%s" % enc)  # 返回响应头内容
            self.end_headers()  # 返回响应头结束
            buf = {"status": 0,  # 返回包体数据
                   "data": {"filepath": "success", "port" : "ok"} }
            # 这里一定要加encode(),不然会报错，bytes<-> str转换的错,bytes和str的互转有三种方式，# s.encode(encoding="utf-8")
            self.wfile.write(json.dumps(buf).encode())  # 发送json格式的返回包体

        if path == "/addLocation":
            length = int(self.headers.get('Content-Length'))
            message = json.loads(self.rfile.read(length))

            message['received'] = 'ok'

            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(message).encode())

        # 上传图片
        if path == "/upload":
            form = cgi.FieldStorage(
                fp=self.rfile,
                headers=self.headers,
                environ={'REQUEST_METHOD': 'post',
                         'CONTENT_TYPE': self.headers['Content-Type']
                         }
            )
            fname = self.headers["filename"]
            temp = self.headers["temp"]
            print("%s" % temp)
            local_path = os.getcwd()
            for i in range(len(form['file'])):
                data = form['file'][i].value
                fn = "%s/images/%s_%s" % (local_path, str(i+1), fname)   # 生成文件存储路径
                outf = open(fn, 'wb')
                outf.write(data)
                outf.close()

            # data = form['file'].value
            # fn = local_path + "/images/%s" % (fname)  # 生成文件存储路径
            # outf = open(fn, 'wb')  # 写打开文件
            # outf.write(data)  # 将接收到的内容写入文件
            # outf.close()  # 关闭文件

            # 如多於一張圖片
            # for i in range(len(form['file'])):
            #     data = form['file'][i].value
            #     fn = "C:/Users/yvon6/Desktop/tmp/%s_%i.jpg"%(fname, i+1)  # 生成文件存储路径
            #     outf = open(fn, 'wb')  # 写打开文件
            #     outf.write(data)  # 将接收到的内容写入文件
            #     outf.close()  # 关闭文件

            self.send_response(200)
            self.send_header("Content-type", "text/html;charset=%s" % enc)
            self.send_header("test", "This is test!")
            self.end_headers()
            buf = {"status": 0,
                   "data": {
                       "msg": u"上传成功"}}
            self.wfile.write(json.dumps(buf).encode())

if __name__ == '__main__':
    try:
        server = HTTPServer(host, WebRequestHandler)
        print("Starting server, listening at: %s:%s" % host)
        print("Images located at: %s" % img_path)
        server.serve_forever()
    except KeyboardInterrupt:
        print('Shutting down server...')
        server.socket.close()
