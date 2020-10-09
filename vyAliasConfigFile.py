import re
from pprint import pprint
from typing import List, Union, Tuple, Dict, Callable, Any, Optional
from vyConfigFileParser import VyConfigFile
from vyDebug import VyDebug, VyDebugLevel
from .vyAliasConfigFileBlocks import VyAliasConfigFileBlock, VyAliasesBlock
from .vyAliasConfigFileBlocks import VyAliasEnvVarHeaderBlock, VyAliasConfigBlock

AliasInfoType = Tuple[List[str], List[str], Dict[str, str]]
vyd = VyDebug(VyDebugLevel.SILENT)
vyd.level = 0

class VyAliasConfigFile(VyConfigFile):
    def __init__(self, configFilePath: str):
        super().__init__(configFilePath)

    def parse(self):
        parsed = super().parse(VyAliasConfigFileBlock)
        envVarInfos = []
        configInfos = {}
        for subblock in parsed.subblocks:
            if isinstance(subblock, VyAliasesBlock):
                aliasInfoRoot = self.processAliasBlock(subblock) # TODO: check, should come here only once
                helpAliasInfo = {
                    'aliases'   : 'h, --vyabsg-null-alias--, -h, --help', 
                    'commands'  : [], 
                    'label'     : 'help', 
                    'snippet'   : 'This help message',
                }
                aliasInfoRoot['sub-aliases'].insert(0, helpAliasInfo)
            elif isinstance(subblock, VyAliasEnvVarHeaderBlock):
                envVarInfos = self.processEnvVarBlock(subblock)
            elif isinstance(subblock, VyAliasConfigBlock):
                configInfos = subblock.attribs
            else:
                raise Exception('Unexpected return from VyConfigFile.parse')
        return aliasInfoRoot, envVarInfos, configInfos

    def processEnvVarBlock(self, block):
        envVarInfos = []
        for subblock in block.subblocks:
            d = subblock.attribs
            envVarInfo = (d['envVar'], d)
            del envVarInfo[1]['envVar']
            envVarInfos.append(envVarInfo)
        return envVarInfos

    def processAliasBlock(self, block):
        aliasInfo = block.attribs

        if block.subblocks:
            aliasInfo['sub-aliases'] = []
        for subblock in block.subblocks:
            subAliasInfo = self.processAliasBlock(subblock)
            aliasInfo['sub-aliases'].append(subAliasInfo)
        return aliasInfo
