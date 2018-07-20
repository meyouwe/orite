#!/usr/local/bin/python3
import subprocess, os, sys
from shutil import copyfile

'''
orite.py - is an opinionated rsync wrapper written in Python.

'''


'''This will add the current working directory to the python path.
Meaning if this is run from the command line – whatever directory the terminal is in.
'''
sys.path.insert(0, os.getcwd())


exclude_file_name = "_orite_exclude.txt"
config_file_name = "_orite_config.py"


def format_output(message, colour='34'):
	'''Makes the CLI output bold and gives it a colour.
	The default colour – 34 is blue.
	Colour numbers can be found here: https://en.wikipedia.org/wiki/ANSI_escape_code'''
	return "\x1b[1;" + colour + "m" + message + "\x1b[0m"


class initialise():
	def __init__(self, config_file_name, exclude_file_name):
		self.config_file_name = config_file_name
		self.exclude_file_name = exclude_file_name


	# Initialise: put down an initialising file to be filled out.
	def initialise_config_file(self):
		file = open(config_file_name, 'w')
		url = input( "Set your URL: " )
		file.write("url = '%s'\n" % url)

		current_ip_address = input("The remote IP address: ")
		file.write("remote_server = '%s'\n" % current_ip_address)

		path_to_local_folder = os.getcwd()
		file.write("path_to_local_folder = '%s'\n" % path_to_local_folder )
		
		path_to_remote_folder = "/"
		file.write("path_to_remote_folder = '%s'\n" % path_to_remote_folder )

		username = input("What is the username: ")
		file.write("username = '%s'\n" % username)

		# This can come out
		file.write("server = remote_server\n")

		file.close()

		sys.stdout.write(
			format_output("The file 'sync_settings.py' has been made.\n".format(
				**globals()
			)
		))


	def copy_exclude_file(self):
		'''Copy across the default exclude file as a starting point.
		I have seen .gitignore used as an exclude file. This is an interesting idea but not there will be differences between these two.
		'''
		script_dest = os.path.dirname(sys.argv[0])
		copyfile(os.path.join(script_dest, exclude_file_name), os.path.join(os.getcwd(), exclude_file_name))


	def initialise_exclude_file(self):
		'''Test to see if the exclude file exists. If not copy the default file across.'''
		try:
			exclude_file = open(self.exclude_file_name)
		except FileNotFoundError:
			self.copy_exclude_file()
			sys.stdout.write(format_output("A default exclude file has been made at '%s'\n" % self.exclude_file_name))



init = initialise(config_file_name, exclude_file_name)
try:
	from _orite_config import *
	settings_file_test = True
	init.initialise_exclude_file()
except ModuleNotFoundError:
	settings_file_test = False
	sys.stdout.write(format_output('You have no %s file in this directory.\n' % config_file_name))
	init.initialise_config_file()
	init.initialise_exclude_file()




def local_to_remote(dry_run=True):
	sys.stdout.write('\nSync the local folder to the remote folder\n')
	vars = globals()
	if dry_run:
		vars['dry_run'] = ' --dry-run'
	else:
		vars['dry_run'] = ''

	'''Add the dash to the end. The reason for this can be found on this page: https://www.digitalocean.com/community/tutorials/how-to-use-rsync-to-sync-local-and-remote-directories-on-a-vps'''
	if vars['path_to_local_folder'][-1] != '/':
		vars['path_to_local_folder'] = vars['path_to_local_folder'] + '/'
	'''Remove the dash from the end'''
	if vars['path_to_remote_folder'][-1] == '/':
		vars['path_to_remote_folder'] = vars['path_to_remote_folder'][:-1]

	'''Ensire that rsync is >= 3.1 for the --info=flist flag to work.
	Mac contains a version from 2006.
	This can be updated and documentation can be found here: https://f-a.nz/dev/update-macos-rsync-with-homebrew/
	'''
	command = 'rsync --human-readable --info=flist --stats --archive --verbose --partial -ic --progress{dry_run} {path_to_local_folder} {username}@{server}:{path_to_remote_folder} --exclude-from="{exclude_file_name}"'.format(**vars)
	# Option for rsync <3.1
	# command = 'rsync --human-readable --stats --archive --verbose --partial --progress{dry_run} {path_to_local_folder} {username}@{server}:{path_to_remote_folder} --exclude-from="sync_exclude.txt"'.format(**vars)
	sys.stdout.write(format_output('\nRunning this command: \n') + command + '\n\n')
	return subprocess.call(command, shell=True)




def remote_to_local(dry_run=True):
	sys.stdout.write('\nSync the remote folder to the local folder\n')
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
	command = 'rsync --human-readable --info=flist --stats --archive --verbose --partial --progress{dry_run} {username}@{server}:{path_to_remote_folder} {path_to_local_folder} --exclude-from="{exclude_file_name}"'.format(**vars)
	sys.stdout.write(format_output('\nRunning this command: \n') + command + '\n\n')
	return subprocess.call(command, shell=True)




def ssh_prompt():
	'''sftp sync for servers that you can't get ssh access to.'''
	print('SSH command:')
	vars = globals()
	print('ssh %s@%s' % ( vars['username'], vars['server']) )




if __name__ == '__main__':

	import argparse
	'''argparse documentation is here: https://docs.python.org/2/library/argparse.html'''
	parser = argparse.ArgumentParser(prog='Snyc', description='A wrapper for rsync with configuration files')
	parser.add_argument("-i", "--init", help="Initialise the config and exclude files")
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

		if args.from_remote_to_local:
			remote_to_local(dry_run)
		elif args.from_local_to_remote:
			local_to_remote(dry_run)
		elif args.ssh_prompt:
			ssh_prompt()
