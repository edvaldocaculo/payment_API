import qrcode
import uuid


class Pix:
    def __init__(self) -> None:
        pass

    def create_payment(self):
        bank_payment_id = str(uuid.uuid4()) # Criação de um ID aleatório
        hash_payment = f"hash_payment{bank_payment_id}" # Concatenação desse ID
        img = qrcode.make(hash_payment) # Criação do QR Code do ID gerado
        img.save(f"static/img/qr_code_payment_{bank_payment_id}.png") # Salvar o QR Code como imagem

        return {
            "bank_payment_id": bank_payment_id,
            "qr_code_path": f"qr_code_payment_{bank_payment_id}"
        }
