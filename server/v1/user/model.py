from audioop import tostereo
from db import Db
import hashlib, hmac

class UserModel():
    def sanitize(self, users, password_isOptional = False):
        if not isinstance(users, (list, tuple)):
            users = [users]
        clean_users = []
        for user in users:
            if not isinstance(user, dict):
                continue
            if password_isOptional:
                if  not ('id' in user and 'username' in user): # defining password is optional
                    continue
            else:
                if not ('id' in user and 'username' in user and 'password' in user):
                    continue
            clean_users.append(user)
        return clean_users

    def create(self, users):
        if not isinstance(users, (list, tuple)):
            users = [users]
        clean_users = self.sanitize(users)
        if len(users) != len(clean_users):
            return False
        queries = []
        for user in clean_users:
            user['password'] = hashlib.md5(user['password'].encode()).hexdigest() # hash the password
            # hmac.new('key', 'msg').hexdigest() # use when above is inconsistent (di ko sure sa consistency sa private key) FROM:https://stackoverflow.com/questions/697134/how-to-set-the-crypto-key-for-pythons-md5-module

            sql = "INSERT INTO users(username, password, type, fname, lname) VALUES(%s, %s, %s, %s, %s)"
            queries.append({"sql": sql, "bind": (user['username'], user['password'], user['type'], user["fname"], user["lname"])})
        db = Db.get_instance()
        result = db.transactional(queries)
        return users

    def read(self, filters=None, count_only=False):
        db = Db.get_instance()
        fields = ['*'] # should i include password????
        # fields = ['id', 'username'] # does not include password
        offset = 0
        limit = 5
        if filters is not None:
            if 'fields' in filters:
                tmp_fields = []
                for field in filters['fields']:
                    if field in ['id', 'username']:
                        tmp_fields.append(field)
                if len(tmp_fields) > 0:
                    fields = tmp_fields
            if 'id' in filters:
                sql = "SELECT " + ','.join(fields) + " FROM users WHERE id = %s"
                user = db.fetchone(sql, filters['id'])
                return user
            if 'offset' in filters:
                offset = int(filters['offset'])
            if 'limit' in filters:
                limit = int(filters['limit'])
        cols = 'COUNT(*) AS total' if count_only else ','.join(fields)
        sql = "SELECT " + cols + " FROM users"
        if not count_only:
            sql += " ORDER BY username LIMIT " + str(offset) + ", " + str(limit)
        if count_only:
            row = db.fetchone(sql)
            return row['total'] if row else 0
        else:
            return db.fetchall(sql)

    def update(self, users):
        if not isinstance(users, (list, tuple)):
            users = [users]
        clean_users = self.sanitize(users,  password_isOptional = True)
        if len(users) != len(clean_users):
            return False
        queries = []
        for user in clean_users:

            # if password is in the json update password, otherwise only update username
            if "password" in user:
                user['password'] = hashlib.md5(user['password'].encode()).hexdigest() # hash the password
            
                sql = "UPDATE users SET username = %s, password = %s, type = %s, fname = %s, lname = %s WHERE id = %s"
                queries.append({"sql": sql, "bind": (user['username'], user['password'], user['type'], user['fname'], user['lname'], user['id'])})
            else:
                sql = "UPDATE users SET username = %s WHERE id = %s"
                queries.append({"sql": sql, "bind": (user['username'], user['id'])})
                
        db = Db.get_instance()
        db.transactional(queries)
        # db.execute(queries[])
        return users

    def delete(self, users):
        counter = 0
        if not isinstance(users, (list, tuple)):
            users = [users]
        placeholder = []
        queries = []
        for user in users:
            placeholder.append('%s')
        sql = "DELETE FROM users WHERE id IN (" + ", ".join(placeholder) + ")"
        queries.append({"sql": sql, "bind": users})
        db = Db.get_instance()
        counter = db.transactional(queries)
        return counter
