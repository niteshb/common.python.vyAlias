import os
from .vyAliasCommand import vyAliasCommand, vyAliasCommandsTree

class vyCOIdx():
    MainShortSwitcher = 0
    HelpSnippets = 1
    Commands = 2
    OtherShortsSwitcher = 3
    SubCommandsSwitcher = 4

class vyAliasBatchScriptGenerator():
    def __init__(self, aliasInfos, envVarInfos, cmdTemplates, envVarTemplates, 
    inputFolder, outputFolder, outputFileName=None):
        self.aliasInfos = aliasInfos
        self.envVarInfos = envVarInfos
        self.cmdTemplates = cmdTemplates
        self.envVarTemplates = envVarTemplates
        self.inputFolder = inputFolder
        self.outputFolder = outputFolder
        self.outputFileName = outputFileName
    
    def generate(self):
        aliasInfos = self.aliasInfos
        envVarInfos = self.envVarInfos
        cmdTemplates = self.cmdTemplates
        envVarTemplates = self.envVarTemplates
        inputFolder = self.inputFolder
        outputFolder = self.outputFolder
        outputFileName = self.outputFileName
        tree = vyAliasCommandsTree(aliasInfos)

        envVarOutputs = [''] * len(envVarTemplates)
        cmdOutputs = [''] * len(cmdTemplates) + [''] + ['']

        for idx, aliasObj in enumerate(tree.traverse()):
            if idx == 0 or aliasObj.traversalState == 'post':
                continue
            if aliasObj.level == 1:
                cmdOutputs[vyCOIdx.MainShortSwitcher] += cmdTemplates[0].format(
                    level=1,
                    alias=aliasObj.primaryAlias,
                    label=aliasObj.final.label,
                )
                for otherAlias in aliasObj.aliases[1:]:
                    cmdOutputs[vyCOIdx.OtherShortsSwitcher] += cmdTemplates[0].format(
                        level=1,
                        alias=otherAlias,
                        label=aliasObj.final.label,
                    )
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
            if aliasObj.level > 1:
                for alias in aliasObj.aliases:
                    cmdOutputs[vyCOIdx.SubCommandsSwitcher] += cmdTemplates[0].format(
                        level=aliasObj.level,
                        alias=alias,
                        label=aliasObj.final.label,
                    )
            if aliasObj.lastchild:
                cmdOutputs[vyCOIdx.SubCommandsSwitcher] += f'GOTO label_invalid & REM ({aliasObj.parent.final.label}) <- ({aliasObj.final.label})\n'
            if aliasObj.hasChildren:
                cmdOutputs[vyCOIdx.SubCommandsSwitcher] += f':label_{aliasObj.final.label}\n'
                cmdOutputs[vyCOIdx.SubCommandsSwitcher] += f'if x%VY_GIT_CMD_NO_DEBUG%==x echo label_{aliasObj.final.label}\n'

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
