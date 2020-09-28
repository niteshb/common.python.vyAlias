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
if x%VY_ALIAS_BATCH_GEN_NO_DEBUG%==x echo label_Switcher & REM (Switcher) <- (help)
if x%1==xh         GOTO label_help
if x%1==x          GOTO label_help
if x%1==x-h        GOTO label_help
if x%1==x--help    GOTO label_help
if x%1==xgit       GOTO label_git
if x%1==xmake      GOTO label_make
if x%1==xexe       GOTO label_exe
if x%1==xclear     GOTO label_clear
if x%1==xclean     GOTO label_clear
if x%1==x__clear_main_build GOTO label_clear_main_build
GOTO label_invalid & REM (Switcher) <- (clear_main_build)

##############################################################
:label_invalid
echo Invalid command. Type '%0 h' to get help
GOTO label_exit

##############################################################
:label_help
@echo on
@echo Command Options:
@echo   make h        : This help message
@echo   make git      : Generate git alias files from both, vyalias ^& python, config files
@echo   make make     : Generates this make batch file from its config file
@echo   make exe      : Generate main.exe from main.py
@echo   make clear    : Cleans up stuff from nuitka
@echo   make __clear_main_build   : Cleans up main.build from nuitka
@echo.
@echo off
GOTO label_exit

##############################################################
:label_git
@echo on
python main.py input/config.vyalias -o output -f g.vyalias.cmd
python main.py input/config.vyalias.py -o output -f g.py.cmd
@echo off
GOTO label_exit

##############################################################
:label_make
@echo on
python main.py input/config.makefile.vyalias
@echo off
GOTO label_exit

##############################################################
:label_exe
@echo on
make clear
nuitka main.py
@echo off
GOTO label_exit

##############################################################
:label_clear
@echo on
if exist main.exe del main.exe
if exist main.build make __clear_main_build
@echo off
GOTO label_exit

##############################################################
:label_clear_main_build
@echo on
cd main.build
del /f/q/s *
cd ..
rmdir /q/s main.build
@echo off
GOTO label_exit

##############################################################
:label_exit