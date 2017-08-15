from slackclient import SlackClient
import os
import time
import re
import json
import requests
from requests.auth import HTTPBasicAuth

class SlackBot(object):

    SLACK_BOT_TOKEN=os.environ.get('SLACK_BOT_TOKEN')
    JIRA_BASE_URL=os.environ.get('JIRA_BASE_URL')
    JIRA_ISSUE_FORMAT=os.environ.get('JIRA_ISSUE_FORMAT')
    JIRA_REST_PATH=os.environ.get('JIRA_REST_PATH')
    JIRA_ISSUE_PATH=os.environ.get('JIRA_ISSUE_PATH')
    JIRA_USERNAME=os.environ.get('JIRA_USERNAME')
    JIRA_PASSWORD=os.environ.get('JIRA_PASSWORD')
    WAIT_TIME=os.environ.get('WAIT_TIME')

    def __init__(self):
        self.slack_client = SlackClient(SlackBot.SLACK_BOT_TOKEN)

    def connectToSlack(self):
        if self.slack_client.rtm_connect():
            print("Spark-Jira Bot connected and running")
            while True:
                message = self.slack_client.rtm_read()
                jira_issues=self.parse_slack_incoming_message(message)
                if jira_issues and len(jira_issues)>0:
                    self.post_jira_issues_url(jira_issues)
                time.sleep(SlackBot.WAIT_TIME)
        else:
            print("Unable to connect to Slack. Check your SLACK_BOT_TOKEN "+SlackBot.SLACK_BOT_TOKEN)


    def parse_slack_incoming_message(self,slack_incoming_messages):
        '''Parse the slack messages received from slack rtm api and get the text and channel from it'''
        if slack_incoming_messages and len(slack_incoming_messages)>0:
            jira_issue_channel_list=[]
            for slack_incoming_message in slack_incoming_messages:
                if slack_incoming_message and 'text' in slack_incoming_message and 'bot_id' not in slack_incoming_message:
                    jiras = re.findall(SlackBot.JIRA_ISSUE_FORMAT,slack_incoming_message["text"])
                    for jira in jiras:
                        print("Found a jira issue in the message: "+str(jira))
                        jira_issue_channel_list.append([jira,slack_incoming_message['channel']])
            return jira_issue_channel_list
        return None

    def post_jira_issues_url(self,jira_issues):
        '''Builds jira issue url and post it using slack api'''
        for jira_issue in jira_issues:
            response = self.build_url(jira_issue[0])
            attachments = self.build_attachments(response,jira_issue[0])
            self.slack_client.api_call("chat.postMessage",channel=jira_issue[1],attachments=attachments,as_user=True)

    def build_url(self,jira):
        if jira is None or not jira:
            return None
        return self.JIRA_BASE_URL+"browse/"+str(jira)

    def build_attachments(self,jira_web_url,jira):
        '''Build Attachments'''
        attachments={}
        attachments['title']=jira
        attachments['title_link']=jira_web_url
        fields = self.build_fields(jira)
        field_json={}
        field_json['title']="Assignee"
        field_json['value']=fields[0]
        field_json['short']=True
        field_json_status={}
        field_json_status['title']="Status"
        field_json_status['value']=fields[1]
        field_json_status['short']=True
        attachments['fields']=[field_json,field_json_status]
        return [attachments]

    def build_fields(self,jira):
        response = requests.get(SlackBot.JIRA_BASE_URL+SlackBot.JIRA_REST_PATH+SlackBot.JIRA_ISSUE_PATH+jira,headers={'Content-Type': 'application/json'},verify=False,auth=HTTPBasicAuth(SlackBot.JIRA_USERNAME,SlackBot.JIRA_PASSWORD))
        jira_json = response.json()
        jira_fields_json = jira_json['fields']
        if jira_fields_json['assignee']:
            assignee= jira_fields_json['assignee']['displayName']
        else:
            assignee = "Unassigned"
        status = jira_fields_json['status']['name']
        return [assignee,status]




if __name__ == "__main__":
    client = SlackBot()
    client.connectToSlack()







