import paramiko
import re
from threading import Thread

PRIVATE_KEY_FILE = 'id_rsa'

# Object representing a generic ssh node
class SshNode(object):

  # Initialization
  def __init__(self, host, name, username):
    # Store the internal state
    self.host = host
    self.name = name
    self.username = username
    self.passwd = ""
    # Explicit stop
    self.stop = False
    # Spawn a new thread and connect in ssh
    self.t_connect()

  # Connect in ssh using a new thread
  def t_connect(self):
    # Main function is self.connect
    self.conn_thread = Thread(target=self.connect)
    # Start the thread
    self.conn_thread.start()
    # Wait for the end
    self.conn_thread.join()

  # Connect function
  def connect(self):
    # Spawn a ssh client
    self.client = paramiko.SSHClient()
    # Auto add policy
    self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    # Connect to the host
    self.client.connect(self.host, username=self.username, key_filename=PRIVATE_KEY_FILE)
    # Spawn a channel to send commands
    self.chan = self.client.invoke_shell()
    # Wait for the end
    self.wait()

  # Wait for the end of the previous command
  def wait(self):
    # Init steps
    buff = ''
    # Exit conditions
    u = re.compile('[$] ')
    # Iterate until the stdout ends or the stop condition has been triggered
    while not u.search(buff) and self.stop == False:
      # Rcv from the channel the stdout
      resp = self.chan.recv(1024).decode('utf-8')
      # if it is a sudo command, send the password
      if re.search(".*\[sudo\].*", resp):
        self.chan.send("%s\r" % (self.passwd))
      # Add response on buffer
      buff += resp
    # Done, return the response
    return buff

  # Run the command and wait for the end
  def run_command(self, command):
    # Send the command on the channel with \r
    self.chan.send(command + "\r")
    # Wait for the end and take the stdout
    buff = self.wait()
    # Save in data the stdout of the last cmd
    self.data = buff

  # Create a new worker thread
  def run(self, command):
    # Create a new Thread
    self.op_thread = Thread(
      target=self.run_command,
      args=([command])
      )
    # Start the thread
    self.op_thread.start()

  # Stop any running execution and close the connection
  def terminate(self):
    # Terminate signal for the thread
    self.stop = True
    # If the connection has been initialized
    if self.client != None:
      # Let's close it
      self.client.close()
    # Wait for the termination of the worker thread
    self.op_thread.join()

  # Join with the thread
  def join(self):
    self.op_thread.join()
