from pyrcareworld.envs.dressing_env import DressingEnv
import pyrcareworld.attributes as attr
import cv2
import os
import numpy as np
import json
import argparse

def _main(use_graphics=False):
    if use_graphics:
        text = """
        An example of the usage of the dressing environment.

        The robot will move to the first position, pick up the cloth, and move to the second position to drop the cloth.

        You can obtain low level information of the cloth, the robot, and use unlimited numbers of cameras to observe the scene.

        Check the website detailed rubric. After each run of the simulation, a json file will be generated in the current directory
        (~/.config/unity3d/RCareWorld/DressingPlayer).
        The path may be different according to the OS and your computer configuration.
        """
        
        print(text)

    # Initialize
    env = DressingEnv(graphics=use_graphics)
    print(env.attrs)
    robot = env.get_robot()
    env.step()
    gripper = env.get_gripper()

    # Move to cloth
    cloth = env.get_cloth()
    cloth_position = cloth.data['position']
    robot.IKTargetDoMove(
        position=[cloth_position[0], cloth_position[1], cloth_position[2]+0.1],  
        duration=2,
        speed_based=False,
    )
    robot.IKTargetDoRotate(
        rotation=[0, 45, -90], 
        duration=2,
        speed_based=False,
    )
    robot.WaitDo()
    env.step()

    # grab cloth
    gripper.GripperClose()
    env.step(300)
    cloth.AddAttach(id=gripper.id, max_dis=0.2)
    env.step()

    # Move to person
    right_arm = [cloth_position[0]-0.93, cloth_position[1]+0.2, cloth_position[2]+0.7]
    robot.IKTargetDoMove(
        right_arm,  
        duration=3,
        speed_based=False,
    )
    robot.IKTargetDoRotate(
        rotation=[0, 90, -90], 
        duration=2,
        speed_based=False,
    )
    robot.WaitDo()
    env.step()

    robot.IKTargetDoMove(
        position=[cloth_position[0]-0.87, cloth_position[1]+0.03, cloth_position[2]+0.7],  
        duration=3,
        speed_based=False,
    )
    robot.WaitDo()
    env.step()

    robot.IKTargetDoMove(
        position=[cloth_position[0]-0.83, cloth_position[1]+0.03, cloth_position[2]+0.2],  
        duration=3,
        speed_based=False,
    )
    robot.WaitDo()
    env.step()

    gripper.GripperOpen()
    cloth.RemoveAttach(id=gripper.id)
    env.step(300)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run RCareWorld dressing environment simulation.')
    parser.add_argument('-g', '--graphics', action='store_true', help='Enable graphics')
    args = parser.parse_args()
    _main(use_graphics=args.graphics)
