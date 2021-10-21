import os
import msvcrt
import win32security
import win32con
import win32pipe
import win32process
import win32api
import win32net
import win32file
import win32event
import win32profile
import win32service


GENERIC_ACCESS = win32con.GENERIC_READ | win32con.GENERIC_WRITE | win32con.GENERIC_EXECUTE | win32con.GENERIC_ALL

WINSTA_ALL = (win32con.WINSTA_ACCESSCLIPBOARD  | win32con.WINSTA_ACCESSGLOBALATOMS | \
win32con.WINSTA_CREATEDESKTOP    | win32con.WINSTA_ENUMDESKTOPS      | \
win32con.WINSTA_ENUMERATE        | win32con.WINSTA_EXITWINDOWS       | \
win32con.WINSTA_READATTRIBUTES   | win32con.WINSTA_READSCREEN        | \
win32con.WINSTA_WRITEATTRIBUTES  | win32con.DELETE                   | \
win32con.READ_CONTROL            | win32con.WRITE_DAC                | \
win32con.WRITE_OWNER)

DESKTOP_ALL = (win32con.DESKTOP_CREATEMENU      | win32con.DESKTOP_CREATEWINDOW  | \
win32con.DESKTOP_ENUMERATE       | win32con.DESKTOP_HOOKCONTROL   | \
win32con.DESKTOP_JOURNALPLAYBACK | win32con.DESKTOP_JOURNALRECORD | \
win32con.DESKTOP_READOBJECTS     | win32con.DESKTOP_SWITCHDESKTOP | \
win32con.DESKTOP_WRITEOBJECTS    | win32con.DELETE                | \
win32con.READ_CONTROL            | win32con.WRITE_DAC             | \
win32con.WRITE_OWNER)

class ProgramExecuter():

    def runAsDomainUser(self, domainName, userName, password, cmdLine, maxWait):
        # maxWait = Maximum execution time in ms
        userGroupSid = win32security.LookupAccountName(domainName, userName)[0]
        # Login as domain user and create new session
        userToken = win32security.LogonUser(userName, domainName, password,
                                            win32con.LOGON32_LOGON_INTERACTIVE,
                                            win32con.LOGON32_PROVIDER_DEFAULT)
        rc = win32api.GetLastError()
        if userToken is None or (rc != 0):
            return -1, "", "LogonUser failed with RC=%d!" % rc
        profileDir = win32profile.GetUserProfileDirectory(userToken)
        tokenUser = win32security.GetTokenInformation(userToken, win32security.TokenUser)

        # Set access rights to window station
        hWinSta = win32service.OpenWindowStation("winsta0", False, win32con.READ_CONTROL | win32con.WRITE_DAC )
        # Get security descriptor by winsta0-handle
        secDescWinSta = win32security.GetUserObjectSecurity(hWinSta, win32security.OWNER_SECURITY_INFORMATION
                                                                     | win32security.DACL_SECURITY_INFORMATION
                                                                     | win32con.GROUP_SECURITY_INFORMATION)
        # Get DACL from security descriptor
        daclWinSta = secDescWinSta.GetSecurityDescriptorDacl()
        if daclWinSta is None:
            # Create DACL if not exisiting
            daclWinSta = win32security.ACL()
        # Add ACEs to DACL for specific user group
        daclWinSta.AddAccessAllowedAce(win32security.ACL_REVISION_DS, GENERIC_ACCESS, userGroupSid)
        daclWinSta.AddAccessAllowedAce(win32security.ACL_REVISION_DS, WINSTA_ALL, userGroupSid)
        # Set modified DACL for winsta0
        win32security.SetSecurityInfo(hWinSta, win32security.SE_WINDOW_OBJECT, win32security.DACL_SECURITY_INFORMATION,
                                      None, None, daclWinSta, None)

        # Set access rights to desktop
        hDesktop = win32service.OpenDesktop("default", 0, False, win32con.READ_CONTROL
                                                                 | win32con.WRITE_DAC
                                                                 | win32con.DESKTOP_WRITEOBJECTS
                                                                 | win32con.DESKTOP_READOBJECTS)
        # Get security descriptor by desktop-handle
        secDescDesktop = win32security.GetUserObjectSecurity(hDesktop, win32security.OWNER_SECURITY_INFORMATION
                                                                       | win32security.DACL_SECURITY_INFORMATION
                                                                       | win32con.GROUP_SECURITY_INFORMATION )
        # Get DACL from security descriptor
        daclDesktop = secDescDesktop.GetSecurityDescriptorDacl()
        if daclDesktop is None:
            #create DACL if not exisiting
            daclDesktop = win32security.ACL()
        # Add ACEs to DACL for specific user group
        daclDesktop.AddAccessAllowedAce(win32security.ACL_REVISION_DS, GENERIC_ACCESS, userGroupSid)
        daclDesktop.AddAccessAllowedAce(win32security.ACL_REVISION_DS, DESKTOP_ALL, userGroupSid)
        # Set modified DACL for desktop
        win32security.SetSecurityInfo(hDesktop, win32security.SE_WINDOW_OBJECT, win32security.DACL_SECURITY_INFORMATION,
                                      None, None, daclDesktop, None)

        # Setup stdin, stdOut and stderr
        secAttrs = win32security.SECURITY_ATTRIBUTES()
        secAttrs.bInheritHandle = 1
        stdOutRd, stdOutWr = win32pipe.CreatePipe(secAttrs, 0)
        stdErrRd, stdErrWr = win32pipe.CreatePipe(secAttrs, 0)

        ppid = win32api.GetCurrentProcess()
        tmp = win32api.DuplicateHandle(ppid, stdOutRd, ppid, 0, 0, win32con.DUPLICATE_SAME_ACCESS)
        win32file.CloseHandle(stdOutRd)
        stdOutRd = tmp

        environment = win32profile.CreateEnvironmentBlock(userToken, False)

        startupInfo = win32process.STARTUPINFO()
        startupInfo.dwFlags = win32con.STARTF_USESTDHANDLES
        startupInfo.hStdOutput = stdOutWr
        startupInfo.hStdError = stdErrWr

        hPrc = win32process.CreateProcessAsUser(
                                userToken,
                                None,               # appName
                                cmdLine,            # commandLine
                                None,               # processAttributes
                                None,               # threadAttributes
                                1,                  # bInheritHandles
                                win32process.CREATE_NEW_CONSOLE, # dwCreationFlags
                                environment,        # newEnvironment
                                profileDir,         # currentDirectory
                                startupInfo)[0]

        win32file.CloseHandle(stdErrWr)
        win32file.CloseHandle(stdOutWr)
        win32security.RevertToSelf()

        # Wait for process to complete
        stdOutBuf = os.fdopen(msvcrt.open_osfhandle(int(stdOutRd), 0), "rb")
        stdErrBuf = os.fdopen(msvcrt.open_osfhandle(int(stdErrRd), 0), "rb")
        win32event.WaitForSingleObject(hPrc, maxWait)
        stdOut = stdOutBuf.read()
        stdErr = stdErrBuf.read()
        rc = win32process.GetExitCodeProcess(hPrc)
        return rc, str(stdOut, "utf-8"), str(stdErr, "utf-8")


if __name__ == "__main__":
    cmdLine = "C:/Windows/System32/cmd.exe"
    domainName = input("Domain: ")
    userName = input("User: ")
    password = input("Password: ")
    exec = ProgramExecuter()
    print(exec.runAsDomainUser(domainName, userName, password, cmdLine, 60000))