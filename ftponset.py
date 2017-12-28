#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script dedicado a enviar arquivos da maquina para um servidor ftp
"""

import ftplib
import os
import datetime
import configparser
import argparse
import logging
import sys


parser = argparse.ArgumentParser(description='Envia arquivos da maquina para algum servidor ftp')

parser.add_argument('-c', '--config', help='.env or config file', required=True)
args = parser.parse_args()
CONFIG_FILE = args.config


def config_parser(section):
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)
    if config.has_section(section):
        items_dict = dict(config.items(section))
        return items_dict


ftp_config = config_parser('ftp')
logging.basicConfig(stream=sys.stdout, level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')


def connect(servidor, usuario, senha):
    try:
        ftp = ftplib.FTP(host=servidor)
        ftp.login(user=usuario, passwd=senha)
        return ftp

    except Exception as error:
        logging.error('Error to connect: {}'.format(error))
        exit(2)


def send_file(ftp, local_file, remote_directory):
    remote_file = '{0}/{1}/{2}'.format(ftp_config['remote_directory'], remote_directory, local_file.split('/')[-1])
    try:
        with open(local_file, 'rb') as file:
            logging.info('Enviando arquivo: {0} para: {1}'.format(local_file, remote_file))
            ftp.storbinary('STOR {0}'.format(remote_file), file)

    except Exception as error:
        logging.error('Error to send file: {0}'.format(error))
        exit(2)


def main():
    ftp = connect(ftp_config['server'], ftp_config['user'], ftp_config['password'])
    date_yesterday = datetime.datetime.strftime(datetime.datetime.today() - datetime.timedelta(days=1), '%Y%m%d')

    try:
        os.chdir(ftp_config['local_directory'])

        for directory in ftp_config['sub_directories'].split():
            files = os.listdir(directory)

            for file_name in files:
                if date_yesterday in file_name:
                    complete_file_name = '{0}/{1}/{2}'.format(ftp_config['local_directory'], directory, file_name)
                    send_file(ftp, complete_file_name, directory)

    except Exception as error:
        logging.error('Error to process files: {0}'.format(error))
        exit(2)


if __name__ == '__main__':
    main()
