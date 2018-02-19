from googleapiclient.discovery import build
from apiclient import errors
from flask import json
from googleapiclient.http import MediaFileUpload
import httplib2
import os
from oauth2client.client import SignedJwtAssertionCredentials
from poster.streaminghttp import register_openers
from components.Resources import Resources

SCOPE = 'https://www.googleapis.com/auth/drive'
CLIENT_SECRET_FILE = 'components/resources/dts-241384e599c0.json'


class GoogleDriveService:

    def __init__(self, commandObject):
        with open(CLIENT_SECRET_FILE) as data_file:
            data = json.load(data_file)

        credentials = SignedJwtAssertionCredentials(data['client_email'], data['private_key'], scope=SCOPE)
        credentials.authorize(httplib2.Http())

        http = credentials.authorize(httplib2.Http())
        apikey = Resources.Settings('apikey')
        self.drive_service = build('drive', 'v2', http=http, developerKey=apikey)

        self.commandObject = commandObject

    def get_files_in_folder(self, folder_id):
        files = []
        page_token = None

        while True:
            try:
                param = {}

                if page_token:
                    param['pageToken'] = page_token

                children = self.drive_service.children().list(
                    folderId=folder_id, **param).execute()

                for child in children.get('items', []):
                    file = self.drive_service.files().get(fileId=child['id']).execute()
                    if not file['explicitlyTrashed']:
                        files.append(file)

                page_token = children.get('nextPageToken')

                if not page_token:
                    break

            except errors.HttpError, error:
                print('An error occurred: %s' % error)
                break

        return files

    def pushPems(self, args):
        # Register the streaming http handlers with urllib2

        def checkFile(file):
            if '-update' in args:
                return True

            return file not in drive_files

        register_openers()
        dir = '/home/andrey/pems'
        folder_id = '0B8ptRVFTKCKAbUNJWXR5NzVkeG8'

        os_pems = os.listdir(dir)
        files = self.get_files_in_folder(folder_id)
        drive_files = []

        for file in files:
            if not file['explicitlyTrashed']:
                drive_files.append(file['title'])

        for os_pem in os_pems:
            if checkFile(os_pem) and not os_pem.endswith('~'):
                description = os_pem + ' pem'
                self.commandObject.emitMessage(os_pem + ' pushed')
                self.insert_file(os_pem, description, folder_id, 'application/x-pem-file', dir + '/' + os_pem)

    def getPems(self, args):
        files = self.get_files_in_folder('0B8ptRVFTKCKAbUNJWXR5NzVkeG8')

        for file in files:
            f = open('components/resources/pems/' + file['title'], 'w')
            self.commandObject.emitMessage('download ' + file['title'])
            self.download_file(file['id'], f)
            f.close()

    def pushConf(self, args):
        def checkFile(file):
            if '-update' in args:
                return True

            return file not in drive_files

        dir = '/home/andrey/conf'
        os_confs = os.listdir(dir)
        folder_id = '0B8ptRVFTKCKANk1QTVhLVk1xZk0'

        files = self.get_files_in_folder(folder_id)
        drive_files = []

        for file in files:
            if not file['explicitlyTrashed']:
                drive_files.append(file['title'])

        for os_conf in os_confs:
            if checkFile(os_conf):
                #print(dir + '/' + os_conf)
                print(os_conf)
                description = os_conf + ' conf'
                self.insert_file(os_conf, description, folder_id, 'text/plain', dir + '/' + os_conf)
                self.commandObject.emitMessage('push ' + os_conf)

    def getConf(self, args):
        files = self.get_files_in_folder('0B8ptRVFTKCKANk1QTVhLVk1xZk0')

        for file in files:
            #print file['title']
            f = open('components/resources/conf/' + file['title'], 'w')
            self.download_file(file['id'], f)
            f.close()
            self.commandObject.emitMessage('get ' + file['title'])

    def download_file(self, file_id, local_fd):
        """Download a Drive file's content to the local filesystem.

        Args:
          service: Drive API Service instance.
          file_id: ID of the Drive file that will downloaded.
          local_fd: io.Base or file object, the stream that the Drive file's
              contents will be written to.
        """
        from apiclient import http
        request = self.drive_service.files().get_media(fileId=file_id)
        media_request = http.MediaIoBaseDownload(local_fd, request)

        while True:
            try:
                download_progress, done = media_request.next_chunk()
            except errors.HttpError, error:
                print 'An error occurred: %s' % error
                return
            if download_progress:
                print 'Download Progress: %d%%' % int(download_progress.progress() * 100)
            if done:
                print 'Download Complete'
                return

    def insert_file(self, title, description, parent_id, mime_type, filename):
        """Insert new file.

        Args:
          service: Drive API service instance.
          title: Title of the file to insert, including the extension.
          description: Description of the file to insert.
          parent_id: Parent folder's ID.
          mime_type: MIME type of the file to insert.
          filename: Filename of the file to insert.
        Returns:
          Inserted file metadata if successful, None otherwise.
        """
        media_body = MediaFileUpload(filename, mimetype=mime_type, resumable=True)
        body = {
            'title': title,
            'description': description,
            'mimeType': mime_type
        }
        # Set the parent folder.
        if parent_id:
            body['parents'] = [{'id': parent_id}]

        try:
            file = self.drive_service.files().insert(
                body=body,
                media_body=media_body).execute()

            # Uncomment the following line to print the File ID
            # print 'File ID: %s' % file['id']

            return file
        except errors.HttpError, error:
            print 'An error occured: %s' % error
            return None