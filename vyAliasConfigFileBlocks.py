from vyConfigFileParser import VyConfigFileBlock

class VyAliasesBlock(VyConfigFileBlock):
    pass

VyAliasesBlock.indentLevelMarkers = {
    0: {
        None: { 'target': 'aliases', } 
    },
    1: {
                None: { 'target': 'commands', 'mode': 'append',},
          'label:.*': {},
        'snippet:.*': {},
    },
    2: [VyAliasesBlock, ],
}

class VyAliasConfigBlock(VyConfigFileBlock):
    indentLevelMarkers = {
        0: {
            'vyalias:config': {
                'target': None
            },
        },
        1: {
            '.*:.*': {},
        }
    }

class VyAliasEnvVarBlock(VyConfigFileBlock):
    indentLevelMarkers = {
        0: {
            None: {
                'target': 'envVar',
            }
        },
        1: {
            'default:.*': {},
            'target:.*': {},
            'Target:.*': {},
        }
    }

class VyAliasEnvVarHeaderBlock(VyConfigFileBlock):
    indentLevelMarkers = {
        0: {
            'vyalias:envvar': {
                'target': None
            },
        },
        1: [VyAliasEnvVarBlock,],
    }

class VyAliasConfigFileBlock(VyConfigFileBlock):
    indentLevelMarkers = {
        0: [VyAliasesBlock, VyAliasEnvVarHeaderBlock, VyAliasConfigBlock],
    }
