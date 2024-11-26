import os
from dynamic_leds.dynamic_leds import DynamicLeds


def print_heading():
    print('''
_______  ____    ____ .__   __.      ___      .___  ___.  __    ______     __       _______  _______       _______.
|       \ \   \  /   / |  \ |  |     /   \     |   \/   | |  |  /      |   |  |     |   ____||       \     /       |
|  .--.  | \   \/   /  |   \|  |    /  ^  \    |  \  /  | |  | |  ,----'   |  |     |  |__   |  .--.  |   |   (----`
|  |  |  |  \_    _/   |  . `  |   /  /_\  \   |  |\/|  | |  | |  |        |  |     |   __|  |  |  |  |    \   \    
|  '--'  |    |  |     |  |\   |  /  _____  \  |  |  |  | |  | |  `----.   |  `----.|  |____ |  '--'  |.----)   |   
|_______/     |__|     |__| \__| /__/     \__\ |__|  |__| |__|  \______|   |_______||_______||_______/ |_______/    
''')

def input_choice():
    return input("Enter your choice (or Ctrl+D to exit): ")
    
def choose_scene():
    global l
    scenes_path = 'scenes'  # Specify the path to the scenes folder
    try:
        # List all directories in the scenes folder
        scene_dirs = sorted([d for d in os.listdir(scenes_path) if os.path.isdir(os.path.join(scenes_path, d))])
        if scene_dirs:
            print('\nAvailable scenes:')
            for i, scene in enumerate(scene_dirs):
                print(f'{i+1}. {scene}')
        else:
            print("No scenes found.")
            return
        
        while True:
            # Ask user to choose a scene and load it
            scene_no = input_choice()
            if scene_no.isdigit() and 0 < int(scene_no) <= len(scene_dirs):
                scene_name = scene_dirs[int(scene_no) - 1]
                print()
                l.load_scene(scene_name)
                break
            else:
                print("Invalid choice. Please try again.")
            
    except FileNotFoundError:
        print(f"Error: The directory '{scenes_path}' does not exist.")
        

def choose_effect():
    global l
    effect_names = l.scene.list_effects()
    
    print('\nAvailable effects:')
    for i, effect_name in enumerate(effect_names):
        print(f'{i+1}. {effect_name}')
    
    while True:
        # Ask user to choose an effect and run it
        effect_no = input_choice()
        if effect_no.isdigit() and 0 < int(effect_no) <= len(effect_names):
            effect_name = effect_names[int(effect_no) - 1]
            print()
            l.scene.run_effect(effect_name)
            break
        else:
            print("Invalid choice. Please try again.")

def scan():
    global l
    
    # TODO select correct scanner class based on config file.
    # or based on user input??
    # Scanner.__subclasses__()
    
    l.scene.scan()
    
l = DynamicLeds()

print_heading()
print('To begin, please choose a scene.')
choose_scene()
print('\nNext, choose an effect to run.')
choose_effect()

while True:
    print('\n----------')
    print('Current scene:', l.scene.name)
    print("\n1. Run an effect.")
    print("2. Load a new scene.")
    if l.scene.layout != 'LINE':
        print("3. Rescan the scene")
    choice = input_choice()
    if choice == '1':
        choose_effect()
    elif choice == '2':
        choose_scene()
    elif choice == '3':
        l.scene.scan()