#define AppName "Battery Alert"
#define AppVersion "1.0.0"

[Setup]
AppId={{B1A2F0C1-A6D4-4B5B-92F0-318B6E8D7124}
AppName={#AppName}
AppVersion={#AppVersion}
DefaultDirName={localappdata}\Programs\Battery Alert
DefaultGroupName={#AppName}
DisableProgramGroupPage=yes
PrivilegesRequired=lowest
OutputDir=dist\installer
OutputBaseFilename=BatteryAlert-Setup
SetupIconFile=battery_alert.ico
UninstallDisplayIcon={app}\BatteryAlert.exe
WizardStyle=modern
Compression=lzma2
SolidCompression=yes

[Files]
Source: "dist\BatteryAlert.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{autoprograms}\Battery Alert"; Filename: "{app}\BatteryAlert.exe"
Name: "{autodesktop}\Battery Alert"; Filename: "{app}\BatteryAlert.exe"

[Registry]
Root: HKCU; Subkey: "Software\Microsoft\Windows\CurrentVersion\Run"; ValueName: "Battery Alert"; ValueType: string; ValueData: """{app}\BatteryAlert.exe"""; Flags: uninsdeletevalue

[Run]
Filename: "{app}\BatteryAlert.exe"; Description: "Launch Battery Alert now"; Flags: postinstall nowait skipifsilent
