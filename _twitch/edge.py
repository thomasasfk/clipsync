from _twitch import utils


class Edge:
    def __init__(self, edge):
        self.id = edge["node"]["id"]
        self.start = utils.parse_time(edge["node"]["createdAt"])
        self.end = utils.add_offset_to_start(self.start, edge["node"]["lengthSeconds"])
