from flask import request, make_response, jsonify
from v1.basecontroller import BaseController
from v1.item.model import ItemModel

class ItemController(BaseController):
    _instance = None

    def __init__(self) -> None:
        self._instance = ItemModel()

    def post(self):
        print(request.json)
        resp = self._instance.create(request.json)
        if resp == False:
            return make_response(jsonify({
                "error": "Failed to add. There are items in your request that are invalid."
            }), 400)
        return jsonify(resp)

    def check(self, item_id, filters=None):
        if filters is not None:
            filters['id'] = item_id
        else:
            filters = {"id": item_id}
        item = self._instance.read(filters)
        if item is None:
            return make_response(jsonify({"error": "Item id not found."}), 404)
        return item

    def get(self, item_id=None):
        filters = {}
        if 'fields' in request.args:
            filters['fields'] = request.args['fields'].split(',')
        if item_id is not None:
            item = self.check(item_id, filters)
            if not isinstance(item, dict):
                return item
            return jsonify(item)
        filters['offset'] = int(request.args['offset']) if 'offset' in request.args else 0
        filters['limit'] = int(request.args['limit']) if 'limit' in request.args else 5
        items = self._instance.read(filters)
        total = self._instance.read(filters, True)
        return jsonify({
            'metadata': {
                'total': total,
                'links': self.build_links(total, filters['offset'], filters['limit'])
            },
            'data': items
        })

    def put(self, item_id=None):
        if item_id is not None:
            item = self.check(item_id)
            if not isinstance(item, dict):
                return item
            item_data = request.json
            item_data['id'] = item_id
            resp = self._instance.update(item_data)
            if resp == False:
                return make_response(jsonify({
                    "error": "Failed to update. There are items in your request that are invalid."
                }), 400)
            return jsonify(resp)
        return jsonify(self._instance.update(request.json))

    def delete(self, item_id=None):
        if item_id is not None:
            item = self.check(item_id)
            if not isinstance(item, dict):
                return item
            return jsonify(self._instance.delete(item_id))
        return jsonify(self._instance.delete(request.json))