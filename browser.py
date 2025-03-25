import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPushButton, QLineEdit, QWidget, QHBoxLayout
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl
from PyQt5.QtNetwork import QNetworkProxy

class TorBrowser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Wraith Browser")
        self.setGeometry(100, 100, 1024, 768)
        
        self.browser = QWebEngineView()
        
        self.hidden_service_url = "http://aqkilehdwr7tbcr3b6gjyffmq7ioziqqeiuflfppgtegsynenx3qk3ad.onion"
        self.browser.setUrl(QUrl(self.hidden_service_url))
        
        self.back_button = QPushButton("◀")
        self.back_button.clicked.connect(self.browser.back)
        
        self.reload_button = QPushButton("⟳")
        self.reload_button.clicked.connect(self.browser.reload)
        
        self.forward_button = QPushButton("▶")
        self.forward_button.clicked.connect(self.browser.forward)
        
        self.url_bar = QLineEdit()
        self.url_bar.setPlaceholderText("Enter URL...")
        self.url_bar.returnPressed.connect(self.load_url)
        
        top_layout = QHBoxLayout()
        top_layout.addWidget(self.back_button)
        top_layout.addWidget(self.reload_button)
        top_layout.addWidget(self.forward_button)
        top_layout.addWidget(self.url_bar)
        
        main_layout = QVBoxLayout()
        main_layout.addLayout(top_layout)
        main_layout.addWidget(self.browser)
        
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)
        
        self.configure_tor_proxy()
    
    def configure_tor_proxy(self):
        proxy = QNetworkProxy()
        proxy.setType(QNetworkProxy.Socks5Proxy)
        proxy.setHostName("127.0.0.1")
        proxy.setPort(9050)
        QNetworkProxy.setApplicationProxy(proxy)
    
    def load_url(self):
        url = self.url_bar.text()
        if not url.startswith("http"):
            url = "http://" + url
        self.browser.setUrl(QUrl(url))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TorBrowser()
    
    window.browser.setUrl(QUrl("http://aqkilehdwr7tbcr3b6gjyffmq7ioziqqeiuflfppgtegsynenx3qk3ad.onion"))
    
    window.show()
    sys.exit(app.exec_())

# first C:\Tor\tor.exe -f C:\Tor\torrc run this on your cmd to run 