from PySide6.QtWidgets import QWidget, QVBoxLayout, QTextBrowser
from core.formatters.styles import get_common_css



class HelpWindow(QWidget):
    # 1. Wir akzeptieren parent und accent_color
    def __init__(self, accent_color, parent=None):
        
        # 2. WICHTIG: An super() geben wir NUR parent weiter!
        # Nicht die accent_color, denn QWidget kennt die nicht.
        super().__init__(parent)
        
        self.setWindowTitle("Documentation")
        self.resize(600, 500)
        
        # Layout erstellen
        layout = QVBoxLayout(self)
        self.browser = QTextBrowser()
        
        # Damit Links im Browser funktionieren (falls du später welche einbaust)
        self.browser.setOpenExternalLinks(True)
        
        layout.addWidget(self.browser)
        
        # Inhalt setzen
        self.set_content(accent_color)

    def set_content(self, accent_color):
        style = get_common_css(accent_color)
        
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>{style}</head>
        <body>
            <h2>Documentation</h2>
            
            <div class="result-entry">
                <div class="artist-title">
                    <h3>1. Start Searching</h3>
                </div>
                <div class="info-text">
                    Enter a term in the search field and select the desired category in the toolbar.
                    (<b>Alles</b>, <b>Music</b>, <b>Literature</b>).
                    Press <span class="label">ENTER</span> or klick Search-Button.
                </div>
            </div>
            <br>
            <div class="result-entry">
                <div class="artist-title">
                    <h3>2. View Settings</h3> 
                </div>
                <div class="info-text">
                    Use the <span class="label">View</span> menu to adjust how results are displayed.
                    You can zoom in and out using <span class="label">CTRL + MOUSE WHEEL</span> or the shortcuts:
                    <br>
                    <span class="label">CTRL + PLUS</span> to zoom in,
                    <span class="label">CTRL + MINUS</span> to zoom out,
                    and <span class="label">CTRL + 0</span> to reset the zoom level.
                </div>
            </div>
            <br>            
            <div class="result-entry">
                <div class="artist-title">
                    <h3>3. Scientific search (CORE)</h3>
                </div>
                <div class="info-text">
                    This app uses the CORE.ac.uk database to provide access to millions of scientific articles.
                </div>
                <h4>Setup:</h4>
                <ol type="1">
                    <li>Use is free of charge, but requires a personal access key (API key).</li>
                    <li>Register at [https://core.ac.uk/services/api](https://core.ac.uk/services/api).</li>
                    <li>Copy the key displayed.</li>
                    <li>When you start the context search in the app, you will be asked for this key. Paste it in.</li>
                </ol>
                <h4>Security:</h4>
                <div class="info-text">
                    Your key is **not** stored in the app, but securely stored in your operating system's password vault (Windows Credential Manager, macOS Keychain, Linux Keyring/Wallet). 
                </div>
            </div>
        </body>
        </html>
        """
        self.browser.setHtml(html)






# class HelpWindow(QWidget):
#     def __init__(self, parent=None):
#         super().__init__(parent)
#         self.setWindowTitle("Documentation")
#         self.resize(600, 400)

#         layout = QVBoxLayout()
#         self.text_browser = QTextBrowser()
#         layout.addWidget(self.text_browser)
#         self.setLayout(layout)

#         self.load_help_content()

#     def load_help_content(self):
#         #css = get_common_css()
#         help_content = """
#         <h1>Help Documentation</h1>
#         <p>Welcome to the help section of the application. Here you can find information on how to use various features.</p>
#         <h2>Feature 1</h2>
#         <p>Details about feature 1...</p>
#         <h2>Feature 2</h2>
#         <p>Details about feature 2...</p>
#         """

#         #full_content = f"<style>{css}</style>{help_content}"
        
#         self.text_browser.setHtml(help_content)