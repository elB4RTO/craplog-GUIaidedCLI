#!/usr/bin/python3

import os
import time
import subprocess
from sys import argv
from pathlib import Path
from datetime import datetime

# GETTING ARGUMENTS
LessOutput			= int( argv[1]  )
AccessLogs			= int( argv[2]  )
CleanAccessLogs		= int( argv[3]  )
ErrorLogs			= int( argv[4]  )
ErrorsOnly			= int( argv[5]  )
GlobalsOnly			= int( argv[6]  )
GlobalsAvoid		= int( argv[7]  )
Backup				= int( argv[8]  )
BackupDelete		= int( argv[9]  )
AutoDelete			= int( argv[10] )
Trash				= int( argv[11] )
Shred				= int( argv[12] )

# GETTING OWN MODULES
import Clean, Stat
if not GlobalsAvoid:
	import Glob

# GETTING CRAPLOG'S PATH
crappath = os.path.abspath(__file__)
crappath = crappath[:crappath.rfind('/crappy/Main.py')]

# CRAPLOGO
print("\
\033[1;40m                                                     \033[0m\n\
\033[1;40m   \033[31m CCCC  \033[33mRRRR   \033[32mAAAAA  \033[36mPPPP   \033[34mL      \033[35mOOOOO  \033[37mGGGGG   \033[0m\n\
\033[1;40m   \033[31mC      \033[33mR   R  \033[32mA   A  \033[36mP   P  \033[34mL      \033[35mO   O  \033[37mG       \033[0m\n\
\033[1;40m   \033[31mC      \033[33mRRRR   \033[32mAAAAA  \033[36mPPPP   \033[34mL      \033[35mO   O  \033[37mG  GG   \033[0m\n\
\033[1;40m   \033[31mC      \033[33mR  R   \033[32mA   A  \033[36mP      \033[34mL      \033[35mO   O  \033[37mG   G   \033[0m\n\
\033[1;40m   \033[31m CCCC  \033[33mR   R  \033[32mA   A  \033[36mP      \033[34mLLLLL  \033[35mOOOOO  \033[37mGGGGG   \033[0m\n\
\033[1;40m                                                     \033[0m\n")

# VARIABLES INTEGRITY CHECKS
if not AccessLogs and not ErrorLogs:
	print("\033[33mError\033[0m: you can't avoid using both access and error log files, nothing will be done")
	closing = input("Show more? [Y/n] : ")
	if closing == "" or closing == "y" or closing == "Y":
		print("\n\033[33m[+]\033[0m: this should be only a security check")
		print("\033[33m[+]\033[0m: if you're reading this, both the [\033[36mAccessLogs\033[0m] and the [\033[36mErrorLogs\033[0m] variable are set to \033[31m0\033[0m.")
		print("\033[33m[+]\033[0m: if you manually edited any file, undo the changes or copy paste the original from https://github.com/elB4RTO/craplog-GUI")
		print("\033[33m[+]\033[0m: if you haven't edited any file, please report this issue")
		input("\n\033[90mPress any key to continue ...\033[0m\n")
	else:
		print()
	exit()

if not AccessLogs and CleanAccessLogs:
	print("\033[33mError\033[0m: not possible to make a clean access log file [\033[36m-c\033[0m] without working on a access.log file [\033[36m--only-errors\033[0m]")
	input("\n\033[90mPress any key to continue ...\033[0m\n")
	exit()

if not ErrorLogs and ErrorsOnly:
	print("\033[33mError\033[0m: not possible to only use error logs file [\033[36m--only-errors\033[0m] without working on a error.log file [\033[36m--errors\033[0m]")
	closing = input("Show more? [Y/n] : ")
	if closing == "" or closing == "y" or closing == "Y":
		print("\n\033[33m[+]\033[0m: this should be only a security check")
		print("\033[33m[+]\033[0m: if you're reading this, the [\033[36mErrorsOnly\033[0m] variable is set to \033[31m1\033[0m, but the [\033[36mErrorLogs\033[0m] variable is set to \033[31m0\033[0m.")
		print("\033[33m[+]\033[0m: if you manually edited any file, undo the changes or copy paste the original from https://github.com/elB4RTO/craplog-GUI")
		print("\033[33m[+]\033[0m: if you haven't edited any file, please report this error")
		input("\n\033[90mPress any key to continue ...\033[0m\n")
	else:
		print()
	exit()

if GlobalsOnly and GlobalsAvoid:
	print("\033[33mError\033[0m: you can't use \033[36m--only-globals\033[0m toghether with \033[36m--avoid-globals\033[0m")
	input("\n\033[90mPress any key to continue ...\033[0m\n")
	exit()

if Trash and Shred:
	print("\033[33mError\033[0m: you can't use \033[36m--trash\033[0m toghether with \033[36m--shred\033[0m")
	input("\n\033[90mPress any key to continue ...\033[0m\n")
	exit()

# INPUT FILES EXISTENCE CHECKS
if not os.path.exists("/var/log/apache2"):
	print("\033[33mError\033[0m: directory \033[31m/var/log/apache2/\033[0m does not exist")
	input("\n\033[90mPress any key to continue ...\033[0m\n")
	exit()

