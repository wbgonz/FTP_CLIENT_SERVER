from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

import FTPClient_
from MainWindow import Ui_MainWindow

PASSWORD_MODE = 2
NORMAL_MODE = 0

POSSIBLE_CLIENT_OPERATIONS = ['', 'List', 'Upload', 'Download', 'Move', 'Delete']
POSSIBLE_OPERATIONS_ACTION = {'': 0, 'List': 1, 'Upload': 2, 'Download': 3, 'Move': 4, 'Delete': 5}


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, *args, obj=None, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.show()
        self._server_message = ''
        self._ftp_client = FTPClient_.FTPclient()
        self._userAction = ''
        self._loggedIn = False
        # Setting up check list
        self.cb_show_password.setChecked(False)

        # Setting Up the labels
        f = self.lb_ftp_server_address.font()
        f.setPointSize(8)
        self.lb_password.setFont(f)
        self.lb_username.setFont(f)
        self.lb_ftp_server_address.setFont(f)
        self.lb_server_response.setFont(f)
        self.lb_action.setFont(f)

        # Setting up line edits (User Input textbox)
        self.le_ftp_server_address.setPlaceholderText('i.e ftp.mirror.ac.za')
        self.le_username.setPlaceholderText('hint: Your account username')
        self.le_password.setPlaceholderText('hint: Your account password')
        self.le_password.setEchoMode(PASSWORD_MODE)  # Hides the text

        # Setting up Combo Box
        self.comboBox_userAction.addItems(POSSIBLE_CLIENT_OPERATIONS)

        # Handling events
        self.btn_connect.pressed.connect(self.btn_connect_handler)
        self.btn_disconnect.pressed.connect(self.btn_disconnect_handler)
        self.cb_show_password.stateChanged.connect(self.cb_show_password_handler)
        self.comboBox_userAction.currentIndexChanged[str].connect(self.comboBox_userAction_handler)
        self.btn_proceed.pressed.connect(self.btn_proceed_handler)

    # CONNECTION BUTTONS HANDLERS
    def btn_connect_handler(self):
        ftp_server_address = self.le_ftp_server_address.text()
        username = self.le_username.text()
        password = self.le_password.text()
        self._loggedIn = self._ftp_client.login(ftp_server_address, username, password)
        self._server_message = self._ftp_client.getServerMessage()
        self.td_server_response.setText(self._server_message)
        print(self._server_message)

        if self._loggedIn == True:
            # lock all the inputs for user name and servers.
            print('Logged IN')

    def btn_disconnect_handler(self):
        self._ftp_client.quit()

    # RADIO BUTTON HANDLERS
    def cb_show_password_handler(self, s):
        if s == Qt.Checked:
            self.le_password.setEchoMode(NORMAL_MODE)
        else:
            self.le_password.setEchoMode(PASSWORD_MODE)

    # COMBOBOX HANDLER ['':0, 'List':1, 'Upload':2, 'Download':3, 'Move':4, 'Delete':5]
    def comboBox_userAction_handler(self, choice):
        self._userAction = choice

    # PROCEED BUTTON HANDLER
    def btn_proceed_handler(self):
        if self._loggedIn:
            if self._userAction == 'List':
                self._ftp_client.list()
                self._server_message += self._ftp_client.getServerMessage()
                self.td_server_response.setText(self._server_message)
            else:
                print(self._userAction)
        else:
            print("You are not logged in")


if __name__ == '__main__':
    app = QApplication([])
    w = MainWindow()
    app.exec_()
