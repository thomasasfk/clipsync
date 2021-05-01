from twitch.src.queries import MultiVodInfo
from . import utils
from .user import User


class Sync():
    def __init__(self, logins):
        formattedLogins = set([l for l in logins if utils.validLoginFormat(l)])
        logins = list(formattedLogins)
        self.setupUsers(logins)

    def setupUsers(self, logins):
        self.users = []
        data = MultiVodInfo.post(logins=logins)

        for state in data.get('users', []):
            if 'videos' in state:
                self.users.append(
                    User(login=state.get('login'),
                         edges=state.get('videos', {}).get('edges', None)))

    def syncAll(self, vodInterval, clipTitles=None):
        results = {}
        for user in self.users:
            newInterval = user.sync(vodInterval, clipTitles)
            if newInterval:
                results[user.login] = newInterval
        return results
