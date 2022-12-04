import pickle


def setup_comment():
    comment_mock = open("testing/comment_mock", "rb")
    return pickle.load(comment_mock)
