@echo off
if x%VY_GIT_CMD_NO_DEBUG%==xtransfer GOTO label_transfer_start

REM '1st call' mode
set VY_GIT_CMD_NO_DEBUG=y
if NOT x%1==xdebug GOTO label_start

REM 'debug' mode
echo Debug mode on
set VY_GIT_CMD_NO_DEBUG=transfer
%0 %2 %3 %4 %5 %6 %7 %8 %9
GOTO label_exit

REM 'transfer' mode. Here we debug by setting VY_GIT_CMD_NO_DEBUG=<blank>
:label_transfer_start
echo Tranferred into batchfile sub call
set VY_GIT_CMD_NO_DEBUG=
if x%VY_GIT_CMD_NO_DEBUG%==x echo (0, '%0') (1, '%1') (2, '%2') (3, '%3') (4, '%4') (5, '%5') (6, '%6') (7, '%7') (8, '%8') (9, '%9')
echo ##############################################################
GOTO label_start

##############################################################
REM Actual start of the program
:label_start
{{ ev[0] }}:label_MainShortSwitcher
if x%VY_GIT_CMD_NO_DEBUG%==x echo label_MainShortSwitcher
{{ cmd[{vyCOIdx.MainShortSwitcher}] }}:label_OtherShortsSwitcher
if x%VY_GIT_CMD_NO_DEBUG%==x echo label_OtherShortsSwitcher
{{ cmd[{vyCOIdx.OtherShortsSwitcher}] }}GOTO label_invalid
:label_SubCommandsSwitcher
if x%VY_GIT_CMD_NO_DEBUG%==x echo label_SubCommandsSwitcher
{{ cmd[{vyCOIdx.SubCommandsSwitcher}] }}GOTO label_invalid

##############################################################
:label_invalid
echo Invalid command. Type 'g h' to get help
GOTO label_exit

##############################################################
:label_help
@echo on
@echo Command Options:
{{ cmd[{vyCOIdx.HelpSnippets}] }}@echo.
{{ ev[1] }}@echo off
GOTO label_exit

{{ cmd[{vyCOIdx.Commands}] }}##############################################################
:label_exit