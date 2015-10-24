#PyDownload

Using Python, download all files from several FTP sources

#PEP8 Compliant



Example Usage:

	hosts = ['domain01.com', 'domain02.com']
	user = 'username'
	password = 'secr3t'

	for host in hosts:
		Ftp(host, user, password).download()
	
