class REDDIT:
    # config for logging into _reddit, see https://praw.readthedocs.io/en/latest/getting_started/authentication.html
    USERNAME = ""
    PASSWORD = ""
    CLIENT_ID = ""
    CLIENT_SECRET = ""
    USER_AGENT = "github.com/thomasasfk/clipsync"

    # subreddits to monitor for clipsync requests
    SUBREDDITS = ["livestreamfail", "rpclipsgta", "clipsync"]

    # username to send feedback to if there is an error/bug
    CONTACT_USERNAME = "wee_tommy"


class TWITCH:
    GQL_URL = "https://gql.twitch.tv/gql"

    # oauth for creating _twitch clips, taken from _twitch webui
    OAUTH = ""
    # _twitch's default client-id, taken from _twitch webui
    CLIENT_ID = "kimne78kx3ncx6brgo4mv6wki5h1ko"


if __name__ == "__main__":
    print("This file is not meant to be run directly.")
    exit(1)
