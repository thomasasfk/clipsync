from twitch.queries import VodInfo
from .clips import TwitchClipService
from .edge import Edge

import logging
logging.basicConfig(filename='debug.log',
                    level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(threadName)s -  %(levelname)s - %(message)s')

class User():
    def __init__(self, login, edges=None):
        self.login = login
        self.cursor = None
        self.edges = {}
        if edges:
            self.setupEdges(edges)
        else:
            self.paginate()

    def setupEdges(self, edges):
        edges = [edge for edge in edges if edge]
        for edge in edges:
            if edge['node']['id'] in self.edges:
                continue

            _edge = Edge(edge)
            self.edges[_edge.id] = _edge
            if edge.get('cursor', False):
                self.cursor = edge.get('cursor')

    def paginate(self):
        data = VodInfo.post(login=self.login, cursor=self.cursor)

        if data.get('user', None):
            self.setupEdges(data.get('user', {}).get('videos', {}).get('edges', {}))

    def sync(self, intervalTime, clipTitle=None):
        veryStart = list(self.edges.values())[-1].start

        if intervalTime < veryStart:
            if self.cursor:
                self.paginate()
                return self.sync(intervalTime, clipTitle)
            return None

        for edge in self.edges.values():
            if edge.start <= intervalTime <= edge.end:
                vodIntervalOffset = intervalTime - edge.start

                if clipTitle:
                    twitchClip = None
                    try:
                        clipResponse = TwitchClipService \
                            .instance() \
                            .createTwitchClip(edge.id, vodIntervalOffset, clipTitle)
                        twitchClip = clipResponse.get('publishClip', {}).get('clip', {}).get('slug', None)
                    except AttributeError:
                        logging.error(f"Error Creating Twitch Clip for: {self.login}")

                    return edge.id, vodIntervalOffset, twitchClip

                return edge.id, vodIntervalOffset
