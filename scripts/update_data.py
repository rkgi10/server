"""
Installs the most up to date genome data on the file system that
is required for development
"""
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os
import tarfile
import time

import utils


dataDirPath = 'ga4gh-example-data'
zipFilePath = 'ga4gh-example-data.tar.gz'
archivePath = 'ga4gh-example-data-archive'


def archiveExistingData():
    paths = [dataDirPath, zipFilePath]
    archiveExists = os.path.exists(archivePath)
    archiveFolderCreated = False
    for path in paths:
        resourceExists = os.path.exists(path)
        if resourceExists:
            if not archiveExists:
                os.mkdir(archivePath)
                archiveExists = True
            if not archiveFolderCreated:
                archiveFolderName = time.ctime().replace(' ', '_')
                archiveFolderPath = os.path.join(
                    archivePath, archiveFolderName)
                os.mkdir(archiveFolderPath)
                archiveFolderCreated = True
            newPath = os.path.join(archiveFolderPath, path)
            utils.log("Archiving '{}' to '{}'".format(path, newPath))
            os.rename(path, newPath)
    utils.log("Archiving finished")


def downloadData():
    url = "http://www.well.ox.ac.uk/~jk/ga4gh-example-data.tar.gz"
    fileDownloader = utils.FileDownloader(url, zipFilePath)
    fileDownloader.download()
    utils.log("Downloading finished")


def extractData():
    utils.log("Extracting {}".format(zipFilePath))
    tar = tarfile.open(zipFilePath)
    tar.extractall()
    tar.close()
    utils.log("Extracting finished")


@utils.Timed()
def main():
    archiveExistingData()
    downloadData()
    extractData()


if __name__ == '__main__':
    main()
