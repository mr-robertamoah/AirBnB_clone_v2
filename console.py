#!/usr/bin/python3
""" Console Module """
import cmd
import sys
from models.base_model import BaseModel
import models
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review
import shlex


class HBNBCommand(cmd.Cmd):
    """ Contains the functionality for the HBNB console"""

    # determines prompt for interactive/non-interactive modes
    prompt = '(hbnb) '

    classes = {
               'BaseModel': BaseModel, 'User': User, 'Place': Place,
               'State': State, 'City': City, 'Amenity': Amenity,
               'Review': Review
              }
    dot_cmds = ['all', 'count', 'show', 'destroy', 'update']
    integers = [
             'number_rooms', 'number_bathrooms',
             'max_guest', 'price_by_night'
             ]
    floats = [
             'latitude', 'longitude'
             ]

    def preloop(self):
        """Prints if isatty is false"""
        if not sys.__stdin__.isatty():
            print('(hbnb)')

    def precmd(self, line):
        """Reformat command line for advanced command syntax.

        Usage: <class name>.<command>([<id> [<*args> or <**kwargs>]])
        (Brackets denote optional fields in usage example.)
        """
        _cmd = _cls = _id = _args = ''  # initialize line elements

        # scan for general formating - i.e '.', '(', ')'
        if not ('.' in line and '(' in line and ')' in line):
            return line

        try:  # parse line left to right
            pline = line[:]  # parsed line

            # isolate <class name>
            _cls = pline[:pline.find('.')]

            # isolate and validate <command>
            _cmd = pline[pline.find('.') + 1:pline.find('(')]
            if _cmd not in HBNBCommand.dot_cmds:
                raise Exception

            # if parantheses contain arguments, parse them
            pline = pline[pline.find('(') + 1:pline.find(')')]
            if pline:
                # partition args: (<id>, [<delim>], [<*args>])
                pline = pline.partition(', ')  # pline convert to tuple

                # isolate _id, stripping quotes
                _id = pline[0].replace('\"', '')
                # possible bug here:
                # empty quotes register as empty _id when replaced

                # if arguments exist beyond _id
                pline = pline[2].strip()  # pline is now str
                if pline:
                    # check for *args or **kwargs
                    if pline[0] == '{' and pline[-1] == '}'\
                            and type(eval(pline)) is dict:
                        _args = pline
                    else:
                        _args = pline.replace(',', '')
                        # _args = _args.replace('\"', '')
            line = ' '.join([_cmd, _cls, _id, _args])

        except Exception as mess:
            pass
        finally:
            return line

    def postcmd(self, stop, line):
        """Prints if isatty is false"""
        if not sys.__stdin__.isatty():
            print('(hbnb) ', end='')
        return stop

    def do_quit(self, command):
        """ Method to exit the HBNB console"""
        exit(0)

    def help_quit(self):
        """ Prints the help documentation for quit  """
        print("Exits the program with formatting\n")

    def do_EOF(self, arg):
        """ Handles EOF to exit program """
        print()
        exit(0)

    def help_EOF(self):
        """ Prints the help documentation for EOF """
        print("Exits the program without formatting\n")

    def emptyline(self):
        """ Overrides the emptyline method of CMD """
        pass

    def _parse_args(self, args):
        """ parse the args to return proper dictionary """
        a_dict = {}
        for arg in args:
            if arg == "=":
                pair = arg.split("=", 1)
                key = pair[0]
                value = pair[1]
                if value[0] == value[-1] == '"':
                    shlex.split(value)[0].replace("_", " ")
                else:
                    try:
                        value = int(value)
                    except Exception:
                        try:
                            value = float(value)
                        except Exception:
                            continue
                a_dict[key] = value

        return a_dict

    def do_create(self, arg):
        """ Create an object of any class"""
        args = arg.split()

        if len(args) < 1:
            print("** class name missing **")
            return False

        if args[0] not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return False

        a_dict = self._parse_args(args[1:])

        new_instance = HBNBCommand.classes[args[0]](**a_dict)

        print(new_instance.id)
        new_instance.save()

    def help_create(self):
        """ Help information for the create method """
        print("Creates a class of any type")
        print("[Usage]: create <className>\n")

    def do_show(self, arg):
        """ Method to show an individual object """
        args = shlex.split(arg)
        if len(args) < 1:
            print("** class name missing **")
            return False

        if args[0] not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return False

        if len(args) < 2:
            print("** instance id missing **")
            return False

        key = args[0] + "." + args[1]
        if key in models.storage.all():
            print(models.storage.all()[key])
        else:
            print("** no instance found **")
            return False

    def help_show(self):
        """ Help information for the show command """
        print("Shows an individual instance of a class")
        print("[Usage]: show <className> <objectId>\n")

    def do_destroy(self, arg):
        """ Destroys a specified object """
        args = shlex.split(arg)
        if len(args) < 1:
            print("** class name missing **")
            return False

        if args[0] not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return False

        if len(args) < 2:
            print("** instance id missing **")
            return False

        key = args[0] + "." + args[1]
        if key in models.storage.all():
            del (storage.all()[key])
            storage.save()
        else:
            print("** no instance found **")

    def help_destroy(self):
        """ Help information for the destroy command """
        print("Destroys an individual instance of a class")
        print("[Usage]: destroy <className> <objectId>\n")

    def do_all(self, arg):
        """ Shows all objects, or all objects of a class"""
        args = shlex.split(arg)
        print_list = []
        if len(args) == 0:
            print_dict = models.storage.all()
        elif args[0] in HBNBCommand.classes:
            print_dict = models.storage.all(HBNBCommand.classes[args[0]])
        else:
            print("** class doesn't exist **")
            return False

        for key in print_dict:
            print_list.append(str(print_dict[key]))

        print("[", end="")
        print(", ".join(print_list), end="")
        print("]")

    def help_all(self):
        """ Help information for the all command """
        print("Shows all objects, or all of a class")
        print("[Usage]: all <className>\n")

    def do_count(self, args):
        """Count current number of class instances"""
        count = 0
        for k, v in storage.all().items():
            if args == k.split('.')[0]:
                count += 1
        print(count)

    def help_count(self):
        """ """
        print("Usage: count <class_name>")

    def do_update(self, arg):
        """ Updates a certain object with new info """
        args = shlex.split(arg)
        if len(args) < 1:
            print("** class name missing **")
            return False

        if args[0] not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return False

        if len(args) < 2:
            print("** instance id missing **")
            return False

        key = args[0] + "." + args[1]
        if key in models.storage.all():
            if len(args) > 2:
                if len(args) > 3:
                    if args[0] == "Place":
                        if args[2] in integers:
                            try:
                                args[3] = int(args[3])
                            except Exception:
                                args[3] = 0
                        elif args[2] in floats:
                            try:
                                args[3] = float(args[3])
                            except Exception:
                                args[3] = 0.0
                    setattr(models.storage.all()[key], args[2], args[3])
                    models.storage.all()[key].save()
                else:
                    print("** value missing **")
            else:
                print("** attribute name missing **")
        else:
            print("** no instance found **")

    def help_update(self):
        """ Help information for the update class """
        print("Updates an object with new information")
        print("Usage: update <className> <id> <attName> <attVal>\n")


if __name__ == "__main__":
    HBNBCommand().cmdloop()
