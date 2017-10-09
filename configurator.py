from ConfigParser import SafeConfigParser


class Configurator():

    config = None

    def __init__(self):
        configfile = 'config.ini'
        config = SafeConfigParser()
        config.read(configfile)

        # Paths
        self.path_axon_home = self.config.get('path', 'axon_home')
        self.path_services = self.path_axon_home + self.config.get('path', 'axon_relative_services')
        self.path_javauser = self.path_axon_home + self.config.get('path', 'axon_relative_javauser') + 'javauser.jar'
        self.path_libs = self.path_axon_home + self.config.get('path', 'axon_relative_libs')
        self.path_classes = self.path_axon_home + self.config.get('path', 'axon_relative_classes')
        self.commander = self.path_axon_home + 'engine/' + config.get('files', 'axon_commander')
        self.sync_home = self.config.get('path', 'synchronizer_home')

        # Adresses and ports
        # Primary node
        self.ax_primary_node = self.config.get('primary_node', 'address')
        self.ax_primary_port = self.config.get('primary_node', 'port')

        # Secondary node
        self.ax_primary_node = self.config.get('secondary_node', 'address')
        self.ax_secondary_port = self.config.get('secondary_node', 'port')

        # Files
        # Services files
        self.services_md5_file = self.config.get('files', 'serviceschecksumfile')
        self.services_to_reload = self.config.get('files', 'servicestoreload')

        # Classes files
        self.classes_md5_file = self.config.get('files', 'classeschecksumfile')
        self.classes_to_reload_file = self.config.get('files', 'classestoreload')
        self.classes_temp_file = self.config.get('files', 'temp_file')

        # Javauser files
        self.javauser_md5_file = self.config.get('files', 'javauser_checksum_file')

        # Reloaders
        # Javauser
        self.javauser_wsclasses_reloader = self.sync_home + self.config.get('scripts', 'javauser_wsclasses_reloader')
