#define MyAppName "AVAPoint"
#define MyAppVersion "1.1"
#define MyAppPublisher "Katriel Fonseca"

[Setup]

AppId={{B8F1A6C2-8D55-4F12-9999-AVAPOINT}}

AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}

DefaultDirName=C:\AVAPoint
DefaultGroupName=AVAPoint

UsePreviousAppDir=yes
DisableDirPage=no

OutputDir=output
OutputBaseFilename=AVAPoint_Setup

Compression=lzma2
SolidCompression=yes

WizardStyle=modern

SetupIconFile=ava.ico

UninstallDisplayIcon={app}\Launcher.exe

PrivilegesRequired=admin

[Files]

Source: "Launcher.exe"; \
DestDir: "{app}"; \
Flags: ignoreversion

Source: "AVAPoint.exe"; \
DestDir: "{app}"; \
Flags: ignoreversion

Source: "AVAPointAPI.exe"; \
DestDir: "{app}"; \
Flags: ignoreversion

Source: "ava.ico"; \
DestDir: "{app}"; \
Flags: ignoreversion

Source: "evopoint.db"; \
DestDir: "{app}"; \
Flags: onlyifdoesntexist

Source: "assets\*"; \
DestDir: "{app}\assets"; \
Flags: ignoreversion recursesubdirs createallsubdirs

[Dirs]

Name: "{app}\logs"

Name: "{app}\exports"

Name: "{app}\backups"

[Icons]

Name: "{group}\AVAPoint"; \
Filename: "{app}\Launcher.exe"; \
IconFilename: "{app}\ava.ico"

Name: "{autodesktop}\AVAPoint"; \
Filename: "{app}\Launcher.exe"; \
IconFilename: "{app}\ava.ico"

[Run]

Filename: "{app}\Launcher.exe"; \
Description: "Iniciar AVAPoint"; \
Flags: nowait postinstall skipifsilent