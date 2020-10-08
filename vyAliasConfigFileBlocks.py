"""
This is the interface between vyConfigFileParser package and this (vyAlias) package.
This defines the different kind of blocks in an .alias file
"""

from vyConfigFileParser import VyConfigFileBlock

class VyAliasesBlock(VyConfigFileBlock):
    pass

"""
    Aliases
    indent-0: aliases
        indent-1: commands, labels, help-snippets
                - no-attribute lines append to 'commands'
            indent-2: subblocks
"""
VyAliasesBlock.indentLevelMarkers = {
        0: { (None, '([^&|])*')                 : { 'target': 'aliases', } },
        1: { (None, '.*')                       : { 'target': 'commands', 'mode': 'append',},
             ('label', r'([a-zA-Z0-9_]*|--vyabsg-null-label--)')        : {},
             ('snippet', '.*')                  : {},},
        2:   [VyAliasesBlock, ],
}

class VyAliasConfigBlock(VyConfigFileBlock):
    indentLevelMarkers = {
        0: { ('vyalias', 'config')              : { 'target': None },},
        1: { ('.*', '.*')                       : {},}
    }

class VyAliasEnvVarBlock(VyConfigFileBlock):
    indentLevelMarkers = {
        0: { (None, '.*')                       : { 'target': 'envVar',} },
        1: { ('(default|[tT]arget)', '.*')      : {}, }
    }

class VyAliasEnvVarHeaderBlock(VyConfigFileBlock):
    indentLevelMarkers = {
        0: { ('vyalias', 'envvar')               : { 'target': None },},
        1:   [VyAliasEnvVarBlock,],
    }

class VyAliasConfigFileBlock(VyConfigFileBlock):
    indentLevelMarkers = {
        0:   [VyAliasesBlock, VyAliasEnvVarHeaderBlock, VyAliasConfigBlock],
    }
