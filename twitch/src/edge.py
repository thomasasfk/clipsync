from . import utils


class Edge:
    def __init__(self, edge):
        self.id = edge['node']['id']
        self.start = utils.parseTime(edge['node']['createdAt'])
        self.end = utils.addOffsetToStart(
            self.start, edge['node']['lengthSeconds'])
