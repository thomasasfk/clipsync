import requests

from abc import ABC, abstractmethod


class AbstractTwitchGQLQuery(ABC):

    @property
    @abstractmethod
    def gqlQuery(self):
        """ return the GQL query """

    @classmethod
    def do_post(cls):
        HEADERS = {'client-id': 'kimne78kx3ncx6brgo4mv6wki5h1ko'}

        QUERY = {
            'query': cls.gqlQuery,
            'variables': cls.variables,
        }

        response = requests.post(
            'https://gql.twitch.tv/gql', json=QUERY, headers=HEADERS)

        if response.ok:
            return response.json()['data']
        else:
            response.raise_for_status()


class ClipInfoQuery(AbstractTwitchGQLQuery):
    gqlQuery = """
    query($slug: ID!) {
        clip(slug: $slug) {
            video {
                createdAt
            }
            videoOffsetSeconds
        }
    }
    """

    @classmethod
    def post(cls, slug):
        cls.variables = {'slug': slug, }
        return cls.do_post()


class MultiVodInfoQuery(AbstractTwitchGQLQuery):
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
        cls.variables = {'logins': logins, }
        return cls.do_post()


class VodInfoQuery(AbstractTwitchGQLQuery):
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
        cls.variables = {'login': login, 'cursor': cursor}
        return cls.do_post()
