import unittest
import json
from server import SlackBot

class SlackBotTest(unittest.TestCase):

    def setUp(self):
        self.bot = SlackBot()

    def assertIsJSONSame(self,actual_json,expected_json):
        for actual,expected in zip(actual_json,expected_json):
            if actual['title'] != expected['title'] or actual['title_link'] != expected['title_link']:
                return False
        return True

    def test_parse_message_jira_only(self):
        self.message=[]
        self.message.append(json.loads('{"text":"SLAC-324","channel":"1234"}'))
        jiras_list = self.bot.parse_slack_incoming_message(self.message)
        expected_list=[['SLAC-324','1234']]
        self.assertEqual(jiras_list,expected_list)

    def test_parse_message_jira_at_end(self):
        self.message=[]
        self.message.append(json.loads('{"text":"jira number SLAC-3","channel":"1234"}'))
        jiras_list = self.bot.parse_slack_incoming_message(self.message)
        expected_list=[['SLAC-3','1234']]
        self.assertEqual(jiras_list,expected_list)

    def test_parse_message_jira_at_begining(self):
        self.message=[]
        self.message.append(json.loads('{"text":"SLAC-22 is opened against slack hq team","channel":"3455"}'))
        jiras_list = self.bot.parse_slack_incoming_message(self.message)
        expected_list=[['SLAC-22','3455']]
        self.assertEqual(jiras_list,expected_list)

    def test_parse_message_jira_in_middle(self):
        self.message=[]
        self.message.append(json.loads('{"text":"Jira number SLAC-1 is resolved","channel":"3455"}'))
        jiras_list = self.bot.parse_slack_incoming_message(self.message)
        expected_list=[['SLAC-1','3455']]
        self.assertEqual(jiras_list,expected_list)

    def test_build_valid_url(self):
        jira="SLAC-1"
        expected_url = self.bot.JIRA_BASE_URL+"browse/"+jira
        jira_url = self.bot.build_url(jira)
        self.assertEqual(jira_url,expected_url)

    def test_build_invalid_url(self):
        jira=""
        expected_url = self.bot.JIRA_BASE_URL+"browse/"+jira
        jira_url = self.bot.build_url(jira)
        self.assertNotEqual(jira_url,expected_url)

    def test_build_null_url(self):
        jira=None
        expected_url = self.bot.JIRA_BASE_URL+"browse/"
        jira_url = self.bot.build_url(jira)
        self.assertNotEqual(jira_url,expected_url)
    def tearDown(self):
        self.bot = None




if __name__ == "__main__":
    unittest.main()

