from twitch.src.queries import MultiUserVodsInfo
from . import utils
from .user import User


class Sync:
    def __init__(self, logins):
        self.users = []
        formattedLogins = {login for login in logins if utils.validLoginFormat(login)}
        logins = list(formattedLogins)
        self.__setupUsers(logins)

    def __setupUsers(self, logins):
        data = MultiUserVodsInfo.post(logins=logins)

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
