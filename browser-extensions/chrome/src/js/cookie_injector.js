var DEFAULT_SETTINGS = {
    host: "localhost",
    port: 9000
}

var socket = {
    socket: false,

    connect: function (host, port, eventHandlers) {
        var socket = new WebSocket("ws://" + host + ":" + port);

        socket.onerror = message => {
            console.log("Connection error")
            eventHandlers.error()
        }

        socket.onopen = message => {
            console.log("Connection open")
            eventHandlers.connected()
        }

        socket.onclose = message => {
            console.log("Connection closed")
            eventHandlers.disconnected()
        }

        socket.onmessage = message => {
            eventHandlers.data(JSON.parse(message.data))
        }

        this.socket = socket
  },

  isConnected: function() {
    return this.socket && this.socket.OPEN == this.socket.readyState
  },

  disconnect: function() {
      if(this.socket) {
          this.socket.close()
      }
  }
}

var handleSocketEvents = {
    cookie_counter: 0,
    db: false,

    error: function() {
        chrome.browserAction.setIcon({
            "path": {"19": "img/icons/icon-red.png"}
        })
    },
    connected: function() {
        this.reset_counter()
        chrome.browserAction.setIcon({
            "path": {"19": "img/icons/icon-green.png"}
        })

    },
    disconnected: function() {
        chrome.browserAction.setIcon({
            "path": {"19": "img/icons/icon-grayscale.png"}
        })
        chrome.browserAction.setBadgeText({"text": ""})
    },
    data: function(cookie_data) {
        var cookie = {
            "name": cookie_data.name,
            "url": cookie_data.url,
            "value": cookie_data.value,
            "domain": cookie_data.domain,
            "expirationDate": (cookie_data.expiry == null) ? null : cookie_data.expiry
        }

        chrome.cookies.set(cookie, c => {
            console.log(c)

            if(this.db) {
                this.db.cookies.put({
                    id: cookie.domain + "_" + cookie.name,
                    name: cookie.name,
                    value: cookie.value,
                    url: cookie.url
                })
            }
        })

        this.cookie_counter += 1
        chrome.browserAction.setBadgeText({text: this.cookie_counter.toString() })
    },
    reset_counter: function() {
        chrome.browserAction.setBadgeText({text: "" })
        this.cookie_counter = 0
    }
}

document.addEventListener("DOMContentLoaded", function() {
    var db = new Dexie("cookie_database")

    db.version(1).stores({
        cookies: "id,name,value,url"
    })

    chrome.browserAction.onClicked.addListener(function(d) {
        chrome.storage.sync.get(DEFAULT_SETTINGS, function(data) {
            if(!socket.isConnected()) {
                handleSocketEvents.db = db
                socket.connect(data.host, data.port, handleSocketEvents)
            } else {
                socket.disconnect()
            }
        })
    })
})
