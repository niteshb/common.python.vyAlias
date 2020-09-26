import os
from .vyAliasCommand import vyAliasCommand, vyAliasCommandsTree

class vyCOIdx():
    Switcher = 0
    HelpSnippets = 1
    Commands = 2

def vyAliasBatchScriptGenerator(aliasInfos, envVarInfos, cmdTemplates, 
envVarTemplates, inputFolder, outputFolder, outputFileName=None):
    tree = vyAliasCommandsTree(aliasInfos)
    tree.root.final.label = 'Switcher'

    envVarOutputs = [''] * len(envVarTemplates)
    cmdOutputs = [''] * len(cmdTemplates) + [''] + ['']

    aliasQueue = [_ for _ in tree.root.subAliases]
    for aliasObj in aliasQueue:
        if aliasObj.firstchild:
            cmdOutputs[vyCOIdx.Switcher] += f':label_{aliasObj.parent.final.label}\n'
            cmdOutputs[vyCOIdx.Switcher] += f'if x%VY_GIT_CMD_NO_DEBUG%==x echo label_{aliasObj.parent.final.label} & REM ({aliasObj.parent.final.label}) <- ({aliasObj.final.label})\n'

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

    for environmentVar in envVarInfos:
        suffix = environmentVar[0]
        default = environmentVar[1]
        target = suffix.lower()
        Target = target[0].upper() + target[1:]
        for idx, envVarTemplate in enumerate(envVarTemplates):
            envVarOutputs[idx] += envVarTemplate.format(
                suffix=suffix,
                default=default,
                target=target,
                Target=Target,
            )
    # procesing done
    gTemplate = open(os.path.join(inputFolder, 'template.cmd')).read()
    gTemplate = gTemplate.format(vyCOIdx=vyCOIdx)
    gTemplate = gTemplate.replace('{ ', '{')
    gTemplate = gTemplate.replace(' }', '}')
    out = gTemplate.format(ev=envVarOutputs, cmd=cmdOutputs)
    if not outputFileName:
        outputFileName = f'{tree.root.aliases[0]}.cmd'
    outputFilePath = os.path.join(outputFolder, outputFileName)
    print('Output File Path:', outputFilePath)
    with open(outputFilePath, 'w') as ofid:
        ofid.write(out)
        ofid.close()
