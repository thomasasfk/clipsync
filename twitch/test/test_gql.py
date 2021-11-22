from twitch.src.queries import ClipInfo, MultiUserVodsInfo, UserVodsInfo


def test_getClipInfo():
    data = ClipInfo.post('TrappedFrigidPenguinSeemsGood')

    assert data == {'clip': {'video': {'id': '174256129', 'createdAt': '2017-09-12T17:36:46Z'}, 'videoOffsetSeconds': 5452}}


def test_getVodInfoMulti():
    data = MultiUserVodsInfo.post(logins=['xqcow', 'hasanabi'])

    assert len(data['users']) == 2
    assert data['users'][0]['login'] == 'xqcow'
    assert data['users'][1]['login'] == 'hasanabi'


def test_getVodInfo():
    data = UserVodsInfo.post(login='xqcow')

    assert data['user']['login'] == 'xqcow'
    assert len(data['user']['videos']['edges']) > 0
