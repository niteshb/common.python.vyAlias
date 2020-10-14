import re
from vyConfigFileParser import VyConfigFileBlock
import vyConsoleEscapes as vce

class Generic():
    pass
rootPrefix = Generic()
rootPrefix.command = ''
rootPrefix.alias = ''
rootPrefix.label = ''

class VyAliasBlock(VyConfigFileBlock):
    def process(self, prefix, configInfos):
        self.prefix = prefix
        attribs = self.attribs

        self.aliases = ['' if alias.strip().lower() == '--vyabsg-null-alias--' else alias.strip() for alias in self.aliases.split(',')]
        self.primaryAlias = self.aliases[0]

        rawCommands = attribs['commands'] if 'commands' in attribs else []
        self.commands = []
        for cmd in rawCommands:
            if cmd != '--vyabsg-no-command--':
                if cmd == '--vyabsg-empty-command-suffix--':
                    cmd = ''
                self.commands.append(cmd)

        if 'label' in attribs:
            if self.label.lower() == '--vyabsg-null-label--':
                self.label = ''
        else:
            if configInfos['label-source'] == 'command':
                self.label = self.commands[0].split(' ')[0] if len(self.commands) else ''
            else: #  configInfos['label-source'] == 'alias'
                self.label = self.primaryAlias

        self.final = Generic()
        self.final.primaryAlias = ' '.join([self.prefix.alias, self.primaryAlias]).strip(' ')
        self.final.aliasSnippet = '{0:<11}'.format(self.final.primaryAlias)
        if 'color-alias' in configInfos:
            self.final.aliasSnippet = vce.format(self.final.aliasSnippet, fgColor=configInfos['color-alias'])

        self.final.label = '_'.join([self.prefix.label, self.label]).strip('_')
        self.final.commands = []
        for cmd in self.commands:
            if cmd[:3] == '<= ':
                newCmd = cmd[3:]
            else:
                newCmd = ' '.join([self.prefix.command, cmd]).strip(' ')
            self.final.commands.append(newCmd)
        
        # set up command-snippet
        if self.final.commands and self.final.commands[0]:
            cmdSnippet = self.final.commands[0]
            if 'color-command' in configInfos:
                cmdSnippet = vce.format(cmdSnippet, fgColor=configInfos['color-command'])
            self.command_snippet = [cmdSnippet]
        else:
            self.command_snippet = []

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

        if 'snippet' in attribs:
            snippet = attribs['snippet']
            if snippet[:3] == '<= ':
                self.command_snippet = []
                snippet = snippet[3:]
            if 'color-snippet' in configInfos:
                snippet = vce.format(snippet, fgColor=configInfos['color-snippet'])
            self.snippet = [snippet]
        else:
            self.snippet = []
        self.final.snippet = ' : '.join(self.command_snippet + self.snippet)
        for char in ['<', '>', '&']: # this escaping is not perfect. "<" should not be escaped
            self.final.snippet = self.final.snippet.replace(char, '^' + char)
        if not self.hasChildren:
            return
        assert(len(self.commands) <= 1)
        for subAliasBlock in self.subAliasBlocks:
            thisPrefix = Generic()
            thisPrefix.command = self.commands[0] if len(self.commands) else ''
            thisPrefix.alias = self.aliases[0]
            thisPrefix.label = self.label
            
            subPrefix = Generic()
            subPrefix.command = ' '.join([self.prefix.command, thisPrefix.command]).strip(' ')
            subPrefix.alias = self.final.primaryAlias
            subPrefix.label = self.final.label

            subAliasBlock.process(subPrefix, configInfos)

    def __setattr__(self, attr, value):
        if attr in ['label']:
            self.attribs[attr] = value
        else:
            super().__setattr__(attr, value)

    def __getattr__(self, attr):
        if attr == 'subAliasBlocks':
            return self.subBlocks
        elif attr in ['aliases', 'commands', 'label']:
            return self.attribs[attr]
        return super().__getattr__(attr)
