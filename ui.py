#ui.py
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QTabWidget,
    QVBoxLayout, QHBoxLayout, QTextEdit, QPushButton,
    QFileDialog, QMessageBox, QGroupBox
)
from utils import check_len


class SteganographyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Стенография")
        self.setGeometry(200, 100, 1000, 700)

        self.init_ui()
        self.apply_styles()

    def init_ui(self):
        self.tabs = QTabWidget()
        self.tabs.addTab(self.create_encrypt_tab(), "Шифрование")
        self.tabs.addTab(self.create_decrypt_tab(), "Дешифрование")

        self.setCentralWidget(self.tabs)

    def create_encrypt_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)

        container_group = QGroupBox("Контейнер (текст-носитель)")
        container_layout = QVBoxLayout()

        self.container_text = QTextEdit()
        self.container_text.setPlaceholderText("Введите текст контейнера или загрузите из файла...")
        container_layout.addWidget(self.container_text)

        container_btn = QPushButton("Загрузить контейнер из файла")
        container_btn.clicked.connect(self.load_container_file)
        container_layout.addWidget(container_btn)

        container_group.setLayout(container_layout)

        message_group = QGroupBox("Секретное сообщение")
        message_layout = QVBoxLayout()

        self.secret_text = QTextEdit()
        self.secret_text.setPlaceholderText("Введите секретное сообщение...")
        message_layout.addWidget(self.secret_text)

        message_btn = QPushButton("Загрузить сообщение из файла")
        message_btn.clicked.connect(self.load_secret_file)
        message_layout.addWidget(message_btn)

        message_group.setLayout(message_layout)

        buttons_layout = QHBoxLayout()

        check_btn = QPushButton("Проверить длину")
        check_btn.clicked.connect(self.check_length)

        encrypt_btn = QPushButton("Зашифровать")
        encrypt_btn.clicked.connect(self.encrypt)

        save_btn = QPushButton("Сохранить в файл")
        save_btn.clicked.connect(self.save_encrypted_file)
        save_btn.setObjectName("saveButton")

        buttons_layout.addWidget(check_btn)
        buttons_layout.addWidget(encrypt_btn)
        buttons_layout.addWidget(save_btn)

        result_group = QGroupBox("Зашифрованный текст")
        result_layout = QVBoxLayout()

        self.encrypted_text = QTextEdit()
        self.encrypted_text.setReadOnly(True)
        result_layout.addWidget(self.encrypted_text)

        result_group.setLayout(result_layout)

        layout.addWidget(container_group)
        layout.addWidget(message_group)
        layout.addLayout(buttons_layout)
        layout.addWidget(result_group)

        return tab

    def create_decrypt_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)

        input_group = QGroupBox("Зашифрованный текст")
        input_layout = QVBoxLayout()

        self.encrypted_input = QTextEdit()
        self.encrypted_input.setPlaceholderText("Вставьте зашифрованный текст...")
        input_layout.addWidget(self.encrypted_input)

        load_btn = QPushButton("Загрузить зашифрованный текст из файла")
        load_btn.clicked.connect(self.load_encrypted_file)
        input_layout.addWidget(load_btn)

        input_group.setLayout(input_layout)

        decrypt_btn = QPushButton("Расшифровать")
        decrypt_btn.clicked.connect(self.decrypt_stub)

        output_group = QGroupBox("Расшифрованное сообщение")
        output_layout = QVBoxLayout()

        self.decrypted_text = QTextEdit()
        self.decrypted_text.setReadOnly(True)
        output_layout.addWidget(self.decrypted_text)

        output_group.setLayout(output_layout)

        layout.addWidget(input_group)
        layout.addWidget(decrypt_btn)
        layout.addWidget(output_group)

        return tab

    def load_container_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Выбор файла")
        if file_path:
            with open(file_path, "r", encoding="utf-8") as f:
                self.container_text.setText(f.read())

    def load_encrypted_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Выбор зашифрованного файла",
            "",
            "Текстовые файлы (*.txt);;Все файлы (*)"
        )

        if file_path:
            with open(file_path, "r", encoding="utf-8") as f:
                self.encrypted_input.setText(f.read())

    def load_secret_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Выбор файла")
        if file_path:
            with open(file_path, "r", encoding="utf-8") as f:
                self.secret_text.setText(f.read())

    def check_length(self):
        from utils import check_len

        container = self.container_text.toPlainText()
        secret = self.secret_text.toPlainText()

        try:
            result = check_len(container, secret)
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", str(e))
            return

        verdict = "Сообщение поместится" if result.fits else "Сообщение не поместится"

        QMessageBox.information(
            self,
            "Проверка длины",
            f"Размер контейнера: {result.container_capacity}\n"
            f"Текущая длина сообщения: {result.message_length}\n\n"
            f"{verdict}"
        )

    def encrypt(self):
        from utils import text_to_bits, trim_spaces, put_end_marker
        from cypher import cypher

        result_str = None

        try:
            container = self.container_text.toPlainText()
            secret = self.secret_text.toPlainText()

            secret_bits = text_to_bits(secret)
            secret_len = len(secret_bits)

            result = check_len(container, secret)

            if not result.fits:
                raise ValueError("Текущее сообщение не поместится в контейнер.")

            trimmed = trim_spaces(container)
            trimmed_with_end = put_end_marker(secret_len, trimmed)
            result = cypher(trimmed_with_end, secret_bits)
            result_str = ''.join(result)
        except ValueError as e:
            QMessageBox.warning(self, "Ошибка", str(e))
            return
        except Exception:
            QMessageBox.critical(self, "Ошибка", "Внутренняя ошибка приложения")
            return

        if result_str is not None:
            self.encrypted_text.setText(result_str)

    def save_encrypted_file(self):
        encrypted_text = self.encrypted_text.toPlainText()

        if not encrypted_text.strip():
            QMessageBox.warning(
                self,
                "Ошибка сохранения",
                "Зашифрованный текст пуст. Сначала выполните шифрование."
            )
            return

        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Сохранить зашифрованный текст",
            "",
            "Текстовые файлы (*.txt);;Все файлы (*)"
        )

        if file_path:
            if not file_path.endswith(".txt"):
                file_path += ".txt"

            with open(file_path, "w", encoding="utf-8") as f:
                f.write(encrypted_text)

            QMessageBox.information(
                self,
                "Сохранено",
                "Зашифрованный текст успешно сохранён."
            )

    def decrypt_stub(self):
        from utils import extract_spaces, bits_to_text
        from cypher import decypher

        result_str = None

        try:
            encrypted_text = self.encrypted_input.toPlainText()
            spaces = extract_spaces(encrypted_text)
            bits = decypher(spaces)
            decrypted_text = bits_to_text(bits)
            result_str = decrypted_text
        except ValueError as e:
            QMessageBox.warning(self, "Ошибка", str(e))
            return
        except Exception:
            QMessageBox.critical(self, "Ошибка", "Внутренняя ошибка приложения")
            return

        self.decrypted_text.setText(result_str)

    def apply_styles(self):
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f7fa;
            }
            QGroupBox {
                font-weight: bold;
                border: 1px solid #dcdcdc;
                border-radius: 8px;
                margin-top: 10px;
                padding: 10px;
                background-color: #ffffff;
            }
            QTextEdit {
                border: 1px solid #cccccc;
                border-radius: 6px;
                padding: 8px;
                font-size: 14px;
            }
            QPushButton {
                background-color: #4a90e2;
                color: white;
                border-radius: 6px;
                padding: 8px 14px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #357ab8;
            }
            QTabWidget::pane {
                border: none;
            }
            QTabBar::tab {
                background: #e6e9ef;
                padding: 5px 5px;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
                margin-right: 2px;
                min-width: 120px; 
            }
            QTabBar::tab:selected {
                background: #ffffff;
                font-weight: bold;
                min-width: 120px;
            }
            QPushButton#saveButton {
                background-color: #2ecc71;
            }
        """)


