from twitch.src.queries import MultiUserVodsInfo
from . import utils
from .user import User


class Sync:
    def __init__(self, logins):
        self.users = []
        logins = [login for login in logins if utils.validLoginFormat(login)]
        self.__setupUsers(logins)

    def __setupUsers(self, logins):
        data = MultiUserVodsInfo.post(logins=logins)

        for login in logins:
            for state in data.get('users', []):
                if (
                    'login' in state
                    and login.lower() in state.get('login').lower()
                    and 'videos' in state
                ):
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
