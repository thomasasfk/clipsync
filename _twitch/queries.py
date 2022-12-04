import logging
from abc import ABC
from abc import abstractmethod

from requests import Session
from requests.adapters import HTTPAdapter

import config

DEFAULT_TWITCH_CLIENT_ID = config.TWITCH.CLIENT_ID
CUSTOM_TWITCH_USER_OAUTH = config.TWITCH.OAUTH

session = Session()
session.mount(config.TWITCH.GQL_URL, HTTPAdapter(max_retries=5))


class AbstractTwitchGQL(ABC):
    @property
    @abstractmethod
    def gql_query(self) -> str:
        """returns a gql query"""

    @property
    @abstractmethod
    def headers(self) -> dict:
        """returns a dict of headers"""

    @abstractmethod
    def post(self, *args):
        """implement post method with variables signature"""

    @classmethod
    def _do_post(cls, variables: dict) -> dict:
        response = session.post(
            config.TWITCH.GQL_URL,
            json={
                "query": cls.gql_query,
                "variables": variables,

            },
            headers=cls.headers,  # type: ignore
            timeout=5,
        )

        if response.ok:
            response_json = response.json()
            return response_json.get("data", {})

        logging.error(
            f"Error while trying to post to {config.TWITCH.GQL_URL}: {response.text}",
        )
        return {}


class UnauthenticatedTwitchGQL(AbstractTwitchGQL, ABC):
    headers = {"client-id": DEFAULT_TWITCH_CLIENT_ID}


class AuthenticatedTwitchGQL(AbstractTwitchGQL, ABC):
    headers = {
        "Authorization": f"OAuth {CUSTOM_TWITCH_USER_OAUTH}",
        "client-id": DEFAULT_TWITCH_CLIENT_ID,
    }


class ClipInfo(UnauthenticatedTwitchGQL, ABC):
    gql_query = """
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
        return cls._do_post({"slug": slug})


class MultiUserVodsInfo(UnauthenticatedTwitchGQL, ABC):
    gql_query = """
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
        return cls._do_post({"logins": logins})


class UserVodsInfo(UnauthenticatedTwitchGQL, ABC):
    gql_query = """
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
        return cls._do_post({"login": login, "cursor": cursor})


class VodCreatedAt(UnauthenticatedTwitchGQL, ABC):
    gql_query = """
    query($videoID: ID) {
        video(id: $videoID) {
            createdAt
        }
    }
    """

    @classmethod
    def post(cls, video_id):
        return cls._do_post({"videoID": video_id})


class BroadcasterIDFromVideoID(UnauthenticatedTwitchGQL, ABC):
    gql_query = """
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
        return cls._do_post({"videoID": videoID})


class CreateClipMutation(AuthenticatedTwitchGQL, ABC):
    gql_query = """
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
    def post(cls, broadcasterID, videoID, offsetSeconds, retry=False):
        return cls._do_post(
            {
                "broadcasterID": broadcasterID,
                "videoID": videoID,
                "offsetSeconds": offsetSeconds,
            },
        )


class PublishClipMutation(AuthenticatedTwitchGQL, ABC):
    gql_query = """
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
        return cls._do_post({"slug": slug, "title": title})
