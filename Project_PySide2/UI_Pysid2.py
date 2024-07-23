import os.path
from maya import cmds
from PySide2 import QtWidgets
import main


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle("UI Window")
        self.setMinimumWidth(850)
        self.main_layout = QtWidgets.QVBoxLayout()
        self.second_layout = QtWidgets.QVBoxLayout()
        self.file_browser = QtWidgets.QFileDialog()
        layout_1 = QtWidgets.QHBoxLayout()
        layout_2 = QtWidgets.QHBoxLayout()
        layout_3 = QtWidgets.QHBoxLayout()
        layout_4 = QtWidgets.QHBoxLayout()
        layout_5 = QtWidgets.QVBoxLayout()
        layout_6 = QtWidgets.QHBoxLayout()
        layout_10 = QtWidgets.QHBoxLayout()
        layout_7 = QtWidgets.QHBoxLayout()

        self.text_edit_file = QtWidgets.QLineEdit()
        self.button_usd = QtWidgets.QPushButton("File")

        self.text_edit_audio = QtWidgets.QLineEdit()
        self.button_audio = QtWidgets.QPushButton("Audio Path")

        self.text_edit_output = QtWidgets.QLineEdit()
        self.button_output = QtWidgets.QPushButton("Output Path")

        self.button_open = QtWidgets.QPushButton("Generate")
        self.button_open.setMinimumHeight(40)
        self.button_open.setFixedWidth(200)
        self.label_export = QtWidgets.QLabel("Export Now")
        self.label_export.setFixedWidth(70)
        self.rb_option = QtWidgets.QRadioButton()
        self.frame_line_one = QtWidgets.QFrame()
        self.frame_line_one.setFrameShape(QtWidgets.QFrame.HLine)
        self.frame_line_two = QtWidgets.QFrame()
        self.frame_line_two.setFrameShape(QtWidgets.QFrame.HLine)
        self.button_files_exp = QtWidgets.QPushButton("Files Export")
        self.button_files_exp.setMinimumHeight(40)
        self.button_files_exp.setEnabled(False)
        self.button_anim_exp = QtWidgets.QPushButton("Anim Export")
        self.button_anim_exp.setMinimumHeight(40)
        self.button_anim_exp.setEnabled(False)
        self.widget = QtWidgets.QWidget()

        # layout_1 widget
        layout_1.addWidget(self.text_edit_file)
        layout_1.addWidget(self.button_usd)

        # layout_2 widget
        layout_2.addWidget(self.text_edit_audio)
        layout_2.addWidget(self.button_audio)

        # layout_3 widget
        layout_3.addWidget(self.text_edit_output)
        layout_3.addWidget(self.button_output)

        # layout_4 widget
        layout_4.addWidget(self.button_open)

        # layout5 widget
        layout_5.addWidget(self.frame_line_one)
        layout_7.addWidget(self.label_export)
        layout_7.addWidget(self.rb_option)

        # layout6 widget
        layout_6.addWidget(self.button_files_exp)
        layout_6.addWidget(self.button_anim_exp)

        # adding layout
        self.main_layout.addLayout(layout_1)
        self.main_layout.addLayout(layout_2)
        self.main_layout.addLayout(layout_3)
        self.main_layout.addLayout(layout_4)
        self.main_layout.addLayout(layout_5)
        self.main_layout.addLayout(layout_7)
        self.main_layout.addLayout(layout_6)
        self.main_layout.addLayout(layout_10)

        # setting layout
        self.widget.setLayout(self.main_layout)

        self.setCentralWidget(self.widget)

        # files function calling
        self.button_usd.clicked.connect(self.button_browser_file)
        self.button_audio.clicked.connect(self.button_browser_audio)
        self.button_output.clicked.connect(self.button_browser_output)
        self.rb_option.toggled.connect(self.radio_option_function)

        # file open function
        self.button_open.clicked.connect(self.file_open)

        # Export function
        self.button_files_exp.clicked.connect(self.export_characters)
        self.button_anim_exp.clicked.connect(self.export_json)

    def button_browser_file(self):
        path_name = self.file_browser.getOpenFileName()
        print(path_name[0])
        if path_name[0].endswith("mb" or "ma"):
            self.text_edit_file.setText(path_name[0])
        else:
            self.validation_file_open(condition="maya file mb or ma format")

    def button_browser_audio(self):
        path_name = self.file_browser.getOpenFileName()
        print(path_name[0])
        if path_name[0].endswith("wav"):
            self.text_edit_audio.setText(path_name[0])
        else:
            self.validation_file_open(condition="audio file wav format")

    def button_browser_output(self):
        path_name = self.file_browser.getExistingDirectory()
        print(path_name)
        self.text_edit_output.setText(path_name)

    def file_open(self):
        file_path = self.text_edit_file.text()
        audio_path = self.text_edit_audio.text()
        output = self.text_edit_output.text()

        if file_path:
            if audio_path:
                if output:
                    self.validation_file_open(event=True)
                    main.generate_function(file_path, audio_path)
                    message = "Files Generates"
                    self.message_info(message, success=True)

        if not file_path:
            self.validation_file_open(condition="file")
            return
        if not audio_path:
            self.validation_file_open(condition="audio")
            return
        if not output:
            self.validation_file_open(condition="output")
            return

    def validation_file_open(self, condition=None, event=None):
        if not event:
            message = "{} path".format(condition)
            self.message_info(message)
            self.button_files_exp.setEnabled(False)
            self.button_anim_exp.setEnabled(False)

        if event:
            self.button_files_exp.setEnabled(True)
            self.button_anim_exp.setEnabled(True)

    def message_info(self, message, success=None):
        msg_box = QtWidgets.QMessageBox()
        if success:
            msg_box.setText("Successfully done, {}".format(message))
        if not success:
            msg_box.setText("Please select the {}".format(message))
        msg_box.exec_()

    def export_characters(self):
        path = self.text_edit_output.text()
        op_path = os.path.join("{}/output".format(path))
        if path:
            selection_name = cmds.ls(sl=True)
            try:
                mesh_name = selection_name[0].split(":")
            except Exception as info_error:
                message = "the object group, {}".format(info_error)
                self.message_info(message)
                return
            info_error = main.export_characters(op_path, mesh_name[0])
            if info_error:
                message = "object {}".format(info_error)
                self.message_info(message)
                return
            if not info_error:
                message = "Exported the obj"
                self.message_info(message, success=True)

        if not path:
            message = "output path"
            self.message_info(message)
            return

    def radio_option_function(self):
        if self.rb_option.isChecked():
            self.button_files_exp.setEnabled(True)
            self.button_anim_exp.setEnabled(True)
        if not self.rb_option.isChecked():
            self.button_files_exp.setEnabled(False)
            self.button_anim_exp.setEnabled(False)

    def export_json(self):
        path = self.text_edit_output.text()
        selection_ctrls = cmds.ls(sl=True)
        op_path = os.path.join("{}/output".format(path))
        if not path:
            message = "output path"
            self.message_info(message)
            return
        if not selection_ctrls:
            message = "control curves"
            self.message_info(message)
            return
        if path and selection_ctrls:
            info_error = main.export_anim_json(selection_ctrls, op_path)
            if info_error:
                message = "control curves which have key frames, {}".format(info_error)
                self.message_info(message)
            if not info_error:
                message = "Exported the control"
                self.message_info(message, success=True)


window = MainWindow()
window.show()
