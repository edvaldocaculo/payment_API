from flask import Flask, jsonify, send_file, request, render_template
from database import db
from models.payment import Payment
from datetime import datetime, timedelta
from pix import Pix

app = Flask(__name__)


app.config["SECRET_KEY"] = 'ola edvaldo'
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
# initialize the app with the extension
db.init_app(app)

# Create a payment
@app.route('/payments/pix/create', methods=['POST',])
def create_payment_pix():
    data = request.get_json()
    if 'value' not in data:
        return jsonify({'message': 'Invalid Value'}), 400
    expiration_date = datetime.now() + timedelta(minutes=30)
    value = data["value"]

    pix_obj = Pix()
    data_pix_payment = pix_obj.create_payment()

    new_payment = Payment(value=value, expiration_date=expiration_date)
    
    new_payment.bank_payment_id = data_pix_payment["bank_payment_id"]
    new_payment.qr_code = data_pix_payment["qr_code_path"]
    db.session.add(new_payment)
    db.session.commit()
    return jsonify({'message':'The pyaments was been created',
                    'payment':new_payment.to_dict()
                    })

@app.route('/payments/pix/confirmation',methods=['POST'])
def pix_confirmation():
    return jsonify({"message": 'The payment was been confirmated'})

@app.route('/payments/pix/<int:payment_id>', methods=['GET'])    
def payment_pix_page(payment_id):
    return render_template('payment.html')

@app.route('/payments/pix/qrcode/<file_name>', methods=['GET'])
def get_image(file_name):
    return send_file(f"static/img/{file_name}.png", mimetype='image/png')


if __name__ == '__main__':
    app.run(debug=True)