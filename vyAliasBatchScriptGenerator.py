import os
from vyImport import vyLoadModuleFromFilePath
from .vyAliasCommand import VyAliasCommand, VyAliasCommandsTree
from .vyAliasConfigFile import VyAliasConfigFile

class VyCOIdx():
    Switcher = 0
    HelpSnippets = 1
    Commands = 2

def vyAliasBatchScriptGenerator(configFilePath, outputFolder='.', outputFileName=None):
    acf = VyAliasConfigFile(configFilePath)
    aliasInfoRoot, envVarInfos, configInfos = acf.parse()

    cmdTemplates = None
    envVarTemplates = None
    moduleFolder = os.path.dirname(os.path.realpath(__file__))
    subTemplates = vyLoadModuleFromFilePath(os.path.join(moduleFolder, 'subTemplates.py'))
    cmdTemplates = subTemplates.cmdTemplates
    envVarTemplates = subTemplates.envVarTemplates

    tree = VyAliasCommandsTree(aliasInfoRoot, **configInfos)
    tree.root.final.label = 'Switcher'

    envVarOutputs = [''] * len(envVarTemplates)
    cmdOutputs = [''] * len(cmdTemplates) + [''] + ['']

    aliasQueue = [_ for _ in tree.root.subAliases]
    for aliasObj in aliasQueue:
        if aliasObj.firstchild:
            cmdOutputs[VyCOIdx.Switcher] += cmdTemplates[3].format(
                parent_label=aliasObj.parent.final.label,
                label=aliasObj.final.label)

        for alias in aliasObj.aliases:
            cmdOutputs[VyCOIdx.Switcher] += cmdTemplates[0].format(
                level=aliasObj.level,
                alias=alias,
                label=aliasObj.final.label,
            )

        if aliasObj.lastchild:
            cmdOutputs[VyCOIdx.Switcher] += f'GOTO label_invalid & REM ({aliasObj.parent.final.label}) <- ({aliasObj.final.label})\n'

        if aliasObj.hasChildren:
            aliasQueue += [_ for _ in aliasObj.subAliases]

    for aliasObj in tree.root.traverse():
        if aliasObj.traversalState == 'post':
            continue
        if not aliasObj.hasChildren:
            cmdOutputs[VyCOIdx.HelpSnippets] += cmdTemplates[1].format(
                alias=aliasObj.final.primaryAlias,
                final_snippet=aliasObj.final.snippet,
            )
            if len(aliasObj.commands) > 0:
                cmdOutputs[VyCOIdx.Commands] += cmdTemplates[2].format(
                    commands=aliasObj.commandsStr,
                    label=aliasObj.final.label,
                )

    for envVarInfo in envVarInfos:
        suffix = envVarInfo['envVar']
        default = envVarInfo['default']
        target = envVarInfo['target'] if 'target' in envVarInfo else suffix.lower()
        Target = envVarInfo['Target'] if 'Target' in envVarInfo else target[0].upper() + target[1:]
        for idx, envVarTemplate in enumerate(envVarTemplates):
            envVarOutputs[idx] += envVarTemplate.format(
                suffix=suffix,
                default=default,
                target=target,
                Target=Target,
            )
    # procesing done
    gTemplate = open(os.path.join(moduleFolder, 'template.cmd')).read()
    gTemplate = gTemplate.format(VyCOIdx=VyCOIdx)
    labelHelp = tree.root.subAliases[0].final.label # help is inserted in the beginning
    out = gTemplate.format(ev=envVarOutputs, cmd=cmdOutputs, labelHelp=labelHelp)
    if not outputFileName:
        outputFileName = f'{tree.root.aliases[0]}.cmd'
    outputFilePath = os.path.join(outputFolder, outputFileName)
    print('Output File Path:', outputFilePath)
    with open(outputFilePath, 'w') as ofid:
        ofid.write(out)
        ofid.close()
