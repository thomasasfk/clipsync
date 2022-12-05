from _twitch import utils
from _twitch.queries import multi_user_vods_info
from _twitch.user import User


class Sync:
    def __init__(self, logins):
        self.users = []
        logins = [login for login in logins if utils.valid_login_format(login)]
        self._setup_users(logins)

    def _setup_users(self, logins):
        data = multi_user_vods_info(logins=logins)

        for login in logins:
            for state in data.get("users", []):
                if (
                    state and
                    "login" in state
                    and login.lower() in state.get("login").lower()
                    and "videos" in state
                ):
                    if "videos" not in state or "edges" not in state["videos"]:
                        continue

                    self.users.append(
                        User(
                            login=state.get("login"),
                            edges=state.get("videos", {}).get("edges", None),
                        ),
                    )

    def sync_all(self, vod_interval, clip_titles=None):
        results = {}
        for user in self.users:
            new_interval = user.sync(vod_interval, clip_titles)
            if new_interval:
                results[user.login] = new_interval
        return results
