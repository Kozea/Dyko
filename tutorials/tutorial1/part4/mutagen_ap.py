"""
This module defines a simple access point wrapper, allowing to store meta
data in the id3 tags of a file.

"""

from kalamar.access_point.decorator import Decorator, DecoratorItem, DecoratorProperty
from kalamar.property import to_type
from tempfile import NamedTemporaryFile
from mutagen import File


# This access point wrapper defines some additional properties on top of our
# good old file system access point. We will inherit from the
# DecoratorAccessPoint, since it provide the plumbery for our additional
# properties.

class MutagenItem(DecoratorItem):
    """Item storing properties in ID3 tags."""

    # The class MutagenItem inherits from DecoratorItem. A DecoratorItem wraps
    # another item (the "wrapped_item") and stores additional properties, which
    # will be processed by the access point at save time."""

    def __init__(self, access_point, wrapped_item, decorated_values=None):

        # Access point is the MutagenAccessPoint, wrapped item is an item from
        # the underlying access point, and decorated_values are additional
        # values not found in the underlying access point. In our example,
        # decorated_values should be provided at item creation for every tag we
        # want to support.

        super(MutagenItem, self).__init__(access_point, wrapped_item, decorated_values)
        self._mutagen_info = None
        self._temp_file = None

    @property
    def mutagen_info(self):
        """Mutagen id3 informations."""

        # This property is not necessary per se, but is useful to cache the tag
        # information so that we don't copy and parse the stream at each
        # property access.

        if self._mutagen_info is None:
            self._temp_file = NamedTemporaryFile()
            self._temp_file.write(self[self.access_point.stream_property].read())
            self._mutagen_info = File(self._temp_file.name, easy=True)
        return self._mutagen_info


class MutagenProperty(DecoratorProperty):
    """Property used for Mutagen access point definition."""

    # To decorate an Item, the Decorator access point must be initialized with
    # special properties: those properties offer a 'getter' method, wich is
    # called every time the additional property is accessed.

    def __init__(self, property_type, tag_name):

        # The property is inialized with a property type, like a standard
        # property, and a tag name which will be used to retrieve the
        # meta-data.

        super(MutagenProperty, self).__init__(property_type, self.getter)
        self.tag_name = tag_name

    def getter(self, item):
        """Get item value of the property."""

        # This is the actual getter implementation. It accesses the meta data
        # from the tag name.

        return self.cast(item.mutagen_info[self.tag_name])


class MutagenAP(Decorator):
    """Access point wrapper adding ID3-Tag information to the low-level AP."""

    # The ItemDecorator class attribute is the class used to instantiate new
    # items.
    ItemDecorator = MutagenItem

    def __init__(self, wrapped_ap, decorated_properties, stream_property):

        # Our access point is initiliazed with a wrapped access point, a
        # dictionary of decorated properties, and the porperty name
        # corresponding to the actual file content property.

        self.stream_property = stream_property
        super(MutagenAP, self).__init__(wrapped_ap, decorated_properties)

    def preprocess_save(self, item):
        """Manage the tags before we save the item."""

        # Each time someone sets one of the decorated properties (mapped to the
        # tags), it will be temporarily stored in the unsaved_properties
        # dictionary. In the preprocess_save method, we use those properties to
        # fill the ID3 tags, saving the file to a temporary one and then
        # updating the wrapped item stream property to persist them properly to
        # the filesystem.

        if len(item.unsaved_properties):
            for key, value in item.unsaved_properties.items():
                tag_name = self.decorated_properties[key].tag_name
                item.mutagen_info[tag_name] = to_type(value, unicode)
            item._temp_file.file.flush()
            item.mutagen_info.save()
            item._temp_file.file.seek(0)
            data = item._temp_file.file
            item[self.stream_property] = data
