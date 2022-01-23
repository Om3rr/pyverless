from pprint import pprint

from framework import framework as sls
import functions
import resources

resources.DbAlarm(
    sls,
    "DatabaseSampleName",
    "DatabaseSampleArn",
    "SNSAlarmARN"
)

resources.DbAlarm(
    sls,
    "OtherDatabaseName",
    "OtherDatabaseSampleArn",
    "SNSAlarmARN"
)
