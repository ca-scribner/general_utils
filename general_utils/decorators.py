def read_only_properties(*attrs):
    """
    Decorator to make select attributes from a class read-only.

    Overrides _setattr_ to raise an AttributeError whenever any attributes listed in attrs is set.  This results in
    attributes that are initially writable (during __init__ of the object), but immediately after __setattr__ is
    overridden to protect the attributes, so it can only be done on an attribute that is fixed after instantiation.

    Modified from: https://stackoverflow.com/questions/14594120/python-read-only-property
                   https://github.com/oz123/oz123.github.com/blob/master/media/uploads/readonly_properties.py

    Args:
        *attrs: String names of attributes to be read-only
    """

    def class_decorator(cls):
        class WrappedClass(cls):
            """The wrapped class"""
            def __setattr__(self, key, value):
                if key in attrs and key in self.__dict__:
                    raise AttributeError(f"Cannot set attribute {key} - attribute is protected")
                else:
                    super().__setattr__(key, value)

        return WrappedClass
    return class_decorator
