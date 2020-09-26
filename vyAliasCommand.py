import re

stars80 = '*' * 80
class Generic():
    pass

class vyAliasCommandsTree():
    def __init__(self, aliasInfos):
        assert(len(aliasInfos) == 1)
        aliasInfo = aliasInfos[0]
        #assert(aliasInfo[0] == [])
        assert('sub-aliases' in aliasInfo[2])
        self.root = vyAliasCommand(*aliasInfo)
    
    def traverse(self):
        return self.root.traverse()

rootPrefix = Generic()
rootPrefix.command = ''
rootPrefix.alias = ''
rootPrefix.label = ''

class vyAliasCommand():
    def __init__(self, aliases, commands, aliasDict, 
        level=0, parent=None,
        prefix=rootPrefix):
        self.aliases = aliases
        self.commands = commands
        self.aliasDict = aliasDict
        self.level = level
        self.parent = parent
        self.prefix = prefix
        self.subAliases = []
        self.hasChildren = False
        keys = aliasDict.keys()

        self.primaryAlias = aliases[0]
        self.verb = commands[0].split(' ')[0] if len(commands) else None
        self.label = aliasDict['label'] if 'label' in keys else self.verb
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
            #moi = re.finditer(pattern, cmd)
            spans = [_.span() for _ in re.finditer(pattern, cmd)]
            spanIdxs = [_ for _ in enumerate(spans)]
            matchStrs = re.findall(pattern, cmd) # or [_.group(0) for _ in re.finditer(pattern, cmd)]
            for idx, span in spanIdxs[::-1]:
                #span = mo.span()
                #matchStr = mo.group()
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
            #print([mo.group(idx) for idx in range(mo.groups())])
        self.commandsStr = '\n'.join(self.final.execCommands)

        if 'snippet' in keys:
            snippet = aliasDict['snippet']
            if snippet[:3] == '<= ':
                self.command_snippet = []
                snippet = snippet[3:]
            self.snippet = [snippet]
        else:
            self.snippet = []
        self.final.snippet = ' : '.join(self.command_snippet + self.snippet)
        for char in ['<', '>', '&']: # this escaping is not perfect. "<" should not be escaped
            self.final.snippet = self.final.snippet.replace(char, '^' + char)
        print(stars80)
        print(self.aliases, "'%s'" % self.final.primaryAlias, self.label)
        if 'sub-aliases' not in keys:
            return
        assert(len(commands) <= 1)
        self.hasChildren = True
        for aliasInfo in aliasDict['sub-aliases']:
            thisPrefix = Generic()
            thisPrefix.command = self.commands[0] if len(self.commands) else ''
            thisPrefix.alias = self.aliases[0]
            thisPrefix.label = self.label
            
            subPrefix = Generic()
            subPrefix.command = ' '.join([self.prefix.command, thisPrefix.command]).strip(' ')
            subPrefix.alias = self.final.primaryAlias
            subPrefix.label = self.final.label

            ac = vyAliasCommand(*aliasInfo, level=level+1, parent=self, 
                prefix=subPrefix)
            self.subAliases.append(ac)

    def __getattr__(self, attr):
        if attr == 'lastchild':
            if self.parent == None:
                return True
            elif self.parent.subAliases[-1] == self:
                return True
            else:
                return False

    def traverse(self):
        self.traversalState = 'pre'
        yield self
        for subAlias in self.subAliases:
            for _ in subAlias.traverse():
                yield _
        self.traversalState = 'post'
        yield self

