' GUI만 실행, 터미널 창 숨김 (더블클릭 시 콘솔 안 뜸)
Set WshShell = CreateObject("WScript.Shell")
Set FSO = CreateObject("Scripting.FileSystemObject")
WshShell.CurrentDirectory = FSO.GetParentFolderName(WScript.ScriptFullName)
WshShell.Run "py -3.12 gui_main.py", 0, False
