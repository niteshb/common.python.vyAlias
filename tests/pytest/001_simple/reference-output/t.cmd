@echo off
if x%VY_ALIAS_BATCH_GEN_NO_DEBUG%==xtransfer GOTO label_transfer_start

REM '1st call' mode
set VY_ALIAS_BATCH_GEN_NO_DEBUG=y
if NOT x%1==xdebug GOTO label_start

REM 'debug' mode
echo Debug mode on
set VY_ALIAS_BATCH_GEN_NO_DEBUG=transfer
%0 %2 %3 %4 %5 %6 %7 %8 %9
GOTO label_exit

REM 'transfer' mode. Here we debug by setting VY_ALIAS_BATCH_GEN_NO_DEBUG=<blank>
:label_transfer_start
echo Tranferred into batchfile sub call
set VY_ALIAS_BATCH_GEN_NO_DEBUG=
if x%VY_ALIAS_BATCH_GEN_NO_DEBUG%==x echo arguments    :: (0, '%0') (1, '%1') (2, '%2') (3, '%3') (4, '%4') (5, '%5') (6, '%6') (7, '%7') (8, '%8') (9, '%9')
if x%VY_ALIAS_BATCH_GEN_NO_DEBUG%==x echo command line :: %0 %1 %2 %3 %4 %5 %6 %7 %8 %9
echo ##############################################################
GOTO label_start

##############################################################
REM Actual start of the program
:label_start

:label_Switcher
if x%VY_ALIAS_BATCH_GEN_NO_DEBUG%==x echo label_Switcher & REM (Switcher) <- (t_help)
if x%1==xh         GOTO label_t_help
if x%1==x          GOTO label_t_help
if x%1==x-h        GOTO label_t_help
if x%1==x--help    GOTO label_t_help
if x%1==xa         GOTO label_t_a
if x%1==xd         GOTO label_t_dev
GOTO label_invalid & REM (Switcher) <- (t_dev)

##############################################################
:label_invalid
echo Invalid command. Type '%0 h' to get help
GOTO label_exit

##############################################################
:label_t_help
@echo on
@echo Command Options:
@echo   t h           : This help message
@echo   t a           : echo test all : test everything
@echo   t d           : echo test -branch development : test the development branch only
@echo.
@echo off
GOTO label_exit

##############################################################
:label_t_a
@echo on
echo test all
@echo off
GOTO label_exit

##############################################################
:label_t_dev
@echo on
echo test -branch development
@echo off
GOTO label_exit

##############################################################
:label_exit