# map.py

import globals as cmt

import modules.boottime
import modules.load
import modules.certificate
import modules.cpu
import modules.disk
import modules.folder
import modules.memory
import modules.mount
import modules.ping
import modules.process
import modules.socket
import modules.swap
import modules.url
import modules.send
import modules.mysql
import modules.sendfile

cmt.GLOBAL_MODULE_MAP = {
    "boottime"   : {"check": modules.boottime.check    },
    "load"       : {"check": modules.load.check        },
    "certificate": {"check": modules.certificate.check },
    "cpu"        : {"check": modules.cpu.check         },
    "disk"       : {"check": modules.disk.check        },
    "folder"     : {"check": modules.folder.check      },
    "memory"     : {"check": modules.memory.check      },
    "mount"      : {"check": modules.mount.check       },
    "ping"       : {"check": modules.ping.check        },
    "process"    : {"check": modules.process.check     },
    "socket"     : {"check": modules.socket.check      },
    "swap"       : {"check": modules.swap.check        },
    "url"        : {"check": modules.url.check         },
    "send"       : {"check": modules.send.check        },
    "mysql"      : {"check": modules.mysql.check       },
    "sendfile"   : {"check": modules.sendfile.check    },
}
