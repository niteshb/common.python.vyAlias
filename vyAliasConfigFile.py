import re
from pprint import pprint
from typing import List, Union, Tuple, Dict, Callable, Any, Optional
from vyConfigFileParser import VyConfigFile
from vyDebug import VyDebug, VyDebugLevel
from . import VyAliasBlock
from .vyAliasConfigFileBlocks import VyAliasConfigFileBlock
from .vyAliasConfigFileBlocks import VyAliasEnvVarHeaderBlock, VyAliasConfigBlock

AliasInfoType = Tuple[List[str], List[str], Dict[str, str]]
vyd = VyDebug(VyDebugLevel.SILENT)
vyd.level = 0

class VyAliasConfigFile(VyConfigFile):
    def __init__(self, configFilePath: str):
        super().__init__(configFilePath)

    def parse(self):
        parsed = super().parse(VyAliasConfigFileBlock)
        envVarInfos = {}
        configInfos = {}
        for subBlock in parsed.subBlocks:
            if isinstance(subBlock, VyAliasBlock):
                # TODO: check, should come here only once
                helpAliasBlock = VyAliasBlock()
                helpAliasBlock.attribs = {
                    'aliases'   : 'h, --vyabsg-null-alias--, -h, --help', 
                    'label'     : 'help', 
                    'snippet'   : 'This help message',
                }
                subBlock.subBlocks.insert(0, helpAliasBlock)
                aliasBlock = subBlock
            elif isinstance(subBlock, VyAliasEnvVarHeaderBlock):
                envVarInfos = subBlock.subBlocks
            elif isinstance(subBlock, VyAliasConfigBlock):
                configInfos = subBlock.attribs
            else:
                raise Exception('Unexpected return from VyConfigFile.parse')
        return aliasBlock, envVarInfos, configInfos
