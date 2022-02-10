import redis
from redis.commands.json.path import Path




class Redis_data:


    def __init__(self,host='127.0.0.1', port='6379', password='heslo_je_heslo', ttl=9+60*60):
        """
        Methods realisation default for using REDIS as cache
        :param host: *
        :param port: *
        :param password: *
        :param ttl: Key lifetime
        """
        self.client = redis.Redis(host=host, port=port, password=password)
        self.ttl = ttl


    def set_data(self, user_id, data):
        self.client.json().set(user_id, Path.rootPath(), data)
        self.client.expire(user_id, self.ttl)

    def get_data(self, user_id):
        return self.client.json().get(user_id)

    def rm_data(self, user_id):
        self.client.delete(user_id)

