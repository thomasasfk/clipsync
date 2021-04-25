from twitch.queries import ClipInfoQuery, MultiVodInfoQuery, VodInfoQuery


def test_getClipInfo():
    data = ClipInfoQuery.post('TrappedFrigidPenguinSeemsGood')

    assert data == {'clip': {'video': {'createdAt': '2017-09-12T17:36:46Z'}, 'videoOffsetSeconds': 5452}}


def test_getVodInfoMulti():
    data = MultiVodInfoQuery.post(logins=['xqcow', 'hasanabi'])

    assert len(data['users']) == 2
    assert data['users'][0]['login'] == 'xqcow'
    assert data['users'][1]['login'] == 'hasanabi'


def test_getVodInfo():
    data = VodInfoQuery.post(login='xqcow')

    assert data['user']['login'] == 'xqcow'
    assert len(data['user']['videos']['edges']) > 0
