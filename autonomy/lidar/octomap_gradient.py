import octomap


class OcTreeGradient(octomap.OcTree):
    def __init__(self, resolution):
        octomap.OcTree.__init__(self, resolution)

    def calculate_gradient(self, x, y, z):
        if (!self.search((x, y, z)):
            return None
        else:
            pass
