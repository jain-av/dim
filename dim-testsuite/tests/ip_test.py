from ipaddress import IPv4Network, IPv4Address


def test_mask():
    ip1 = IPv4Network('12.0.0.0/24')
    assert int(ip1.hostmask) == 0x000000ff
    assert int(ip1.netmask) == 0xffffff00


def test_contains():
    ip1 = IPv4Network('12.0.0.0/25')
    ip2 = IPv4Network('12.0.0.0/24')
    assert ip1.subnet_of(ip2)
    assert not ip2.subnet_of(ip1)
    assert ip1.subnet_of(ip1)

    assert IPv4Address('12.0.0.2') in ip1
