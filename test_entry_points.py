from importlib.metadata import entry_points

discovered_plugins = entry_points()

print(sorted(discovered_plugins.groups))
