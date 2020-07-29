#!/usr/bin/env python3

def get_info():
    """This will be the function that makes adding modules to ame easier."""

    temp_modules = []


    print("Welcome to the module creator.")

    while True:
        
        module_name = input("What is the name of the module? (Enter 'q' to quit) ")
        
        if module_name == 'q':
            break
        
        module_type = input(f"What type of module is this (module types can be found in ansible documentation): ")

        parameters = []
        while True:
            parameter = input("What are the parameter of this module? (Enter 'q' to quit) ")
            if parameter == 'q':
                make_module(module_name, module_type, parameters)
                break
            else:
                parameters.append(parameter)
        




def make_module(module_name, module_type, parameters):
    """Make the module using the info from get_info and put it in the file."""

    module = {module_name: {}}
    
    for parameter in parameters:
        required = input("Is " + parameter + " required (y/n)?")
        
        if required == 'n':
            module[module_name][parameter] = None    

        elif required == 'y':
            module[module_name][parameter] = 'r'
    
    with open('all_modules.yml', 'a') as file_object:
        yaml.dump(module, file_object, default_flow_style=False, sort_keys=False)



def build_playbook():
    """"Starts building a play book"""

    # Prepends the keys at the top of a basic playbook
    building_playbook = [{'hosts': None, 'remote_user': None, 'vars_files': None, 'tasks':[]}]

    # Opening the file that holds all the different Ansible modules
    with open('all_modules.yml') as file_object:
        all_modules = yaml.safe_load(file_object)


    # Infinite loop so it continues to ask for modules to add
    while True:
        # If the users selected module does not exist, it will bring the user to get_info. Which will allow them to add the module then go back to building the playbook.
        selected_module = input("Please enter the name of a module you would like you use (q to quit): ")
        if selected_module not in all_modules.keys():
            if selected_module =='q':
                break
            answer = input("We do not have a record of that module, would you like to add it now (y/n): ")
            if answer == 'y':
                get_info()
                with open('all_modules.yml') as file_object:
                    all_modules = yaml.safe_load(file_object)

        # Drops into this once it determines you do not want to quit or that the module exists        
        else:
            building_playbook[0]['tasks'].append({'name': '', selected_module: all_modules[selected_module]})
            print(building_playbook)
    
    # Allows the user to name the file
    new_file = input("What would you like to call this new playbook: ")
    with open(new_file + '.yml', 'w') as file_object:
        yaml.dump(building_playbook, file_object, sort_keys=False, default_flow_style=False, explicit_start=True)




def edit_playbook():
    start_red_text = '\033[31m'
    end_red_text = '\033[39m'
    filename = input("Please enter the name of the playbook you would like to edit: ")


    with open(filename, "r+") as file_object:
        playbook = yaml.safe_load(file_object)


    while True:

        for section in playbook[0]:
            print(section)
        selected_section = input("What section would you like to edit (or 'q' to quit): ")
            
        if selected_section == 'q':
            break

        elif selected_section not in playbook[0].keys():
            print(start_red_text + 'This section does not exist, please select another one.' + end_red_text)
            continue
            
        # Edit the tasks in the playbook
        elif selected_section == 'tasks':
            edit_tasks(playbook)

        elif selected_section == 'hosts':
            playbook[0]['hosts'] = input("What host/group would you like to have this playbook run on: ")

        elif selected_section == 'remote_user':
            playbook[0]['remote_user'] = input("Enter the username Ansible will log in as: ")

        elif selected_section == 'vars_files':
            playbook[0]['vars_files'] = input("Enter the name of the vars file: ")

        elif selected_section in playbook[0].keys():
            playbook[0][selected_section] = input("Please enter the value for " + selected_section + " : ")
    
    with open(filename, 'r+') as file_object:
        yaml.dump(playbook, file_object, sort_keys=False, default_flow_style=False, explicit_start=True)
    
    
def edit_tasks(playbook):
    # Initialize the index for reaching different tasks
    while True:
        i = 0
        for task in playbook[0]['tasks']:
            print(str(i) + ". " + str(task))
            i = i + 1

                
        task_num = input("Which task would you like to edit: ")

        if task_num == 'q':
            break

        else:
            task_num = int(task_num)


        task_name = input("What is the name of this task: ")            
        playbook[0]['tasks'][task_num]['name'] = task_name

        # Gets the name of the module in the task. I think I will need another way of getting this.
        for key in playbook[0]['tasks'][task_num]:
            if key != 'name':
                module_name = key

                        
        # Enter values for all parameters
        for module_key in playbook[0]['tasks'][task_num][module_name]:
            value = input(module_key + " value: ")

                        
            if value != None:
                playbook[0]['tasks'][task_num][module_name][module_key] = value

            # Need to add ability to add values to module importer for this if statement to work
            elif playbook[0]['tasks'][task_num][module_name][module_key] == 'r':
                pass
                        
            elif key == None:
                to_delete = input("Would you like to delete this parameter (y/n): ")

                if to_delete.title() == 'y':
                    playbook[0]['tasks'][task_num][module_name].pop(module_key)
                            
                elif to_delete.title() == 'n':
                    continue
                    



import yaml


# Shamelessly ripped from stackoverflow
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'



print(bcolors.UNDERLINE + bcolors.HEADER + "\nWelcome to Ansible Made Easier" + bcolors.ENDC + bcolors.ENDC)

option = input("Please enter what you would like to do: \n 1. Enter new modules \n 2. Build a playbook \n 3. Edit a playbook \n 4. Quit \n  >>> ")


if option == '1':
    get_info()

elif option == '2':
    build_playbook()               

elif option == '3':
    edit_playbook()

elif option == '4':
    pass