import requests

from requests.adapters import HTTPAdapter
from abc import ABC, abstractmethod

TWITCH_TV_GQL_URL = 'https://gql.twitch.tv/gql'
DEFAULT_TWITCH_GQL_HEADERS = {'client-id': 'kimne78kx3ncx6brgo4mv6wki5h1ko'}
CLIP_ACCOUNT_GQL_OAUTH = ''

session = requests.Session()
session.mount('http://gql.twitch.tv/gql', HTTPAdapter(max_retries=5))
session.mount('https://gql.twitch.tv/gql', HTTPAdapter(max_retries=5))


class AbstractTwitchGQL(ABC):
    variables = None

    @property
    @abstractmethod
    def gqlQuery(self):
        """ return the GQL query """

    @property
    @abstractmethod
    def headers(self):
        """ return the GQL query """

    @abstractmethod
    def post(self, *args):
        """ implement post method with variables signature """

    @classmethod
    def do_post(cls):
        HEADERS = cls.headers

        QUERY = {
            'query': cls.gqlQuery,
            'variables': cls.variables,
        }

        response = session.post(
            TWITCH_TV_GQL_URL, json=QUERY, headers=HEADERS, timeout=5)

        if response.ok:
            responseJSON = response.json()
            return responseJSON.get('data', {})


class UnauthenticatedTwitchGQL(AbstractTwitchGQL, ABC):
    headers = DEFAULT_TWITCH_GQL_HEADERS


class AuthenticatedTwitchGQL(AbstractTwitchGQL, ABC):
    headers = DEFAULT_TWITCH_GQL_HEADERS
    headers.update({'Authorization': CLIP_ACCOUNT_GQL_OAUTH})


class ClipInfo(UnauthenticatedTwitchGQL):
    gqlQuery = """
    query($slug: ID!) {
        clip(slug: $slug) {
            video {
                id
                createdAt
            }
            videoOffsetSeconds
        }
    }
    """

    @classmethod
    def post(cls, slug):
        cls.variables = {'slug': slug}
        return cls.do_post()


class MultiUserVodsInfo(UnauthenticatedTwitchGQL):
    gqlQuery = """
    query($logins: [String!]) {
        users(logins: $logins) {
            login
            videos(first: 100) {
                edges {
                    node {
                        id
                        createdAt
                        lengthSeconds
                    }
                    cursor
                }
            }
        }
    }
    """

    @classmethod
    def post(cls, logins):
        cls.variables = {'logins': logins}
        return cls.do_post()


class UserVodsInfo(UnauthenticatedTwitchGQL):
    gqlQuery = """
    query($login: String, $cursor: Cursor) {
        user(login: $login) {
            login
            videos(first: 100, after: $cursor) {
                edges {
                    node {
                        id
                        createdAt
                        lengthSeconds
                    }
                    cursor
                }
            }
        }
    }
    """

    @classmethod
    def post(cls, login, cursor=None):
        cls.variables = {'login': login,
                         'cursor': cursor}
        return cls.do_post()


class VodCreatedAt(UnauthenticatedTwitchGQL):
    gqlQuery = """
    query($videoID: ID) {
        video(id: $videoID) {
            createdAt
        }
    }
    """

    @classmethod
    def post(cls, videoID):
        cls.variables = {'videoID': videoID}
        return cls.do_post()


class BroadcasterIDFromVideoID(UnauthenticatedTwitchGQL):
    gqlQuery = """
    query($videoID: ID) {
        video(id: $videoID) {
            owner {
                id
            }
        }
    }
    """

    @classmethod
    def post(cls, videoID):
        cls.variables = {'videoID': videoID}
        return cls.do_post()


class CreateClipMutation(AuthenticatedTwitchGQL):
    gqlQuery = """
    mutation($broadcasterID: ID!, $videoID: ID, $offsetSeconds: Float!) {
        createClip(input: {broadcasterID: $broadcasterID, videoID: $videoID, offsetSeconds: $offsetSeconds}) {
            clip {
                slug
            }
            error {
                code
            }
        }
    }
    """

    @classmethod
    def post(cls, broadcasterID, videoID, offsetSeconds):
        cls.variables = {'broadcasterID': broadcasterID,
                         'videoID': videoID,
                         'offsetSeconds': offsetSeconds}
        return cls.do_post()


class PublishClipMutation(AuthenticatedTwitchGQL):
    gqlQuery = """
    mutation($slug: ID!, $title: String) {
        publishClip(input: {segments: {durationSeconds: 60.0, offsetSeconds: 0.0}, slug: $slug, title: $title}) {
            clip {
                slug
            }
            error{
                message
            }
        }
    }
    """

    @classmethod
    def post(cls, slug, title):
        cls.variables = {'slug': slug,
                         'title': title}
        return cls.do_post()
