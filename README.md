[![build status](https://travis-ci.org/wvoliveira/ftponset.svg?branch=master)](https://travis-ci.org/wvoliveira/ftponset)

FTPOnset
---------

Simplesmente envia arquivos locais para um servidor FTP.  

How to
-----

Download e configure
```bash
git clone https://github.com/wvoliveira/ftponset.git
cp conf/example.ini conf/own.ini
```

Altere o arquivo conf/own.ini conforme suas credenciais de acesso:
```
server = ftp server
user = username
password = passwordd
remote_directory = Remote directory name
local_directory = /path/local/directory
sub_directories = directory1 directory2 directory3
```

Agora só rodar:
```bash
./ftponset.py -c conf/own.ini
```

Todos os logs estão indo para o sys.out. Irá aparecer na sua tela os errors e info.
