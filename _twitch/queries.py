import logging

from requests import Session
from requests.adapters import HTTPAdapter

import config

DEFAULT_TWITCH_CLIENT_ID = config.TWITCH.CLIENT_ID
CUSTOM_TWITCH_USER_OAUTH = config.TWITCH.OAUTH

session = Session()
session.mount(config.TWITCH.GQL_URL, HTTPAdapter(max_retries=5))


def __post_gql_query(
        gql_query: str,
        variables: dict,
        headers: dict,
) -> dict:
    response = session.post(
        config.TWITCH.GQL_URL,
        json={
            "query": gql_query,
            "variables": variables,
        },
        headers=headers,
        timeout=5,
    )

    if response.ok:
        response_json = response.json()
        return response_json.get("data", {})

    logging.error(
        f"Error while trying to post to {config.TWITCH.GQL_URL}: {response.text}",
    )
    return {}


def _post_authenticated_gql_query(
        gql_query: str, variables: dict,
) -> dict:
    return __post_gql_query(
        gql_query,
        variables,
        {
            "Client-ID": DEFAULT_TWITCH_CLIENT_ID,
            "Authorization": f"OAuth {CUSTOM_TWITCH_USER_OAUTH}",
        },
    )


def _post_gql_query(
        gql_query: str, variables: dict,
) -> dict:
    return __post_gql_query(
        gql_query,
        variables,
        {"Client-ID": DEFAULT_TWITCH_CLIENT_ID},
    )


def clip_info(slug: str) -> dict:
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
    return _post_gql_query(
        gql_query,
        {"slug": slug},
    )


def multi_user_vods_info(logins: list[str]) -> dict:
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
    return _post_gql_query(
        gql_query,
        {"logins": logins},
    )


def user_vods_info(login: str, cursor: str | None = None) -> dict:
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
    return _post_gql_query(
        gql_query,
        {"login": login, "cursor": cursor},
    )


def vod_created_at(video_id: str) -> dict:
    return _post_gql_query(
        """
        query($videoID: ID) {
            video(id: $videoID) {
                createdAt
            }
        }
        """,
        {"videoID": video_id},
    )


def broadcaster_id_from_video_id(video_id: str) -> dict:
    return _post_gql_query(
        """
        query($videoID: ID) {
            video(id: $videoID) {
                owner {
                    id
                }
            }
        }
        """,
        {"videoID": video_id},
    )


def create_clip_mutation(
        broadcaster_id: str,
        video_id: str,
        offset_seconds: float,
) -> dict:
    return _post_authenticated_gql_query(
        """
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
        """,
        {
            "broadcasterID": broadcaster_id,
            "videoID": video_id,
            "offsetSeconds": offset_seconds,
        },
    )


def publish_clip_mutation(slug: str, title: str) -> dict:
    return _post_authenticated_gql_query(
        """
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
        """,
        {"slug": slug, "title": title},
    )
