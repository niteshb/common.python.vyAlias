
envVarTemplates = [
    'if x%VY_GIT_CMD_{suffix}%==x SET VY_GIT_CMD_{suffix}={default}\n',
    "@echo Set environment variable 'VY_GIT_CMD_{suffix}' to set {target}. default='{default}', current='%VY_GIT_CMD_{suffix}%'\n",
]

cmdTemplates = ['']*4
cmdTemplates[0] = 'if x%{level}==x{alias:<9} GOTO label_{label}\n'
cmdTemplates[1] = '@echo   {alias:<11}   : {final_snippet}\n'

cmdTemplates[2] =  '##############################################################\n'
cmdTemplates[2] += ':label_{label}\n'
cmdTemplates[2] += '@echo on\n'
cmdTemplates[2] += '{commands}\n'
cmdTemplates[2] += '@echo off\n'
cmdTemplates[2] += 'GOTO label_exit\n\n'

cmdTemplates[3] =  ':label_{parent_label}\n'
cmdTemplates[3] += 'if x%VY_ALIAS_BATCH_GEN_NO_DEBUG%==x echo label_{parent_label} & REM ({parent_label}) <- ({label})\n'
