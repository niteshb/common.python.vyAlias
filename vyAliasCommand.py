import re

class Generic():
    pass

rootPrefix = Generic()
rootPrefix.command = ''
rootPrefix.alias = ''
rootPrefix.label = ''

class VyAliasCommandsTree():
    def __init__(self, aliasInfoRoot, **config):
        if 'label-source' in config:
            if config['label-source'] in ['alias', 'command']:
                labelSource = config['label-source']
            else:
                raise Exception('Invalid label source')
        else:
            labelSource = 'alias'
        self.root = VyAliasCommand(aliasInfoRoot, rootPrefix, labelSource)
        assert(self.root.hasChildren)

    def traverse(self):
        return self.root.traverse()

class VyAliasCommand():
    def __init__(
            self, 
            aliasInfo, 
            prefix,
            labelSource,
            level=0, 
            parent=None,
        ):
        self.aliasInfo = aliasInfo
        self.prefix = prefix
        self.level = level
        self.parent = parent
        self.subAliases = []
        self.hasChildren = 'sub-aliases' in aliasInfo

        self.aliases = ['' if alias.strip().lower() == '--vyabsg-null-alias--' else alias.strip() for alias in self.aliases.split(',')]
        self.primaryAlias = self.aliases[0]

        rawCommands = aliasInfo['commands'] if 'commands' in aliasInfo else []
        self.commands = []
        for cmd in rawCommands:
            if cmd != '--vyabsg-no-command--':
                if cmd == '--vyabsg-empty-command-suffix--':
                    cmd = ''
                self.commands.append(cmd)

        if 'label' in aliasInfo:
            if self.label.lower() == '--vyabsg-null-label--':
                self.label = ''
        else:
            if labelSource == 'command':
                self.label = self.commands[0].split(' ')[0] if len(self.commands) else ''
            else: #  labelSource == 'alias'
                self.label = self.primaryAlias

        self.final = Generic()
        self.final.primaryAlias = ' '.join([self.prefix.alias, self.primaryAlias]).strip(' ')
        self.final.label = '_'.join([self.prefix.label, self.label]).strip('_')
        self.final.commands = []
        for cmd in self.commands:
            if cmd[:3] == '<= ':
                newCmd = cmd[3:]
            else:
                newCmd = ' '.join([self.prefix.command, cmd]).strip(' ')
            self.final.commands.append(newCmd)
        self.command_snippet = [self.final.commands[0]] if self.final.commands and self.final.commands[0] else []
        self.final.execCommands = []
        self.argumentsMapper = {}
        for cmd in self.final.commands:
            startIdx = len(self.final.primaryAlias.split())
            pattern = r'(<[a-zA-Z0-9/-]+?>|\[[a-zA-Z0-9/-]+?\]|\.\.\.)'
            spans = [_.span() for _ in re.finditer(pattern, cmd)]
            spanIdxs = [_ for _ in enumerate(spans)]
            matchStrs = re.findall(pattern, cmd) # or [_.group(0) for _ in re.finditer(pattern, cmd)]
            for idx, span in spanIdxs[::-1]:
                matchStr = matchStrs[idx]
                if matchStr == '...':
                    assert(idx == len(spans) - 1)
                    consumed = [_ for _ in range(idx + startIdx, 10)]
                    self.argumentsMapper[matchStr] = consumed
                    cmd = cmd[:span[0]] + ' '.join([f'%{_}' for _ in consumed]) + cmd[span[1]:]
                else:
                    consumed = idx + startIdx
                    self.argumentsMapper[matchStr] = [consumed]
                    cmd = cmd[:span[0]] + f'%{consumed}' + cmd[span[1]:]
            self.final.execCommands.append(cmd)
        self.commandsStr = '\n'.join(self.final.execCommands)

        if 'snippet' in aliasInfo:
            snippet = aliasInfo['snippet']
            if snippet[:3] == '<= ':
                self.command_snippet = []
                snippet = snippet[3:]
            self.snippet = [snippet]
        else:
            self.snippet = []
        self.final.snippet = ' : '.join(self.command_snippet + self.snippet)
        for char in ['<', '>', '&']: # this escaping is not perfect. "<" should not be escaped
            self.final.snippet = self.final.snippet.replace(char, '^' + char)
        if not self.hasChildren:
            return
        assert(len(self.commands) <= 1)
        for subAliasInfo in aliasInfo['sub-aliases']:
            thisPrefix = Generic()
            thisPrefix.command = self.commands[0] if len(self.commands) else ''
            thisPrefix.alias = self.aliases[0]
            thisPrefix.label = self.label
            
            subPrefix = Generic()
            subPrefix.command = ' '.join([self.prefix.command, thisPrefix.command]).strip(' ')
            subPrefix.alias = self.final.primaryAlias
            subPrefix.label = self.final.label

            ac = VyAliasCommand(subAliasInfo, level=level+1, parent=self, 
                prefix=subPrefix, labelSource=labelSource)
            self.subAliases.append(ac)

    def __setattr__(self, attr, value):
        if attr in ['label']:
            self.aliasInfo[attr] = value
        else:
            super().__setattr__(attr, value)

    def __getattr__(self, attr):
        if attr == 'firstchild':
            if self.parent == None:
                return True
            elif self.parent.subAliases[0] == self:
                return True
            else:
                return False
        elif attr == 'lastchild':
            if self.parent == None:
                return True
            elif self.parent.subAliases[-1] == self:
                return True
            else:
                return False
        elif attr in ['aliases', 'commands', 'label']:
            return self.aliasInfo[attr]

    def traverse(self):
        self.traversalState = 'pre'
        yield self
        for subAlias in self.subAliases:
            for _ in subAlias.traverse():
                yield _
        self.traversalState = 'post'
        yield self

