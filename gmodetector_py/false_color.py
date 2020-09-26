from gmodetector_py import checkIfDuplicates_l
from gmodetector_py import stack_images

class FalseColor:
    """A combination of channels visualized from either a hybercube, or from a weight array produced by regression

    :param inputs: A list of ``ImageChannel`` objects
    :ivar IDs: stores a list of strings passed by the ``channel`` attributes of objects in the ``inputs`` list
    :ivar colors: stores a list strings passed by the ``color`` attributes of objects in the ``inputs`` list
    :ivar caps: stores a list of numeric values passed by ``cap`` attributes of objects in the ``inputs`` list
    :ivar image: An image channel stored as a ``PIL.Image`` object, produced by the ``plot`` method of either ``Hypercube`` or ``WeightArray``)

    """

    def save(self, path_prefix, output_dir = "./"):
        import pandas as pd
        metadata = pd.DataFrame(zip(self.IDs,
                                    self.colors,
                                    self.caps),
                                columns = ['Channel', 'Color', 'Cap'])

        metadata_path = output_dir + path_prefix + ".csv"
        image_path = output_dir + path_prefix + ".png"

        print('Saving image to ' + image_path)
        print('Saving image metadata to ' + metadata_path)

        metadata.to_csv(metadata_path)
        self.image.save(image_path)

    def __init__(self, inputs):

        # Thank you Reto Aebersold for showing how to obtain a list of attributes for a list of objects
        # https://stackoverflow.com/questions/2739800/extract-list-of-attributes-from-list-of-objects-in-python
        channels = list(x.channel for x in inputs)
        images = list(x.image for x in inputs)
        colors = list(x.color for x in inputs)
        caps = list(x.cap for x in inputs)

        sources = list(x.source for x in inputs)
        if len(set(sources)) > 1:
            raise Exception('The image channels submitted do not appear to be from the same sample.')

        if checkIfDuplicates_l(colors):
            raise Exception('Cannot produce false color image from multiple channels of a single color. The colors must be different for each channel.')

        stacked_image = stack_images(images)

        self.IDs = channels
        self.colors = colors
        self.caps = caps
        self.image = stacked_image
        self.source = sources[0]
