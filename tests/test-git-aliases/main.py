from vyAliasBatchScriptGenerator import vyAliasBatchScriptGenerator
import argparse

parser = argparse.ArgumentParser(description='Generate an alias Windows batch file')
parser.add_argument('ConfigFilePath', help='Path to the input config file')
parser.add_argument('-o', help='Path to the output folder', default='.', dest='OutputFolder', metavar='OutputFolder')
parser.add_argument('-f', help='Output Filename. NOT RECOMMENDED. Script auto-generates it', default=None, dest='OutputFileName', metavar='OutputFileName')
args = parser.parse_args()

configFilePath = args.ConfigFilePath
outputFolder = args.OutputFolder
outputFileName = args.OutputFileName

vyAliasBatchScriptGenerator(configFilePath, outputFolder, outputFileName)
