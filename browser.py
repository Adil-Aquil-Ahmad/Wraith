import sys
import os
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPushButton, QLineEdit, QWidget, QHBoxLayout, QTabWidget
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWebEngineCore import QWebEnginePage, QWebEngineProfile, QWebEngineSettings
from PyQt6.QtCore import QUrl
from PyQt6.QtNetwork import QNetworkProxy

class CustomWebEnginePage(QWebEnginePage):

    def __init__(self, parent=None):
        super().__init__(parent)

    def createWindow(self, _type):
        new_browser = QWebEngineView()
        new_browser.setPage(CustomWebEnginePage(new_browser))
        parent_window.add_new_tab_widget(new_browser, "New Tab")
        return new_browser.page()


class TorBrowser(QMainWindow):
    def __init__(self, onion_url=None):
        super().__init__()
        self.setWindowTitle("Wraith Browser")
        self.setGeometry(100, 100, 1024, 768)
        
        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)
        
        self.new_tab_button = QPushButton("+")
        self.new_tab_button.setFixedSize(20, 20)
        self.new_tab_button.clicked.connect(self.add_new_tab)
        
        self.tabs.setCornerWidget(self.new_tab_button)
        
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.tabs)
        
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)
        
        self.configure_tor_proxy()
        
        if onion_url is None:
            hostname_file = os.path.join(os.getcwd(), "tor", "hidden_service", "hostname")
            if os.path.exists(hostname_file):
                with open(hostname_file, 'r') as f:
                    onion_url = "http://" + f.read().strip()
            else:
                onion_url = "http://"
        
        self.add_new_tab(onion_url, "Home")

    def configure_tor_proxy(self):
        proxy = QNetworkProxy()
        proxy.setType(QNetworkProxy.ProxyType.Socks5Proxy)
        proxy.setHostName("127.0.0.1")
        proxy.setPort(9050)
        QNetworkProxy.setApplicationProxy(proxy)
    
    def add_new_tab(self, url="http://", label="New Tab"):
        if not isinstance(url, str):
            url = "http://"
        
        browser = QWebEngineView()
        browser.setPage(CustomWebEnginePage(browser))
        browser.setUrl(QUrl(url))
        
        back_button = QPushButton("◀")
        back_button.clicked.connect(browser.back)
        
        reload_button = QPushButton("⟳")
        reload_button.clicked.connect(browser.reload)
        
        forward_button = QPushButton("▶")
        forward_button.clicked.connect(browser.forward)
        
        url_bar = QLineEdit()
        url_bar.setPlaceholderText("Enter URL...")
        url_bar.setText(url)
        url_bar.returnPressed.connect(lambda: self.load_url(url_bar, browser))
        
        top_layout = QHBoxLayout()
        top_layout.addWidget(back_button)
        top_layout.addWidget(reload_button)
        top_layout.addWidget(forward_button)
        top_layout.addWidget(url_bar)
        
        tab_layout = QVBoxLayout()
        tab_layout.addLayout(top_layout)
        tab_layout.addWidget(browser)
        
        tab_container = QWidget()
        tab_container.setLayout(tab_layout)
        
        self.tabs.addTab(tab_container, label)
        self.tabs.setCurrentWidget(tab_container)
    
    def add_new_tab_widget(self, browser, label="New Tab"):
        tab_layout = QVBoxLayout()
        tab_layout.addWidget(browser)
        
        tab_container = QWidget()
        tab_container.setLayout(tab_layout)
        
        self.tabs.addTab(tab_container, label)
        self.tabs.setCurrentWidget(tab_container)
    
    def load_url(self, url_bar, browser):
        url = url_bar.text().strip()
        if not url.startswith("http"):
            url = "http://" + url
        browser.setUrl(QUrl(url))
    
    def close_tab(self, index):
        if self.tabs.count() > 1:
            self.tabs.removeTab(index)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    onion_url = None
    if len(sys.argv) > 1:
        onion_url = sys.argv[1]
    
    window = TorBrowser(onion_url)
    parent_window = window
    window.show()
    sys.exit(app.exec())
