from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    mapping_params_file = LaunchConfiguration("mapping_params_file")
    default_mapping_params_file = PathJoinSubstitution([
        FindPackageShare("slam_bringup"),
        "config",
        "slam_mapping.yaml",
    ])

    return LaunchDescription([
        DeclareLaunchArgument(
            "mapping_params_file",
            default_value=default_mapping_params_file,
            description="Path to slam mapping parameter file.",
        ),

        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                PathJoinSubstitution([
                    FindPackageShare("small_point_lio"),
                    "launch",
                    "small_point_lio.launch.py",
                ])
            ),
            launch_arguments={
                "params_file": mapping_params_file,
            }.items(),
        ),
    ])
