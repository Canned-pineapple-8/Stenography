from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QTabWidget,
    QVBoxLayout, QHBoxLayout, QPushButton,
    QFileDialog, QMessageBox, QGroupBox,
    QRadioButton, QButtonGroup, QSpinBox, QLabel, QPlainTextEdit
)
from utils import check_len
from constants import Mode


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

    def create_mode_group(self, for_encrypt=True):
        group = QGroupBox("Режим" if for_encrypt else "Режим дешифрования")
        layout = QVBoxLayout()

        rb_simple = QRadioButton("Обыкновенные пробелы")
        rb_nbsp = QRadioButton("Обычный и неразрывный пробелы")
        rb_simple.setChecked(True)

        buttons = QButtonGroup(self)
        buttons.addButton(rb_simple)
        buttons.addButton(rb_nbsp)

        spin = QSpinBox()
        spin.setRange(1, 10000)
        spin.setValue(1)
        spin.setEnabled(False)

        rb_nbsp.toggled.connect(spin.setEnabled)

        line_layout = QHBoxLayout()
        line_layout.addWidget(QLabel("Количество шифруемых символов на строку:"))
        line_layout.addWidget(spin)

        layout.addWidget(rb_simple)
        layout.addWidget(rb_nbsp)
        layout.addLayout(line_layout)
        group.setLayout(layout)

        return group, rb_simple, rb_nbsp, spin

    def create_encrypt_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)

        container_group = QGroupBox("Контейнер (текст-носитель)")
        container_layout = QVBoxLayout()
        self.container_text = QPlainTextEdit()
        container_layout.addWidget(self.container_text)
        btn = QPushButton("Загрузить контейнер из файла")
        btn.clicked.connect(self.load_container_file)
        container_layout.addWidget(btn)
        container_group.setLayout(container_layout)

        message_group = QGroupBox("Секретное сообщение")
        message_layout = QVBoxLayout()
        self.secret_text = QPlainTextEdit()
        message_layout.addWidget(self.secret_text)
        btn = QPushButton("Загрузить сообщение из файла")
        btn.clicked.connect(self.load_secret_file)
        message_layout.addWidget(btn)
        message_group.setLayout(message_layout)

        self.enc_mode_group, self.enc_simple_rb, self.enc_nbsp_rb, self.enc_spin = self.create_mode_group(True)

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
        self.encrypted_text = QPlainTextEdit()
        self.encrypted_text.setReadOnly(True)
        result_layout.addWidget(self.encrypted_text)
        result_group.setLayout(result_layout)

        layout.addWidget(container_group)
        layout.addWidget(message_group)
        layout.addWidget(self.enc_mode_group)
        layout.addLayout(buttons_layout)
        layout.addWidget(result_group)

        return tab

    def create_decrypt_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)

        input_group = QGroupBox("Зашифрованный текст")
        input_layout = QVBoxLayout()
        self.encrypted_input = QPlainTextEdit()
        input_layout.addWidget(self.encrypted_input)
        btn = QPushButton("Загрузить зашифрованный текст из файла")
        btn.clicked.connect(self.load_encrypted_file)
        input_layout.addWidget(btn)
        input_group.setLayout(input_layout)

        self.dec_mode_group, self.dec_simple_rb, self.dec_nbsp_rb, self.dec_spin = self.create_mode_group(False)

        decrypt_btn = QPushButton("Расшифровать")
        decrypt_btn.clicked.connect(self.decrypt)

        output_group = QGroupBox("Расшифрованное сообщение")
        output_layout = QVBoxLayout()
        self.decrypted_text = QPlainTextEdit()
        self.decrypted_text.setReadOnly(True)
        output_layout.addWidget(self.decrypted_text)
        output_group.setLayout(output_layout)

        layout.addWidget(input_group)
        layout.addWidget(self.dec_mode_group)
        layout.addWidget(decrypt_btn)
        layout.addWidget(output_group)

        return tab

    def load_container_file(self):
        path, _ = QFileDialog.getOpenFileName(self, "Выбор файла")
        if path:
            with open(path, "r", encoding="utf-8") as f:
                self.container_text.setPlainText(f.read())

    def load_secret_file(self):
        path, _ = QFileDialog.getOpenFileName(self, "Выбор файла")
        if path:
            with open(path, "r", encoding="utf-8") as f:
                self.secret_text.setPlainText(f.read())

    def load_encrypted_file(self):
        path, _ = QFileDialog.getOpenFileName(self, "Выбор файла", "", "Текстовые файлы (*.txt)")
        if path:
            with open(path, "r", encoding="utf-8") as f:
                self.encrypted_input.setPlainText(f.read())

    def check_length(self):
        result = check_len(
            self.container_text.toPlainText(),
            self.secret_text.toPlainText()
        )
        QMessageBox.information(
            self,
            "Проверка длины",
            f"Размер контейнера: {result.container_capacity}\n"
            f"Текущая длина сообщения: {result.message_length}\n\n"
            f"{'Сообщение поместится' if result.fits else 'Сообщение не поместится'}"
        )

    def encrypt(self):
        from utils import text_to_bits, trim_spaces
        from cypher import cypher

        container = self.container_text.toPlainText()
        secret = self.secret_text.toPlainText()
        bits = text_to_bits(secret)

        check = check_len(container, secret)
        if not check.fits:
            self.encrypted_text.setPlainText("Сообщение не помещается в контейнер")
            return

        mode = Mode.REGULAR_SPACES if self.enc_simple_rb.isChecked() else Mode.NON_BREAKING_SPACES
        per_line = 1 if mode == Mode.REGULAR_SPACES else self.enc_spin.value()

        trimmed = trim_spaces(container)
        result = cypher(trimmed, bits, mode=mode, number_of_bits=per_line)
        self.encrypted_text.setPlainText("".join(result))

    def decrypt(self):
        from utils import extract_spaces, bits_to_text
        from cypher import decypher

        mode = Mode.REGULAR_SPACES if self.dec_simple_rb.isChecked() else Mode.NON_BREAKING_SPACES
        per_line = 1 if mode == Mode.REGULAR_SPACES else self.dec_spin.value()

        encrypted = self.encrypted_input.toPlainText()
        spaces = extract_spaces(encrypted)
        bits = decypher(spaces, mode=mode, number_of_bits=per_line)
        self.decrypted_text.setPlainText(bits_to_text(bits))

    def save_encrypted_file(self):
        text = self.encrypted_text.toPlainText()
        if not text.strip():
            QMessageBox.warning(self, "Ошибка", "Нет данных для сохранения")
            return

        path, _ = QFileDialog.getSaveFileName(self, "Сохранить", "", "Текстовые файлы (*.txt)")
        if path:
            if not path.endswith(".txt"):
                path += ".txt"
            with open(path, "w", encoding="utf-8") as f:
                f.write(text)

    def apply_styles(self):
        self.setStyleSheet("""
            QMainWindow { background-color: #f5f7fa; }
            QGroupBox {
                font-weight: bold;
                border: 1px solid #dcdcdc;
                border-radius: 8px;
                margin-top: 10px;
                padding: 10px;
                background-color: #ffffff;
            }
            QPlainTextEdit {
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
            QPushButton:hover { background-color: #357ab8; }
            QPushButton#saveButton { background-color: #2ecc71; }
        """)
