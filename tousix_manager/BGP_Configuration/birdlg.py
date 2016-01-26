# -*- coding: utf8 -*-
__author__ = 'remy'


import requests
import logging
LOG = logging.getLogger("BGP_Configuration")

def bird_proxy(host, port, proto, service, query):
    """Retreive data of a service from a running lgproxy on a remote node

    First and second arguments are the node and the port of the running lgproxy
    Third argument is the service, can be "traceroute" or "bird"
    Last argument, the query to pass to the service

    return tuple with the success of the command and the returned data
    """

    path = ""
    if proto == "ipv6":
        path = service + "6"
    elif proto == "ipv4":
        path = service

    if not port or not host:
        return False, 'Host "%s" invalid' % host
    elif not path:
        return False, 'Proto "%s" invalid' % proto
    else:
        url = 'http://{host}:{port}/{path}'.format(host=host,
                                                   port=int(port),
                                                   path=path)
        query = "'{}'".format(query)
        param = {'q': query}
        try:
            f = requests.get(url, params=param)
            resultat = f.text
            status = True                # retreive remote status
        except requests.ConnectionError:
            resultat = "Failed retreive url: %s" % url
            status = False
        return status, resultat
