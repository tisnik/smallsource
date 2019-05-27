from stackapi import StackAPI
import re

class SOFetcher(object):
    def __init__(self, s_tags, s_timestamp=1217648155, s_pagesize=100, s_order='asc', s_sort='creation'):
        self.s_tags = s_tags
        self.s_timestamp = s_timestamp
        self.s_pagesize = s_pagesize
        self.s_order = s_order
        self.s_sort = s_sort
        self.posts = []
        
    def __str__(self):
        return self.posts

    def load(self):
        SITE = StackAPI('stackoverflow')
        data = SITE.fetch('questions', filter='!-y(KwOdKQqjehDBmb0h5Opw_j44BmcMCwAOxyvp5P', pagesize=s_pagesize, fromdate=s_pagesize, order=s_order, sort=s_sort, tagged=s_tags)
        questions = []

        for i in data['items']:
            if(i['answer_count'] > 0):
                qid = i['question_id']
                closed = 0
                ans = []
                if('closed_date' in i):
                    closed = i['closed_date']
                
                if not any(qid in x for x in questions):
                    for x in i['answers']:
                        body = re.findall('<code>(.*?)<\/code>', x['body'])
                        if body:
                            ans.append([x['answer_id'], x['question_id'], x['score'], body])
                    if ans:
                        questions.append([qid, i['title'], i['last_activity_date'], closed, ans])

        self.posts = questions
        return questions