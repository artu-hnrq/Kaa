import pkg_resources as pkg

def package_discovery(entry_point_group):
    "Return {name: func} for each entry point in the given group"

    return {
        entry_point.name: entry_point.load()
        for entry_point
        in pkg.iter_entry_points(entry_point_group)
    }
