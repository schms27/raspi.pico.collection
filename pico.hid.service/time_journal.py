import csv
import time
import os
from enum import Enum
from datetime import datetime

from util import resolvePath
from settings import Settings

class TimeJournalCommand(Enum):
    TOGGLE_PROJECT = 0
    TOGGLE_BREAK = 1

class TimeJournalKeywords(Enum):
    START = 0
    STOP = 1

class TimeJournal():
    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self.runningProjects = []

    def write_in_csv(self, rows):

        if not self.settings.hasSetting('time_journal_filepath'):
            return
        journalFilePath = resolvePath(self.settings.getSetting('time_journal_filepath'))
        journalBasePath = os.path.dirname(journalFilePath)
        if not os.path.exists(journalBasePath):
            os.makedirs(journalBasePath, exist_ok=True)

        # Opening the CSV file in read and
        # write mode using the open() module
        with open(journalFilePath, 'a+', newline='') as file:
  
            # creating the csv writer
            file_write = csv.writer(file)
    
            # Iterating over all the data in the rows 
            # variable
            for val in rows:

                # writing the data in csv file
                file_write.writerow(val)

    def write_with_timestamp(self, *msg):
        current_date_time = datetime.now()
        rows = []
        row = [current_date_time]
        for m in msg:
            row.append(m)
        
        rows.append(row)
        self.write_in_csv(rows)

    def toggleRunningProject(self, projectName) -> bool:
        if projectName in self.runningProjects:
            self.write_with_timestamp(projectName, TimeJournalKeywords.STOP.name)
            self.runningProjects.clear()
            return False
        
        for p in self.runningProjects:
            self.write_with_timestamp(p, TimeJournalKeywords.STOP.name)
        self.runningProjects.clear()
        self.runningProjects.append(projectName)
        self.write_with_timestamp(projectName, TimeJournalKeywords.START.name)
        return True

    def execCommand(self, action, key):
        command = action['command']
        if command == TimeJournalCommand.TOGGLE_PROJECT.name:
            self.toggleRunningProject(action['project_name'])
        elif command == TimeJournalCommand.TOGGLE_BREAK.name:
            self.toggleRunningProject('pause')
