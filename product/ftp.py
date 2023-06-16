import mmap
import os
import zipfile
from ftplib import FTP
import xmltodict


def getfile(ftp_host, ftp_user, ftp_password, ftp_folder, local_folder, index=0):
    if index == 3:
        return
    ftp = FTP()
    ftp.connect(ftp_host, 21021)
    ftp.login(user=ftp_user, passwd=ftp_password)
    ftp.cwd(ftp_folder)
    file_list = ftp.nlst()
    file_list = sorted(file_list, reverse=True)

    local_path = os.path.join(local_folder, file_list[index])

    with open(local_path, 'wb+') as file:
        ftp.retrbinary('RETR ' + file_list[index], file.write)

    ftp.quit()

    with open(local_path, 'r') as file:
        mapped_file = mmap.mmap(file.fileno(), 0, access=mmap.ACCESS_READ)
        xml_string = mapped_file.read()
        mapped_file.close()
        xml_dict = xmltodict.parse(xml_string)

    return xml_dict


def getfile_zip(ftp_host, ftp_user, ftp_password, ftp_folder, local_folder, index=0):
    ftp = FTP()
    ftp.connect(ftp_host, 21021)
    ftp.login(user=ftp_user, passwd=ftp_password)
    ftp.cwd(ftp_folder)
    file_list = ftp.nlst()
    file_list = sorted(file_list, reverse=True)

    local_path = os.path.join(local_folder, file_list[index])

    with open(local_path, 'wb+') as file:
        ftp.retrbinary('RETR ' + file_list[index], file.write)
        file_path_zip = file.name
    ftp.quit()

    with zipfile.ZipFile(file_path_zip, 'r') as zip_ref:
        zip_ref.extractall(local_folder)

        file_path = local_folder + zip_ref.filelist[0].filename

    with open(file_path, 'r') as file:
        mapped_file = mmap.mmap(file.fileno(), 0, access=mmap.ACCESS_READ)
        xml_string = mapped_file.read()
        mapped_file.close()
        xml_dict = xmltodict.parse(xml_string)
    return xml_dict
