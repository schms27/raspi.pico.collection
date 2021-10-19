; Script generated by the Inno Setup Script Wizard.
; SEE THE DOCUMENTATION FOR DETAILS ON CREATING INNO SETUP SCRIPT FILES!

#define MyAppName "MacroPad Service"
#define MyAppVersion "0.1"
#define MyAppPublisher "Softy Inc."
#define MyAppExeName "macropad_service.exe"

[Setup]
; NOTE: The value of AppId uniquely identifies this application. Do not use the same AppId value in installers for other applications.
; (To generate a new GUID, click Tools | Generate GUID inside the IDE.)
AppId={{428E30DF-80A8-4F8F-96CB-0F2A7FFD75FD}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
;AppVerName={#MyAppName} {#MyAppVersion}
AppPublisher={#MyAppPublisher}
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
DisableProgramGroupPage=yes
; Uncomment the following line to run in non administrative install mode (install for current user only.)
;PrivilegesRequired=lowest
OutputDir=pico.hid.service\installer
OutputBaseFilename=setup-macropad-service
SetupIconFile=pico.hid.service\dist\makro_icon.ico
Compression=lzma
SolidCompression=yes
WizardStyle=modern

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "pico.hid.service/dist/{#MyAppExeName}"; DestDir: "{app}"; Flags: ignoreversion
Source: "pico.hid.service/dist/appdata/*"; DestDir: "{autoappdata}\MacroPadService\"; Flags: ignoreversion createallsubdirs recursesubdirs comparetimestamp
; NOTE: Don't use "Flags: ignoreversion" on any shared system files

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{group}\{cm:UninstallProgram,{#MyAppName}}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Code]
procedure InstallService;

var
ResultCode: Integer;

begin
  // Install Service and wait for it to terminate
  if Exec(ExpandConstant('{app}\{#MyAppExeName}'), 'debug -s C:\ProgramData\MacroPadService', '', SW_SHOWNORMAL,
     ewWaitUntilTerminated, ResultCode) then
   begin
    MsgBox('Failed to install Service!' + #13#10 +
      SysErrorMessage(ResultCode), mbError, MB_OK);
  end;
end;

var
  CustomQueryPage: TInputQueryWizardPage;
  ResultCode: Integer;
  Password: String;

procedure GetPasswordForServiceAndInstall();
begin
  CustomQueryPage := CreateInputQueryPage(
    wpWelcome,
    'Password',
    'Field for Password',
    'Custom instructions');

  { Add items (False means it's not a password edit) }
  CustomQueryPage.Add('&Password:', False);
end;

procedure InitializeWizard();
begin
  GetPasswordForServiceAndInstall();
end;

procedure CurStepChanged(CurStep: TSetupStep);
begin
  if CurStep = ssPostInstall then
  begin
    { Read custom value }
    Password := CustomQueryPage.Values[0];
    MsgBox(Password, mbInformation, MB_OK);

    MsgBox(ExpandConstant('{app}\{#MyAppExeName}') + ' install -s ' + ExpandConstant('{autoappdata}\MacroPadService\') +' -p ' + Password, mbInformation, MB_OK);
    // Install Service and wait for it to terminate
    if not Exec(ExpandConstant('{app}\{#MyAppExeName}'), 'install -s ' + ExpandConstant('{autoappdata}\MacroPadService\') +' -p ' + Password, '', SW_SHOWNORMAL,
     ewWaitUntilTerminated, ResultCode) then
      begin
        MsgBox('Failed to install Service!' + #13#10 +
          SysErrorMessage(ResultCode), mbError, MB_OK);
      end;
  end;
end;


