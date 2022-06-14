from db import Db

class ItemModel():
    def sanitize(self, items):
        if not isinstance(items, (list, tuple)):
            items = [items]
        clean_items = []
        for item in items:
            if not isinstance(item, dict):
                continue
            if not ('id' in item and 'name' in item and 'quantity' in item):
                continue
            clean_items.append(item)
        return clean_items

    def create(self, items):
        if not isinstance(items, (list, tuple)):
            items = [items]
        clean_items = self.sanitize(items)
        if len(items) != len(clean_items):
            return False
        queries = []
        for item in clean_items:
            sql = "INSERT INTO items(name, quantity, price) VALUES(%s, %s, %s)"
            queries.append({"sql": sql, "bind": (item['name'], item['quantity'], item['price'])})
        db = Db.get_instance()
        result = db.transactional(queries)
        return items

    def read(self, filters=None, count_only=False):
        db = Db.get_instance()
        fields = ['*']
        offset = 0
        limit = 5
        if filters is not None:
            if 'fields' in filters:
                tmp_fields = []
                for field in filters['fields']:
                    if field in ['id', 'name']:
                        tmp_fields.append(field)
                if len(tmp_fields) > 0:
                    fields = tmp_fields
            if 'id' in filters:
                sql = "SELECT " + ','.join(fields) + " FROM items WHERE id = %s"
                item = db.fetchone(sql, filters['id'])
                return item
            if 'offset' in filters:
                offset = int(filters['offset'])
            if 'limit' in filters:
                limit = int(filters['limit'])
        cols = 'COUNT(*) AS total' if count_only else ','.join(fields)
        sql = "SELECT " + cols + " FROM items"
        if not count_only:
            sql += " ORDER BY name LIMIT " + str(offset) + ", " + str(limit)
        if count_only:
            row = db.fetchone(sql)
            return row['total'] if row else 0
        else:
            print("sql")
            print(sql)
            return db.fetchall(sql)

    def update(self, items):
        if not isinstance(items, (list, tuple)):
            items = [items]
        clean_items = self.sanitize(items)
        if len(items) != len(clean_items):
            return False
        print("chongkong")
        print(items)
        queries = []
        for item in clean_items:
            sql = "UPDATE items SET name = %s, quantity = %s, price = %s WHERE id = %s"
            queries.append({"sql": sql, "bind": (item['name'], item['quantity'], item['price'], item['id'])})
        db = Db.get_instance()
        db.transactional(queries)
        return items

    def delete(self, items):
        counter = 0
        if not isinstance(items, (list, tuple)):
            items = [items]
        placeholder = []
        queries = []
        for item in items:
            placeholder.append('%s')
        sql = "DELETE FROM items WHERE id IN (" + ", ".join(placeholder) + ")"
        queries.append({"sql": sql, "bind": items})
        db = Db.get_instance()
        counter = db.transactional(queries)
        return counter
