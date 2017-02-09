"""
A service that provides a download link to an archive of the user's files.

Call it with http://{jupyterhub_url}/services/jh-save
"""
from getpass import getuser
import os
import re
from io import BytesIO
import zipfile

from urllib.parse import urlparse

from tornado.gen import coroutine
from tornado.ioloop import IOLoop
from tornado.httpserver import HTTPServer
from tornado.web import RequestHandler, Application, authenticated

from jupyterhub.services.auth import HubAuthenticated


import time


class GetHandler(HubAuthenticated, RequestHandler):
    hub_users = {getuser()} # the users allowed to access me

    @authenticated
    @coroutine
    def get(self):
        user_model = self.get_current_user()

        user_path = os.environ['JUPYTERHUB_USER_PATH'].format(user=user_model['name'])
        save_regex = re.compile(os.environ['JUPYTERHUB_SAVE_REGEX'], re.IGNORECASE)

        #store the zip file in memory
        outf = BytesIO()
        zipf = zipfile.ZipFile(outf, 'w', zipfile.ZIP_DEFLATED)

        #add files
        for root, dirs, files in os.walk(user_path):
            #cull full path
            dest = root.replace(os.path.dirname(user_path),'',1)
            for file in files:
                if re.match(save_regex, file) != None:
                    zipf.write(os.path.join(root, file), arcname=os.path.join(dest, file))
        zipf.close()

        #now return the zip
        self.set_header('content-type', 'application/zip')
        outf.flush()
        outf.seek(0)
        self.write(outf.read())



def main():
    app = Application([
        (os.environ['JUPYTERHUB_SERVICE_PREFIX'], GetHandler),
        (r'.*', GetHandler),
    ], login_url='/hub/login')
    
    http_server = HTTPServer(app)
    url = urlparse(os.environ['JUPYTERHUB_SERVICE_URL'])

    http_server.listen(url.port, url.hostname)

    IOLoop.current().start()



if __name__ == '__main__':
    main()
