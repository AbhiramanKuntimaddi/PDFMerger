from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QFileDialog, QListWidget, \
    QPushButton, QLabel, QMessageBox, QProgressBar, QListWidgetItem, QGraphicsDropShadowEffect, QAction
from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve, QSize, QMimeData
from PyQt5.QtGui import QPixmap, QIcon
from qt_material import apply_stylesheet
import subprocess
import sys
import os


class PDFMergerApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.selected_file_paths = []

        # Set up UI elements
        self.setWindowTitle('PDF Merger')
        self.setGeometry(50,50,900, 650) 
        self.central_widget = QWidget()
        self.layout = QVBoxLayout()
        self.listbox = QListWidget()
        self.listbox.setViewMode(QListWidget.IconMode)
        self.listbox.setIconSize(QSize(100, 100))
        self.listbox.setResizeMode(QListWidget.Adjust)
        self.listbox.setSpacing(10)
        self.listbox.setAcceptDrops(True)  # Enable drop event
        self.add_button = QPushButton('Add PDFs')
        self.merge_button = QPushButton('Merge PDFs')
        self.clear_button = QPushButton('Clear Selection')
        self.delete_button = QPushButton('Delete Selected')
        self.label = QLabel('Selected PDFs:')
        # self.progress_bar = QProgressBar()

        self.listbox.setDragEnabled(True)
        self.listbox.setSelectionMode(QListWidget.ExtendedSelection)
        self.listbox.setDragDropMode(QListWidget.InternalMove)
        self.listbox.viewport().setAcceptDrops(True)
        self.listbox.setDropIndicatorShown(True)
        self.listbox.setDragDropOverwriteMode(False)

        self.layout.addWidget(self.label)
        self.layout.addWidget(self.listbox)
        self.layout.addWidget(self.merge_button)
        self.layout.addWidget(self.clear_button)
        self.layout.addWidget(self.delete_button)
        self.layout.addWidget(self.add_button)
        # self.layout.addWidget(self.progress_bar)

        self.central_widget.setLayout(self.layout)
        self.setCentralWidget(self.central_widget)


        # Connect signals to slots
        self.merge_button.clicked.connect(self.merge_pdfs)
        self.clear_button.clicked.connect(self.clear_selection)
        self.delete_button.clicked.connect(self.delete_selected)
        self.add_button.clicked.connect(self.open_file_dialog)

        # Apply hover effect using QSS
        hover_style = '''
            QPushButton:hover {
                background-color: #008080;
                color: #ffffff;
                border: none;
            }
        '''
        self.merge_button.setStyleSheet(hover_style)
        self.clear_button.setStyleSheet(hover_style)
        self.delete_button.setStyleSheet(hover_style)
        self.add_button.setStyleSheet(hover_style)

        # Apply dark material theme
        apply_stylesheet(self, theme='dark_teal.xml')

    def open_file_dialog(self):
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.ExistingFiles)
        file_dialog.setNameFilters(["PDF Files (*.pdf)"])
        if file_dialog.exec_():
            selected_files = file_dialog.selectedFiles()
            for file_path in selected_files:
                # Create QListWidgetItem with thumbnail icon and file path
                item = QListWidgetItem()
                item.setIcon(self.create_thumbnail_icon(file_path))
                item.setText(os.path.basename(file_path))
                item.setToolTip(file_path)
                self.listbox.addItem(item)
                self.selected_file_paths.append(file_path)

    def clear_selection(self):
        self.listbox.clear()
        self.selected_file_paths = []

    def delete_selected(self):
        selected_items = self.listbox.selectedItems()
        for item in selected_items:
            self.listbox.takeItem(self.listbox.row(item))
            self.selected_file_paths.remove(item.toolTip())

    def merge_pdfs(self):
        if not self.selected_file_paths:
            QMessageBox.critical(self, 'Error', 'No files selected.')
            return

        save_dialog = QFileDialog()
        save_dialog.setAcceptMode(QFileDialog.AcceptSave)
        save_dialog.setDefaultSuffix(".pdf")
        save_dialog.setNameFilter("PDF Files (*.pdf)")
    
        if save_dialog.exec_():
            output_file_path = save_dialog.selectedFiles()[0]
            #self.progress_bar.setValue(0)
            #self.progress_bar.setVisible(True)
            # Merge PDFs using Ghostscript
            merge_command = ['gs', '-q', '-dNOPAUSE', '-dBATCH', '-sDEVICE=pdfwrite',
                            f'-sOutputFile={output_file_path}'] + self.selected_file_paths
            merge_process = subprocess.Popen(merge_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            while True:
                #self.progress_bar.setValue(self.progress_bar.value() + 1)
                #self.progress_bar.repaint()
                if merge_process.poll() is not None:
                    break
                QApplication.processEvents()

            if merge_process.returncode == 0:
                QMessageBox.information(self, 'Success', 'PDFs merged successfully.')
            else:
                QMessageBox.critical(self, 'Error', 'Failed to merge PDFs.')

            #self.progress_bar.setValue(0)
            #self.progress_bar.setVisible(False)

            # Clear the selection after merging
            self.clear_selection()


    def create_thumbnail_icon(self, file_path):
        pixmap = QPixmap(file_path)
        if not pixmap.isNull():
            pixmap = pixmap.scaled(32, 32, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        return QIcon(pixmap)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = PDFMergerApp()
    window.show()
    sys.exit(app.exec_())