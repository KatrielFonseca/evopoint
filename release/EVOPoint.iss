#define MyAppName "AVAPoint"
#define MyAppVersion "1.0"
#define MyAppPublisher "Katriel Fonseca"

[Setup]

AppId={{B8F1A6C2-8D55-4F12-9999-EVOPOINTV2}}

AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}

DefaultDirName=C:\EVOPoint
DefaultGroupName=EVOPoint

UsePreviousAppDir=yes

DisableDirPage=no

OutputDir=output
OutputBaseFilename=EVOPoint_Setup

Compression=lzma
SolidCompression=yes

WizardStyle=modern

SetupIconFile=evopoint.ico

UninstallDisplayIcon={app}\Launcher.exe

[Files]

Source: "Launcher.exe"; \
DestDir: "{app}"; \
Flags: ignoreversion

Source: "EVOPoint.exe"; \
DestDir: "{app}"; \
Flags: ignoreversion

Source: "EVOPointAPI.exe"; \
DestDir: "{app}"; \
Flags: ignoreversion

Source: "evopoint.ico"; \
DestDir: "{app}"; \
Flags: ignoreversion

Source: "evopoint.db"; \
DestDir: "{app}"; \
Flags: onlyifdoesntexist

[Icons]

Name: "{group}\EVOPoint"; \
Filename: "{app}\Launcher.exe"; \
IconFilename: "{app}\evopoint.ico"

Name: "{autodesktop}\EVOPoint"; \
Filename: "{app}\Launcher.exe"; \
IconFilename: "{app}\evopoint.ico"

[Run]

Filename: "{app}\Launcher.exe"; \
Description: "Iniciar EVOPoint"; \
Flags: nowait postinstall skipifsilent