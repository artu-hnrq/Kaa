import pkg_resources as pkg

def package_discovery(entry_point_group):
    return {
        entry_point.name: entry_point.load()
        for entry_point
        in pkg.iter_entry_points(entry_point_group)
    }

def collect_from(entry_point_group):
    discovery = {}
    for entry_point in pkg.iter_entry_points(entry_point_group):
        name = entry_point.name
        load = entry_point.load()

        discovery.setdefault(name, [])
        discovery[name].append(load)

    return discovery

# class Meta(type):
# 	def __new__(meta, name, bases, attr):
# 		"""Meta description of class definition"""
# 		return super(Meta, meta).__new__(meta, name, bases, attr)
#
# 	def __init__(cls, name, bases, attr, compound):
# 		""" Meta intervention on class instantiation """
# 		return super(Meta, cls).__init__(cls, name, bases, attr)
#
# 	def __call__(cls, *args):
# 		""" Meta modifications in object instantiation """
# 		return super(Meta, cls).__call__(cls, *args)
