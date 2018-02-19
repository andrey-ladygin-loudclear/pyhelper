from os.path import join, dirname, realpath

def generateSh(conf):
    params = list(conf.items())
    host = getConf('host', params)
    port = getConf('port', params)
    folder = getConf('folder', params)
    password = getConf('password', params)
    fastconnect = getConf('fastconnect', params)

    port = ' -p'+port if port else ''
    changefolder = ' && cd ' + folder if folder else ''

    if fastconnect:
        file = join(dirname(realpath(__file__)), '..', 'resources', 'sh', host)
        f = open(file, 'w')
        f.write("echo 'Connect to: " + host + "' && " + fastconnect + changefolder )
        f.close()
        return file

    elif host and password:
        file = join(dirname(realpath(__file__)), '..', 'resources', 'sh', host)
        f = open(file, 'w')
        f.write("echo 'Connect to: " + host + ", password: " + password + "' && ssh " + host + port)
        f.close()
        return file

    return None


def getConf(key, conf):
    for i in conf:
        if key == i[0]:
            return i[1]

    return None