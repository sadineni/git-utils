
class CommitInfo():

    def __init__(self, author, commit_message, jira, commit_date, sha, fix_versions):
        self.author = author
        self.commit_message = commit_message
        self.jira = jira
        self.commit_date = commit_date
        self.sha = sha
        self.fix_versions = fix_versions

    def __init__(self, author, commit_message, jira, commit_date, sha):
        self.author = author
        self.commit_message = commit_message
        self.jira = jira
        self.commit_date = commit_date
        self.sha = sha

    def __str__(self):
        return self.jira+'\t'+self.commit_date+'\t'+self.sha+'\t'+self.fix_versions+'\t'+self.author+'\t'+self.commit_message+'\t'

    def __eq__(self, other):
        return self.jira==other.jira

    def __hash__(self):
        return hash(('jira', self.jira))