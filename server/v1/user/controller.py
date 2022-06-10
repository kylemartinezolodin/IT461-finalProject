from flask import request, make_response, jsonify
from v1.basecontroller import BaseController
from v1.user.model import UserModel

class UserController(BaseController):
    _instance = None

    def __init__(self) -> None:
        self._instance = UserModel()

    def post(self):
        print(request.json)
        resp = self._instance.create(request.json)
        if resp == False:
            return make_response(jsonify({
                "error": "Failed to add. There are items in your request that are invalid."
            }), 400)
        return jsonify(resp)

    def check(self, user_id, filters=None):
        if filters is not None:
            filters['id'] = user_id
        else:
            filters = {"id": user_id}
        user = self._instance.read(filters)
        if user is None:
            return make_response(jsonify({"error": "User id not found."}), 404)
        return user

    def get(self, user_id=None):
        filters = {}
        if 'fields' in request.args:
            filters['fields'] = request.args['fields'].split(',')
        if user_id is not None:
            user = self.check(user_id, filters)
            if not isinstance(user, dict):
                return user
            return jsonify(user)
        filters['offset'] = int(request.args['offset']) if 'offset' in request.args else 0
        filters['limit'] = int(request.args['limit']) if 'limit' in request.args else 5
        users = self._instance.read(filters)
        total = self._instance.read(filters, True)
        return jsonify({
            'metadata': {
                'total': total,
                'links': self.build_links(total, filters['offset'], filters['limit'])
            },
            'data': users
        })

    def put(self, user_id=None):
        if user_id is not None:
            user = self.check(user_id)
            if not isinstance(user, dict):
                return user
            user_data = request.json
            user_data['id'] = user_id
            resp = self._instance.update(user_data)
            if resp == False:
                return make_response(jsonify({
                    "error": "Failed to update. There are items in your request that are invalid."
                }), 400)
            return jsonify(resp)
        return jsonify(self._instance.update(request.json))

    def delete(self, user_id=None):
        if user_id is not None:
            user = self.check(user_id)
            if not isinstance(user, dict):
                return user
            return jsonify(self._instance.delete(user_id))
        return jsonify(self._instance.delete(request.json))