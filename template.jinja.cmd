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
{% for envvar in envvars %}if x%VY_GIT_CMD_{{ envvar["envVar"] }}%==x SET VY_GIT_CMD_{{ envvar["envVar"] }}={{ envvar["default"] }}
{% endfor %}{% for aliasObj in aliasQueue %}{% if aliasObj.firstchild %}
:label_{{ aliasObj.parent.final.label }}
if x%VY_ALIAS_BATCH_GEN_NO_DEBUG%==x echo label_{{ aliasObj.parent.final.label }} & REM ({{ aliasObj.parent.final.label }}) <- ({{ aliasObj.final.label }}){% endif %}{% for alias in aliasObj.aliases %}
if x%{{ aliasObj.level }}==x{{ '{0:<9}'.format(alias) }} GOTO label_{{ aliasObj.final.label }}{% endfor %}{% if aliasObj.lastchild %}
GOTO label_invalid & REM ({{ aliasObj.parent.final.label }}) <- ({{ aliasObj.final.label }}){% endif %}{% endfor %}

##############################################################
:label_invalid
echo Invalid command. Type '%0 h' to get help
GOTO label_exit

##############################################################
:label_{{ labelHelp }}
@echo on
@echo Command Options:{% for aliasObj in aliasRootBlock.traverse() %}{% if aliasObj.traversalState == 'pre' and not aliasObj.hasChildren %}
@echo   {{ '{0:<11}'.format(aliasObj.final.primaryAlias) }}   : {{ aliasObj.final.snippet }}{% endif %}{% endfor %}
@echo.{% for envvar in envvars %}
@echo Set environment variable 'VY_GIT_CMD_{{ envvar["envVar"] }}' to set {{ envvar["target"] }}. default='{{ envvar["default"] }}', current='%VY_GIT_CMD_{{ envvar["envVar"] }}%'{% endfor %}
@echo off
GOTO label_exit
{% for aliasObj in aliasRootBlock.traverse() %}{% if aliasObj.traversalState == 'pre' and not aliasObj.hasChildren and (aliasObj.commands)|length > 0 %}
##############################################################
:label_{{ aliasObj.final.label }}
@echo on
{{ aliasObj.commandsStr }}
@echo off
GOTO label_exit
{% endif %}{% endfor %}
##############################################################
:label_exit