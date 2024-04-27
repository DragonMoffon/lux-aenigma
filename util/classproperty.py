# https://stackoverflow.com/questions/5189699/how-to-make-a-class-property
class classproperty(object):
    def __init__(self, f):
        self.f = f

    def __get__(self, obj, owner):
        return self.f(owner)
