import logging

from _twitch.clips import create_twitch_clip
from _twitch.edge import Edge
from _twitch.queries import user_vods_info

logging.basicConfig(
    filename="debug.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(threadName)s -  %(levelname)s - %(message)s",
)


class User:
    def __init__(self, login, edges=None):
        self.login = login
        self.cursor = None
        self.edges = {}
        if edges:
            self._setup_edges(edges)
        else:
            self.paginate()

    def _setup_edges(self, edges):
        edges = [edge for edge in edges if edge]
        for edge in edges:
            _edge = Edge(edge)
            self.edges[_edge.id] = _edge
            if edge.get("cursor", False):
                self.cursor = edge.get("cursor")

    def paginate(self):
        data = user_vods_info(login=self.login, cursor=self.cursor)
        previous_cursor = self.cursor
        if data.get("user", None):
            self._setup_edges(data.get("user", {}).get("videos", {}).get("edges", {}))
        if self.cursor == previous_cursor:
            self.cursor = None

    def sync(self, interval_time, clip_title=None):
        if not self.edges:
            return None

        very_start = list(self.edges.values())[-1].start

        if interval_time < very_start:
            if self.cursor:
                self.paginate()
                return self.sync(interval_time, clip_title)
            return None

        for edge in self.edges.values():
            if edge.start <= interval_time <= edge.end:
                vod_interval_offset = interval_time - edge.start

                if clip_title:
                    vod_interval_offset = float(vod_interval_offset.total_seconds())
                    try:
                        clip_response = create_twitch_clip(
                            video_id=edge.id,
                            offset_seconds=vod_interval_offset,
                            title=clip_title,
                        )
                        twitch_clip = (
                            clip_response.get("publishClip", {})
                            .get("clip", {})
                            .get("slug", None)
                        )
                    except (TypeError, AttributeError):
                        twitch_clip = None

                    return edge.id, vod_interval_offset, twitch_clip

                return edge.id, vod_interval_offset
