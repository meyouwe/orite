#!/usr/local/bin/python3
'''
orite - is an opinionated rsync wrapper written in Python.

Whilst this is a Python module the intention is for it be run from the command line.
For a detailed write-up visit: https://github.com/meyouwe/orite
'''

from shutil import copyfile
import subprocess, os, sys
import argparse
import configparser


'''This will add the current working directory to the python path.
Meaning if this is run from the command line - whatever directory the terminal is in.
'''
sys.path.insert(0, os.getcwd())


exclude_file_name = "_orite_exclude.txt"
config_file_name = "_orite_config.ini"




def format_output(message, colour='34'):
	'''Makes the CLI output bold and gives it a colour.
	The default colour - 34 is blue.
	Colour numbers can be found here: https://en.wikipedia.org/wiki/ANSI_escape_code'''
	return "\x1b[1;" + colour + "m" + message + "\x1b[0m"




class initialise():
	'''This class has methods that check to see if the config file and exclude file is in the path where the script is running from. If they aren't then there two methods the can initialise these files.'''
	def __init__(self):
		self.config_file_name = config_file_name
		self.exclude_file_name = exclude_file_name


	def initialise_config_file(self):
		''' Prompt the user and lay down and configuration file.'''
		file = open(config_file_name, 'w')
		url = input( "Set your URL: " )
		file.write("url = '%s'\n" % url)

		current_ip_address = input("Set the remote IP address: ")
		file.write("remote_server = '%s'\n" % current_ip_address)

		username = input("Set your username: ")
		file.write("username = '%s'\n" % username)

		'''pwd and getcwd() don't escape a space. This escapes that space for use later''' 
		default_path_to_local_folder = '\ '.join(os.getcwd().split(' '))
		continue_question = input("Is your local folder: %s  [y/n]" % default_path_to_local_folder)
		if continue_question.lower() == 'n':
			path_to_local_folder = input("Set your local folder: ")
		else:
			path_to_local_folder = default_path_to_local_folder
		file.write("path_to_local_folder = '%s'\n" % path_to_local_folder )
		
		path_to_remote_folder = input("Set your remote folder path: ")
		file.write("path_to_remote_folder = '%s'\n" % path_to_remote_folder )

		file.close()

		sys.stdout.write(
			format_output("The file orite configuration file '{config_file_name}' has been made.\n".format(
				**globals()
			)
		))


	def config_file_exists(self):
		"""Test to see if the config file exists. If id doesn't make one."""
		try:
			config_file_test = open(self.config_file_name)
			config_file_test.close()
		except FileNotFoundError:
			continue_question = input(format_output('You have no config file in this directory. Would you like to make one? [y/n] \n'))
			if continue_question.lower() == 'n':
				sys.exit()
			else:
				self.initialise_config_file()


	def copy_exclude_file(self):
		'''Copy across the default exclude file as a starting point.
		I have seen .gitignore used as an exclude file. This is an interesting idea but not there will be differences between these two.
		'''
		script_dest = os.path.dirname(os.path.realpath(__file__))
		copyfile(os.path.join(script_dest, exclude_file_name), os.path.join(os.getcwd(), exclude_file_name))
		sys.stdout.write(format_output("A default exclude file has been made at '%s'\n" % self.exclude_file_name))


	def exclude_file_exists(self):
		'''Test to see if the exclude file exists. If not copy the default file across.'''
		try:
			exclude_file_test = open(self.exclude_file_name)
			exclude_file_test.close()
		except FileNotFoundError:
			self.copy_exclude_file()




def local_to_remote(dry_run=True):
	'''Sync from the local path to the remote server'''
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
	command = 'rsync --human-readable --info=flist --stats --archive --verbose --partial -ic --progress{dry_run} {path_to_local_folder} {username}@{remote_server}:{path_to_remote_folder} --exclude-from="{exclude_file_name}"'.format(**vars)
	# Option for rsync <3.1
	# command = 'rsync --human-readable --stats --archive --verbose --partial --progress{dry_run} {path_to_local_folder} {username}@{remote_server}:{path_to_remote_folder} --exclude-from="sync_exclude.txt"'.format(**vars)
	sys.stdout.write(format_output('\nRunning this command: \n') + command + '\n\n')
	return subprocess.call(command, shell=True)




def remote_to_local(dry_run=True):
	'''Sync from the remote server to the local directory'''
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
	command = 'rsync --human-readable --info=flist --stats --archive --verbose --partial --progress{dry_run} {username}@{remote_server}:{path_to_remote_folder} {path_to_local_folder} --exclude-from="{exclude_file_name}"'.format(**vars)
	sys.stdout.write(format_output('\nRunning this command: \n') + command + '\n\n')
	return subprocess.call(command, shell=True)




def ssh_prompt():
	'''sftp sync for servers that you can't get ssh access to.'''
	sys.stdout.write('SSH command:')
	vars = globals()
	sys.stdout.write('ssh %s@%s' % ( vars['username'], vars['remote_server']) )


try:
	from _orite_config import *
except ModuleNotFoundError:
	pass

def main():
	'''argparse documentation is here: https://docs.python.org/2/library/argparse.html'''
	parser = argparse.ArgumentParser(prog='Snyc', description='A wrapper for rsync with configuration files')
	parser.add_argument("-i", "--init", help="Initialise the config and exclude files")
	parser.add_argument("-v", "--from_remote_to_local", help="Sync the remote folder to the local folder", action="store_true")
	parser.add_argument("-^", "--from_local_to_remote", help="Sync the local folder to remote folder", action="store_true")
	parser.add_argument("-d", "--dry_run", help="Do a dry run. This is the default", action="store_true", default='')
	parser.add_argument("-r", "--for_real", help="Not a dry run, do it for real", action="store_true", default='')
	parser.add_argument("-ssh", "--ssh_prompt", help="Login using SSH", action="store_true", default='')
	args = parser.parse_args()

	init = initialise()
	init.config_file_exists()
	init.exclude_file_exists()

	config = configparser.ConfigParser()
	config.read(config_file_name)
	try:
		config = config['DEFAULT']
		remote_server = config['remote_server']
		username = config['username']
		path_to_local_folder = config['path_to_local_folder']
		path_to_remote_folder = config['path_to_remote_folder']
	except KeyError:
		sys.stdout.write(format_output('A keyword is missing in your config file\n', '31'))
		sys.stdout.write('Check the spelling or remove the config file altogther and re-initialise orite.\n')


	dry_run = True
	if args.for_real:
		dry_run = False

	if args.from_remote_to_local:
		remote_to_local(dry_run)
	elif args.from_local_to_remote:
		local_to_remote(dry_run)
	elif args.ssh_prompt:
		ssh_prompt()


if __name__ == '__main__':
	main()