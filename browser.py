import sys

# ligo pio omorfo version
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import (
    QSizePolicy,
    QApplication,
    QMainWindow,
    QToolBar,
    QAction,
    QLineEdit,
    QTabWidget,
    QWidget,
    QVBoxLayout,
    QListWidget,
    QDockWidget,
    QMessageBox,
)
from PyQt5.QtWebEngineWidgets import QWebEngineView


class BrowserTab(QWebEngineView):
    def __init__(self):
        super().__init__()
        self.setUrl(QUrl("https://www.google.com"))


class MinimalBrowser(QMainWindow):
    DARK_STYLE = """
        QMainWindow {
            background-color: #121212;
        }

        QToolBar {
            background: #1e1e1e;
            color: white;
            border: none;
            spacing: 6px;
            padding: 8px;
        }

        QLineEdit {
            background: #2a2a2a;
            border: 1px solid #3a3a3a;
            border-radius: 12px;
            padding: 10px;
            color: white;
            font-size: 14px;
        }

        QTabWidget::pane {
            border: none;
        }

        QTabBar::tab {
            background: #242424;
            color: #bbbbbb;
            padding: 10px 18px;
            border-top-left-radius: 10px;
            border-top-right-radius: 10px;
            margin-right: 4px;
        }

        QTabBar::tab:selected {
            background: #353535;
            color: white;
        }

        QToolButton {
            color: white;
            background: transparent;
            border: none;
            padding: 6px;
            font-size: 16px;
        }

        QToolButton:hover {
            background: #333333;
            border-radius: 8px;
            color: white;
        }

        QListWidget {
            background: #1d1d1d;
            color: white;
            border: none;
            padding: 8px;
            font-size: 13px;
        }

        QListWidget::item {
            padding: 8px;
            border-radius: 8px;
        }

        QListWidget::item:selected {
            background: #3b82f6;
        }

        QDockWidget {
            color: white;
            font-size: 14px;
        }

        QPushButton {
            background: #2c2c2c;
            color: white;
            border: none;
            border-radius: 10px;
            padding: 8px;
        }

        QPushButton:hover {
            background: #3a3a3a;
        }
    """

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Whackk Browser")
        self.setStyleSheet(self.DARK_STYLE)
        self.resize(1200, 800)

        self.bookmarks = []

        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)
        self.tabs.currentChanged.connect(lambda _: self.update_url_bar())

        self.setCentralWidget(self.tabs)

        self.create_toolbar()
        self.create_bookmarks_panel()

        self.add_new_tab()

    def create_toolbar(self):
        toolbar = QToolBar()
        toolbar.setMovable(False)
        self.addToolBar(toolbar)

        back_btn = QAction("◀", self)
        back_btn.setToolTip("Back")
        back_btn.triggered.connect(lambda: self.current_browser().back())
        toolbar.addAction(back_btn)

        forward_btn = QAction("▶", self)
        forward_btn.setToolTip("Forward")
        forward_btn.triggered.connect(lambda: self.current_browser().forward())
        toolbar.addAction(forward_btn)

        reload_btn = QAction("↻", self)
        reload_btn.setToolTip("Reload")
        reload_btn.triggered.connect(lambda: self.current_browser().reload())
        toolbar.addAction(reload_btn)

        # afairesh undo/redo gt Qt pisteue pws htan diakosmhsh gia kapoion logo

        new_tab_btn = QAction("＋", self)
        new_tab_btn.triggered.connect(lambda: self.add_new_tab())
        toolbar.addAction(new_tab_btn)

        bookmark_btn = QAction("⭐", self)
        bookmark_btn.triggered.connect(self.add_bookmark)
        toolbar.addAction(bookmark_btn)

        self.url_bar = QLineEdit()
        self.url_bar.setPlaceholderText("Search Google or enter URL...")
        self.url_bar.setMinimumHeight(38)
        self.url_bar.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.url_bar.returnPressed.connect(self.navigate)
        toolbar.addWidget(self.url_bar)

    def create_bookmarks_panel(self):
        self.bookmark_list = QListWidget()
        self.bookmark_list.itemDoubleClicked.connect(self.open_bookmark)

        dock = QDockWidget("★ Bookmarks", self)
        dock.setMinimumWidth(250)
        dock.setWidget(self.bookmark_list)
        self.addDockWidget(1, dock)

    def current_browser(self):
        return self.tabs.currentWidget()

    def add_new_tab(self, url="https://www.google.com"):
        if isinstance(url, bool):
            url = "https://www.google.com"
        browser = BrowserTab()
        browser.setUrl(QUrl(url))

        browser.urlChanged.connect(lambda qurl, browser=browser: self.sync_url(qurl, browser))
        browser.titleChanged.connect(lambda title, browser=browser: self.update_tab_title(title, browser))

        index = self.tabs.addTab(browser, "New Tab")
        self.tabs.setCurrentIndex(index)

    def close_tab(self, index):
        if self.tabs.count() == 1:
            self.close()
            return

        self.tabs.removeTab(index)

    def navigate(self):
        text = self.url_bar.text().strip()

        if "." in text and " " not in text:
            if not text.startswith("http"):
                text = "https://" + text
        else:
            text = f"https://www.google.com/search?q={text}"

        self.current_browser().setUrl(QUrl(text))

    def sync_url(self, qurl, browser):
        if browser == self.current_browser():
            self.url_bar.setText(qurl.toString())

    def update_tab_title(self, title, browser):
        index = self.tabs.indexOf(browser)
        if index != -1:
            self.tabs.setTabText(index, title[:20])

    def update_url_bar(self, *args):
        browser = self.current_browser()
        if browser:
            self.url_bar.setText(browser.url().toString())

    def add_bookmark(self):
        browser = self.current_browser()
        url = browser.url().toString()
        title = self.tabs.tabText(self.tabs.currentIndex())

        bookmark_text = f"{title} | {url}"

        if bookmark_text not in self.bookmarks:
            self.bookmarks.append(bookmark_text)
            self.bookmark_list.addItem(bookmark_text)

    def open_bookmark(self, item):
        try:
            url = item.text().split(" | ", 1)[1]
            self.add_new_tab(url)
        except Exception:
            QMessageBox.warning(self, "Error", "Invalid bookmark.")


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MinimalBrowser()
    window.show()

    sys.exit(app.exec_())
