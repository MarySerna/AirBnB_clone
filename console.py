#!/usr/bin/python3
"""
This is a module for HBNBCommand class.
"""
import shlex
import cmd
import models
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


class HBNBCommand(cmd.Cmd):
    """
    Define commands for HBNB
    """
    prompt = '(hbnb) '
    obj_dict = models.storage._FileStorage__objects
    cls_dict = {"BaseModel": BaseModel,
                "User": User,
                "State": State,
                "City": City,
                "Amenity": Amenity,
                "Place": Place,
                "Review": Review}

    def do_EOF(self, line):
        """
        Command to exit the Interpreter typing EOF
        """
        print()
        return True

    def do_quit(self, line):
        """
        Quit command to exit the program\n
        """
        return True

    def emptyline(self):
        """
        Empty line + ENTER execute anything
        """
        pass

    def do_create(self, arg):
        """
        A method that creates an instance of a class
        """
        if not arg:
            print("** class name missing **")
        elif arg in self.cls_dict:
            name = self.cls_dict[arg]
            new = name()
            new.save()
            print(new.id)
        else:
            print("** class doesn't exist **")

    def do_destroy(self, line):
        """
        Deletes an instance with the class name and id
        """
        args = shlex.split(line)
        if not args:
            print("** class name missing **")
        elif args[0] in self.cls_dict:
            if len(args) != 2:
                print("** instance id missing **")
            elif "{}.{}".format(args[0], args[1]) in HBNBCommand.obj_dict:
                del(HBNBCommand.obj_dict["{}.{}".format(args[0], args[1])])
            else:
                print("** no instance found **")
        else:
            print("** class doesn't exist **")
        models.storage.save()

    def do_show(self, arg):
        """
        Prints representation of based on the class name and id
        """
        commands = shlex.split(arg)
        if len(commands) == 0:
            print('** class name missing **')
        elif len(commands) == 1:
            print("** instance id missing **")
        elif commands[0] not in self.cls_dict:
            print("** class doesn't exist **")
        else:
            instance = commands[0] + '.' + commands[1]
            if instance in models.storage.all():
                print(models.storage.all()[instance])
            else:
                print('** no instance found **')

    def do_all(self, line):
        """
        String representation of all instances based on the class name
        """
        args = shlex.split(line)
        if len(args) == 0:
            obj_list = []
            for key in models.storage.all():
                obj_list.append(str(models.storage.all()[key]))
            print(obj_list)
        elif args[0] in self.cls_dict:
            obj_list = []
            for key in models.storage.all():
                if args[0] in key:
                    obj_list.append(str(models.storage.all()[key]))
            print(obj_list)
        else:
            print("** class doesn't exist **")

    def do_update(self, line):
        """
        Updated instances
        """
        args = shlex.split(line)
        if not args:
            print("** class name missing **")
            return
        elif args[0] not in self.cls_dict:
            print("** class doesn't exist **")
        elif len(args) < 2:
            print("** instance id missing **")
        else:
            k = "{}.{}".format(args[0], args[1])
            try:
                ins = HBNBCommand.obj_dict[k]
            except:
                print("** no instance found **")
                return
            if len(args) < 3:
                print("** attribute name missing **")
                return
            else:
                if len(args) < 4:
                    print("** value missing **")
                    return
                else:
                    try:
                        type_ = type(getattr(ins, args[2]))
                        try:
                            setattr(ins, args[2], type_(args[3]))
                        except:
                            print("You can't cast to type: {}".format(type_))
                    except:
                        setattr(ins, args[2], str(args[3]))

    def default(self, line):
        args = line.split(".")

        if len(args) > 1:
            use_class = args[0]
            use_method = args[1]
            obj_list = models.storage.all()
        if args[1] == "all()":
            self.do_all(use_class)
        elif args[1] == "count()":
            count = 0
            for k in obj_list:
                tok = k.split(".")
                if tok[0] == use_class:
                    count += 1
            print(count)
        elif use_method[:5] == "show(" and use_method[-1] == ")":
                id_str = use_method[5:-1]
                id_num = shlex.split(id_str)
                key = use_class + "." + id_num[0]
                if key not in obj_list:
                    print("** no instance found **")
                else:
                    print(obj_list[key])
        elif use_method[:8] == "destroy(" and use_method[-1] == ")":
                id_str = use_method[8:-1]
                id_num = shlex.split(id_str)
                key = use_class + "." + id_num[0]
                if key not in obj_list:
                    print("** no instance found **")
                else:
                    del obj_list[key]
                    models.storage.save()

if __name__ == '__main__':
    HBNBCommand().cmdloop()
