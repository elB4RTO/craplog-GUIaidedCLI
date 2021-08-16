#!/usr/bin/python3

import tkinter as tk
from tkinter import ttk

import subprocess
import os
import time

Terminals			= []
PossibleTerminals	= [
	"xterm",
	"uxterm",
	"gnome-terminal",
	"konsole",
	"mate-terminal",
	"xfce4-terminal",
	"Terminal",
	"sakura",
	"terminator",
	"roxterm"
	]

for term in PossibleTerminals:
	if os.path.isfile("/usr/bin/%s" %term) == True:
		Terminals.append(term)


window = tk.Tk()

terminal			= tk.StringVar(value=Terminals[0])

LessOutput			= tk.IntVar(value=0)
CleanAccessLogs		= tk.IntVar(value=0)
AccessLogs			= tk.IntVar(value=1)
ErrorLogs			= tk.IntVar(value=0)
ErrorsOnly			= tk.IntVar(value=0)
GlobalsOnly			= tk.IntVar(value=0)
GlobalsAvoid		= tk.IntVar(value=0)
Backup				= tk.IntVar(value=0)
BackupDelete		= tk.IntVar(value=0)
AutoDelete			= tk.IntVar(value=0)
Trash				= tk.IntVar(value=0)
Shred				= tk.IntVar(value=0)

Remember			= tk.IntVar(value=0)
FallbackClean		= CleanAccessLogs.get()
FallbackErrors		= ErrorLogs.get()

def error_NoConfig():
	subwin = tk.Tk()
	subwin.title("Error")
	tk.Label(
		master = subwin,
		text = "CONFIGURATIONS FILE NOT FOUND OR INVALID",
		foreground = "black",
		background = "red",
		width = 50,
		height = 3
	).pack()

def error_Writing():
	subwin = tk.Tk()
	subwin.title("Error")
	tk.Label(
		master = subwin,
		text = "UNABLE TO WRITE CONFIGURATIONS FILE",
		foreground = "black",
		background = "red",
		width = 50,
		height = 3
	).pack(fill=BOTH)

def done_Writing():
	subwin = tk.Tk()
	subwin.title("Done")
	tk.Label(
		master = subwin,
		text = "CONFIGURATIONS FILE HAS BEEN WRITTEN SUCCESFULLY",
		foreground = "white",
		background = "green",
		width = 50,
		height = 3
	).pack()

def ReadConfigs():
	global FallbackClean, FallbackErrors
	try:
		file = open("./config/CONFIG", "r")
		configs = file.read()
		file.close
		configs = configs.split('\n')

		terminal.set(			str(configs[0]))
		LessOutput.set(			int(configs[1]))
		CleanAccessLogs.set(	int(configs[2]))
		AccessLogs.set(			int(configs[3]))
		ErrorLogs.set(			int(configs[4]))
		ErrorsOnly.set(			int(configs[5]))
		GlobalsOnly.set(		int(configs[6]))
		GlobalsAvoid.set(		int(configs[7]))
		Backup.set(				int(configs[8]))
		BackupDelete.set(		int(configs[9]))
		AutoDelete.set(			int(configs[10]))
		Trash.set(				int(configs[11]))
		Shred.set(				int(configs[12]))

		FallbackClean	= CleanAccessLogs.get()
		FallbackErrors	= ErrorLogs.get()
	except:
		window.after(1000, error_NoConfig)

def WriteConfigs():
	try:
		configs = str("%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s" %(
			terminal.get(),
			LessOutput.get(),
			CleanAccessLogs.get(),
			AccessLogs.get(),
			ErrorLogs.get(),
			ErrorsOnly.get(),
			GlobalsOnly.get(),
			GlobalsAvoid.get(),
			Backup.get(),
			BackupDelete.get(),
			AutoDelete.get(),
			Trash.get(),
			Shred.get()
		))
		file = open("./config/CONFIG", "w")
		file.write(configs)
		file.close()
		window.after(100, done_Writing)
	except:
		window.after(100, error_Writing)

def LockAll():
	button_START.config(		state="disabled")
	check_LESS.config(			state="disabled")
	check_ERRORS.config(		state="disabled")
	check_ERRORSONLY.config(	state="disabled")
	check_CLEAN.config(			state="disabled")
	check_GLOBONLY.config(		state="disabled")
	check_GLOBAVOID.config(		state="disabled")
	check_BACKUP.config(		state="disabled")
	check_BACKDEL.config(		state="disabled")
	check_AUTODEL.config(		state="disabled")
	check_SHRED.config(			state="disabled")
	button_HELP.config(			state="disabled")
	menu_TERM.config(			state="disabled")
	button_REMEMBER.config(		state="disabled")
	window.after(100,StartCRAPLOG)

