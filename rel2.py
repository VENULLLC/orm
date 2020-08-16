class BelongsTo:
    
    def __init__(self, fn, local_key="id", foreign_key="user_id"):
        self.fn = fn
        self.local_key = local_key
        self.foreign_key = foreign_key

    def __get__(self, owner, owner_cls):
        return self.fn(owner)()

class Model:
    
    def __call__(self):
        return 'QueryBuilder'

class Post(Model):
    pass

class User(Model):

    @BelongsTo
    def posts(self):
        return Post

x = User()

print(x.posts)
print(x.posts())