from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare

def generate_launch_description():
    save_pcd_arg = DeclareLaunchArgument("save_pcd", default_value="false")
    num_threads_arg = DeclareLaunchArgument("num_threads", default_value="4")
    num_neighbors_arg = DeclareLaunchArgument("num_neighbors", default_value="10")
    global_leaf_size_arg = DeclareLaunchArgument("global_leaf_size", default_value="0.25")
    registered_leaf_size_arg = DeclareLaunchArgument("registered_leaf_size", default_value="0.25")
    tf_x_arg = DeclareLaunchArgument("tf_x", default_value="0.0")
    tf_y_arg = DeclareLaunchArgument("tf_y", default_value="0.0")
    tf_z_arg = DeclareLaunchArgument("tf_z", default_value="0.0")
    tf_roll_arg = DeclareLaunchArgument("tf_roll", default_value="0.0")
    tf_pitch_arg = DeclareLaunchArgument("tf_pitch", default_value="0.0")
    tf_yaw_arg = DeclareLaunchArgument("tf_yaw", default_value="0.0")
    tf_parent_frame_arg = DeclareLaunchArgument("tf_parent_frame", default_value="base_link")
    tf_child_frame_arg = DeclareLaunchArgument("tf_child_frame", default_value="livox_frame")
    prior_pcd_file_arg = DeclareLaunchArgument(
        "prior_pcd_file",
        default_value="/home/xli/catkin_ws/src/mapping_relocalization/small_point_lio/pcd/scan.pcd",
    )

    odomtary_node = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution([
                FindPackageShare('small_point_lio'),
                'launch',
                'small_point_lio.launch.py'
            ])
        ),
        launch_arguments={
            'save_pcd': LaunchConfiguration('save_pcd'),
            'tf_x': LaunchConfiguration('tf_x'),
            'tf_y': LaunchConfiguration('tf_y'),
            'tf_z': LaunchConfiguration('tf_z'),
            'tf_roll': LaunchConfiguration('tf_roll'),
            'tf_pitch': LaunchConfiguration('tf_pitch'),
            'tf_yaw': LaunchConfiguration('tf_yaw'),
            'tf_parent_frame': LaunchConfiguration('tf_parent_frame'),
            'tf_child_frame': LaunchConfiguration('tf_child_frame'),
        }.items())
    
    relocalization_node = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution([
                FindPackageShare('small_gicp_relocalization'),
                'launch',
                'small_gicp_relocalization_launch.py'
            ])
        ),
        launch_arguments={
            'num_threads': LaunchConfiguration('num_threads'),
            'num_neighbors': LaunchConfiguration('num_neighbors'),
            'global_leaf_size': LaunchConfiguration('global_leaf_size'),
            'registered_leaf_size': LaunchConfiguration('registered_leaf_size'),
            "prior_pcd_file": LaunchConfiguration('prior_pcd_file')
        }.items())

    return LaunchDescription([
        save_pcd_arg,
        num_threads_arg,
        num_neighbors_arg,
        global_leaf_size_arg,
        registered_leaf_size_arg,
        tf_x_arg,
        tf_y_arg,
        tf_z_arg,
        tf_roll_arg,
        tf_pitch_arg,
        tf_yaw_arg,
        tf_parent_frame_arg,
        tf_child_frame_arg,
        prior_pcd_file_arg,
        odomtary_node,
        relocalization_node,
    ])
