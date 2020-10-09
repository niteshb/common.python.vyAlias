import os
from jinja2 import Template
from .vyAliasTree import VyAliasTree
from .vyAliasConfigFile import VyAliasConfigFile

class VyCOIdx():
    Switcher = 0
    HelpSnippets = 1
    Commands = 2

def vyAliasBatchScriptGenerator(configFilePath, outputFolder='.', outputFileName=None):
    acf = VyAliasConfigFile(configFilePath)
    aliasRootBlock, envVarInfos, configInfos = acf.parse()
    tree = VyAliasTree(aliasRootBlock, **configInfos)
    tree.root.final.label = 'Switcher'

    aliasQueue = [_ for _ in tree.root.subAliasBlocks]
    for aliasObj in aliasQueue:
        if aliasObj.hasChildren:
            aliasQueue += [_ for _ in aliasObj.subAliasBlocks]
    labelHelp = tree.root.subAliasBlocks[0].final.label # help is inserted in the beginning
    for envVarInfo in envVarInfos:
        envVarInfo['target'] = envVarInfo['target'] if 'target' in envVarInfo else envVarInfo['envVar'].lower()
        envVarInfo['Target'] = envVarInfo['Target'] if 'Target' in envVarInfo else envVarInfo['target'][0].upper() + envVarInfo['target'][1:]

    # Jinja Starts Here
    moduleFolder = os.path.dirname(os.path.realpath(__file__))
    template = Template(open(os.path.join(moduleFolder, 'template.jinja.cmd')).read())
    out = template.render(labelHelp=labelHelp, envvars=envVarInfos, tree=tree, aliasQueue=aliasQueue)

    if not outputFileName:
        outputFileName = f'{tree.root.aliases[0]}.cmd'
    outputFilePath = os.path.join(outputFolder, outputFileName)
    print('Output File Path:', outputFilePath)
    with open(outputFilePath, 'w') as ofid:
        ofid.write(out)
        ofid.close()
