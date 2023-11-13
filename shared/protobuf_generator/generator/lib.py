import importlib
import inspect
import sys
import os

from google.protobuf.descriptor import FieldDescriptor
import geometry3d_pb2
import geometry2d_pb2
import kinematics_pb2


class ProtobufModule:
    def __init__(self, subfolder, module_name):
        importlib.import_module(module_name, package=None)
        clsmembers = inspect.getmembers(sys.modules[module_name], inspect.isclass)

        self.subfolder = subfolder.replace("2d", "").replace("3d", "")
        self.java_proto_subpath = subfolder.replace("2d", "2D").replace("3d", "3D")
        self.java_proto_subpath = (
            self.java_proto_subpath[0].upper() + self.java_proto_subpath[1:]
        )
        self.cpp_proto_header = module_name[:-4] + ".pb.h"
        self.messages = []

        for clazz in clsmembers:
            self.messages.append(MessageClass(clazz[0], clazz[1]))


class MessageClass:
    def __init__(self, protobuf_type, protobuf_class):
        self.protobuf_short_type = protobuf_type
        self.has_nested_types = False
        self.local_type = protobuf_type[len("Protobuf") :]

        self.fields: MessageField = []

        for field in protobuf_class.DESCRIPTOR.fields:
            if field.type == FieldDescriptor.TYPE_MESSAGE:
                self.has_nested_types = True

            self.fields.append(MessageField(protobuf_class, field))


class MessageField:
    def __init__(self, protobuf_class, protobuf_field: FieldDescriptor):
        self.name = protobuf_field.name
        self.protobuf_type = protobuf_field.type
        self.is_message = self.protobuf_type == FieldDescriptor.TYPE_MESSAGE
        self.is_private = False
        self.has_units = not self.is_message
        if not self.is_message:
            has_units = False
            has_units = has_units or self.name.endswith("_radians")
            has_units = has_units or self.name.endswith("_meters")

            self.has_units = has_units

        # TODO the thing
        if False:
            pass
        elif isinstance(protobuf_class(), geometry2d_pb2.ProtobufTransform2d):
            self.is_private = True
        elif isinstance(protobuf_class(), geometry2d_pb2.ProtobufRotation2d):
            self.is_private = True
        elif isinstance(protobuf_class(), geometry2d_pb2.ProtobufTranslation2d):
            self.is_private = True
        elif isinstance(protobuf_class(), geometry2d_pb2.ProtobufPose2d):
            self.is_private = True

        elif isinstance(protobuf_class(), geometry3d_pb2.ProtobufTransform3d):
            self.is_private = True
        elif isinstance(protobuf_class(), geometry3d_pb2.ProtobufTranslation3d):
            self.is_private = True
        elif isinstance(protobuf_class(), geometry3d_pb2.ProtobufQuaternion):
            self.is_private = True
        elif isinstance(protobuf_class(), geometry3d_pb2.ProtobufTranslation3d):
            self.is_private = True
        elif isinstance(protobuf_class(), geometry3d_pb2.ProtobufPose3d):
            self.is_private = True
        # if isinstance(protobuf_class(), kinematics_pb2.ProtobufSwerveModulePosition) and self.name == "angle":
        #     self.is_private = True

        if self.is_message:
            field_clazz = type(getattr(protobuf_class(), self.name))
            self.message_type = field_clazz.__name__.replace("Protobuf", "")

        self.name_without_units = self.name
        self.name_without_units = self.name_without_units.replace("_volts", "")
        self.name_without_units = self.name_without_units.replace("_meters", "")
        self.name_without_units = self.name_without_units.replace("_radians", "")
        self.name_without_units = self.name_without_units.replace("_mps", "")
        self.name_without_units = self.name_without_units.replace("_rps", "")

    def get_schema(self, primitive_lookup):
        if self.is_message:
            return self.message_type + " " + self.name

        return primitive_lookup[self.protobuf_type] + " " + self.name


def strip_units(field_name):
    field_name = field_name.replace("_meters", "")
    field_name = field_name.replace("_radians", "")

    return field_name


def snake_to_camel_case(snake_str):
    return "".join(x.capitalize() for x in snake_str.lower().split("_"))


def upper_camel_case(name):
    name = snake_to_camel_case(name)
    return name[0].upper() + name[1:]


def lower_camel_case(name):
    name = snake_to_camel_case(name)
    return name[0].lower() + name[1:]


def render_template(env, template_file, output_file, **kwargs):
    dirname = os.path.dirname(output_file)
    if not os.path.exists(dirname):
        os.mkdir(dirname)
    with open(output_file, "w") as f:
        f.write(env.get_template(template_file).render(**kwargs))
