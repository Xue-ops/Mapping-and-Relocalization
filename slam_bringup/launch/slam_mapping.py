from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, OpaqueFunction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare
import yaml


YAML_VALUE = "__from_yaml__"


def _to_launch_value(value):
    if isinstance(value, bool):
        return "true" if value else "false"
    return str(value)


def _load_small_point_lio_params(context):
    params_file = LaunchConfiguration("mapping_params_file").perform(context)
    with open(params_file, "r") as file:
        params = yaml.safe_load(file) or {}

    return params.get("small_point_lio", {}).get("ros__parameters", {})


def _launch_setup(context, *args, **kwargs):
    small_point_lio_params = _load_small_point_lio_params(context)

    def param(name, default):
        launch_value = LaunchConfiguration(name).perform(context)
        if launch_value != YAML_VALUE:
            return launch_value
        return _to_launch_value(small_point_lio_params.get(name, default))

    return [
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                PathJoinSubstitution([
                    FindPackageShare("small_point_lio"),
                    "launch",
                    "small_point_lio.launch.py",
                ])
            ),
            launch_arguments={
                "save_pcd": param("save_pcd", True),
                "tf_x": param("tf_x", 0.0),
                "tf_y": param("tf_y", 0.0),
                "tf_z": param("tf_z", 0.0),
                "tf_roll": param("tf_roll", 0.0),
                "tf_pitch": param("tf_pitch", 0.0),
                "tf_yaw": param("tf_yaw", 0.0),
                "tf_parent_frame": param("tf_parent_frame", "base_link"),
                "tf_child_frame": param("tf_child_frame", "livox_frame"),
                "mid2_tf_x": param("mid2_tf_x", 0.0),
                "mid2_tf_y": param("mid2_tf_y", 0.0),
                "mid2_tf_z": param("mid2_tf_z", 0.0),
                "mid2_tf_roll": param("mid2_tf_roll", 0.0),
                "mid2_tf_pitch": param("mid2_tf_pitch", 0.0),
                "mid2_tf_yaw": param("mid2_tf_yaw", 0.0),
                "mid2_tf_parent_frame": param("mid2_tf_parent_frame", "base_link"),
                "mid2_tf_child_frame": param("mid2_tf_child_frame", "mid2_base_link"),
            }.items(),
        ),
    ]


def generate_launch_description():
    default_mapping_params_file = PathJoinSubstitution([
        FindPackageShare("slam_bringup"),
        "config",
        "slam_mapping.yaml",
    ])

    small_point_lio_arg_names = [
        "save_pcd",
        "tf_x",
        "tf_y",
        "tf_z",
        "tf_roll",
        "tf_pitch",
        "tf_yaw",
        "tf_parent_frame",
        "tf_child_frame",
        "mid2_tf_x",
        "mid2_tf_y",
        "mid2_tf_z",
        "mid2_tf_roll",
        "mid2_tf_pitch",
        "mid2_tf_yaw",
        "mid2_tf_parent_frame",
        "mid2_tf_child_frame",
    ]

    return LaunchDescription([
        DeclareLaunchArgument(
            "mapping_params_file",
            default_value=default_mapping_params_file,
            description="Path to slam mapping parameter file.",
        ),
        *[
            DeclareLaunchArgument(
                name,
                default_value=YAML_VALUE,
                description=f"Override {name}; default is loaded from mapping_params_file.",
            )
            for name in small_point_lio_arg_names
        ],
        OpaqueFunction(function=_launch_setup),
    ])
