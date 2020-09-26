from vyAliasBatchScriptGenerator import vyAliasBatchScriptGenerator

from input.aliasInfos import aliasInfos
from input.envVarInfos import envVarInfos
from input.subTemplates import cmdTemplates, envVarTemplates
inputFolder = 'input'
outputFolder = r'P:\@common\misc\vyGit'

absg = vyAliasBatchScriptGenerator(aliasInfos, envVarInfos, cmdTemplates, envVarTemplates, inputFolder, outputFolder)
absg.generate()
