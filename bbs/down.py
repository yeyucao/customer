import os

import zipstream
from django.http import StreamingHttpResponse
from django.shortcuts import render


class ZipUtilities:
    zip_file = None

    def __init__(self):
        self.zip_file = zipstream.ZipFile(mode='w', compression=zipstream.ZIP_DEFLATED)

    def toZip(self, file, name):
        if os.path.isfile(file):
            self.zip_file.write(file, arcname=os.path.basename(file))


    def addFolderToZip(self, folder, name):
        for file in os.listdir(folder):
            full_path = os.path.join(folder, file)
            if os.path.isfile(full_path):
                self.zip_file.write(full_path, arcname=os.path.join(name, os.path.basename(full_path)))
            elif os.path.isdir(full_path):
                self.addFolderToZip(full_path, os.path.join(name, os.path.basename(full_path)))

    def close(self):
        if self.zip_file:
            self.zip_file.close()



def download_file(request):

    file_name = request.GET.get('finaName')
    if not file_name:
        return render(request, '404.html')
    print(file_name)
    file_path = os.path.dirname(os.path.abspath(__file__))
    print(file_path)
    if not os.path.isfile(os.path.join(file_path, file_name)):
        return render(request, '404.html')
    utilities = ZipUtilities()
    utilities.toZip(os.path.join(file_path, file_name), file_name)
    response = StreamingHttpResponse(utilities.zip_file, content_type='application/zip')
    response['Content-Disposition'] = 'attachment;filename="{0}"'.format("电小服.zip")
    return response

