import os
import sys
import colorama

from art import tprint
from colorama import Fore
colorama.init(autoreset=True)


class FileEditor():

    def __init__(self, argv) -> None:
        user_file = open(argv[1])
        self.file_map = user_file.readlines()
        self.seperator = Fore.WHITE + '\n' + '-'*15 + '\n'

    def check_user_input(self, line):
        try:
            index = int(line) - 1
        except ValueError:
            print(Fore.RED + 'Invalid Line Type\n')
            return -1
        if index > len(self.file_map):
            print(Fore.RED + f'No such line found : {index+1}\n')
            return -1
        return index

    def read_file(self):
        print(self.seperator)
        print(Fore.YELLOW + 'Total number of lines : ' +
              str(len(self.file_map)) + '\n')
        for item, i in zip(self.file_map, range(len(self.file_map))):
            print(Fore.YELLOW + f'[{str(i + 1)}]\t' + Fore.GREEN + item)
        print(self.seperator)

    def edit_file(self):
        print(self.seperator)
        line = input(Fore.YELLOW + 'Enter line position to edit to : ')
        index = self.check_user_input(line)
        if index == -1:
            return
        content = input(Fore.YELLOW + 'Enter edited string : ')
        self.file_map.remove(self.file_map[index])
        self.file_map.insert(index, content + '\n')
        print(Fore.GREEN + 'File edited successfully')
        print(self.seperator)

    def delete_line(self):
        print(self.seperator)
        lines = input(Fore.YELLOW + 'Enter lines to be deleted : ').split(' ')
        indexes = [self.check_user_input(i) for i in lines]
        deleted_items = [self.file_map[i] for i in indexes]
        for item in deleted_items:
            self.file_map.remove(item)
        print(Fore.GREEN + 'Following lines were removed successfully:\n')
        for item in deleted_items:
            print('> ' + item)
        print(self.seperator)

    def add_line(self):
        print(self.seperator)
        line = input(
            Fore.YELLOW + 'Add line position to add to (leave blank if want to add last) : ')
        if line == '':
            index = len(self.file_map)+1
        else:
            index = self.check_user_input(line)
        if index == -1:
            return
        content = input(Fore.YELLOW + 'Enter line data : ')
        self.file_map.insert(index, content + '\n')
        print(Fore.GREEN + 'Line added successfully')
        print(self.seperator)

    def save_file(self):
        data = ''
        for item in self.file_map:
            data += item
        with open(sys.argv[1], 'w') as f:
            f.write(data)
        print(Fore.GREEN + 'File saved successfully\n')

    def search_line(self):
        print(self.seperator)
        line = input(Fore.YELLOW + 'Enter line to search : ').upper()
        general_data = [i.upper() for i in self.file_map]
        result = []
        for i, item in zip(range(len(general_data)), general_data):
            if line in item:
                result.append((i, self.file_map[i]))
        print(Fore.YELLOW + f'The search returned {len(result)} results : \n')
        for item in result:
            print(Fore.GREEN + f'[{item[0]}]\t{item[1]}')
        print(self.seperator)


class CommandLine():

    def __init__(self, argv):
        self.args = argv
        self.editor = FileEditor(argv)

    def intro(self):
        try:
            os.system("cls")
        except os.error:
            os.system("clear")
        print(Fore.CYAN + '\n' + '='*51)
        print(Fore.CYAN + '========   COMMAND LINE TEXT EDITOR v1.0   ========')
        print(Fore.CYAN + '='*51 + '\n')
        tprint("Pied   Piper")
        print(Fore.MAGENTA + "\nFile Opened : " + Fore.WHITE + self.args[1])
        print(Fore.MAGENTA + "Run $help to get started\n")

    def show_commands(self):
        print(Fore.YELLOW +
              '\n Remember to run $save for the changes to be reflected on the file.')
        print(Fore.MAGENTA + '\n CMD\t\tFunction')
        print(' ---\t\t--------\n')
        print(Fore.YELLOW + ' $read\t\tRead file contents\n')
        print(Fore.YELLOW + ' $edit\t\tEdit lines in file at specified position\n')
        print(Fore.YELLOW +
              ' $delete\tDelete lines frome file at specified position\n')
        print(Fore.YELLOW + ' $add\t\tAdd line at specified position in the file\n')
        print(Fore.YELLOW + ' $save\t\tSave the changes made to the file\n')
        print(Fore.YELLOW + ' $search\tSearch for keywords within the file\n')
        print(Fore.YELLOW + ' $clc\t\tClears the command prompt\n')
        print(Fore.YELLOW + ' $exit\t\tExit the program')
        print('\n')

    def exit_program(self):
        while True:
            print(self.editor.seperator)
            user_input = input(
                Fore.MAGENTA + "Are you sure you want to exit ? Y\\N\n").upper()
            if user_input == 'Y':
                print(Fore.CYAN + '\n' + '='*51)
                print(Fore.CYAN + '======    THANK YOU FOR USING PIED PIPER!    ======')
                print(Fore.CYAN + '='*51 + '\n')
                sys.exit()
            elif user_input == 'N':
                print('-'*35)
                print('\n')
                return
            else:
                print(Fore.RED + 'Invalid Answer')

    def panel(self):
        while True:
            try:
                user_input = input(Fore.CYAN + '>> ')
                if user_input == '$exit':
                    self.exit_program()
                elif user_input == '$read':
                    self.editor.read_file()
                elif user_input == '$edit':
                    self.editor.edit_file()
                elif user_input == '$delete':
                    self.editor.delete_line()
                elif user_input == '$add':
                    self.editor.add_line()
                elif user_input == '$save':
                    self.editor.save_file()
                elif user_input == '$search':
                    self.editor.search_line()
                elif user_input == '$clc':
                    self.intro()
                elif user_input == '$help':
                    self.show_commands()
                elif user_input == '':
                    continue
                else:
                    print(Fore.RED + '>> Undefined Argument')
            except KeyboardInterrupt:
                self.exit_program()

    def check_file(self):
        if len(self.args) == 1:
            print(Fore.RED + 'Please specify a file path as a CMD line argument')
            return False
        elif len(self.args) > 2:
            print(Fore.RED + 'Too many arguments to unpack.')
            return False
        elif not os.path.exists(self.args[1]):
            print(Fore.RED + 'Argument File path does not exist.')
            return False
        return True


def main():
    cmd_line = CommandLine(sys.argv)
    file_status = cmd_line.check_file()
    if file_status:
        cmd_line.intro()
        cmd_line.panel()
    else:
        exit(1)


if __name__ == '__main__':
    main()
