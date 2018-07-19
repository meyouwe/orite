#!/usr/local/bin/python3
import subprocess, os, sys

'''This will add the current working directory to the python path.
Meaning if this is run from the command line whatever directory the terminal is in.
'''
sys.path.insert(0, os.getcwd())


# Could do something like run the sync. If it has trouble connecting it could look for an RSA key.
# If it exists then copy it to the server.
# If it doesn't then make one and copy it to the server.


# Initialise: put down an initialising file to be filled out.
def initialise_settings():
	file = open('sync_settings.py', 'w')
	url = input( "Set your URL: " )
	file.write("url = '%s'\n" % url)
	# dev_url = input( "Set your Development URL: " )
	# file.write("dev_url = '%s'\n" % dev_url)
	file.write("dev_url = ''\n")
	current_ip_address = input("The current IP address: ")
	file.write("fromIP = '%s'\n" % current_ip_address)
	file.write("toIP = ''\n")
	file.write("docker_prefix = 'mdmediastack'\n")
	file.write("report_email = None\n")
	file.write("dropbox_access_token = None\n")

	# path_to_local_folder = input("The current IP address: ")
	path_to_local_folder = os.getcwd()
	file.write("path_to_local_folder = %s\n" % path_to_local_folder )
	
	path_to_remote_folder = "/"
	file.write("path_to_remote_folder = %s\n" % path_to_remote_folder )

	file.write("username = 'root'\n")
	file.write("server = fromIP\n")

	file.close()
	try: 
		exclude_file = open('_orite_exclude.txt')
	except FileNotFoundError:
		exclude_file = open('_orite_exclude.txt', 'w')
		exclude_file.write('''.git/
.DS_Store
.gitignore
# Cerificates
certs
dh.pem
key.pem
cert.pem
migrations
# Database files
*.sqlite
*.sqlite3
db/data
# Python cache files
*.pyc
__pycache__''')
		exclude_file.close()
	sys.stdout.write("The file 'sync_settings.py' and a default '_orite_exclude.txt' file have been made for you.")


try:
	from sync_settings import *
	settings_file_test = True
except ModuleNotFoundError:
	settings_file_test = False
	print('You have no sync_settings file.')
	# print('Initialise a settings file by running sync -i')
	initialise_settings()


# How does this directory differ from the remote one?


def local_to_remote(dry_run=True):
	print( 'Sync the local folder to the remote folder')
	vars = globals()
	print(vars['path_to_local_folder'])
	if dry_run:
		vars['dry_run'] = ' --dry-run'
	else:
		vars['dry_run'] = ''

	'''Add the dash to the end. The reason for this can be found on this page:
	https://www.digitalocean.com/community/tutorials/how-to-use-rsync-to-sync-local-and-remote-directories-on-a-vps
	'''
	if vars['path_to_local_folder'][-1] != '/':
		vars['path_to_local_folder'] = vars['path_to_local_folder'] + '/'

	'''Remove the dash from the end'''
	if vars['path_to_remote_folder'][-1] == '/':
		vars['path_to_remote_folder'] = vars['path_to_remote_folder'][:-1]

	'''Ensire that rsync is >= 3.1 for the --info=flist flag to work.
	Mac contains a version from 2006.
	This can be updated and documentation can be found here:
	https://f-a.nz/dev/update-macos-rsync-with-homebrew/
	'''
	command = 'rsync --human-readable --info=flist --stats --archive --verbose --partial -ic --progress{dry_run} {path_to_local_folder} {username}@{server}:{path_to_remote_folder} --exclude-from="sync_exclude.txt"'.format(**vars)
	# command = 'rsync --human-readable --info=flist --stats --archive --verbose --partial --progress{dry_run} {path_to_local_folder} {username}@{server}:{path_to_remote_folder} --exclude-from="sync_exclude.txt"'.format(**vars)
	# command = 'rsync --human-readable --stats --archive --verbose --partial --progress{dry_run} {path_to_local_folder} {username}@{server}:{path_to_remote_folder} --exclude-from="sync_exclude.txt"'.format(**vars)
	print( 'Running this command: ' + command )
	print('\n')
	return subprocess.call(command, shell=True)




def remote_to_local(dry_run=True):
	print( 'Sync the remote folder to the local folder')
	vars = globals()
	if dry_run:
		vars['dry_run'] = ' --dry-run'
	else:
		vars['dry_run'] = ''

	'''Remove the dash from the end'''
	if vars['path_to_local_folder'][-1] == '/':
		vars['path_to_local_folder'] = vars['path_to_local_folder'][:-1]
	'''Add the dash to the end'''
	if vars['path_to_remote_folder'][-1] != '/':
		vars['path_to_remote_folder'] = vars['path_to_remote_folder'] + '/'

	'''--info=flist flag only works in rysnc that is >= 3.1 Read comment in local_to_remote()'''
	command = 'rsync --human-readable --info=flist --stats --archive --verbose --partial --progress{dry_run} {username}@{server}:{path_to_remote_folder} {path_to_local_folder} --exclude-from="sync_exclude.txt"'.format(**vars)
	print( 'Running this command: ' + command )
	return subprocess.call(command, shell=True)


# rsync

# delete after flag


# sftp sync for servers that you can't get ssh access to.
def ssh_prompt():
	print('SSH command:')
	vars = globals()
	print('ssh %s@%s' % ( vars['username'], vars['server']) )



if __name__ == '__main__':

	import argparse
	'''
		Documentation here: https://docs.python.org/2/library/argparse.html
	'''
	parser = argparse.ArgumentParser(prog='Snyc', description='A wrapper for rsync with settings')
	parser.add_argument("-i", "--initialise_settings", help="Initialise the settings file")
	parser.add_argument("-v", "--from_remote_to_local", help="Sync the remote folder to the local folder", action="store_true")
	parser.add_argument("-^", "--from_local_to_remote", help="Sync the local folder to remote folder", action="store_true")
	parser.add_argument("-d", "--dry_run", help="Do a dry run. This is the default", action="store_true", default='')
	parser.add_argument("-r", "--for_real", help="Not a dry run, do it for real", action="store_true", default='')
	parser.add_argument("-ssh", "--ssh_prompt", help="Login using SSH", action="store_true", default='')
	args = parser.parse_args()


	if settings_file_test:
		dry_run = True
		if args.for_real:
			dry_run = False

		# remote_to_local(dry_run=True)
		if args.from_remote_to_local:
			remote_to_local(dry_run)
		elif args.from_local_to_remote:
			local_to_remote(dry_run)
		elif args.ssh_prompt:
			ssh_prompt()


# Make an invisible copy of the local folder to .<folder_name>--sync
# Sync from the remote to the copy
# run diff -r  <local-folder> .<local-folder>--sync/ --exclude-from <path-to>/sync_exclude.txt
# Bring this into sync and change so that it has more colour and is clearer what is what.

# Run diff but with numbers of the dirrences. Then the prompted can copy some of these accross.