if AccessLogs:
	if not os.path.exists("/var/log/apache2/access.log.1"):
		print("\033[33mError\033[0m: there is no \033[31maccess.log.1\033[0m file inside \033[32m/var/log/apache2/\033[0m")
		input("\n\033[90mPress any key to continue ...\033[0m\n")
		exit()
	else:
		try:
			file = open("/var/log/apache2/access.log.1", "r")
			file.close()
		except IOError:
			print("\033[33mError\033[0m: can't read \033[32m/var/log/apache2/\033[31maccess.log.1\033[0m")
			input("\n\033[90mPress any key to continue ...\033[0m\n")
			exit()

if ErrorLogs:
	if not os.path.exists("/var/log/apache2/error.log.1"):
		print("\033[33mError\033[0m: there is no \033[31merror.log.1\033[0m file inside \033[32m/var/log/apache2/\033[0m")
		input("\n\033[90mPress any key to continue ...\033[0m\n")
		exit()
	else:
		try:
			file = open("/var/log/apache2/error.log.1", "r")
			file.close()
		except IOError:
			print("\033[33mError\033[0m: can't read \033[32m/var/log/apache2/\033[31merror.log.1\033[0m")
			input("\n\033[90mPress any key to continue ...\033[0m\n")
			exit()

# TRASH EXISTENCE CHECK
if Trash:
	TrashPath = "%s/.local/share/Trash/files/" %( os.environ['HOME'] )
	if not os.path.exists(TrashPath):
		print("\033[33mError\033[0m: directory \033[31m%s\033[0m does not exist" %( TrashPath ))
		input("\n\033[90mPress any key to continue ...\033[0m\n")
		exit()

# ALL CHECKS PASSED

# WELCOME MESSAGE
print("WELCOME TO CRAPLOG")
if not LessOutput:
	print("Use \033[36m--help\033[0m to view an help screen")
if AutoDelete :
	print("\033[93mAuto-Delete\033[0m is \033[1mON\033[0m")
print()
time.sleep(2)

# CHECKING AND REMOVING CONFLICT FILES
FilesList		= []
ConflictFiles	= []
if os.exists("%s/STATS/" %( crappath )):
	for (path, dirs, files) in os.walk("%s/STATS/" %( crappath )):
		FilesList.extend(files)
		break
	if len(FilesList) > 0:
		for File in FilesList:
			if File.endswith(".crap") or File.endswith(".crapstats") or File == "CLEAN.access.log":			
				ConflictFiles.append(File)

	FilesList		= []
	for (path, dirs, files) in os.walk("%s/STATS/GLOBALS/" %( crappath )):
		FilesList.extend(files)
		break
	if len(FilesList) > 0:
		for File in FilesList:
			if File.startswith(".GLOBAL.") and File.endswith(".crap"):
				ConflictFiles.append("GLOBALS/%s" %( File ))
else:
	Path("%s/STATS" %( crappath )).mkdir(parents=True, exist_ok=True)

