settings {
        logfile         = "/tmp/lsyncd.log",
        statusFile      = "/tmp/lsyncd.stat",
        statusInterval = 1,
        nodaemon        = true
}

sync {
        default.rsyncssh,
        source = "/var/log/cs",
        host = "FILESYNC_HOST",
        targetdir = "/home/scponly/logs",
        delay           = 5,
        rsync = { rsh="/usr/bin/ssh -l scponly -p 2222 -i /home/scponly/.ssh/id_rsa -o StrictHostKeyChecking=no"}
}