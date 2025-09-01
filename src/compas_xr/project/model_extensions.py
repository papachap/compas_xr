import os  # noqa: I001

from compas.datastructures import Mesh
from compas.datastructures import Part
from compas.geometry import Brep
from compas.geometry import Frame
from compas.geometry import Point
from compas.geometry import Shape
from compas.geometry import Transformation
from compas.geometry import Vector

from compas_model.elements import Element
from compas_model.models import Model


class ModelExtensions(object):
    """
    ModelExtensions is a class for extending the functionality of the :class:`~compas_model.models.Model` class.

    The ModelExtensions class provides additional functionalities such as exporting elements as .obj files
    and creating a frame model from a list of :class:`~compas.geometry.Frame` with a specific data structure
    for localization information.

    """

    def export_model_elements_objs(self, model, folder_path, new_folder_name, z_to_y_remap=False):
        """
        Export model elements as .obj files to a folder path.

        Parameters
        ----------
        model : :class:`~compas_model.models.Model` or :class:`~compas_timber.model.TimberModel`
            The model that you want to export elements from.
        folder_path : str
            The path in which you would like to create a storage folder.
        new_folder_name : str
            The name of the folder you would like to create.
        z_to_y_remap : bool, optional
            A boolean that determines if the z-axis should be remapped to the y-axis for .obj export. Default is False.

        Returns
        -------
        None

        """
        target_folder_path = os.path.join(folder_path, new_folder_name)
        if not os.path.exists(target_folder_path):
            os.makedirs(target_folder_path)

        for element in model.elements:
            element_geometry = element.elementgeometry  # geometry in local coordinate system (WorldXY)
            mesh_geometry = self.get_mesh_from_elementgeometry(element_geometry)

            if z_to_y_remap:
                mesh_geometry.transform(Transformation.from_frame(Frame(Point(0, 0, 0), Vector.Xaxis(), Vector.Zaxis())))

            # Export the mesh geometry to .obj file
            filename = "{}.obj".format(str(element.graphnode))
            mesh_geometry.to_obj(os.path.join(target_folder_path, filename))

    def create_qr_model(self, qr_frames):
        """
        Create a frame model from a list of :class:`~compas.geometry.Frame` with a specific data structure for localization.

        Parameters
        ----------
        qr_frames : list of :class:`~compas.geometry.Frame`
            A list of frames at specific locations for localization data.

        Returns
        -------
        :class:`~compas_model.models.Model`
            The constructed database reference.

        """
        model = Model()
        for i, frame in enumerate(qr_frames):
            name = "QR_{}".format(i)
            element = Element(name=name, frame=frame, shape=frame)

            model.add_element(element)
        return model

    @staticmethod
    def get_mesh_from_elementgeometry(geometry):
        """
        Extract the mesh from a model element's geometry.

        Parameters
        ----------
        geometry : :class:`~compas.geometry.Mesh` or :class:`~compas.geometry.Brep`
            The geometry of the model element.

        Returns
        -------
        :class:`~compas.datastructures.Mesh`
            The mesh representation of the element geometry.

        """
        if isinstance(geometry, Mesh):
            return geometry
        elif isinstance(geometry, Brep):
            mesh_faces = geometry.to_meshes()
            mesh_geometry = Mesh()
            for face in mesh_faces:
                mesh_geometry.join(face)
            return mesh_geometry
        else:
            raise TypeError("Unsupported geometry type: {}".format(type(geometry)))
