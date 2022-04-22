from repo_util import *
def baseline1():
    print("baseline 1:")
    # [Vi-1, Vi+1]
    repo = RepoUtil.get_repo(github_url='https://github.com/apache/tomcat',path='./repo')
    tags = repo.tags
    print(tags)

def baseline2():
    print("baseline 2:")

def baseline3():
    print("baseline 3:")

if __name__ == '__main__':
    baseline1()