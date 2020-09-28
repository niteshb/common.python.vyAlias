envVarInfos = [
    # (SUFFIX, default, {[target], [Target]})
    ('REMOTE', {'default': 'github', }),
    ('BRANCH', {'default': 'master', }),
]

aliasInfosLevel1 = [
    (
        ['h', '', '-h', '--help'], 
        [],
        {
            'label': 'help',
            'snippet': 'This help message',
        },
    ),
    (
        ['a'], 
        ['add <file1> [file2] [file3] ...'],
        {},
    ),
    (
        ['cm'],
        ['commit -m <msg>'],
        {
            'snippet': 'Commits staged with message provided',
            'label': 'commit_message',
        },
    ),
    (
        ['c'],
        ['commit'],
        {
            'sub-aliases' : [
                (
                    [''], 
                    [''],
                    {
                        'snippet': 'Opens your editor for commit message',
                        'label': 'staged',
                    },
                ),
                (
                    ['a'], 
                    ['-a'],
                    {
                        'snippet': 'Stages all & opens your editor for commit message',
                        'label': 'all',
                    },
                ),
                (
                    ['fix', 'amend'],
                    ['--amend'],
                    {
                        'snippet': 'Change your previous commit message',
                        'label': 'amend',
                    },
                ),
            ],
        },
    ),
    (
        ['s'], 
        ['status'],
        {},
    ),
    (
        ['ss'],
        ['status -s'],
        {
            'label': 'status_short'
        },
    ),
    (
        ['pl'], 
        ['pull --rebase %VY_GIT_CMD_REMOTE% %VY_GIT_CMD_BRANCH%'],
        {},
    ),
    (
        ['ps'], 
        ['push %VY_GIT_CMD_REMOTE% %VY_GIT_CMD_BRANCH%'],
        {},
    ), 
    (
        ['l'], 
        ['log'],
        {},
    ),
    (
        ['l1'], 
        ['log --oneline'],
        {
            'label': 'log_oneline',
        },
    ),
    (
        ['r'], 
        [],
        {
            'label': 'remote',
            'sub-aliases': [
                (
                    ['', 'l', 'list'], 
                    ['remote -v'],
                    {
                        'label': 'list',
                    },
                ),
                (
                    ['s', 'set'], 
                    ['remote set-url %VY_GIT_CMD_REMOTE% <repo-url>'],
                    {
                        'label': 'set',
                    },
                ),
                (
                    ['a'], 
                    [
                        'remote add %VY_GIT_CMD_REMOTE% <repo-url>',
                        'config branch.%VY_GIT_CMD_BRANCH%.remote %VY_GIT_CMD_REMOTE%',
                        'config branch.%VY_GIT_CMD_BRANCH%.merge refs/heads/%VY_GIT_CMD_BRANCH%',
                    ],
                    {
                        'label': 'add',
                        'snippet': 'Also sets %VY_GIT_CMD_REMOTE% as default remote for branch %VY_GIT_CMD_BRANCH%',
                    },
                ),
            ]
        },
    ),
    (
        ['us'],
        ['restore --staged <file1> [file2] [file3] ...'],
        {
            'label': 'unstage',
            'snippet': 'Unstage files',
        },
    ),
    (
        ['rm'],
        ['rm <file1> [file2] [file3] ...'],
        {
            'label': 'delete',
            'snippet': 'Delete files',
        },
    ),
    (
        ['i'],
        ['init'],
        {},
    ),
    (
        ['cl'],
        ['clone <repo-url> [target-dir]'],
        {},
    ),
    (
        ['b'],
        ['branch'],
        {
            'sub-aliases' : [
                (
                    ['', 'l', 'list'],
                    ['-a'],
                    {
                        'snippet': 'List all branches',
                        'label': 'list',
                    },
                ),
                (
                    ['sw'],
                    [
                        '<= git switch <branch>',
                        '<= set VY_GIT_CMD_BRANCH=<branch>',
                    ],
                    {
                        'label': 'switch',
                    },
                ),
                (
                    ['csw'],
                    [
                        '<= git switch -c <branch>',
                        '<= set VY_GIT_CMD_BRANCH=<branch>',
                    ],
                    {
                        'snippet': 'Create & switch branch',
                        'label': 'create_switch',
                    },
                ),
                (
                    ['c'],
                    ['<branch>'],
                    {
                        'snippet': 'Create branch',
                        'label': 'create',
                    },
                ),
                (
                    ['rm', 'del'],
                    ['-d <branch>'],
                    {
                        'snippet': 'Delete merged branch',
                        'label': 'delete',
                    },
                ),
                (
                    ['delU'],
                    ['-D <branch>'],
                    {
                        'snippet': 'Delete unmerged branch',
                        'label': 'delete_unmerged',
                    },
                ),
                (
                    ['ren'],
                    ['-m <old-branch-name> <new-branch-name>'],
                    {
                        'snippet': 'Rename unmerged branch',
                        'label': 'rename',
                    },
                ),
            ],
        },
    ),
    (
        ['df', 'dif', 'diff'],
        ['difftool --no-prompt <file/folder>'],
        {},
    ),
    (
        ['con'],
        ['config'],
        {
            'sub-aliases': [
                (
                    ['vsc'],
                    [
                        '--global core.editor "code --wait"',
                        '--global merge.tool vscode',
                        '--global mergetool.vscode.cmd "code --wait $MERGED"',
                        '--global diff.tool vscode',
                        '--global difftool.vscode.cmd "code --wait --diff $LOCAL $REMOTE"',
                    ],
                    {
                        'snippet': '<= Configure VSCode as git editor, difftool & mergetool', # <= in the beginning kills command snippet
                        'label': 'vscode',
                    },
                ),
                (
                    ['so'],
                    ['--show-origin'],
                    {
                        'label': 'show_origin',
                        'sub-aliases': [
                            (
                                [''],
                                ['--list'],
                                {
                                    'label': 'list',
                                },
                            ),
                            (
                                # want to keep blank alias
                                # distinction from previous to come due to argument availability, TODO: script to identify this distinction
                                ['i'],
                                ['<item>'],
                                {
                                    'label': 'item',
                                },
                            ),
                        ],
                    },
                ),
            ],
        },
    ),
]

aliasInfos = [
    (
        ['g'],
        ['git'],
        {
            'label': '',
            'sub-aliases' : aliasInfosLevel1,
        }
    )
]
