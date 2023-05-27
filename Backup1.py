#! /usr/bin/env python3

#A program to backup my files.


def checkSourceDestination(sourceStr, destinationStr) :
  from pathlib import Path
 
  #Check to see that the destination exists.
  pDestination = Path(destinationStr)
  pSource = Path(sourceStr)

  #Lets get some file exist information.
  if(pDestination.exists()) :
    pDExistsFlag = 1
  else :
    pDExistsFlag = 0
    print('The destination : ' + sourceStr + ' does not exist.')
  #End of if-else statement.
    
  if(pDestination.is_dir()) :
    pDIsDirFlag = 1
  else :
    pDIsDirFlag = 0
    print('The destination : ' + sourceStr + ' is not a directory.')
  #End of if-else statement.

  if(pSource.exists()) :
    pSExistsFlag = 1
  else :
    pSExistsFlag = 0
    print('The source : ' + sourceStr + ' does not exist.')
  #End of if-else statement.

  if(pSource.is_dir()) :
    pSIsDirFlag = 1
  else :
    pSIsDirFlag = 0
    print('The source : ' + sourceStr + ' is not a directory.')
  #End of if-else statement.

  if(pDExistsFlag and pDIsDirFlag and pSExistsFlag and pSIsDirFlag) :
    flag = 1
  else :
    flag = 0
  #End of if-else statement.

  return flag
#end of the function checkSourceDestination.py
###################################################################################

###################################################################################

def getRSYNCErrorCodes(codeValue):
  
  if(codeValue == 0) :
    errorMessage = 'Success'
  elif(codeValue == 1) :
    errorMessage = 'Syntax or usage error'    
  elif(codeValue == 2) :
    errorMessage = 'Protocol incompatibility'
  elif(codeValue == 3) :
    errorMessage = 'Errors selecting input/output files, dirs'
  elif(codeValue == 4) :
    em1 = 'Requested action not supported: an attempt was made to manipulate 64-bit'
    em2 = 'files on a platform that cannot support them; or an option was specified'
    em3 = 'that is supported by the client and not by the server.'
    errorMessage = (em1 + em2 + em3)       
  elif(codeValue == 5) :
    errorMessage = 'Error starting client-server protocol'
  elif(codeValue == 6) :
    errorMessage = 'Daemon unable to append to log-file'
  elif(codeValue == 10) :
    errorMessage = 'Error in socket I/O'
  elif(codeValue == 11) :
    errorMessage = 'Error in file I/O'
  elif(codeValue == 12) :
    errorMessage = 'Error in rsync protocol data stream'
  elif(codeValue == 13) :
    errorMessage = 'Errors with program diagnostics'
  elif(codeValue == 14) :
    errorMessage = 'Error in IPC code'
  elif(codeValue == 20) :
    errorMessage = 'Received SIGUSR1 or SIGINT'
  elif(codeValue == 21) :
    errorMessage = 'Some error returned by waitpid()'
  elif(codeValue == 22) :
    errorMessage = 'Error allocating core memory buffers'
  elif(codeValue == 23) :
    errorMessage = 'Partial transfer due to error'
  elif(codeValue == 24) :
    errorMessage = 'Partial transfer due to vanished source files'
  elif(codeValue == 25) :
    errorMessage = 'The --max-delete limit stopped d  elif(codeValue == 20) :'
  elif(codeValue == 30) :
    errorMessage = 'Timeout in data send/receive'
  elif(codeValue == 35) :
    errorMessage = 'Timeout waiting for daemon connection'
  else :
    errorMessage = 'Unrecognized Error Code'
  #End of if-elif-else clause.
  
  return errorMessage  
#End of the function getRSYNCErrorCodes.py
########################################################################################

########################################################################################

def getArgs(parser) :
  from time import strftime, localtime
 
  #Get the parameters
  parser.add_argument('-d', '--Destination', default = '/run/media/jdw/Birch2/',
                      help = 'Choose the destination directory') 

  parser.add_argument('-s', '--Source', default = '/home/jdw/Downloads',
                      help = 'Choose the source directory.', type = str)

  args = parser.parse_args()

  #Generate variables from the inputs.
  source = args.Source
  destination = args.Destination

  #Add the date to the destination string.
#  backUpStr = strftime("%d%b%Y_%H:%M:%S", localtime())
#  destination = destination + 'Birch' + backUpStr

  return source, destination
#End of the function getArgs(parser).py
#################################################################################

#################################################################################

#Gather our code in a main() function.
def main() :

  import sys
  import os
  sys.path.append('/home/jdw/bin/')
  import argparse

  from time import strftime, localtime
  from subprocess import Popen, PIPE, STDOUT
  from subprocess import check_output

  #Get the local time.
  dateTimeStr = strftime("%a, %d %b %Y %H:%M:%S", localtime())
  backUpStr = strftime("%d%b%Y-%H%M%S", localtime())
  
  #Set up the argument parser.
  parser = argparse.ArgumentParser()

  #Get the arguments.
  source, destination = getArgs(parser)

  #The rsync command line structure.
#  optionsStr = '-av --progress'
  optionsStr = '-av'
  sourceStr = str(source)
  destinationStr = str(destination)

  #Check that the source and destination directories exist.
  sourceDestinationFlag = checkSourceDestination(sourceStr, destinationStr)

  #Now run the command if possible.
  if(sourceDestinationFlag) :
    #Generate the command.
    command = ('rsync ' + optionsStr + ' ' + sourceStr + ' ' + destinationStr)

    #Run the command.
    results = Popen(['rsync', optionsStr, sourceStr, destinationStr],
                         stdout = PIPE, stderr = STDOUT)
    out, err = results.communicate()
    message = getRSYNCErrorCodes(results.returncode)

    #Write the message of the command to a file.
    messageFileDir = '/home/jdw/Backups/Logs/'
    messageFileName = 'BU' + backUpStr
    messageFile = messageFileDir + messageFileName
    with open(messageFile, 'w') as f :
      f.write(message)
  else :
    print('Data is not backed up for : ' + dateTimeStr)

    
# Standard boilerplate to call the main() function to begin
# the program.
if __name__ == '__main__':
  main()
