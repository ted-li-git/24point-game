@echo off
title 24point卸载向导
echo 即将为你卸载24point
pause
del "%USERPROFILE%\Desktop\24point.lnk"
rd /s /q %cd%
echo 卸载完毕！
pause