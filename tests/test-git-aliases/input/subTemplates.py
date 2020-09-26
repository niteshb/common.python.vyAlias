
envVarTemplates = [
    'if x%VY_GIT_CMD_{suffix}%==x SET VY_GIT_CMD_{suffix}={default}\n',
    "@echo Set environment variable 'VY_GIT_CMD_{suffix}' to set {target}. default='{default}', current='%VY_GIT_CMD_{suffix}%'\n",
]

cmdTemplates = ['']*3
cmdTemplates[0] = 'if x%{level}==x{alias:<9} GOTO label_{label}\n'
cmdTemplates[1] = '@echo     {alias:<9}   : {final_snippet}\n'
cmdTemplates[2] = """##############################################################
:label_{label}
@echo on
{commands}
@echo off
GOTO label_exit\n\n"""

