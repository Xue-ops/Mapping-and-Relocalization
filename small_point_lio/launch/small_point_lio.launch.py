from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, OpaqueFunction
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
import yaml


TF_DEFAULTS = {
    "tf_x": "0.0",
    "tf_y": "0.0",
    "tf_z": "0.0",
    "tf_roll": "0.0",
    "tf_pitch": "0.0",
    "tf_yaw": "0.0",
    "tf_parent_frame": "base_link",
    "tf_child_frame": "livox_frame",
}


def _load_small_point_lio_params(params_file):
    with open(params_file, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f) or {}
    return config.get("small_point_lio", {}).get("ros__parameters", {})


def _tf_value(params, key):
    return str(params.get(key, TF_DEFAULTS[key]))


def launch_setup(context, *args, **kwargs):
    params_file = LaunchConfiguration("params_file").perform(context)
    params = _load_small_point_lio_params(params_file)

    static_base_link_to_livox_frame = Node(
        package="tf2_ros",
        executable="static_transform_publisher",
        arguments=[
            "--x",
            _tf_value(params, "tf_x"),
            "--y",
            _tf_value(params, "tf_y"),
            "--z",
            _tf_value(params, "tf_z"),
            "--roll",
            _tf_value(params, "tf_roll"),
            "--pitch",
            _tf_value(params, "tf_pitch"),
            "--yaw",
            _tf_value(params, "tf_yaw"),
            "--frame-id",
            _tf_value(params, "tf_parent_frame"),
            "--child-frame-id",
            _tf_value(params, "tf_child_frame"),
        ],
    )

    return [static_base_link_to_livox_frame]


def generate_launch_description():
    params_file = LaunchConfiguration("params_file")
    default_params_file = PathJoinSubstitution(
        [
            FindPackageShare("small_point_lio"),
            "config",
            "mid360.yaml",
        ]
    )

    params_file_arg = DeclareLaunchArgument(
        "params_file",
        default_value=default_params_file,
        description="Path to small_point_lio parameter file.",
    )

    small_point_lio_node = Node(
        package="small_point_lio",
        executable="small_point_lio_node",
        name="small_point_lio",
        output="screen",
        parameters=[
            default_params_file,
            params_file,
        ],
    )

    return LaunchDescription([
        params_file_arg,
        small_point_lio_node,
        OpaqueFunction(function=launch_setup),
    ])
