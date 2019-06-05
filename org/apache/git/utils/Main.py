# First create a Github instance:
import os
import CommitInfo
import csv
import requests
import sys
import ConfigParser

def extractJira(commit_string):
    if commit_string.startswith('Revert'):
        commit_string = commit_string[8:len(commit_string)]

    jira = commit_string[0:commit_string.find('.', 0)]
    if len(jira) > 10:
        jira = jira[0:commit_string.find('-', 0)] + jira[commit_string.find('-', 0):10]
    jira = jira.replace(':', '')
    jira = jira.replace(' ', '-')
    if jira.endswith('-'):
        jira = jira[0:len(jira) - 1]
    return jira


def extractFixVersion(response_data):
    # print response_data.json()
    if 'fixVersions' in response_data.json()['issues'][0]['fields']:
        if (len(response_data.json()['issues'][0]['fields']['fixVersions']) != 0):
            return response_data.json()['issues'][0]['fields']['fixVersions'][0]['name']
        else:
            return "NONE"
    else:
        return "NONE"


def readCSVFileAndExecuteJiraAPI(csvRecords):
    commitInfoList = set()
    print"------------------------------------------------------------------------------------------------------------------------"
    for row in csvRecords:
        commitInfo = CommitInfo.CommitInfo(row[0], row[3], extractJira(row[3]), row[2], row[1])
        try:
            response_data = requests.get('https://issues.apache.org/jira/rest/api/2/search?jql=id=' + commitInfo.jira)
            commitInfo.fix_versions = extractFixVersion(response_data)
            commitInfoList.add(commitInfo)
            print commitInfo
        except:
            print "exception while parsing row ", row
            pass
    # print "Commit info size ", len(commitInfoList)
    print "------------------------------------------------------------------------------------------------------------------------"
    return commitInfoList


def executeGitLog(projectRootDirectory, command, outputFile):
    os.chdir(projectRootDirectory)
    os.system(command)
    csvFile = open(outputFile)
    csvRecords = csv.reader(csvFile, delimiter=',')
    return readCSVFileAndExecuteJiraAPI(csvRecords)


if __name__ == '__main__':
    if (len(sys.argv) == 1):
        print "Mandatory properties file path missing in arguments"
        sys.exit(2)

    propertiesFilePath = sys.argv[1]
    config = ConfigParser.RawConfigParser()
    config.read(propertiesFilePath)
    projectRootDirectory = config.get("Base", "projectRootDirectory")
    atsProjectDirectories = config.get("Base", "directoryPathsToVerify").split(",")
    branch1 = config.get("Base", "branch1")
    branch2 = config.get("Base", "branch2")
    afterDate = config.get("Base", "afterDate")

    for path in atsProjectDirectories:
        outputFile = '/tmp/trunk_diff.log'
        command = 'git log --pretty=format:"%cn,%h,%cd,%s" --after="' + afterDate + '" ' + branch1 + '..' + branch2 + ' ' + path + ' | grep -i -v SUBMARINE > ' + outputFile
        commitList = executeGitLog(projectRootDirectory, command, outputFile)
        print "Records returned size at " + path, len(commitList)
