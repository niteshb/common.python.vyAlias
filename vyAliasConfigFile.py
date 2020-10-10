import re
#from typing import List, Dict
from vyConfigFileParser import VyConfigFile
from .vyAliasBlock import VyAliasBlock
from .vyAliasConfigFileBlocks import VyAliasConfigBlock, VyAliasConfigFileBlock
from .vyAliasConfigFileBlocks import VyAliasEnvVarHeaderBlock, VyAliasEnvVarBlock

class VyAliasConfigFile(VyConfigFile):
    def parse(self):
        parsed: VyAliasConfigFileBlock = super().parse(VyAliasConfigFileBlock)
        envVarInfos: List[VyAliasEnvVarBlock] = []
        configInfos: Dict[str, str] = {}
        for subBlock in parsed.subBlocks:
            if isinstance(subBlock, VyAliasBlock):
                aliasRootBlock: VyAliasBlock = subBlock # TODO: ensure that we come here exactly once
            elif isinstance(subBlock, VyAliasEnvVarHeaderBlock):
                envVarInfos = subBlock.subBlocks
            elif isinstance(subBlock, VyAliasConfigBlock):
                configInfos = subBlock.attribs
            else:
                raise Exception('Unexpected return from VyConfigFile.parse')
        return aliasRootBlock, envVarInfos, configInfos
