class QueryBuilder:

    def where(self, *arg, **kwargs):
        return self

    def first(self, *arg, **kwargs):
        return 'first'

class Model:
    builder = QueryBuilder()

    def __call__(self, *args, **kwargs):
        return self.builder


class Post(Model):
    title = 'Love It!!'

    builder = QueryBuilder()


    def meth(self):
        return 'method'




class BelongsTo:
    
    def __init__(self, fn=None, local_key="id", foreign_key="author_id"):
        

        if isinstance(fn, str):
            local_key = fn
            foreign_key = local_key
            fn = None


        self.local_key = local_key
        self.foreign_key = foreign_key
        self.model = None
        self.fn = fn
        print('init')
        # self.model = model
        # self.bound_method = bound_method

    def __call__(self, *args, **kwargs):
        print('call', self, self.fn)
        print(args, kwargs)
        if not self.fn:
            """If args has a length the that means it is being called with decorators
            e.x: BelongsTo("id", "user_id")(fn)

            The local and foreign keys are also already set
            """
            self.fn = args[0]
            self.model = self.fn(self)()
            return self.model

        if self.model:
            return self.model.builder
    
    def __set_name__(self, owner, name):
        # do something with owner, i.e.
        print('set name', owner)
        self.model = self.fn(owner)()

    def __getattr__(self, attribute):
        print('gettatr', self.model)
        return getattr(self.model, attribute)


class User(Model):

    @BelongsTo("id", "id")
    def post(self):
        return Post

    # @BelongsTo
    # def post(self):
    #     return Post

x = User()

print(x.post.title)
print(x.post.meth)
print(x.post.meth())
print(x.post)
print(x.post().where(''))
print(x.post().where('').first())