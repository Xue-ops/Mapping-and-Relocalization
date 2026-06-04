from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    relocalization_params_file = LaunchConfiguration("relocalization_params_file")
    default_relocalization_params_file = PathJoinSubstitution([
        FindPackageShare("slam_bringup"),
        "config",
        "slam_relocalization.yaml",
    ])

    return LaunchDescription([
        DeclareLaunchArgument(
            "relocalization_params_file",
            default_value=default_relocalization_params_file,
            description="Path to slam relocalization parameter file.",
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
                "params_file": relocalization_params_file,
            }.items(),
        ),

        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                PathJoinSubstitution([
                    FindPackageShare("small_gicp_relocalization"),
                    "launch",
                    "small_gicp_relocalization_launch.py",
                ])
            ),
            launch_arguments={
                "params_file": relocalization_params_file,
            }.items(),
        ),
    ])
