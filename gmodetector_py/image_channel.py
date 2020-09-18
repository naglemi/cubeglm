class ImageChannel:
    """A single channel plotted either a hybercube, or from a weight array produced by regression

    :param desired_component: A string matching the ID of the component to be plotted (e.g. 'GFP')
    :param color: A string equal to 'red', 'blue', or 'green' – the color that the extracted band will be plotted in
    :param cap: A numeric value of the spectral intensity value that will have maximum brightness in the plot. All with greater intensity will have the same level of brightness. Think of this as image exposure on a camera.
    :ivar channel: stores the value passed by the ``desired_component_or_wavelength`` parameter
    :ivar color: stores the value passed by the ``cap`` parameter
    :ivar cap: stores the value passed by ``desired_component_or_wavelength``
    :ivar weights: 3D array containing weight values
    :ivar image: An image channel stored as a ``PIL.Image`` object, produced by the ``plot`` method of either ``Hypercube`` or ``WeightArray``)

    """
    def __init__(self, weight_array = None, hypercube = None,
    desired_component_or_wavelength, color, cap,
    mode):
        if mode == 'weights':
            image = weight_array.plot(desired_component = desired_component_or_wavelength,
            color = color, cap = cap)
        if mode == 'hypercube':
            image = hypercube.plot(desired_wavelength = desired_component_or_wavelength,
            color = color, cap = cap)

        self.channel = desired_component_or_wavelength
        self.color = color
        self.cap = cap
        self.image = image
