import sys
from PyQt5.QtWidgets import QApplication
from ui import SteganographyApp

def main():
    from utils import text_to_bits
    end_marker = "   "
    text = "Stenography is amazing!"

    print(f"Маркер окончания: \"{end_marker}\"")
    bits_end_marker = text_to_bits(end_marker)
    print(f"\tв виде битовой последовательности: {''.join([str(x) for x in bits_end_marker])}\n\n")

    print(f"Скрываемое сообщение: \"{text}\"")
    bits_text = ''.join([str(x) for x in text_to_bits(text)])
    print(f"\tв виде битовой последовательности: {bits_text[:len(bits_text)//2]}\n{bits_text[len(bits_text)//2:]}")


if __name__ == "__main__":
    #main()
    app = QApplication(sys.argv)
    window = SteganographyApp()
    window.show()
    sys.exit(app.exec_())


