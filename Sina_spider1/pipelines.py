# encoding=utf-8
import pymongo
from items import InformationItem, TweetsItem, FollowsItem, FansItem, ReposterItem, NameItem


class MongoDBPipleline(object):
    def __init__(self):
        clinet = pymongo.MongoClient("localhost", 27017)
        db = clinet["Sina"]
        self.Information = db["Information"]
        self.Tweets = db["Tweets"]
        self.Follows = db["Follows"]
        self.Fans = db["Fans"]
        self.Reposters = db["Reposters"]
        self.Names = db["Names"]

    def process_item(self, item, spider):
        """ 判断item的类型，并作相应的处理，再入数据库 """
        if isinstance(item, InformationItem):
            try:
                self.Information.insert(dict(item))
            except Exception:
                pass
        elif isinstance(item, TweetsItem):
            try:
                self.Tweets.insert(dict(item))
            except Exception:
                pass
        elif isinstance(item, FollowsItem):
            followsItems = dict(item)
            follows = followsItems.pop("follows")
            for i in range(len(follows)):
                followsItems[str(i + 1)] = follows[i]
            try:
                self.Follows.insert(followsItems)
            except Exception:
                pass
        elif isinstance(item, FansItem):
            fansItems = dict(item)
            fans = fansItems.pop("fans")
            for i in range(len(fans)):
                fansItems[str(i + 1)] = fans[i]
            try:
                self.Fans.insert(fansItems)
            except Exception:
                pass
        elif isinstance(item, ReposterItem):
            repostersItems = dict(item)
            reposters = repostersItems.pop("reposters")
            for i in range(len(reposters)):
                repostersItems[str(i + 1)] = reposters[i]
            try:
                self.Reposters.insert(repostersItems)
            except Exception:
                pass
        elif isinstance(item, NameItem):
            try:
                self.Names.insert(dict(item))
            except Exception:
                pass
        return item

