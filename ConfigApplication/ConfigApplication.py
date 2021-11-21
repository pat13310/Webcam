import configparser
import os.path

class ConfigApp:

    def __init__(self, file):
        self.filename = file
        self.config = configparser.ConfigParser()
        self.config.add_section("Paths")
        self.config.add_section("Url")
        self.config.add_section("Image")
        self.config.add_section("Horodate")
        self.config.add_section("Resolution")
        self.config.add_section("Window")
        self.config.add_section("Camera")

        if os.path.isfile(self.filename):
            self.__readIni__()

    def __readIni__(self):
        self.config.read(self.filename)

    def getConfig(self):
        return self.config

    def set_dir_video(self, path):
        self.config.set('Paths', 'dir_video', path)

    def set_dir_image(self, path):
        self.config.set('Paths', 'dir_image', path)

    def set_file_image(self, file):
        self.config.set('Paths', 'file_image', file)

    def set_file_video(self, file):
        self.config.set('Paths', 'file_video', file)

    def get_file_image(self):
        try:
            s=str(self.config.get('Paths', 'file_image') )
        except:
            s=""
        return s

    def get_file_video(self):
        try:
            s=str(self.config.get('Paths', 'file_video') )
        except:
            s=""
        return s


    def set_dir_music(self, path):
        self.config.set('Paths', 'dir_music', path)

    def get_dir_video(self):
        try:
            s=str(self.config.get('Paths', 'dir_video') )
        except:
            s=""
        return s

    def get_dir_image(self):

        try:
            s=str(self.config.get('Paths', 'dir_image') )
        except:
            s=""
        return s

    def get_dir_music(self):
        try:
            s = str(self.config.get('Paths', 'dir_music'))
        except:
            s = ""
        return s

    def set_horodate(self,key,value):
        self.config.set('Horodate', key, value)

    def get_horodate(self, key):
        try:
            s = str(self.config.get('Horodate', key))
        except:
            s = ""
        return s

    def set_image(self,key,value):
        self.config.set('Image', key, value)

    def get_image(self, key):
        try:
            s = str(self.config.get('Image', key))
        except:
            s = ""
        return s

    def set_url(self,key,value):
        self.config.set("Url",key,value)

    def get_url(self,key):
        try:
            s = str(self.config.get('Url', key))
        except:
            s = ""
        return s

    def set_window(self,key,value):
        self.config.set('Window', key, value)

    def get_window(self, key):
        try:
            s = str(self.config.get('Window', key))
        except:
            s = ""
        return s

    def set_camera(self, key, value):
        self.config.set("Camera",key, value)

    def get_camera(self, key):
        try:
            s = str(self.config.get('Camera', key))
        except:
            s = ""
        return s

    def save(self):
        try:
            with open(self.filename, 'w') as conf:
                self.config.write(conf)
        except Exception as err:
            print(err)
