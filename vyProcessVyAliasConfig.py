import re
from pprint import pprint
from vyDebug import vyDebug, vyDebugLevel

vyd = vyDebug(vyDebugLevel.SILENT)
vyd.setLevel(0)

def getNextNonBlankLineIdx(lines, startIdx=0):
    for idx in range(startIdx, len(lines)):
        line = lines[idx].strip()
        if not line:
            continue
        return idx

def processAliasLinesRoot(lines, startIdx, indent=None):
    if indent == None:
        indent = re.search('^ *', lines[startIdx + 1]).group(0)
    idx, aliasInfos = processAliasLines(lines, startIdx, indent, level=0)
    return idx, aliasInfos, indent

def processAliasLines(lines, startIdx, indent, level=0):
    idx = startIdx
    numLines = len(lines)
    aliasInfos = []
    while idx < numLines:
        rline = lines[idx].rstrip() # right clean line
        cline = lines[idx].strip() # clean line
        rlen = len(rline)
        clen = len(cline)
        curIndent = rline[0:rlen - clen]
        # check if indent is as expected
        if len(curIndent) % len(indent) != 0:
            raise Exception('Bad indent')
        indents = len(curIndent) // len(indent)
        if indents == 2 * level:
            state = 'aliases'
            if level == 0:
                if len(aliasInfos): # there can be only one root. it is time to return
                    idx -= 1
                    break
        elif indents > 2 * level + 2:
            raise Exception('Too much indent')
        elif indents < 2 * level:
            idx -= 1
            break
        if cline == '': # got a new line
            idx -= 1
            break
        vyd.print3(rline)
        if state == 'aliases':
            aliases = ['' if alias.strip().lower() == '--vyabsg-null-alias--' else alias.strip() for alias in cline.split(',')]
            aliasInfo = (aliases, [], {})
            aliasInfos.append(aliasInfo)
            prepend = '\n' if vyd.level > 1 else ''
            vyd.print1(prepend + indent * level, '    %10s:' % 'aliases', aliases)
            state = 'post-aliases'
        elif state == 'post-aliases':
            if curIndent == indent * (2 * level + 1): # command, label, help
                for attr in ['label', 'snippet']:
                    if val := findAtrribute(attr, cline):
                        if attr == 'label' and val.lower() == '--vyabsg-null-label--':
                            val = ''
                        aliasInfo[2][attr] = val
                        vyd.print2(indent * level, '    %10s:' % attr, '"%s"' % val)
                        break
                if val == None:
                    cmd = cline
                    if not cmd == '--vyabsg-no-command--':
                        if cmd == '--vyabsg-empty-command-suffix--':
                            cmd = ''
                        aliasInfo[1].append(cmd)
                        vyd.print2(indent * level, '    %10s:' % 'command', '"%s"' % cmd)
                    else:
                        vyd.print2(indent * level, '    %10s:' % 'command', '--no-cmd--')
            elif curIndent == indent * 2 * (level + 1): # subaliases
                idx, subAliasInfos = processAliasLines(lines, idx, indent=indent, level=level+1)
                aliasInfo[2]['sub-aliases'] = subAliasInfos
            else:
                raise Exception('post-alias state without alias state')
        idx += 1
    # do some checking if it is fine
    return idx, aliasInfos

def findAtrribute(attr, txt):
    if mo:=re.search(r'^%s\s*:\s*(.*)' % attr, txt):
        return mo.group(1)
    return None

def processEnvVarLines(lines, startIdx, indent):
    if indent == None:
        indent = re.search('^ *', lines[startIdx + 1]).group(0)
    idx = startIdx
    numLines = len(lines)
    envVarInfos = []
    while idx < numLines:
        rline = lines[idx].rstrip() # right clean line
        cline = lines[idx].strip() # clean line
        if cline == '': # got a new line
            idx -= 1
            break
        rlen = len(rline)
        clen = len(cline)
        curIndent = rline[0:rlen - clen]
        if len(curIndent) % len(indent) != 0:
            raise Exception('Bad indent')
        indents = len(curIndent) // len(indent)

        if indents == 0:
            state = 'envvar'
        elif indents > 1:
            raise Exception('Too much indent')

        if state == 'envvar':
            if envName := findAtrribute('envvar', cline):
                envVarInfo = (envName, {})
                envVarInfos.append(envVarInfo)
                state = 'default'
                vyd.print1('    %10s:' % 'envvar', '"%s"' % envName)

            else:
                idx -= 1
                break # at this indent if you didn't get envvar, it must be a root
        else:
            assert(indents == 1)
            if state == 'default':
                if default := findAtrribute('default', cline):
                    envVarInfo[1]['default'] = default
                    state = 'post-default'
                    vyd.print2('        %10s:' % 'default', '"%s"' % default)
                else:
                    raise Exception('Expected default')
            elif state == 'post-default':
                for attr in ['target', 'Targets']:
                    if val := findAtrribute(attr, cline):
                        envVarInfo[1][attr] = val
                        vyd.print2('        %10s:' % attr, '"%s"' % val)
                        break
                if val == None:
                    raise Exception('Unexpected state')
        idx += 1
    return idx, envVarInfos, indent

def vyProcessVyAliasConfig(configFilePath):
    # ok to have blank lines in the beginning, in between sections & in the end
    lines = open(configFilePath, 'r').readlines()
    #lines = lines[:13]
    idx = 0
    numLines = len(lines)
    foundAliasInfoRoot = False
    foundEnvVars = False
    indent = None
    envVarInfos = []
    while idx < numLines:
        idx = getNextNonBlankLineIdx(lines, idx)
        line = lines[idx].rstrip()
        vyd.print5(line)
        if line != line.strip():
            vyd.print0(f'line({idx+1}): ', line)
            raise Exception('A section must start unindented')
        if line.startswith('envvar:'):
            if foundEnvVars == True:
                raise Exception('Keep your env vars together')
            foundEnvVars = True
            idx, envVarInfos, indent = processEnvVarLines(lines, idx, indent)
        else:
            if foundAliasInfoRoot == True:
                raise Exception('Keep your env vars together')
            foundAliasInfoRoot = True
            idx, aliasInfos, indent = processAliasLinesRoot(lines, idx, indent)
        idx += 1
    return aliasInfos, envVarInfos
