import os
from vyImport import vyLoadModuleFromFilePath
from .vyProcessVyAliasConfig import vyProcessVyAliasConfig
from .vyAliasCommand import vyAliasCommand, vyAliasCommandsTree

class vyCOIdx():
    Switcher = 0
    HelpSnippets = 1
    Commands = 2

def vyAliasBatchScriptGenerator(configFilePath, outputFolder='.', outputFileName=None):
    ext = os.path.splitext(configFilePath)[1]
    if ext == '.vyalias':
        aliasInfos, envVarInfos = vyProcessVyAliasConfig(configFilePath)
    elif ext == '.py':
        config = vyLoadModuleFromFilePath(configFilePath)
        aliasInfos, envVarInfos = config.aliasInfos, config.envVarInfos

    cmdTemplates = None
    envVarTemplates = None
    moduleFolder = os.path.dirname(os.path.realpath(__file__))
    subTemplates = vyLoadModuleFromFilePath(os.path.join(moduleFolder, 'subTemplates.py'))
    cmdTemplates = subTemplates.cmdTemplates
    envVarTemplates = subTemplates.envVarTemplates

    tree = vyAliasCommandsTree(aliasInfos)
    tree.root.final.label = 'Switcher'

    envVarOutputs = [''] * len(envVarTemplates)
    cmdOutputs = [''] * len(cmdTemplates) + [''] + ['']

    aliasQueue = [_ for _ in tree.root.subAliases]
    for aliasObj in aliasQueue:
        if aliasObj.firstchild:
            cmdOutputs[vyCOIdx.Switcher] += cmdTemplates[3].format(
                parent_label=aliasObj.parent.final.label,
                label=aliasObj.final.label)

        for alias in aliasObj.aliases:
            cmdOutputs[vyCOIdx.Switcher] += cmdTemplates[0].format(
                level=aliasObj.level,
                alias=alias,
                label=aliasObj.final.label,
            )

        if aliasObj.lastchild:
            cmdOutputs[vyCOIdx.Switcher] += f'GOTO label_invalid & REM ({aliasObj.parent.final.label}) <- ({aliasObj.final.label})\n'

        if aliasObj.hasChildren:
            aliasQueue += [_ for _ in aliasObj.subAliases]

    for aliasObj in tree.root.traverse():
        if aliasObj.traversalState == 'post':
            continue
        if not aliasObj.hasChildren:
            cmdOutputs[vyCOIdx.HelpSnippets] += cmdTemplates[1].format(
                alias=aliasObj.final.primaryAlias,
                final_snippet=aliasObj.final.snippet,
            )
            if len(aliasObj.commands) > 0:
                cmdOutputs[vyCOIdx.Commands] += cmdTemplates[2].format(
                    commands=aliasObj.commandsStr,
                    label=aliasObj.final.label,
                )

    for envVarInfo in envVarInfos:
        suffix = envVarInfo[0]
        default = envVarInfo[1]['default']
        target = envVarInfo[1]['target'] if 'target' in envVarInfo[1] else suffix.lower()
        Target = envVarInfo[1]['Target'] if 'Target' in envVarInfo[1] else target[0].upper() + target[1:]
        for idx, envVarTemplate in enumerate(envVarTemplates):
            envVarOutputs[idx] += envVarTemplate.format(
                suffix=suffix,
                default=default,
                target=target,
                Target=Target,
            )
    # procesing done
    gTemplate = open(os.path.join(moduleFolder, 'template.cmd')).read()
    gTemplate = gTemplate.format(vyCOIdx=vyCOIdx)
    out = gTemplate.format(ev=envVarOutputs, cmd=cmdOutputs)
    if not outputFileName:
        outputFileName = f'{tree.root.aliases[0]}.cmd'
    outputFilePath = os.path.join(outputFolder, outputFileName)
    print('Output File Path:', outputFilePath)
    with open(outputFilePath, 'w') as ofid:
        ofid.write(out)
        ofid.close()
