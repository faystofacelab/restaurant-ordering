from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Stockage des commandes par table
orders = {str(i): [] for i in range(11)}  # Tables 0 à 10
takeaway_orders = []  # Commandes à emporter

# Menus disponibles
menu_items = [
    "A1", "A2", "A4", "A5", "YBF", "MH2", "MH5", "YP", "TAKO", "RIZ SAUTE",
    "E6", "E5", "E4", "N1", "N2", "N3", "N4", "MH1", "MH3", "MH4", "E3", "E3 VEGE", "E1", "CR CHESSE"
]

@app.route('/')
def index():
    return render_template('index.html', menu_items=menu_items, orders=orders, takeaway_orders=takeaway_orders)

@app.route('/send_order', methods=['POST'])
def send_order():
    data = request.json
    table = data.get('table')
    order = data.get('order')
    quantity = data.get('quantity', 1)
    is_takeaway = data.get('is_takeaway', False)

    if table is not None and order in menu_items:
        if is_takeaway:
            takeaway_orders.append({"order": order, "quantity": quantity})
            return jsonify({"message": f"Commande à emporter ajoutée: {order} (x{quantity})", "orders": takeaway_orders}), 200
        elif table in orders:
            orders[table].append({"order": order, "quantity": quantity, "status": "en attente"})
            return jsonify({"message": f"Commande ajoutée à la table {table}", "orders": orders[table]}), 200
        else:
            return jsonify({"error": "Table invalide"}), 400
    return jsonify({"error": "Données invalides"}), 400

@app.route('/get_orders', methods=['GET'])
def get_orders():
    return jsonify(orders), 200

@app.route('/get_takeaway_orders', methods=['GET'])
def get_takeaway_orders():
    return jsonify(takeaway_orders), 200

@app.route('/history')
def history():
    return render_template('history.html', orders=orders, takeaway_orders=takeaway_orders)

@app.route('/clear_orders', methods=['POST'])
def clear_orders():
    data = request.json
    table = data.get('table')
    if table is not None and table in orders:
        orders[table].clear()
        return jsonify({"message": f"Commandes effacées pour la table {table}"}), 200
    return jsonify({"error": "Table invalide"}), 400

if __name__ == '__main__':
    app.run(debug=True)
