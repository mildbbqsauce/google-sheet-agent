===================
Google Sheets Agent
===================

This project is a Python-based agent designed to interact with Google Sheets, for adding new rows to a specified google sheet.
It utilizes the Google Sheets API and is intended to be run locally in a virtual environment.

You can find the instructions for setting up the project here:
https://www.linkedin.com/pulse/build-ai-agent-ollama-local-model-automate-google-sheets-lisa-wang-qbtre/?trackingId=AtgusVmLSECuO4EEpIloaQ%3D%3D

Notes
-----
1. I've put placeholders in the code for the Google Sheet ID, sheet name, and client secret file. You will need to replace these with your actual Google Sheet ID, the name of the sheet you want to interact with, and the name of your Google API client secret file.

Potential Issues
----------------
When trying to activate virtual Python environment
	PS C:\Users\lisaw\Python Playground\google-sheet-agent> .\Scripts\activate
	.\Scripts\activate : File C:\Users\lisaw\Python Playground\google-sheet-agent\Scripts\Activate.ps1 cannot be loaded 
	because running scripts is disabled on this system. For more information, see about_Execution_Policies at 
	https:/go.microsoft.com/fwlink/?LinkID=135170.
	At line:1 char:1
	+ .\Scripts\activate
	+ ~~~~~~~~~~~~~~~~~~
		+ CategoryInfo          : SecurityError: (:) [], PSSecurityException
		+ FullyQualifiedErrorId : UnauthorizedAccess
Solution: 
1. Open Windows Powershell as administrator
1. Run command:
	Set-ExecutionPolicy RemoteSigned
