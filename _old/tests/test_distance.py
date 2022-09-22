from app import distance


def test_get_coordinates():
    assert distance.get_coordinates("PARIS") == (48.8588897, 2.3200410217200766)


def test_get_distance():
    assert distance.get_distance("PARIS", "MARSEILLE") == 661.6477355748142
