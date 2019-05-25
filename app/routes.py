from app import app, db
from flask import request, jsonify
from app.models import Item

@app.route('/')
def index():
    return ''


@app.route('/api/save', methods=['GET', 'POST'])
def save():
    try:
        # get headers first
        name = request.headers.get('name')
        price = float(request.headers.get('price'))
        desc = request.headers.get('desc')

        if not name and not price and not desc:
            return jsonify({ 'error #301': 'Invalid params' })

        if not isinstance(price, float):
            return jsonify({ 'error #302': 'Prices need to be numbers' })

        # create an event
        item = Item(name=name, price=price, desc=desc)

        # add to stage and commit to db
        db.session.add(item)
        db.session.commit()

        return jsonify({ 'success': 'event created' })
    except:
        return jsonify({ 'error #303': 'something went wrong' })



@app.route('/api/retrieve', methods=['GET', 'POST'])
def retrieve():
    try:
        name = request.headers.get('name')
        price = request.headers.get('price')
        desc = request.headers.get('desc')

        if name and price:
            results = Item.query.filter_by(name=name, price=price).all()
        elif not price and name:
            results = Item.query.filter_by(name=name).all()
        elif not name and price:
            results = Item.query.filter_by(price=price).all()
        else:
            return jsonify({ 'error#304': 'Required params not included' })

        if not results:
            return jsonify({ 'success': 'No Items matching that description.' })

        # remember that results is a list of db.Model objects
        parties = []

        for item in results:
            party = {
                'id': item.id,
                'name': item.name,
                'price': item.price,
                'desc': item.desc
            }

            parties.append(party)

        return jsonify(parties)

    except:
        return jsonify({ 'error#305': 'something went wrong' })



@app.route('/api/delete', methods=['GET', 'POST'])
def delete():
    try:
        item_id = request.headers.get('item_id')

        item = Item.query.filter_by(id=item_id).first()

        if not item:
            return jsonify({ 'error#306': 'Item does not exist.'})

        db.session.delete(item)
        db.session.commit()

        return jsonify({ 'success': f'Item {item_id} deleted.'})

    except:
        return jsonify({ 'error#307': 'Could not delete item.' })