if len(ConflictFiles) > 0:
	if AutoDelete:
		if not LessOutput:
			print("\n\033[93mRemoving conflict files\033[0m ...\n")
			time.sleep(1)
		
		for File in ConflictFiles:
			if Trash:
				subprocess.run([ "mv", "%s/STATS/%s" %( crappath, File ), TrashPath ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

			elif Shred:
				subprocess.run(["shred", "-uvz", "%s/STATS/%s" %( crappath, File )], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
			else:
				subprocess.run(["rm", "%s/STATS/%s" %( crappath, File )], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

	else:
		crapstat = craptemp = 0
		
		print("!!! \033[33mWARNING\033[0m !!!")
		print("Conflict files detected:")
		
		if "CLEAN.access.log" in ConflictFiles:
			crapstat = 1
			print("- %s/STATS/\033[33mCLEAN.access\033[90m.log\033[0m" %( crappath ))

		for File in ConflictFiles:
			if File.endswith(".crapstats") and not File.startswith("GLOBALS"):
				crapstat = 1
				print("- %s/STATS/\033[33m%s\033[0m" %( crappath, File.replace(".crapstats", "\033[90m.crapstats") ))
			elif File.endswith(".crap"):
				craptemp = 1

		if craptemp:
			print("- \033[90mCraplog's temporary files\033[0m")

		if not LessOutput:
			print("\nThese files must be removed to have CRAPLOG working as expected")
			if crapstat:
				print("Files in \033[33mYELLOW\033[0m are the result of your last invocation of CRAPLOG, aborted before the end\nBecause of that, you should consider to delete them\nPlease check these files and make sure you don't need them before to procede")

		if not Trash:
			print("\nEVERY DELETED FILE WILL BE LOST FOREVER AND NOT RECOVERABLE!")
			delete = input("Delete listed files? [Y/n] : ")
		else:
			delete = input("\nMove listed files to Trash? [Y/n] : ")
		
		if delete == "y" or delete == "Y":
			print("\n\033[91mRemoving conflict files\033[0m ...")
			for File in ConflictFiles:
				if Trash:
					subprocess.run(["mv", "%s/STATS/%s" %( crappath, File ), TrashPath ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
				elif Shred:
					subprocess.run(["shred", "-uvz", "%s/STATS/%s" %( crappath, File )], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
				else:
					subprocess.run(["rm", "%s/STATS/%s" %( crappath, File )], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
			if not LessOutput:
				print("Done\n")
				time.sleep(1)
			else:
				print()
			print("STARTING \033[31;40m C\033[33mR\033[32mA\033[36mP\033[34mL\033[35mO\033[37mG \033[0m\n")
			time.sleep(2)
		else:
			print("\nCRAPLOG ABORTED\n")
			exit()


# STARTING CRAPLOG
# CLEANING AND SCRAPING SESSION LOGS
Clean.Access( AccessLogs, CleanAccessLogs)
Clean.Error( ErrorLogs )
if not LessOutput:
	print("Done\n")
	time.sleep(1)
else:
	print()

if not LessOutput:
	if CleanAccessLogs:
		print("New file created:\n- \033[32mCLEAN.access\033[90m.log\033[0m\n")
		time.sleep(2)


# CREATING STATISTICS FROM SESSION LOGS
Stat.Access( AccessLogs )
Stat.Error( ErrorLogs )
if not LessOutput:
	print("Done\n")
	time.sleep(1)
else:
	print()

if not LessOutput:
	if not GlobalsOnly:
		print("New SESSION files created:")
		if AccessLogs:
			print("\033[0m- \033[32mIP\033[90m.crapstats\033[0m\n- \033[32mREQ\033[90m.crapstats\033[0m\n- \033[32mRES\033[90m.crapstats\033[0m\n- \033[32mUA\033[90m.crapstats\033[0m")
		if ErrorLogs:
			print("\033[0m- \033[32mLEV\033[90m.crapstats\033[0m\n- \033[32mERR\033[90m.crapstats\033[0m")
		if AccessLogs or ErrorLogs:
			print()
			time.sleep(2)


# UPDATING GLOBAL STATISTICS
if not GlobalsAvoid:
	if AccessLogs:
		try:
			os.rename("%s/STATS/GLOBALS/GLOBAL.IP.crapstats" %( crappath ), "%s/STATS/GLOBALS/.GLOBAL.IP.crap" %( crappath ))
		except:
			Path("%s/STATS/GLOBALS/.GLOBAL.IP.crap" %( crappath )).touch()

		try:
			os.rename("%s/STATS/GLOBALS/GLOBAL.REQ.crapstats" %( crappath ), "%s/STATS/GLOBALS/.GLOBAL.REQ.crap" %( crappath ))
		except:
			Path("%s/STATS/GLOBALS/.GLOBAL.REQ.crap" %( crappath )).touch()
		
		try:
			os.rename("%s/STATS/GLOBALS/GLOBAL.RES.crapstats" %( crappath ), "%s/STATS/GLOBALS/.GLOBAL.RES.crap" %( crappath ))
		except:
			Path("%s/STATS/GLOBALS/.GLOBAL.RES.crap" %( crappath )).touch()
		
		try:
			os.rename("%s/STATS/GLOBALS/GLOBAL.UA.crapstats" %( crappath ), "%s/STATS/GLOBALS/.GLOBAL.UA.crap" %( crappath ))
		except:
			Path("%s/STATS/GLOBALS/.GLOBAL.UA.crap" %( crappath )).touch()

	if ErrorLogs:
		try:
			os.rename("%s/STATS/GLOBALS/GLOBAL.LEV.crapstats" %( crappath ), "%s/STATS/GLOBALS/.GLOBAL.LEV.crap" %( crappath ))
		except:
			Path("%s/STATS/GLOBALS/.GLOBAL.LEV.crap" %( crappath )).touch()
		
		try:
			os.rename("%s/STATS/GLOBALS/GLOBAL.ERR.crapstats" %( crappath ), "%s/STATS/GLOBALS/.GLOBAL.ERR.crap" %( crappath ))
		except:
			Path("%s/STATS/GLOBALS/.GLOBAL.ERR.crap" %( crappath )).touch()

	Glob.Access( AccessLogs )
	Glob.Error( ErrorLogs )
	if not LessOutput:
		print("Done\n")
		time.sleep(1)
	else:
		print()

	if not LessOutput:
		print("GLOBAL statistics updated:")
		if AccessLogs:
				print("\033[0m- \033[32mGLOBAL.IP\033[90m.crapstats\033[0m\n- \033[32mGLOBAL.REQ\033[90m.crapstats\033[0m\n- \033[32mGLOBAL.RES\033[90m.crapstats\033[0m\n- \033[32mGLOBAL.UA\033[90m.crapstats\033[0m")
		if ErrorLogs:
				print("\033[0m- \033[32mGLOBAL.LEV\033[90m.crapstats\033[0m\n- \033[32mGLOBAL.ERR\033[90m.crapstats\033[0m")
		if AccessLogs or ErrorLogs:
			print()
			time.sleep(2)


# MOVING NEWLY CREATED FILES
if not GlobalsOnly:

	# SETTING YESTERDAY'S DATE
	day = datetime.now().day - 1
	if day < 1:
		# YESTERDAY WAS THE LAST DAY OF THE PREVIOUS MONTH
		month = datetime.now().month - 1
		if month < 1:
			# YESTERDAY WAS THE LAST DAY OF THE LAST MONTH OF THE PREVIOUS YEAR
			day		= 31
			month	= 12
			year	= datetime.now().year - 1
		else:
			year	= datetime.now().year
			if month in [1,3,5,7,8,10]:
				day	= 31
			elif month in [4,6,9,11]:
				day = 30
			else:
				if (year % 4) == 0:
					day = 29
				else:
					day = 28
	else:
		month	= datetime.now().month
		year	= datetime.now().year

	if day < 10:
		day = "0%s" %( day )
	if month < 10:
		month = "0%s" %( month )
	DateDir = "%s/STATS/%s/%s/%s" %( crappath, year, month, day )
	print("\033[92mPreparing to move files\033[0m ...")
	print("\033[36mDestination\033[0m: \033[96m%s/\033[0m" %( DateDir ))
	time.sleep(2)

	if os.path.exists(DateDir):
		if AutoDelete and not LessOutput:
			print("\n\033[93mRemoving conflict files\033[0m ...\n")
		elif not LessOutput:
			print("DIRECTORY ALREADY EXIST!\n")
		else:
			print()
		time.sleep(1)

		if CleanAccessLogs:
			if AutoDelete:				
				if os.path.exists("%s/CLEAN.access.log" %( DateDir )):
					if Trash:
						subprocess.run(["mv", "%s/CLEAN.access.log" %( DateDir ), TrashPath ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
					elif Shred:
						subprocess.run(["shred", "-uvz", "%s/CLEAN.access.log" %( DateDir )], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
					else:
						subprocess.run(["rm", "%s/CLEAN.access.log" %( DateDir )], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
			
			else:
				if os.path.exists("%s/CLEAN.access.log" %( DateDir )):
					print("\033[92mTrying to move CLEAN ACCESS LOGs file\033[0m ...")
					time.sleep(1)
					print("\n!!! \033[31mWARNING\033[0m !!!")
					print("Conflict file detected:")
					print("- \033[91mCLEAN.access\033[90m.log\033[0m")
					if not LessOutput:
						print("\nThis file is the result of your last invocation of CRAPLOG\nIf CRAPLOG succesfully completed the last job, you may need it\nPlease check this file and make sure you don't need it before to procede")
					if not Trash:
						print("\nEVERY DELETED FILE WILL BE LOST FOREVER AND NOT RECOVERABLE!")
						delete = input("Delete listed file? [Y/n] : ")
					else:
						delete = input("\nMove listed file to Trash? [Y/n] : ")
					
					if delete == "y" or delete == "Y":
						print("\n\033[91mRemoving conflict file\033[0m ...")
						if Trash:
							subprocess.run(["mv", "%s/CLEAN.access.log" %( DateDir ), TrashPath ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
						elif Shred:
							subprocess.run(["shred", "-uvz", "%s/CLEAN.access.log" %( DateDir )], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
						else:
							subprocess.run(["rm", "%s/CLEAN.access.log" %( DateDir )], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
						
					else:
						print("\nCRAPLOG ABORTED\n")
						exit()
					
			print("\033[92mMoving CLEAN ACCESS LOGs file\033[0m ...")
			subprocess.run(["mv", "%s/STATS/CLEAN.access.log" %( crappath ), "%s/" %( DateDir )], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
			if not LessOutput:
				print("Done\n")
				time.sleep(1)
			else:
				print()
		
		if AccessLogs:
			if os.path.exists("%s/ACCESS/" %( DateDir )):
				FilesList		= []
				ConflictFiles	= []
				for (path, dirs, files) in os.walk("%s/ACCESS/" %( DateDir )):
					FilesList.extend(files)
					break
				if len(FilesList) > 0:
					for File in FilesList:
						if File.endswith(".crapstats"):
							ConflictFiles.append(File)
			
				if len(ConflictFiles) > 0:
					if AutoDelete:
						for File in ConflictFiles:
							if Trash:
								subprocess.run(["mv", "%s/ACCESS/%s" %( DateDir, File ), TrashPath ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
							elif Shred:
								subprocess.run(["shred", "-uvz", "%s/ACCESS/%s" %( DateDir, File )], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
							else:
								subprocess.run(["rm", "%s/ACCESS/%s" %( DateDir, File )], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
					
					else:
						print("\033[92mTrying to move ACCESS LOGs files ...\033[0m")
						time.sleep(1)
						print("\n!!! \033[31mWARNING\033[0m !!!")
						print("Conflict files detected:")
						for File in ConflictFiles:
							print("- \033[91m%s\033[0m" %( File.replace(".crapstats", "\033[90m.crapstats") ))
						if not LessOutput:
							print("\nThese files are the result of your last invocation of CRAPLOG\nIf CRAPLOG succesfully completed the last job, you may need them\nPlease check these files and make sure you don't need them before to procede")
						if not Trash:
							print("\nEVERY DELETED FILE WILL BE LOST FOREVER AND NOT RECOVERABLE!")
							delete = input("Delete listed files? [Y/n] : ")
						else:
							delete = input("\nMove listed files to Trash? [Y/n] : ")
						
						if delete == "y" or delete == "Y":
							print("\n\033[91mRemoving conflict files\033[0m ...")
							for File in ConflictFiles:
								if Trash:
									subprocess.run(["mv", "%s/ACCESS/%s" %( DateDir, File ), TrashPath ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
								elif Shred:
									subprocess.run(["shred", "-uvz", "%s/ACCESS/%s" %( DateDir, File )], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
								else:
									subprocess.run(["rm", "%s/ACCESS/%s" %( DateDir, File )], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
							
						else:
							print("\nCRAPLOG ABORTED\n")
							exit()
				
			else:
				Path("%s/ACCESS" %( DateDir )).mkdir(parents=True, exist_ok=True)

			print("\033[92mMoving ACCESS LOGs files\033[0m ...")
			subprocess.run(["mv", "%s/STATS/IP.crapstats" %( crappath ), "%s/ACCESS/" %( DateDir )], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
			subprocess.run(["mv", "%s/STATS/REQ.crapstats" %( crappath ), "%s/ACCESS/" %( DateDir )], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
			subprocess.run(["mv", "%s/STATS/RES.crapstats" %( crappath ), "%s/ACCESS/" %( DateDir )], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
			subprocess.run(["mv", "%s/STATS/UA.crapstats" %( crappath ), "%s/ACCESS/" %( DateDir )], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
			if not LessOutput:
				print("Done\n")
				time.sleep(1)
			else:
				print()

		if ErrorLogs:
			if os.path.exists("%s/ERROR/" %( DateDir )):
				FilesList		= []
				ConflictFiles	= []
				for (path, dirs, files) in os.walk("%s/ERROR/" %( DateDir )):
					FilesList.extend(files)
					break
				if len(FilesList) > 0:
					for File in FilesList:
						if File.endswith(".crapstats"):
							ConflictFiles.append(File)
			
				if len(FilesList) > 0:
					if AutoDelete:
						
						for File in ConflictFiles:
							if Trash:
								subprocess.run(["mv", "%s/ERROR/%s" %( DateDir, File ), TrashPath ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
							elif Shred:
								subprocess.run(["shred", "-uvz", "%s/ERROR/%s" %( DateDir, File )], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
							else:
								subprocess.run(["rm", "%s/ERROR/%s" %( DateDir, File )], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
					
					else:
						print("\033[92mTrying to move ERROR LOGs files ...\033[0m")
						time.sleep(1)
						print("\n!!! \033[31mWARNING\033[0m !!!")
						print("Conflict files detected:")
						for File in ConflictFiles:
							print("- \033[91m%s\033[0m" %( File.replace(".crapstats", "\033[90m.crapstats") ))
						if not LessOutput:
							print("\nThese files are the result of your last invocation of CRAPLOG\nIf CRAPLOG succesfully completed the last job, you may need them\nPlease check these files and make sure you don't need them before to procede")
						if not Trash:
							print("\nEVERY DELETED FILE WILL BE LOST FOREVER AND NOT RECOVERABLE!")
							delete = input("Delete listed files? [Y/n] : ")
						else:
							delete = input("\nMove listed files to Trash? [Y/n] : ")
						if delete == "y" or delete == "Y":
							print("\n\033[91mRemoving conflict files\033[0m ...")
							time.sleep(1)
							for File in ConflictFiles:
								if Trash:
									subprocess.run(["mv", "%s/ERROR/%s" %( DateDir, File ), TrashPath ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
								elif Shred:
									subprocess.run(["shred", "-uvz", "%s/ERROR/%s" %( DateDir, File )], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
								else:
									subprocess.run(["rm", "%s/ERROR/%s" %( DateDir, File )], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
							
						else:
							print("\nCRAPLOG ABORTED\n")
							exit()
				
			else:
				Path("%s/ERROR" %( DateDir )).mkdir(parents=True, exist_ok=True)

			print("\033[92mMoving ERROR LOGs files\033[0m ...")
			subprocess.run(["mv", "%s/STATS/ERR.crapstats" %( crappath ), "%s/ERROR/" %( DateDir )], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
			subprocess.run(["mv", "%s/STATS/LEV.crapstats" %( crappath ), "%s/ERROR/" %( DateDir )], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
			if not LessOutput:
				print("Done\n")
				time.sleep(1)
			else:
				print()

	else:
		print("\033[92mCreating directory\033[0m ...")
		time.sleep(1)
		Path("%s" %( DateDir )).mkdir(parents=True, exist_ok=True)
		print("\033[92mMoving SESSION files\033[0m ...")
		time.sleep(1)

		if CleanAccessLogs:
			subprocess.run(["mv", "%s/STATS/CLEAN.access.log" %( crappath ), "%s/" %( DateDir )], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
		
		if AccessLogs:
			Path("%s/ACCESS" %( DateDir )).mkdir(parents=True, exist_ok=True)
			subprocess.run(["mv", "%s/STATS/IP.crapstats" %( crappath ), "%s/ACCESS/" %( DateDir )], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
			subprocess.run(["mv", "%s/STATS/REQ.crapstats" %( crappath ), "%s/ACCESS/" %( DateDir )], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
			subprocess.run(["mv", "%s/STATS/RES.crapstats" %( crappath ), "%s/ACCESS/" %( DateDir )], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
			subprocess.run(["mv", "%s/STATS/UA.crapstats" %( crappath ), "%s/ACCESS/" %( DateDir )], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
		
		if ErrorLogs:
			Path("%s/ERROR" %( DateDir )).mkdir(parents=True, exist_ok=True)
			subprocess.run(["mv", "%s/STATS/ERR.crapstats" %( crappath ), "%s/ERROR/" %( DateDir )], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
			subprocess.run(["mv", "%s/STATS/LEV.crapstats" %( crappath ), "%s/ERROR/" %( DateDir )], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
		
		if not LessOutput:
			print("Done\n")
			time.sleep(1)
		else:
			print()


# CREATING BACKUP OF ORIGINAL LOG FILES
if Backup:
	if AutoDelete:
		if os.path.exists("%s/BACKUP.tar.gz" %( DateDir )):
			if Trash:
				subprocess.run(["mv", "%s/BACKUP.tar.gz" %( DateDir ), TrashPath ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
			elif Shred:
				subprocess.run(["shred", "-uvz", "%s/BACKUP.tar.gz" %( DateDir )], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
			else:
				subprocess.run(["rm", "%s/BACKUP.tar.gz" %( DateDir )], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
		
		if os.path.exists("%s/access.log" %( DateDir )):
			if Trash:
				subprocess.run(["mv", "%s/access.log" %( DateDir ), TrashPath ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
			elif Shred:
				subprocess.run(["shred", "-uvz", "%s/access.log" %( DateDir )], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
			else:
				subprocess.run(["rm", "%s/access.log" %( DateDir )], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

		if os.path.exists("%s/error.log" %( DateDir )):
			if Trash:
				subprocess.run(["mv", "%s/error.log" %( DateDir ), TrashPath ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
			elif Shred:
				subprocess.run(["shred", "-uvz", "%s/error.log" %( DateDir )], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
			else:
				subprocess.run(["rm", "%s/error.log" %( DateDir )], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

	else:
		print("\033[92mTrying to create BACKUP archive ...\033[0m")
		time.sleep(1)
		if os.path.exists("%s/BACKUP.tar.gz" %( DateDir )) or os.path.exists("%s/access.log" %( DateDir )) or os.path.exists("%s/error.log" %( DateDir )):
			print("\n!!! \033[31mWARNING\033[0m !!!")
			print("Conflict files detected:")
			
			if os.path.exists("%s/BACKUP.tar.gz" %( DateDir )):
					print("- \033[91mBACKUP.tar.gz\033[0m")
			
			if os.path.exists("%s/access.log" %( DateDir )):
					print("- \033[93maccess.log\033[0m")
			
			if os.path.exists("%s/error.log" %( DateDir )):
					print("- \033[93merror.log\033[0m")
			
			if not LessOutput:
				if os.path.exists("%s/access.log" %( DateDir )) or os.path.exists("%s/error.log" %( DateDir )):
					print("\nFiles in \033[93mYELLOW\033[0m are the result of your last invocation of CRAPLOG, aborted before the end\nBecause of that, you should consider to delete them", end="")
				print("\nPlease check these files and make sure you don't need them before to procede")
			if not Trash:
				print("\nEVERY DELETED FILE WILL BE LOST FOREVER AND NOT RECOVERABLE!")
				delete = input("Delete conflict files? [Y/n] : ")
			else:
				delete = input("\nMove conflict files to Trash? [Y/n] : ")
			
			if delete == "y" or delete == "Y":
				print("\n\033[91mRemoving conflict files\033[0m ...")
				time.sleep(1)
				if os.path.exists("%s/BACKUP.tar.gz" %( DateDir )):
					if Trash:
						subprocess.run(["mv", "%s/BACKUP.tar.gz" %( DateDir ), TrashPath ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
					elif Shred:
						subprocess.run(["shred", "-uvz", "%s/BACKUP.tar.gz" %( DateDir )], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
					else:
						subprocess.run(["rm", "%s/BACKUP.tar.gz" %( DateDir )], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
				
				if os.path.exists("%s/access.log" %( DateDir )):
					if Trash:
						subprocess.run(["mv", "%s/access.log" %( DateDir ), TrashPath ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
					elif Shred:
						subprocess.run(["shred", "-uvz", "%s/access.log" %( DateDir )], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
					else:
						subprocess.run(["rm", "%s/access.log" %( DateDir )], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

				if os.path.exists("%s/error.log" %( DateDir )):
					if Trash:
						subprocess.run(["mv", "%s/error.log" %( DateDir ), TrashPath ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
					elif Shred:
						subprocess.run(["shred", "-uvz", "%s/error.log" %( DateDir )], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
					else:
						subprocess.run(["rm", "%s/error.log" %( DateDir )], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
			
			else:
				print("\nCRAPLOG ABORTED\n")
				exit()

	print("\033[92mCreating BACKUP archive\033[0m ...")
	subprocess.run(["cp", "/var/log/apache2/access.log.1", "%s/access.log" %( DateDir )], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
	subprocess.run(["cp", "/var/log/apache2/error.log.1", "%s/error.log" %( DateDir )], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

	os.chdir("%s" %( DateDir ) )
	subprocess.run(["tar", "-czf", "BACKUP.tar.gz", "access.log", "error.log"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

	if Trash:
		subprocess.run(["mv", "%s/access.log" %( DateDir ), TrashPath ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
		subprocess.run(["mv", "%s/error.log" %( DateDir ), TrashPath ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
	elif Shred:
		subprocess.run(["shred", "-uvz", "%s/access.log" %( DateDir ), "%s/error.log" %( DateDir )], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
	else:
		subprocess.run(["rm", "%s/access.log" %( DateDir ), "%s/error.log" %( DateDir )], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

	if not LessOutput:
		print("Done\n")
		time.sleep(1)
	else:
		print()

	# DELETING ORIGINAL LOG FILES
	if BackupDelete:
		# TRYING TO UNDERSTAND IF SUDO IS REQUIRED
		needSUDO = 0
		try:
			subprocess.run(["touch", "/var/log/apache2/CraplogCheckingSUDO"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
			subprocess.run(["rm", "/var/log/apache2/CraplogCheckingSUDO"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
		except:
			needSUDO = 1
			while True:
				print("\n\033[92mPreparing to remove ORIGINAL LOG files\033[0m ...")
				time.sleep(1)
				print("SUDO is required to delete ORIGINAL LOG files inside \033[93m/var/log/apache2/\033[0m\nIf you choose '\033[1mN\033[0m', the next step will be skipped")
				delete = input("Do you want to proceed? [Y/n] : ")
				if delete == "y":
					print("\nPlease answer using \033[1mUPPERCASE\033[0m 'Y'\n")
					time.sleep(3)
				elif delete == "Y":
					proceed = 1
					break
				elif delete == "N" or delete == "n":
					proceed = 0
					break
				else:
					print("\nYour choice is not valid\n")
					time.sleep(2)
		
		if proceed:
			if AutoDelete:
				print("\n\033[93mRemoving ORIGINAL LOG files\033[0m ...")
				
				if needSUDO:
					if Trash:
						subprocess.run(["sudo", "mv", "/var/log/apache2/access.log.1", TrashPath ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
						subprocess.run(["sudo", "mv", "/var/log/apache2/error.log.1", TrashPath ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
					elif Shred:
						subprocess.run(["sudo", "shred", "-uvz", "/var/log/apache2/access.log", "/var/log/apache2/error.log"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
					else:
						subprocess.run(["sudo", "rm", "/var/log/apache2/access.log", "/var/log/apache2/error.log"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
				else:
					if Trash:
						subprocess.run(["mv", "/var/log/apache2/access.log.1", TrashPath ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
						subprocess.run(["mv", "/var/log/apache2/error.log.1", TrashPath ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
					elif Shred:
						subprocess.run(["shred", "-uvz", "/var/log/apache2/access.log", "/var/log/apache2/error.log"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
					else:
						subprocess.run(["rm", "/var/log/apache2/access.log", "/var/log/apache2/error.log"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
			
			else:
				if not LessOutput:
					print("\n\033[1mPlease ensure the archive has been created correctly before to proceed\033[0m")
				if not Trash:
					print("\nEVERY DELETED FILE WILL BE LOST FOREVER AND NOT RECOVERABLE!")
					delete = input("Delete ORIGINAL files? [Y/n] : ")
				else:
					delete = input("\nMove ORIGINAL files to Trash? [Y/n] : ")
				if delete == "y" or delete == "Y":
					print("\n\033[91mRemoving original files\033[0m ...")
					time.sleep(1)
					if needSUDO:
						if Trash:
							subprocess.run(["sudo", "mv", "/var/log/apache2/access.log.1", TrashPath ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
							subprocess.run(["sudo", "mv", "/var/log/apache2/error.log.1", TrashPath ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
						elif Shred:
							subprocess.run(["sudo", "shred", "-uvz", "/var/log/apache2/access.log", "/var/log/apache2/error.log"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
						else:
							subprocess.run(["sudo", "rm", "/var/log/apache2/access.log", "/var/log/apache2/error.log"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
					else:
						if Trash:
							subprocess.run(["mv", "/var/log/apache2/access.log.1", TrashPath ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
							subprocess.run(["mv", "/var/log/apache2/error.log.1", TrashPath ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
						elif Shred:
							subprocess.run(["shred", "-uvz", "/var/log/apache2/access.log", "/var/log/apache2/error.log"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
						else:
							subprocess.run(["rm", "/var/log/apache2/access.log", "/var/log/apache2/error.log"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
				else:
					print("\nCRAPLOG ABORTED\n")
					exit()
			
			if not LessOutput:
				print("Done\n")
				time.sleep(1)
			else:
				print()
		else:
			print("Skipping ...\n")
			time.sleep(1)


# REMOVING TEMPORARY FILES
print("\033[92mRemoving temporary files\033[0m ...")

TempFiles	= []
FilesList	= []
for (path, dirs, files) in os.walk("%s/STATS/" %( crappath )):
	FilesList.extend(files)
	break
if len(FilesList) > 0:
	for File in FilesList:
		if File.endswith(".crap") or File.endswith(".crapstats"):
			TempFiles.append(File)

FilesList	= []
for (path, dirs, files) in os.walk("%s/STATS/GLOBALS/" %( crappath )):
	FilesList.extend(files)
	break
if len(FilesList) > 0:
	for File in FilesList:
		if File.startswith(".GLOBAL.") and File.endswith(".crap"):
			TempFiles.append("GLOBALS/%s" %( File ))

if len(TempFiles) > 0:
	for File in TempFiles:
		if Trash:
			subprocess.run(["mv", "%s/STATS/%s" %( crappath, File ), TrashPath ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
		elif Shred:
			subprocess.run(["shred", "-uvz", "%s/STATS/%s" %( crappath, File )], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
		else:
			subprocess.run(["rm", "%s/STATS/%s" %( crappath, File )], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)


# UPDATING GOLBALS' BACKUPS
if not os.path.exists("%s/STATS/GLOBALS/.BACKUPS" %( crappath )):
	Path("%s/STATS/GLOBALS/.BACKUPS" %( crappath )).mkdir(parents=True, exist_ok=True)
	with open("%s/STATS/GLOBALS/.BACKUPS/.last_time" %( crappath ), "w") as file:
		file.write(str(0))

if not os.path.exists("%s/STATS/GLOBALS/.BACKUPS/.last_time" %( crappath )):
	with open("%s/STATS/GLOBALS/.BACKUPS/.last_time" %( crappath ), "w") as file:
		file.write(str( 7 ))

if not os.path.exists("%s/STATS/GLOBALS/.BACKUPS/TMP" %( crappath )):
	Path("%s/STATS/GLOBALS/.BACKUPS/TMP" %( crappath )).mkdir(parents=True, exist_ok=True)

for dirname in [1,2,3,4,5,6,7]:
	if not os.path.exists("%s/STATS/GLOBALS/.BACKUPS/%s" %( crappath, dirname )):
		Path("%s/STATS/GLOBALS/.BACKUPS/%s" %( crappath, dirname )).mkdir(parents=True, exist_ok=True)

# GETTING BACKUP'S LAST-TIME VALUE
with open("%s/STATS/GLOBALS/.BACKUPS/.last_time" %( crappath ), "r") as file:
	LastGlobalsBackup = int(file.read().strip())

if LastGlobalsBackup < 7:
	# INCRASING BACKUP'S LAST-TIME VALUE
	with open("%s/STATS/GLOBALS/.BACKUPS/.last_time" %( crappath ), "w") as file:
		file.write(str( LastGlobalsBackup + 1 ))

else:
	# COPYING ACTUAL GLOBALS TO 'TMP' FOLDER
	FilesList = []
	for (path, dirs, files) in os.walk("%s/STATS/GLOBALS/" %( crappath )):
		FilesList.extend(files)
		break
	if len(FilesList) > 0:
		for File in FilesList:
			if File.endswith(".crapstats"):
				subprocess.run(["cp", "%s/STATS/GLOBALS/%s" %( crappath, File ), "%s/STATS/GLOBALS/.BACKUPS/TMP/" %( crappath )], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
	# SWITCHING BACKUPS FOLDERS' NAMES
	subprocess.run(["rm", "-r", "%s/STATS/GLOBALS/.BACKUPS/1" %( crappath )], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
	os.rename("%s/STATS/GLOBALS/.BACKUPS/2" %( crappath ), "%s/STATS/GLOBALS/.BACKUPS/1" %( crappath ))
	os.rename("%s/STATS/GLOBALS/.BACKUPS/3" %( crappath ), "%s/STATS/GLOBALS/.BACKUPS/2" %( crappath ))
	os.rename("%s/STATS/GLOBALS/.BACKUPS/4" %( crappath ), "%s/STATS/GLOBALS/.BACKUPS/3" %( crappath ))
	os.rename("%s/STATS/GLOBALS/.BACKUPS/5" %( crappath ), "%s/STATS/GLOBALS/.BACKUPS/4" %( crappath ))
	os.rename("%s/STATS/GLOBALS/.BACKUPS/6" %( crappath ), "%s/STATS/GLOBALS/.BACKUPS/5" %( crappath ))
	os.rename("%s/STATS/GLOBALS/.BACKUPS/7" %( crappath ), "%s/STATS/GLOBALS/.BACKUPS/6" %( crappath ))
	os.rename("%s/STATS/GLOBALS/.BACKUPS/TMP" %( crappath ), "%s/STATS/GLOBALS/.BACKUPS/7" %( crappath ))
	# RESETTING BACKUPS' LAST-TIME
	with open("%s/STATS/GLOBALS/.BACKUPS/.last_time" %( crappath ), "w") as file:
		file.write(str( 0 ))

if not LessOutput:
	print("Done\n\n")
else:
	print("\n")

# CRAPLOG HAS DONE HIS JOB
print("\033[1m\
   \033[33mFFFFF  \033[32mII  \033[36mN   N\n\
   \033[33mF      \033[32mII  \033[36mNN  N\n\
   \033[33mFFF    \033[32mII  \033[36mN N N\n\
   \033[33mF      \033[32mII  \033[36mN  NN\n\
   \033[33mF      \033[32mII  \033[36mN   N\n\n\033[0m")
# GIVING TIME TO INSPECT STDOUT TO THE USER
input("\033[90mPress any key to continue ...\033[0m\n")
