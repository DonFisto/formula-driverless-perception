from setuptools import find_packages, setup

package_name = 'lidar_perception'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='donfisto',
    maintainer_email='dmcvg@icloud.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
        'obstacle_node = lidar_perception.obstacle_node:main',
        'scan_to_cloud_node = lidar_perception.scan_to_cloud_node:main',
            'reactive_navigation_node = lidar_perception.reactive_navigation_node:main',
            'occupancy_grid_node = lidar_perception.occupancy_grid_node:main',
        ],
    },
)
