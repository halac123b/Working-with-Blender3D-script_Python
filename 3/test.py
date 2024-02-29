import math

import pykeentools
import cv2
import numpy
from typing import Optional

print("pykeentools %s, built %s" % (pykeentools.__version__, pykeentools.build_time))


def _load_image(image_path: str):
    """Load image by using OpenCV"""
    # Blender use low-left coordinate, while OpenCV use top-left coordinate, so we need to flip the image
    return cv2.flip(cv2.cvtColor(cv2.imread(image_path), cv2.COLOR_BGR2RGBA), 0) / 255.0


def _write_image(image_path: str, img: numpy.array):
    """Write image by using OpenCV, do the same as _load_image"""
    cv2.imwrite(
        image_path,
        cv2.flip(
            cv2.cvtColor((img * 255.0).astype(numpy.uint8), cv2.COLOR_RGBA2BGRA), 0
        ),
    )


def _build_plane_geo() -> pykeentools.Geo:
    """Create a plane Geometry to use in TextureBuilder"""
    # Class to build mesh, part of Geometry
    mesh_builder = pykeentools.MeshBuilder()

    # Geometry include points, faces and Attribute
    # Create 4 point of plane
    mesh_builder.add_point(numpy.array([0.5, -0.5, 0]))
    mesh_builder.add_point(numpy.array([0.5, 0.5, 0]))
    mesh_builder.add_point(numpy.array([-0.5, 0.5, 0]))
    mesh_builder.add_point(numpy.array([-0.5, -0.5, 0]))

    # Draw face
    mesh_builder.add_face([0, 1, 2, 3])
    # Attribute
    mesh_builder.set_uvs_attribute(
        attribute_type='POINT_BASED',
        uvs=[
            numpy.array([1.0, 0.0]),
            numpy.array([1.0, 1.0]),
            numpy.array([0.0, 1.0]),
            numpy.array([0.0, 0.0])
        ])

    # Geometry object
    geo = pykeentools.Geo()
    geo.add_mesh(mesh_builder.mesh())
    return geo


def _build_view_matrix():
    return numpy.array(
        [[math.cos(-math.pi / 4), -math.sin(-math.pi / 4), 0, 0],
         [math.sin(-math.pi / 4), math.cos(-math.pi / 4), 0, 0],
         [0, 0, 1, -5],
         [0, 0, 0, 1]])


def _build_proj_matrix():
    return pykeentools.math.proj_mat(fl_to_haperture=50.0/36, w=1280.0, h=720.0,
                                     pixel_aspect_ratio=1.0, near=0.1, far=1000.0)


def build_plane_texture(rendered_card_path: str, out_path: str):
    def frame_data_loader(frame: int) -> Optional[pykeentools.texture_builder.FrameData]:
        assert (frame == 0)  # only one frame should be requested
        frame_data = pykeentools.texture_builder.FrameData()
        frame_data.geo = _build_plane_geo()
        frame_data.image = _load_image(rendered_card_path)
        frame_data.model = numpy.eye(4)
        frame_data.view = _build_view_matrix()
        frame_data.projection = _build_proj_matrix()

        return frame_data

    class ProgressCallback(pykeentools.ProgressCallback):
        def set_progress_and_check_abort(self, progress):
            print('building texture ...%2.1f%% done' % (progress * 100, ))
            return False  # return True if operation should be cancelled

    built_texture_rgba = pykeentools.texture_builder.build_texture(
        frames_count=1,
        frame_data_loader=frame_data_loader,
        progress_callback=ProgressCallback(),
        texture_w=512,
        texture_h=512
    )

    _write_image(out_path, built_texture_rgba)


if __name__ == '__main__':
    build_plane_texture(
        'D:/Coder/Python/Original/Working-with-Blender3D-script_Python/3/input.jpg',
        'D:/Coder/Python/Original/Working-with-Blender3D-script_Python/3/output.jpg')
