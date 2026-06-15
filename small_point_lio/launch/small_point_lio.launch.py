from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    lidar_topic_arg = DeclareLaunchArgument("lidar_topic", default_value="/livox/lidar")
    imu_topic_arg = DeclareLaunchArgument("imu_topic", default_value="/livox/imu")
    lidar_type_arg = DeclareLaunchArgument("lidar_type", default_value="livox_pointcloud2")
    lidar_frame_arg = DeclareLaunchArgument("lidar_frame", default_value="livox_frame")
    save_pcd_arg = DeclareLaunchArgument(
        "save_pcd",
        default_value="false",
        description="Whether to enable saving the accumulated point cloud.",
    )
    tf_x_arg = DeclareLaunchArgument("tf_x", default_value="0.0")
    tf_y_arg = DeclareLaunchArgument("tf_y", default_value="0.0")
    tf_z_arg = DeclareLaunchArgument("tf_z", default_value="0.0")
    tf_roll_arg = DeclareLaunchArgument("tf_roll", default_value="0.0")
    tf_pitch_arg = DeclareLaunchArgument("tf_pitch", default_value="0.0")
    tf_yaw_arg = DeclareLaunchArgument("tf_yaw", default_value="0.0")
    tf_parent_frame_arg = DeclareLaunchArgument("tf_parent_frame", default_value="base_link")
    tf_child_frame_arg = DeclareLaunchArgument("tf_child_frame", default_value="livox_frame")

    mid2_tf_x_arg = DeclareLaunchArgument("mid2_tf_x", default_value="0.0")
    mid2_tf_y_arg = DeclareLaunchArgument("mid2_tf_y", default_value="0.0")
    mid2_tf_z_arg = DeclareLaunchArgument("mid2_tf_z", default_value="0.0")
    mid2_tf_roll_arg = DeclareLaunchArgument("mid2_tf_roll", default_value="0.0")
    mid2_tf_pitch_arg = DeclareLaunchArgument("mid2_tf_pitch", default_value="0.0")
    mid2_tf_yaw_arg = DeclareLaunchArgument("mid2_tf_yaw", default_value="0.0")
    mid2_tf_parent_frame_arg = DeclareLaunchArgument("mid2_tf_parent_frame", default_value="base_link")
    mid2_tf_child_frame_arg = DeclareLaunchArgument("mid2_tf_child_frame", default_value="mid2_base_link")

    small_point_lio_node = Node(
        package="small_point_lio",
        executable="small_point_lio_node",
        name="small_point_lio",
        output="screen",
        parameters=[
            PathJoinSubstitution(
                [
                    FindPackageShare("small_point_lio"),
                    "config",
                    "mid360.yaml",
                ]
            ),
            {
                "lidar_topic": LaunchConfiguration("lidar_topic"),
                "imu_topic": LaunchConfiguration("imu_topic"),
                "lidar_type": LaunchConfiguration("lidar_type"),
                "lidar_frame": LaunchConfiguration("lidar_frame"),
            },
            {"save_pcd": ParameterValue(LaunchConfiguration("save_pcd"), value_type=bool)},
        ],
    )

    static_base_link_to_livox_frame = Node(
        package="tf2_ros",
        executable="static_transform_publisher",
        arguments=[
            "--x",
            LaunchConfiguration("tf_x"),
            "--y",
            LaunchConfiguration("tf_y"),
            "--z",
            LaunchConfiguration("tf_z"),
            "--roll",
            LaunchConfiguration("tf_roll"),
            "--pitch",
            LaunchConfiguration("tf_pitch"),
            "--yaw",
            LaunchConfiguration("tf_yaw"),
            "--frame-id",
            LaunchConfiguration("tf_parent_frame"),
            "--child-frame-id",
            LaunchConfiguration("tf_child_frame"),
        ],
    )

    static_base_link_to_mid2_frame = Node(
        package="tf2_ros",
        executable="static_transform_publisher",
        arguments=[
            "--x",
            LaunchConfiguration("mid2_tf_x"),
            "--y",
            LaunchConfiguration("mid2_tf_y"),
            "--z",
            LaunchConfiguration("mid2_tf_z"),
            "--roll",
            LaunchConfiguration("mid2_tf_roll"),
            "--pitch",
            LaunchConfiguration("mid2_tf_pitch"),
            "--yaw",
            LaunchConfiguration("mid2_tf_yaw"),
            "--frame-id",
            LaunchConfiguration("mid2_tf_parent_frame"),
            "--child-frame-id",
            LaunchConfiguration("mid2_tf_child_frame"),
        ],
    )

    return LaunchDescription([
        lidar_topic_arg,
        imu_topic_arg,
        lidar_type_arg,
        lidar_frame_arg,
        save_pcd_arg,
        tf_x_arg,
        tf_y_arg,
        tf_z_arg,
        tf_roll_arg,
        tf_pitch_arg,
        tf_yaw_arg,
        tf_parent_frame_arg,
        tf_child_frame_arg,
        mid2_tf_x_arg,
        mid2_tf_y_arg,
        mid2_tf_z_arg,
        mid2_tf_roll_arg,
        mid2_tf_pitch_arg,
        mid2_tf_yaw_arg,
        mid2_tf_parent_frame_arg,
        mid2_tf_child_frame_arg,
        small_point_lio_node,
        static_base_link_to_livox_frame,
        static_base_link_to_mid2_frame,
    ])
