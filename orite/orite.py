#!/usr/local/bin/python3
'''
orite - is an opinionated rsync wrapper written in Python.

Whilst this is a Python module the intention is for it be run from the command line.
For a detailed write-up visit: https://github.com/meyouwe/orite
'''

from shutil import copyfile
import subprocess
import os
import sys
import argparse
import configparser


'''This will add the current working directory to the python path.
Meaning if this is run from the command line - whatever directory the terminal is in.
'''
sys.path.insert(0, os.getcwd())


exclude_file_name = "orite_exclude.txt"
config_file_name = "orite_config.ini"




def format_output(message, colour='34'):
	'''Makes the CLI output bold and gives it a colour.
	The default colour - 34 is blue.
	Colour numbers can be found here: https://en.wikipedia.org/wiki/ANSI_escape_code'''
	return "\x1b[1;" + colour + "m" + message + "\x1b[0m"




class initialise():
	'''This class has methods that check to see if the config file and exclude file is in the path where the script is running from. If they aren't then there are two methods that will initialise these files.'''
	def __init__(self):
		self.config_file_name = config_file_name
		self.exclude_file_name = exclude_file_name


	def initialise_config_file(self):
		''' Prompt the user and lay down and configuration file.'''

		config = configparser.ConfigParser()
		c = {}
		c['url'] = input( "Set your URL: " )

		c['remote_server'] = input("Set the remote IP address: ")

		c['username'] = input("Set your username: ")

		'''pwd and getcwd() doesn't escape spaces and rsync requires spaces to be escaped. This escapes spaces.''' 
		default_path_to_local_folder = '\ '.join(os.getcwd().split(' '))
		continue_question = input("Is your local folder: %s  [y/n]" % default_path_to_local_folder)
		if continue_question.lower() == 'n':
			c['path_to_local_folder'] = input("Set your local folder (escape spaces with a \): ")
		else:
			c['path_to_local_folder'] = default_path_to_local_folder
		
		c['path_to_remote_folder'] = input("Set your remote folder path: ")

		config['DEFAULT'] = c
		with open(config_file_name, 'w') as configfile:
			config.write(configfile)

		sys.stdout.write(
			format_output("The orite configuration file '{config_file_name}' has been made. Edit it how you like.\n".format(
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
		copyfile(os.path.join(script_dest, self.exclude_file_name), os.path.join(os.getcwd(), self.exclude_file_name))
		sys.stdout.write(format_output("A default exclude file has been made at '%s'. Edit it how you like.\n" % self.exclude_file_name))


	def exclude_file_exists(self):
		'''Test to see if the exclude file exists. If not copy the default file across.'''
		try:
			exclude_file_test = open(self.exclude_file_name)
			exclude_file_test.close()
		except FileNotFoundError:
			self.copy_exclude_file()




class commands():

	def __init__(self, username, remote_server, local_path, remote_path, dry_run):
		self.username = username
		self.remote_server = remote_server
		self.local_path = local_path
		self.remote_path = remote_path
		self.exclude_file_name = exclude_file_name

		if dry_run:
			self.dry_run = ' --dry-run'
		else:
			self.dry_run = ''

		if self.local_path[-1] == '/':
			local_path = self.local_path[:-1]
		else:
			local_path = self.local_path
		self.local_folder = os.path.basename(local_path)
		self.local_folder_copy_name = 'orite__%s' % self.local_folder


	def local_to_remote(self):
		'''Sync from the local path to the remote server'''
		sys.stdout.write('\nSync the local folder to the remote folder\n')

		'''Add the dash to the end. The reason for this can be found on this page: https://www.digitalocean.com/community/tutorials/how-to-use-rsync-to-sync-local-and-remote-directories-on-a-vps'''
		if self.local_path[-1] != '/':
			self.local_path = self.local_path + '/'
		'''Remove the dash from the end'''
		if self.remote_path[-1] == '/':
			self.remote_path = self.remote_path[:-1]

		'''Ensure that rsync is >= 3.1 for the --info=flist flag to work.
		Mac contains a version from 2006.
		This can be updated and documentation can be found here: https://f-a.nz/dev/update-macos-rsync-with-homebrew/
		'''
		command = 'rsync --human-readable --info=flist --stats --archive --verbose --partial -ic --progress{o.dry_run} {o.local_path} {o.username}@{o.remote_server}:{o.remote_path} --exclude-from="{o.exclude_file_name}"'.format(o=self)
		# Option for rsync <3.1
		# command = 'rsync --human-readable --stats --archive --verbose --partial --progress{o.dry_run} {o.local_path} {o.username}@{o.remote_server}:{o.remote_path} --exclude-from="{o.exclude_file_name}"'.format(o=self)
		sys.stdout.write(format_output('\nRunning this command: \n') + command + '\n\n')
		return subprocess.call(command, shell=True)


	def remote_to_local(self, local_path=False):
		'''Sync from the remote server to the local directory'''
		sys.stdout.write('\nSync the remote folder to the local folder\n')

		if not local_path:
			local_path = self.local_path

		'''Remove the dash from the end'''
		if local_path[-1] == '/':
			local_path = local_path[:-1]
		'''Add the dash to the end'''
		if self.remote_path[-1] != '/':
			self.remote_path = self.remote_path + '/'

		'''--info=flist flag only works in rysnc that is >= 3.1 Read comment in local_to_remote()'''
		command = 'rsync --human-readable --info=flist --stats --archive --verbose --partial --progress{o.dry_run} {o.username}@{o.remote_server}:{o.remote_path} {local_path} --exclude-from="{o.exclude_file_name}"'.format(o=self, **locals())
		sys.stdout.write(format_output('\nRunning this command: \n') + command + '\n\n')
		return subprocess.call(command, shell=True)


	def copy_local(self):
		if not os.path.isdir(self.local_folder_copy_name):
			command = 'cp -r {o.local_path} {o.local_folder_copy_name}'.format(o=self)
			subprocess.call(command, shell=True)


	def sync_remote_copy(self):
		local_copy_folder_path = '\ '.join(os.getcwd().split(' '))
		if local_copy_folder_path[-1] == '/':
			local_copy_folder_path = local_copy_folder_path + self.local_folder_copy_name
		else:
			local_copy_folder_path = local_copy_folder_path + '/' + self.local_folder_copy_name
			# local_copy_folder_path = '\ '.join(os.getcwd().split(' ')) + '/' + self.local_folder_copy_name
		self.remote_to_local(local_path=local_copy_folder_path)


	def compare_local_to_remote_copy(self):
		'''Compare the local folder to the local remote copy.'''
		command = 'diff -r -N  {o.local_path} {o.local_folder_copy_name}/ --exclude-from {o.exclude_file_name}'.format(o=self, **locals())
		sys.stdout.write(format_output('\nRunning this command: \n') + command + '\n\n')
		return subprocess.call(command, shell=True)


	def ssh_into_remote(self):
		'''ssh into the exact path on the remote server using your config file.'''
		sys.stdout.write(format_output('Running this command: \n'))
		command = 'ssh {o.username}@{o.remote_server} -t "cd {o.remote_path}; bash --login"'.format(o=self)
		sys.stdout.write(command + '\n')
		return subprocess.call(command, shell=True)


	def sftp_into_remote(self):
		'''sftp into the exact path on the remote server using your config file.'''
		sys.stdout.write(format_output('Running this command: \n'))
		command = 'sftp {o.username}@{o.remote_server}:{o.remote_path}'.format(o=self)
		sys.stdout.write(command + '\n')
		return subprocess.call(command, shell=True)




def main():
	'''FYI argparse documentation is here: https://docs.python.org/2/library/argparse.html'''
	parser = argparse.ArgumentParser(prog='Snyc', description='A Python wrapper mainly around rsync with configuration files.')
	parser.add_argument("-v", "--remote_to_local", help="Sync the remote folder to the local folder", action="store_true")
	parser.add_argument("-^", "--local_to_remote", help="Sync the local folder to remote folder", action="store_true")
	parser.add_argument("-d", "--dry_run", help="Do a dry run. This is the default", action="store_true", default='')
	parser.add_argument("-r", "--for_real", help="Not a dry run, do it for real", action="store_true", default='')
	parser.add_argument("-s", "--ssh", help="Login using SSH", action="store_true", default='')
	parser.add_argument("--sftp", help="Login using SFTP", action="store_true", default='')

	parser.add_argument("-C", "--initial_copy", help="Copy the local folder for use in diff.", action="store_true", default='')
	parser.add_argument('-R', "--remote_to_remote_copy", help="Sync the remote folder to the local remote copy", action="store_true", default='')
	parser.add_argument('-D', "--diff", help="Compare the local folder to the local remote copy", action="store_true", default='')
	args = parser.parse_args()

	init = initialise()
	init.config_file_exists()
	init.exclude_file_exists()

	if args.for_real:
		dry_run = False
	else:
		dry_run = True

	config = configparser.ConfigParser()
	config.read(config_file_name)

	try:
		config = config['DEFAULT']
		username = config['username']
		remote_server = config['remote_server']
		local_path = config['path_to_local_folder']
		remote_path = config['path_to_remote_folder']
		
		com = commands(username, remote_server, local_path, remote_path, dry_run)

	except KeyError:
		sys.stdout.write(format_output('A keyword is missing in your config file\n', '31'))
		sys.stdout.write('Check the spelling or remove the config file altogther and re-initialise orite.\n')
		sys.exit()


	if args.remote_to_local:
		com.remote_to_local()
	elif args.local_to_remote:
		com.local_to_remote()
	elif args.ssh:
		com.ssh_into_remote()
	elif args.sftp:
		com.sftp_into_remote()
	elif args.initial_copy:
		com.copy_local()
	elif args.remote_to_remote_copy:
		com.sync_remote_copy()
	elif args.diff:
		com.compare_local_to_remote_copy()

	# Doesn't work.
	else:
		sys.stdout.write(format_output('Use orite -h to see which options are available\n'))



if __name__ == '__main__':
	main()