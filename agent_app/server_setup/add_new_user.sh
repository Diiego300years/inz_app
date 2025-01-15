useradd -M -s /sbin/nologin test2;
smbpasswd -a test2;
service smbd start;