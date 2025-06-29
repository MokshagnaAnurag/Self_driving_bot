import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, GroupAction, ExecuteProcess
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from launch.substitutions import LaunchConfiguration
from launch.actions import DeclareLaunchArgument
from launch.conditions import IfCondition

def generate_launch_description():
    package_name = 'articubot_one'

    world = LaunchConfiguration('world', default=os.path.join(
        get_package_share_directory('articubot_one'), 'worlds', 'empty.world'))

    # Print paths for debugging
    sim_path = os.path.join(get_package_share_directory(package_name), 'launch', 'launch_sim.launch.py')
    print('Including:', sim_path)
    sim = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([sim_path]),
        launch_arguments={'world': world}.items()
    )

    rviz_path = os.path.join(get_package_share_directory(package_name), 'launch', 'rsp.launch.py')
    print('Including:', rviz_path)
    rviz = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([rviz_path])
    )

    nav_path = os.path.join(get_package_share_directory(package_name), 'launch', 'navigation_launch.py')
    print('Including:', nav_path)
    nav = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([nav_path])
    )

    joystick_path = os.path.join(get_package_share_directory(package_name), 'launch', 'joystick.launch.py')
    print('Including:', joystick_path)
    joystick = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([joystick_path])
    )

    slam_path = os.path.join(get_package_share_directory(package_name), 'launch', 'online_async_launch.py')
    print('Including:', slam_path)
    slam = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([slam_path])
    )

    rplidar_path = os.path.join(get_package_share_directory(package_name), 'launch', 'rplidar.launch.py')
    print('Including:', rplidar_path)
    rplidar = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([rplidar_path])
    )

    # Autonomous exploration (uncomment only if package is present and built)
    # explore = Node(
    #     package='explore_lite',  # or 'nav2_explore' if you have it
    #     executable='explore',
    #     name='explore',
    #     output='screen',
    #     parameters=[{'use_sim_time': True}]
    # )

    # Frontier exploration (official Nav2)
    frontier_explorer = Node(
        package='nav2_frontier_exploration',
        executable='frontier_exploration',
        name='frontier_explorer',
        output='screen',
        parameters=[{'use_sim_time': True}]
    )

    declare_explore = DeclareLaunchArgument(
        'autonomous_explore',
        default_value='false',
        description='Enable autonomous exploration (random goal publisher)'
    )

    exploration_node = ExecuteProcess(
        condition=IfCondition(LaunchConfiguration('autonomous_explore')),
        cmd=['ros2', 'run', 'articubot_one', 'simple_explorer'],
        output='screen'
    )

    return LaunchDescription([
        DeclareLaunchArgument('world', default_value=world, description='World file'),
        sim,
        rviz,
        nav,
        joystick,
        slam,
        rplidar,
        # explore,  # Uncomment only if built and present!
        frontier_explorer,
        exploration_node,
        declare_explore,
    ]) 
