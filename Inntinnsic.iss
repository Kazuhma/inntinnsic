#ifndef AppVersion
  #define AppVersion "0.0"
#endif

#define AppName "Inntinnsic"
#define AppExeName "Inntinnsic.exe"
#define PublishDir "bin\Release\net8.0-windows10.0.19041.0\win-x64\publish"

[Setup]
AppId={{8F2B4E5A-1C3D-4A6E-9B7F-0D8E2F4A6C1B}
AppName={#AppName}
AppVersion={#AppVersion}
AppPublisher=Inntinnsic
DefaultDirName={autopf}\{#AppName}
DefaultGroupName={#AppName}
DisableProgramGroupPage=yes
OutputDir=Publish
OutputBaseFilename=Inntinnsic-v{#AppVersion}-win-x64-Setup
SetupIconFile={#PublishDir}\appicon.ico
UninstallDisplayIcon={app}\{#AppExeName}
Compression=lzma2
SolidCompression=yes
PrivilegesRequired=lowest
WizardStyle=modern

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"

[Files]
Source: "{#PublishDir}\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\{#AppName}"; Filename: "{app}\{#AppExeName}"
Name: "{autodesktop}\{#AppName}"; Filename: "{app}\{#AppExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#AppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(AppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent
