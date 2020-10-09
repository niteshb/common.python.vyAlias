class Generic():
    pass

rootPrefix = Generic()
rootPrefix.command = ''
rootPrefix.alias = ''
rootPrefix.label = ''

class VyAliasTree():
    def __init__(self, aliasBlock, **config):
        if 'label-source' in config:
            if config['label-source'] in ['alias', 'command']:
                labelSource = config['label-source']
            else:
                raise Exception('Invalid label source')
        else:
            labelSource = 'alias'
        self.root = aliasBlock
        aliasBlock.process(rootPrefix, labelSource)
        assert(self.root.hasChildren)

    def traverse(self):
        return self.root.traverse()
