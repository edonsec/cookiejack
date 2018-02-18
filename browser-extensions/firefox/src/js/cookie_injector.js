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

var guiHandleSocketEvents = {
    cookie_counter: 0,
    db: false,

    error: function() {
        browser.browserAction.setIcon({
            "path": {"19": "img/icons/icon-red.png"}
        })
    },
    connected: function() {
        this.reset_counter()
        browser.browserAction.setIcon({
            "path": {"19": "img/icons/icon-green.png"}
        })
    },
    disconnected: function() {
        browser.browserAction.setIcon({
            "path": {"19": "img/icons/icon-grayscale.png"}
        })
        browser.browserAction.setBadgeText({"text": ""})
    },
    data: function(cookie_data) {

        var cookie = {
            "name": cookie_data.name,
            "url": cookie_data.url,
            "value": cookie_data.value,
            "domain": cookie_data.domain,
            "expirationDate": (cookie_data.expiry == null) ? null : cookie_data.expiry
        }

        browser.cookies.set(cookie).then(c => {
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
        browser.browserAction.setBadgeText({text: this.cookie_counter.toString() })
    },
    reset_counter: function() {
        browser.browserAction.setBadgeText({text: "" })
        this.cookie_counter = 0
    }
}

document.addEventListener("DOMContentLoaded", () => {
    db = new Dexie("cookie_database")

    db.version(1).stores({
        cookies: "id,name,value,url"
    })

    browser.browserAction.onClicked.addListener(d => {
        browser.storage.sync.get(DEFAULT_SETTINGS, function(data) {
            if(!socket.isConnected()) {
                guiHandleSocketEvents.db = db
                socket.connect(data.host, data.port, guiHandleSocketEvents)
            } else {
                socket.disconnect()
            }
        })
    })
})
