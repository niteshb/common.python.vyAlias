from vyAliasBatchScriptGenerator.vyProcessVyAliasConfig import getFirstNonBlankLineIdx
import pytest

################################################################################
# Just blank lines
################################################################################
# Testing "Nothing" as input
testdata = [(None, 0), (0, 0), (1, 0), (2, 0)]
@pytest.mark.parametrize("num, expected", testdata)
def test_getFirstNonBlankLineIdx_noLines(num, expected):
    lines = []
    if num == None:
        idx = idx = getFirstNonBlankLineIdx(lines)
    else:
        idx = getFirstNonBlankLineIdx(lines, startIdx=num)
    assert idx == expected

################################################################################
# Single blank line
testdata = [(None, 1), (0, 1), (1, 1), (2, 1)]
@pytest.mark.parametrize("num, expected", testdata)
def test_getFirstNonBlankLineIdx_B(num, expected):
    lines = ['    ']
    if num == None:
        idx = idx = getFirstNonBlankLineIdx(lines)
    else:
        idx = getFirstNonBlankLineIdx(lines, startIdx=num)
    assert idx == expected

################################################################################
# Two blank lines
testdata = [(None, 2), (0, 2), (1, 2), (2, 2), (3, 2), (4, 2)]
@pytest.mark.parametrize("num, expected", testdata)
def test_getFirstNonBlankLineIdx_BB(num, expected):
    lines = ['    ', '     ']
    if num == None:
        idx = idx = getFirstNonBlankLineIdx(lines)
    else:
        idx = getFirstNonBlankLineIdx(lines, startIdx=num)
    assert idx == expected

################################################################################
# Not just blank lines
################################################################################
# One non-blank line
testdata = [(None, 0), (0, 0), (1, 1), (2, 1), ]
@pytest.mark.parametrize("num, expected", testdata)
def test_getFirstNonBlankLineIdx_F(num, expected):
    lines = ['   lorem ']
    if num == None:
        idx = idx = getFirstNonBlankLineIdx(lines)
    else:
        idx = getFirstNonBlankLineIdx(lines, startIdx=num)
    assert idx == expected

################################################################################
# Two non blank lines
testdata = [(None, 0), (0, 0), (1, 1), (2, 2), (3, 2), ]
@pytest.mark.parametrize("num, expected", testdata)
def test_getFirstNonBlankLineIdx_FF(num, expected):
    lines = ['   lorem ', '   ipsum ', ]
    if num == None:
        idx = idx = getFirstNonBlankLineIdx(lines)
    else:
        idx = getFirstNonBlankLineIdx(lines, startIdx=num)
    assert idx == expected

################################################################################
# A blank line followed by 2 non-blank lines
testdata = [(None, 1), (0, 1), (1, 1), (2, 2), (3, 3), (4, 3)]
@pytest.mark.parametrize("num, expected", testdata)
def test_getFirstNonBlankLineIdx_BFF(num, expected):
    lines = ['     ', '   lorem ', '   ipsum ', ]
    if num == None:
        idx = idx = getFirstNonBlankLineIdx(lines)
    else:
        idx = getFirstNonBlankLineIdx(lines, startIdx=num)
    assert idx == expected

testdata = [
    (None, 2), # default startIdx
    (0, 2), (1, 2), (2, 2), (3, 3), (4, 4), (5, 8), (6, 8), (7, 8),
    (8, 8), (9, 9), (10, 10), (11, 14), (12, 14), (13, 14), (14, 14), 
    (15, 14), (16, 14),
]
################################################################################
# 
@pytest.mark.parametrize("num, expected", testdata)
def test_getFirstNonBlankLineIdx_BBFFFBBBFFFBBB(num, expected):
    lines = [
        '     ', '     ', '   lorem 2 ', '   ipsum 3 ', 
        '   lorem 4 ', '     ', '     ', '     ', 
        '   ipsum 8', '   lorem 9', '   ipsum 10', '     ', 
        '     ', '     ', 
    ]
    if num == None:
        idx = idx = getFirstNonBlankLineIdx(lines)
    else:
        idx = getFirstNonBlankLineIdx(lines, startIdx=num)
    assert idx == expected

