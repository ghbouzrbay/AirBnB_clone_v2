#!/usr/bin/python3
""" Console Module """
import cmd
import sys
from models.base_model import BaseModel
from models.__init__ import storage
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review
import shlex
from os import environ

cls_list = {
            'BaseModel': BaseModel,
            'User': User,
            'Place': Place,
            'State': State,
            'City': City,
            'Amenity': Amenity,
            'Review': Review
        }


class HBNBCommand(cmd.Cmd):
    """ Contains the functionality for the HBNB console"""
    prompt = "(hbnb) " if sys.__stdin__.isatty() else ''

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
        """Reformat command line for advanced command syntax."""
        cmd = '' 
        _cls = ''
        _id = ''
        arg = ''

        if not ('.' in cmd_line and '(' in cmd_line and ')' in cmd_line):
            return line

        try:
            par_line = cmd_line[:]
            _cls = par_line[:par_line.find('.')]
            cmd = par_line[par_line.find('.') + 1:par_line.find('(')]
            if cmd not in HBNBCommand.cmd_list:
                raise Exception
            par_line = par_line[par_line.find('(') + 1:par_line.find(')')]
            if par_line:
                par_line = par_line.partition(', ')
                _id = par_line[0].replace('\"', '')
                par_line = par_line[2].strip()
                if par_line:
                    if par_line[0] is '{' and par_line[-1] is '}'\
                            and type(eval(par_line)) is dict:
                        arg = par_line
                    else:
                        arg = par_line.replace(',', '')
            cmd_line = ' '.join([cmd, _cls, _id, arg])

        except Exception as mess:
            pass
        finally:
            return cmd_line

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
        """ Create an object of any class"""
        try:
            if not args:
                raise SyntaxError()
            new = args.split(" ")
            objct = eval("{}()".format(new[0]))
            for attribute in new[1:]:
                new_attribute = attribute.split('=')
                try:
                    casted = HBNBCommand.verify_attribute(new_attribute[1])
                except Exception:
                    continue
                if not casted:
                    continue
                setattr(objct, new_attribute[0], casted)
            objct.save()
            print("{}".format(objct.id))
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
        news = args.partition(" ")
        new_user = news[0]
        new_id = news[2]
        if new_id and ' ' in new_id:
            new_id = new_id.partition(' ')[0]

        if not new_user:
            print("** class name missing **")
            return

        if c_name not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return

        if not new_id:
            print("** instance id missing **")
            return

        key = new_user + "." + new_id
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
        news = args.partition(" ")
        new_user = news[0]
        new_id = news[2]
        if new_id and ' ' in new_id:
            new_id = new_id.partition(' ')[0]

        if not new_user:
            print("** class name missing **")
            return

        if new_user not in HBNBCommand.cls_list:
            print("** class doesn't exist **")
            return

        if not new_id:
            print("** instance id missing **")
            return

        key_str = new_user + "." + new_id

        try:
            del(storage.all()[key_str])
            storage.save()
        except KeyError:
            print("** no instance found **")

    def help_destroy(self):
        """ Help information for the destroy command """
        print("Destroys an individual instance of a class")
        print("[Usage]: destroy <className> <objectId>\n")

    def do_all(self, arg):
        """ list all objects, or all objects of a class"""

        arg = shlex.split(arg)
        object_ls = []
        if len(args) == 0:
            object_dict = storage.all()
        elif args[0] in cls_list:
            object_dict = storage.all(cls_list[args[0]])
        else:
            print("** class doesn't exist **")
            return False
        for key_str in object_dict:
            object_ls.append(str(object_dict[key_str]))
        print("[", end="")
        print(", ".join(object_ls), end="")
        print("]")

    def help_all(self):
        """ Help information for the all command """
        print("Shows all objects, or all of a class")
        print("[Usage]: all <className>\n")

    def do_count(self, args):
        """Count current number of class instances"""
        counter = 0
        for key, value in storage._FileStorage__objects.items():
            if args == key.split('.')[0]:
                counter += 1
        print(counter)

    def help_count(self):
        """Help information for the count command"""
        print("Usage: count <class_name>")

    def do_update(self, args):
        """ Updates a certain object with new info """
        new_user = ''
        new_id = ''
        attribute = ''
        value = ''
        key_str = ''
        args = args.partition(" ")
        if args[0]:
            new_user = args[0]
        else:
            print("** class name missing **")
            return
        if new_user not in HBNBCommand.cls_list:
            print("** class doesn't exist **")
            return
        args = args[2].partition(" ")
        if args[0]:
            new_id = args[0]
        else:
            print("** instance id missing **")
            return
        new_key = new_user + "." + new_id
        if new_key not in storage.all():
            print("** no instance found **")
            return
        if '{' in args[2] and '}' in args[2] and type(eval(args[2])) is dict:
            key_str = eval(args[2])
            args = []
            for key, valu in key_str.items():
                args.append(k)
                args.append(v)
        else:
            args = args[2]
            if args and args[0] is '\"':
                quote2 = args.find('\"', 1)
                attibute = args[1:second_quote]
                args = args[second_quote + 1:]

            args = args.partition(' ')
            if not attribute and args[0] is not ' ':
                attribute = args[0]
            if args[2] and args[2][0] is '\"':
                value = args[2][1:args[2].find('\"', 1)]
            if not value and args[2]:
                value = args[2].partition(' ')[0]

            args = [attribute, value]
        new_dict = storage.all()[key_str]
        for i, attribute in enumerate(args):
            if (i % 2 == 0):
                value = args[i + 1]
                if not attribute:
                    print("** attribute name missing **")
                    return
                if not value:
                    print("** value missing **")
                    return
                if attribute in HBNBCommand.variables:
                    value = HBNBCommand.variables[attribute](value)
                new_dict.__dict__.update({attribute: value})

        new_dict.save()

    def help_update(self):
        """ Help information for the update class """
        print("Updates an object with new information")
        print("Usage: update <className> <id> <attName> <attVal>\n")

    @classmethod
    def verification(cls, attribute):
        """verifies that an attribute is correctly formatted

        Args:
            attribute (any): attribute to be verified.

        Returns:
            any: attribute.
        """
        if attribute[0] is attribute[-1] is '"':
            for i, n in enumerate(attribute[1:-1]):
                if n is '"' and attribute[i] is not '\\':
                    return None
                if n is " ":
                    return None
            return attribute.strip('"').replace('_', ' ').replace("\\\"", "\"")
        else:
            lien = 0
            number = "0123456789.-"
            for n in attribute:
                if n not in number:
                    return None
                if n is '.' and lien == 1:
                    return None
                elif n is '.' and lien == 0:
                    lien = 1
            if lien == 1:
                return float(attribute)
            else:
                return int(attribute)


if __name__ == "__main__":
    HBNBCommand().cmdloop()
