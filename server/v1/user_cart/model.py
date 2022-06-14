from db import Db

class User_CartModel():
    def sanitize(self, users_cart):
        if not isinstance(users_cart, (list, tuple)):
            users_cart = [users_cart]
        clean_users_cart = []
        for user_cart in users_cart:
            if not isinstance(user_cart, dict):
                continue
            if not ('id' in user_cart and 'user_id' in user_cart and 'item_id' in user_cart):
                continue
            clean_users_cart.append(user_cart)
        return clean_users_cart

    def create(self, users_cart):
        if not isinstance(users_cart, (list, tuple)):
            users_cart = [users_cart]
        clean_users_cart = self.sanitize(users_cart)
        if len(users_cart) != len(clean_users_cart):
            return False
        queries = []
        for user_cart in clean_users_cart:
            sql = "INSERT INTO users_cart(user_id, item_id) VALUES(%s, %s)"
            queries.append({"sql": sql, "bind": (user_cart['user_id'], user_cart['item_id'])})
        db = Db.get_instance()
        result = db.transactional(queries)
        return users_cart

    def read(self, filters=None, count_only=False):
        db = Db.get_instance()
        fields = ['*']
        offset = 0
        limit = 5
        if filters is not None:
            cols = 'COUNT(*) AS total' if count_only else ','.join(fields)
            sql = "SELECT " + cols + " FROM users_cart "
            bind = ()
            # if 'fields' in filters:
            #     tmp_fields = []
            #     for field in filters['fields']:
            #         if field in ['id', 'user_id']:
            #             tmp_fields.append(field)
            #     if len(tmp_fields) > 0:
            #         fields = tmp_fields
            if 'id' in filters:
                sql += " WHERE user_id = " +filters['id']
                # sql += " WHERE user_id = %s "
                # bind = (*bind, filters['id']) # append by tuple unpacking
            if 'offset' in filters:
                offset = int(filters['offset'])
            if 'limit' in filters:
                limit = int(filters['limit'])
        if not count_only:
            sql += " LIMIT " + str(offset) + ", " + str(limit)
        if count_only:
            row = db.fetchone(sql)
            return row['total'] if row else 0
        else:
            return db.fetchall(sql)
            # return db.fetchall(sql, bind)

    def update(self, users_cart):
        if not isinstance(users_cart, (list, tuple)):
            users_cart = [users_cart]
        clean_users_cart = self.sanitize(users_cart)
        if len(users_cart) != len(clean_users_cart):
            return False
        queries = []
        for user_cart in clean_users_cart:
            sql = "UPDATE users_cart SET name = %s, quantity = %s, price = %s WHERE id = %s"
            queries.append({"sql": sql, "bind": (user_cart['name'], user_cart['quantity'], user_cart['price'], user_cart['id'])})
        db = Db.get_instance()
        db.transactional(queries)
        return users_cart

    def delete(self, users_cart):
        counter = 0
        if not isinstance(users_cart, (list, tuple)):
            users_cart = [users_cart]
        placeholder = []
        queries = []
        for user_cart in users_cart:
            placeholder.append('%s')
        sql = "DELETE FROM users_cart WHERE id IN (" + ", ".join(placeholder) + ")"
        queries.append({"sql": sql, "bind": users_cart})
        db = Db.get_instance()
        counter = db.transactional(queries)
        return counter
