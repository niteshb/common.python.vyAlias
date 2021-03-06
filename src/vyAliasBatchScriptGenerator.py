import os
from typing import Optional
from jinja2 import Template
from .vyAliasConfigFile import VyAliasConfigFile
from .vyAliasBlock import VyAliasBlock, rootPrefix

def vyAliasBatchScriptGenerator(configFilePath: str, outputFolder: str='.', outputFileName: Optional[str]=None):
    aliasRootBlock, envVarInfos, configInfos = VyAliasConfigFile(configFilePath).parse()
    # Add help block
    helpAliasBlock = VyAliasBlock()
    helpAliasBlock.attribs = {
        'aliases'   : 'h, --vyabsg-null-alias--, -h, --help', 
        'label'     : 'help', 
        'snippet'   : 'This help message',
    }
    aliasRootBlock.insertChildBlock(0, helpAliasBlock)

    if 'label-source' in configInfos:
        if configInfos['label-source'] not in ['alias', 'command']:
            raise Exception('Invalid label source')
    else:
        configInfos['label-source'] = 'alias'

    aliasRootBlock.process(rootPrefix, configInfos)
    assert(aliasRootBlock.hasChildren)
    aliasRootBlock.final.label = 'Switcher'

    aliasQueue = [_ for _ in aliasRootBlock.subAliasBlocks]
    for aliasObj in aliasQueue:
        if aliasObj.hasChildren:
            aliasQueue += [_ for _ in aliasObj.subAliasBlocks]
    labelHelp = aliasRootBlock.subAliasBlocks[0].final.label # help is inserted in the beginning
    for envVarInfo in envVarInfos:
        envVarInfo['target'] = envVarInfo['target'] if 'target' in envVarInfo else envVarInfo['envVar'].lower()
        envVarInfo['Target'] = envVarInfo['Target'] if 'Target' in envVarInfo else envVarInfo['target'][0].upper() + envVarInfo['target'][1:]

    # Jinja Starts Here
    moduleFolder = os.path.dirname(os.path.realpath(__file__))
    template = Template(open(os.path.join(moduleFolder, 'template.jinja.cmd')).read())
    out = template.render(labelHelp=labelHelp, envvars=envVarInfos, aliasRootBlock=aliasRootBlock, aliasQueue=aliasQueue)

    if not outputFileName:
        outputFileName = f'{aliasRootBlock.aliases[0]}.cmd'
    outputFilePath = os.path.join(outputFolder, outputFileName)
    print('Output File Path:', outputFilePath)
    with open(outputFilePath, 'w') as ofid:
        ofid.write(out)
        ofid.close()
    return outputFilePath, outputFileName