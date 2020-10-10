import os
import filecmp
from vyAlias import vyAliasBatchScriptGenerator

testFolder = os.path.dirname(os.path.realpath(__file__))

def test_001_simple():
    aliasConfigFilePath = os.path.join(testFolder, 'input/001_simple.vyalias')
    outputFolder = os.path.join(testFolder, 'output')
    refOutputFolder = os.path.join(testFolder, 'reference-output')
    outputFilePath, outputFileName = vyAliasBatchScriptGenerator(aliasConfigFilePath, outputFolder)
    refOutputFilePath = os.path.join(refOutputFolder, outputFileName)
    comparison = filecmp.cmp(outputFilePath, refOutputFilePath)
    assert(comparison == True)