def UnlockAll():
	button_START.config(		state="normal")
	check_LESS.config(			state="normal")
	check_ERRORS.config(		state="normal")
	check_ERRORSONLY.config(	state="normal")
	check_CLEAN.config(			state="normal")
	check_GLOBONLY.config(		state="normal")
	check_GLOBAVOID.config(		state="normal")
	check_BACKUP.config(		state="normal")
	check_BACKDEL.config(		state="normal")
	check_AUTODEL.config(		state="normal")
	check_SHRED.config(			state="normal")
	button_HELP.config(			state="normal")
	menu_TERM.config(			state="normal")
	button_REMEMBER.config(		state="normal")

def StartCRAPLOG():
	crap = "./craplog.sh"
	if LessOutput.get() == 1:
		crap += " --less"
	if CleanAccessLogs.get() == 1:
		crap += " --clean"
	if ErrorLogs.get() == 1:
		crap += " --errors"
	if ErrorsOnly.get() == 1:
		crap += " --only-errors"
	if GlobalsOnly.get() == 1:
		crap += " --only-globals"
	if GlobalsAvoid.get() == 1:
		crap += " --avoid-globals"
	if Backup.get() == 1:
		crap += " --backup"
	if BackupDelete.get() == 1:
		crap += " --backup+delete"
	if AutoDelete.get() == 1:
		crap += " --auto-delete"
	if Trash.get() == 1:
		crap += " --trash"
	if Shred.get() == 1:
		crap += " --shred"

	crapSTART = subprocess.Popen("%s -e '%s'" %(terminal.get(), crap), shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	crapSTART.wait()
	window.after(500,UnlockAll)


def getHelp():
	if terminal.get() == "konsole":
		subprocess.Popen("%s -e './aux/help.sh'" %(terminal.get()), shell=True)
	else:
		subprocess.Popen("%s -e 'cat ./aux/elbarto.txt ./aux/craplogo.txt ./aux/help.txt | less'" %(terminal.get()), shell=True)

def manage_Terminal():
	menu_TERM.config(text=terminal.get())

def manage_ErrOnly():
	global FallbackClean, FallbackErrors
	value = ErrorsOnly.get()
	if value == 1:
		FallbackClean = CleanAccessLogs.get()
		CleanAccessLogs.set(0)
		check_CLEAN["state"] = "disabled"
		AccessLogs.set(0)
		FallbackErrors = ErrorLogs.get()
		ErrorLogs.set(1)
		check_ERRORS["state"] = "disabled"
	else:
		CleanAccessLogs.set(FallbackClean)
		check_CLEAN["state"] = "normal"
		AccessLogs.set(1)
		ErrorLogs.set(FallbackErrors)
		check_ERRORS["state"] = "normal"

def manage_GlobOnly():
	value = GlobalsOnly.get()
	if value == 1:
		GlobalsAvoid.set(0)
		check_GLOBAVOID["state"] = "disabled"
	else:
		check_GLOBAVOID["state"] = "normal"

def manage_GlobAvoid():
	value = GlobalsAvoid.get()
	if value == 1:
		GlobalsOnly.set(0)
		check_GLOBONLY["state"] = "disabled"
	else:
		check_GLOBONLY["state"] = "normal"

def manage_Backup():
	value = Backup.get()
	if value == 1:
		check_BACKDEL["state"] = "normal"
	else:
		BackupDelete.set(0)
		check_BACKDEL["state"] = "disabled"



window.title("CRAPLOG")
window.columnconfigure(0, weight=1, minsize=300)
window.rowconfigure(0, weight=1, minsize=100)
window.rowconfigure(1, weight=1, minsize=200)
window.rowconfigure(2, weight=1, minsize=20)

main = tk.Frame(
	master = window,
	background = "#0f0f0f"
)
main.columnconfigure([0,1,2], weight=1, minsize=100)
main.rowconfigure([0], weight=1, minsize=30)

button_START = tk.Button(
	master = main,
	text="Start CRAPLOG",
	command = LockAll,
	state = "normal",
	foreground="white",
	background="black",
	borderwidth=1,
	relief=tk.GROOVE,
	height="2"
)

arguments = tk.Frame(
	master = window,
	background = "#1e1e1e"
)
arguments.columnconfigure([0,1,2], weight=1, minsize=100)
arguments.rowconfigure([0,10], weight=0, minsize=10)
arguments.rowconfigure([1,2,3,4,5,6,7,8,9], weight=0, minsize=5)

label_TITLE = tk.Label(
	master = arguments,
	text = "  ARGUMENTS",
	justify = "center",
	foreground = "#afafaf",
	background = "#1e1e1e"
)

label_OUTPUT = tk.Label(
	master = arguments,
	text = "Output Control",
	foreground = "#9a9a9a",
	background = "#1e1e1e"
)

check_LESS = tk.Checkbutton(
	master = arguments,
	variable = LessOutput,
	state = "normal",
	offvalue = 0,
	onvalue = 1,
	selectcolor = "black",
	text = "--less",
	justify = "center",
	foreground = "#FFFFFF",
	activeforeground="#FFFFFF",
	disabledforeground="#5e5e5e",
	background = "#1e1e1e",
	activebackground = "#2e2e2e",
	border = 3,
	highlightthickness = 0
)

label_FILEIN = tk.Label(
	master = arguments,
	text = "Input Files",
	foreground = "#9a9a9a",
	background = "#1e1e1e"
)

check_ACCESS = tk.Checkbutton(
	master = arguments,
	variable = AccessLogs,
	state = "disabled",
	offvalue = 0,
	onvalue = 1,
	selectcolor = "black",
	text = "--access",
	justify = "center",
	foreground = "#FFFFFF",
	activeforeground="#FFFFFF",
	disabledforeground="#5e5e5e",
	background = "#1e1e1e",
	activebackground = "#2e2e2e",
	border = 3,
	highlightthickness = 0
)

check_ERRORS = tk.Checkbutton(
	master = arguments,
	variable = ErrorLogs,
	state = "normal",
	offvalue = 0,
	onvalue = 1,
	selectcolor = "black",
	text = "--errors",
	justify = "center",
	foreground = "#FFFFFF",
	activeforeground="#FFFFFF",
	disabledforeground="#5e5e5e",
	background = "#1e1e1e",
	activebackground = "#2e2e2e",
	border = 3,
	highlightthickness = 0
)

check_ERRORSONLY = tk.Checkbutton(
	master = arguments,
	variable = ErrorsOnly,
	command = manage_ErrOnly,
	state = "normal",
	offvalue = 0,
	onvalue = 1,
	selectcolor = "black",
	text = "--only-errors",
	justify = "center",
	foreground = "#FFFFFF",
	activeforeground="#FFFFFF",
	disabledforeground="#5e5e5e",
	background = "#1e1e1e",
	activebackground = "#2e2e2e",
	border = 3,
	highlightthickness = 0
)

label_FILEOUT = tk.Label(
	master = arguments,
	text = "Output Files",
	foreground = "#9a9a9a",
	background = "#1e1e1e"
)

check_CLEAN = tk.Checkbutton(
	master = arguments,
	variable = CleanAccessLogs,
	state = "normal",
	offvalue = 0,
	onvalue = 1,
	selectcolor = "black",
	text = "--clean",
	justify = "center",
	foreground = "#FFFFFF",
	activeforeground="#FFFFFF",
	disabledforeground="#5e5e5e",
	background = "#1e1e1e",
	activebackground = "#2e2e2e",
	border = 3,
	highlightthickness = 0
)

check_GLOBONLY = tk.Checkbutton(
	master = arguments,
	variable = GlobalsOnly,
	command = manage_GlobOnly,
	state = "normal",
	offvalue = 0,
	onvalue = 1,
	selectcolor = "black",
	text = "--only-globals",
	justify = "center",
	foreground = "#FFFFFF",
	activeforeground="#FFFFFF",
	disabledforeground="#5e5e5e",
	background = "#1e1e1e",
	activebackground = "#2e2e2e",
	border = 3,
	highlightthickness = 0
)

check_GLOBAVOID = tk.Checkbutton(
	master = arguments,
	variable = GlobalsAvoid,
	command = manage_GlobAvoid,
	state = "normal",
	offvalue = 0,
	onvalue = 1,
	selectcolor = "black",
	text = "--avoid-globals",
	justify = "center",
	foreground = "#FFFFFF",
	activeforeground="#FFFFFF",
	disabledforeground="#5e5e5e",
	background = "#1e1e1e",
	activebackground = "#2e2e2e",
	border = 3,
	highlightthickness = 0
)

check_BACKUP = tk.Checkbutton(
	master = arguments,
	variable = Backup,
	command = manage_Backup,
	state = "normal",
	offvalue = 0,
	onvalue = 1,
	selectcolor = "black",
	text = "--backup",
	justify = "center",
	foreground = "#FFFFFF",
	activeforeground="#FFFFFF",
	disabledforeground="#5e5e5e",
	background = "#1e1e1e",
	activebackground = "#2e2e2e",
	border = 3,
	highlightthickness = 0
)

check_BACKDEL = tk.Checkbutton(
	master = arguments,
	variable = BackupDelete,
	state = "disabled",
	offvalue = 0,
	onvalue = 1,
	selectcolor = "black",
	text = "--backup+delete",
	justify = "center",
	foreground = "#FFFFFF",
	activeforeground="#FFFFFF",
	disabledforeground="#5e5e5e",
	background = "#1e1e1e",
	activebackground = "#2e2e2e",
	border = 3,
	highlightthickness = 0
)

label_DELETE = tk.Label(
	master = arguments,
	text = "Deletion Options",
	foreground = "#9a9a9a",
	background = "#1e1e1e"
)

check_AUTODEL = tk.Checkbutton(
	master = arguments,
	variable = AutoDelete,
	state = "normal",
	offvalue = 0,
	onvalue = 1,
	selectcolor = "black",
	text = "--auto-delete",
	justify = "center",
	foreground = "#FFFFFF",
	activeforeground="#FFFFFF",
	disabledforeground="#5e5e5e",
	background = "#1e1e1e",
	activebackground = "#2e2e2e",
	border = 3,
	highlightthickness = 0
)

check_TRASH = tk.Checkbutton(
	master = arguments,
	variable = Trash,
	state = "normal",
	offvalue = 0,
	onvalue = 1,
	selectcolor = "black",
	text = "--trash",
	justify = "center",
	foreground = "#FFFFFF",
	activeforeground="#FFFFFF",
	disabledforeground="#5e5e5e",
	background = "#1e1e1e",
	activebackground = "#2e2e2e",
	border = 3,
	highlightthickness = 0
)

check_SHRED = tk.Checkbutton(
	master = arguments,
	variable = Shred,
	state = "normal",
	offvalue = 0,
	onvalue = 1,
	selectcolor = "black",
	text = "--shred",
	justify = "center",
	foreground = "#FFFFFF",
	activeforeground="#FFFFFF",
	disabledforeground="#5e5e5e",
	background = "#1e1e1e",
	activebackground = "#2e2e2e",
	border = 3,
	highlightthickness = 0
)

button_HELP = tk.Button(
	master = arguments,
	command = getHelp,
	text = "--help",
	justify = "center",
	foreground = "#FFFFFF",
	activeforeground="#FFFFFF",
	disabledforeground="#5e5e5e",
	background = "#1e1e1e",
	activebackground = "#2e2e2e",
	border = 3,
	highlightthickness = 0
)


preferences = tk.Frame(
	master = window,
	background = "#b0b0b0"
)
preferences.columnconfigure([0,1,2], weight=1, minsize=100)
preferences.rowconfigure([0], weight=1, minsize=20)

menu_TERM = ttk.Menubutton(
	master = preferences,
	state = "normal",
	text = terminal.get(),
	width = 12
)

options_TERM = tk.Menu(
	master = menu_TERM,
	tearoff = 0
)

for term in Terminals:
	options_TERM.add_radiobutton(
		command = manage_Terminal,
		label=term,
		value=term,
		variable=terminal
	)

menu_TERM["menu"] = options_TERM

button_REMEMBER = tk.Button(
	master = preferences,
	command = WriteConfigs,
	text = "Save these settings",
	relief = "flat",
	justify = "center",
	foreground = "#000000",
	activeforeground="#FFFFFF",
	background = "#FFFFFF",
	activebackground = "#2e2eee",
	highlightthickness = 0,
	width = 15
)



ReadConfigs()
manage_ErrOnly()
manage_Backup()
manage_GlobOnly()
manage_GlobAvoid()
manage_Terminal()

main.grid(row=0, column=0, sticky="nswe")
button_START.grid(row=0, column=1, sticky="we", pady=15)

arguments.grid(row=1, column=0, sticky="nswe")
label_TITLE.grid(row=0, column=1, sticky="ns", pady=5)
label_OUTPUT.grid(row=1, column=0, sticky="w", pady=5)
check_LESS.grid(row=2, column=0, sticky="w")
label_FILEIN.grid(row=3, column=0, sticky="w", pady=5)
check_ACCESS.grid(row=4, column=0, sticky="w")
check_ERRORS.grid(row=4, column=1, sticky="w")
check_ERRORSONLY.grid(row=4, column=2, sticky="w")
label_FILEOUT.grid(row=5, column=0, sticky="w", pady=5)
check_CLEAN.grid(row=6, column=0, sticky="w")
check_GLOBONLY.grid(row=6, column=1, sticky="w")
check_GLOBAVOID.grid(row=6, column=2, sticky="w")
check_BACKUP.grid(row=7, column=0, sticky="w")
check_BACKDEL.grid(row=7, column=1, sticky="w")
label_DELETE.grid(row=8, column=0, sticky="w", pady=5)
check_AUTODEL.grid(row=9, column=0, sticky="w")
check_TRASH.grid(row=9, column=1, sticky="w")
check_SHRED.grid(row=9, column=2, sticky="w")
button_HELP.grid(row=10, column=1, sticky="we",pady=10)

preferences.grid(row=2, column=0, sticky="nswe")
menu_TERM.grid(row=0, column=0, sticky="w", padx=5, pady=5)
button_REMEMBER.grid(row=0, column=2, sticky="e", padx=3)

window.mainloop()
