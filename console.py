#!/usr/bin/python3
"""Defines the HBNB console."""
import cmd
from shlex import split
from models import storage
from datetime import datetime
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


class HBNBCommand(cmd.Cmd):
    """Defines the HolbertonBnB command interpreter."""

    prompt = "(hbnb) "
    __classes = {
        "BaseModel",
        "User",
        "State",
        "City",
        "Amenity",
        "Place",
        "Review"
    }
    cmd_list= {
        'all', 'count',
        'show', 'destroy',
        'update'
    }
    variables = {
             'number_rooms': int, 'number_bathrooms': int,
             'max_guest': int, 'price_by_night': int,
             'latitude': float, 'longitude': float
            }
    
    
    def preloop(self):
        """Prints if isatty is false"""
        if not sys.__stdin__.isatty():
            print('(hbnb)')

    def precmd(self, line):
        """Reformat command line for advanced command syntax.

        Usage: <class name>.<command>([<id> [<*args> or <**kwargs>]])
        (Brackets denote optional fields in usage example.)
        """
        _cmd = '' 
        _cls = ''
        _id = ''
        _args = ''

        if not ('.' in line and '(' in line and ')' in line):
            return line

        try:
            parse = line[:]
            _cls = parse[:parse.find('.')]
            _cmd = parse[parse.find('.') + 1:parse.find('(')]
            if _cmd not in HBNBCommand.cmd_list:
                raise Exception
            parse = parse[parse.find('(') + 1:parse.find(')')]
            if parse:
                parse = parse.partition(', ')
                _id = parse[0].replace('\"', '')
                parse = parse[2].strip()
                if parse:
                    if parse[0] is '{' and parse[-1] is '}'\
                            and type(eval(parse)) is dict:
                        _args = parse
                    else:
                        _args = parse.replace(',', '')
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
        exit()

    def help_quit(self):
        """ Prints the help documentation for quit  """
        print("Exits the program with formatting\n")

    def do_EOF(self, arg):
        """ Handles EOF to exit program """
        print()
        exit()

    def help_EOF(self):
        """ Prints the help documentation for EOF """
        print("Exits the program without formatting\n")

    def emptyline(self):
        """ Overrides the emptyline method of CMD """
        pass

    def do_create(self, args):
        """ Create an object of any class

        Command syntax: create <Class name> <param 1> <param 2> <param 3>...
        Param syntax: <key name>=<value>
        """
        try:
            if not args:
                raise SyntaxError()
            my_list = args.split(" ")
            obj = eval("{}()".format(my_list[0]))
            for attr in my_list[1:]:
                my_att = attr.split('=')
                try:
                    casted = HBNBCommand.verification(my_att[1])
                except Exception:
                    continue
                if not casted:
                    continue
                setattr(obj, my_att[0], casted)
            obj.save()
            print("{}".format(obj.id))
        except SyntaxError:
            print("** class name missing **")
        except NameError as e:
            print("** class doesn't exist **")

    def help_create(self):
        """ Help information for the create method """
        print("Creates a class of any type")
        print("[Usage]: create <className>\n")

    def do_show(self, args):
        """ Method to show an individual object """
        new = args.partition(" ")
        c_name = new[0]
        c_id = new[2]
        if c_id and ' ' in c_id:
            c_id = c_id.partition(' ')[0]

        if not c_name:
            print("** class name missing **")
            return

        if c_name not in HBNBCommand.cls_list:
            print("** class doesn't exist **")
            return

        if not c_id:
            print("** instance id missing **")
            return

        key = c_name + "." + c_id
        try:
            print(storage._FileStorage__objects[key])
        except KeyError:
            print("** no instance found **")

    def help_show(self):
        """ Help information for the show command """
        print("Shows an individual instance of a class")
        print("[Usage]: show <className> <objectId>\n")

    def do_destroy(self, args):
        """ Destroys a specified object """
        new = args.partition(" ")
        c_name = new[0]
        c_id = new[2]
        if c_id and ' ' in c_id:
            c_id = c_id.partition(' ')[0]

        if not c_name:
            print("** class name missing **")
            return

        if c_name not in HBNBCommand.cls_list:
            print("** class doesn't exist **")
            return

        if not c_id:
            print("** instance id missing **")
            return

        key = c_name + "." + c_id

        try:
            del(storage.all()[key])
            storage.save()
        except KeyError:
            print("** no instance found **")

    def help_destroy(self):
        """ Help information for the destroy command """
        print("Destroys an individual instance of a class")
        print("[Usage]: destroy <className> <objectId>\n")

    def do_all(self, arg):
        """ Shows all objects, or all objects of a class"""

        args = shlex.split(arg)
        obj_list = []
        if len(args) == 0:
            obj_dict = storage.all()
        elif args[0] in cls_list:
            obj_dict = storage.all(cls_list[args[0]])
        else:
            print("** class doesn't exist **")
            return False
        for key in obj_dict:
            obj_list.append(str(obj_dict[key]))
        print("[", end="")
        print(", ".join(obj_list), end="")
        print("]")

    def help_all(self):
        """ Help information for the all command """
        print("Shows all objects, or all of a class")
        print("[Usage]: all <className>\n")

    def do_count(self, args):
        """Count current number of class instances"""
        count = 0
        for k, v in storage._FileStorage__objects.items():
            if args == k.split('.')[0]:
                count += 1
        print(count)

    def help_count(self):
        """ """
        print("Usage: count <class_name>")

    def do_update(self, args):
        """ Updates a certain object with new info """
        c_name = ''
        c_id = ''
        att_name = ''
        value = ''
        kwargs = ''
        args = args.partition(" ")
        if args[0]:
            c_name = args[0]
        else:
            print("** class name missing **")
            return
        if c_name not in HBNBCommand.cls_list: 
            print("** class doesn't exist **")
            return
        args = args[2].partition(" ")
        if args[0]:
            c_id = args[0]
        else:
            print("** instance id missing **")
            return
        key = c_name + "." + c_id
        if key not in storage.all():
            print("** no instance found **")
            return

        if '{' in args[2] and '}' in args[2] and type(eval(args[2])) is dict:
            kwargs = eval(args[2])
            args = []
            for k, v in kwargs.items():
                args.append(k)
                args.append(v)
        else:
            args = args[2]
            if args and args[0] is '\"':
                second_quote = args.find('\"', 1)
                att_name = args[1:second_quote]
                args = args[second_quote + 1:]

            args = args.partition(' ')
            if not att_name and args[0] is not ' ':
                att_name = args[0]
            if args[2] and args[2][0] is '\"':
                value = args[2][1:args[2].find('\"', 1)]
            if not att_val and args[2]:
                value = args[2].partition(' ')[0]

            args = [att_name, value]
        new_dict = storage.all()[key]
        for i, att_name in enumerate(args):
            if (i % 2 == 0):
                att_val = args[i + 1]
                if not att_name:
                    print("** attribute name missing **")
                    return
                if not value:
                    print("** value missing **")
                    return
                if att_name in HBNBCommand.variables:
                    value = HBNBCommand.variables[att_name](value)
                new_dict.__dict__.update({att_name: value})

        new_dict.save()

    def help_update(self):
        """ Help information for the update class """
        print("Updates an object with new information")
        print("Usage: update <className> <id> <attName> <attVal>\n")

    @classmethod
    def verification(cls, my_att):
        """verifies that an attribute is correctly formatted

        Args:
            my_att (any): attribute to be verified.

        Returns:
            any: my_att.
        """
        if my_att[0] is my_att[-1] is '"':
            for n, i in enumerate(my_att[1:-1]):
                if i is '"' and my_att[n] is not '\\':
                    return None
                if i is " ":
                    return None
            return my_att.strip('"').replace('_', ' ').replace("\\\"", "\"")
        else:
            value = 0
            number = "0123456789.-"
            for i in my_att:
                if i not in number:
                    return None
                if i is '.' and value == 1:
                    return None
                elif i is '.' and value == 0:
                    value = 1
            if value == 1:
                return float(my_att)
            else:
                return int(my_att)


if __name__ == "__main__":
    HBNBCommand().cmdloop()
