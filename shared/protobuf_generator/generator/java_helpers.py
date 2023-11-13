from google.protobuf.descriptor import FieldDescriptor
from jinja2 import Environment, FileSystemLoader
import os

from shared.protobuf_generator.generator.lib import (
    MessageClass,
    ProtobufModule,
    MessageField,
    upper_camel_case,
    lower_camel_case,
    render_template,
    snake_to_camel_case,
)

PROTO_TYPE_TO_JAVA_TEXT = {
    FieldDescriptor.TYPE_DOUBLE: "double",
    FieldDescriptor.TYPE_BOOL: "boolean",
    FieldDescriptor.TYPE_INT32: "int",
    FieldDescriptor.TYPE_UINT32: "int",
}


def __struct_unpack(field: MessageField):
    if field.is_message:
        return field.message_type + ".struct.unpack(bb)"

    local_type = __local_type(field)
    getter = "get" + local_type[0].upper() + local_type[1:]
    return f"bb.{getter}()"


def __struct_pack(field: MessageField):
    if field.is_message:
        return field.message_type + f".struct.pack(bb, value.{__local_getter(field)})"

    local_type = __local_type(field)
    setter = "put" + local_type[0].upper() + local_type[1:]
    return f"bb.{setter}(value.{__local_getter(field)})"


def __local_type(field: MessageField):
    if field.is_message:
        return field.message_type
    return PROTO_TYPE_TO_JAVA_TEXT[field.protobuf_type]


def __get_schema(message: MessageClass):
    return ";".join(
        field.get_schema(PROTO_TYPE_TO_JAVA_TEXT) for field in message.fields
    )


def __get_struct_size(message: MessageClass):
    num_doubles = 0
    num_ints = 0

    subclass_parts = []

    output = ""

    for field in message.fields:
        if field.is_message:
            subclass_parts.append(f"{field.message_type}.struct.getSize()")
        elif field.protobuf_type == FieldDescriptor.TYPE_DOUBLE:
            num_doubles += 1
        elif field.protobuf_type == FieldDescriptor.TYPE_INT32:
            num_ints += 1
        elif field.protobuf_type == FieldDescriptor.TYPE_UINT32:
            num_ints += 1
        else:
            raise Exception(
                f"Unsupported type {field.protobuf_type} for field {field.name}"
            )

    if num_doubles > 1:
        output += f"kSizeDouble * {num_doubles}"
    elif num_doubles == 1:
        output += f"kSizeDouble"

    if subclass_parts and output:
        output += " + "
    output += " + ".join(subclass_parts)

    return output


def __proto_getter(field: MessageField):
    return f"get{upper_camel_case(field.name)}"


def __proto_setter(field: MessageField):
    if field.is_message:
        return f"getMutable{upper_camel_case(field.name)}"
    return f"set{upper_camel_case(field.name)}"


def __local_getter(field: MessageField):
    field_name = field.name_without_units
    field_name = field_name.replace("volts", "voltage")
    field_name = field_name.replace("mps", "meters_per_second")
    field_name = field_name.replace("rps", "radians_per_second")

    if field.is_message or field.is_private:
        return f"get{snake_to_camel_case(field.name_without_units)}()"

    output = lower_camel_case(field_name)
    return output


def __get_protobuf_unpack(message: MessageClass):
    output_fields = []

    for field in message.fields:
        if field.is_message:
            output_fields.append(
                f"\n        {field.message_type}.proto.unpack(msg.{__proto_getter(field)}())"
            )
            pass
        else:
            output_fields.append(f"msg.{__proto_getter(field)}()")

    return ", ".join(output_fields)


def __get_protobuf_pack(message):
    output = ""

    for field in message.fields:
        if field.is_message:
            output += f"    {field.message_type}.proto.pack(msg.{__proto_setter(field)}(), value.{__local_getter(field)});\n"
        else:
            output += (
                f"    msg.{__proto_setter(field)}(value.{__local_getter(field)});\n"
            )

    return output


def __test_proto_setter(field: MessageField):
    return f"proto.{__proto_setter(field)}(DATA.{__local_getter(field)});"


def __assert_local_equals(field: MessageField):
    return f"assertEquals(DATA.{__local_getter(field)}, data.{__local_getter(field)});"


def __assert_local_vs_proto_equals(field: MessageField):
    return (
        f"assertEquals(DATA.{__local_getter(field)}, proto.{__proto_getter(field)}());"
    )


def render_message_java(
    module: ProtobufModule, message: MessageClass, force_tests: bool
):
    env = Environment(
        loader=FileSystemLoader("shared/protobuf_generator/generator/templates")
    )
    env.globals["struct_unpack"] = __struct_unpack
    env.globals["struct_pack"] = __struct_pack
    env.globals["get_size"] = __get_struct_size
    env.globals["get_schema"] = __get_schema
    env.globals["get_protobuf_unpack"] = __get_protobuf_unpack
    env.globals["get_protobuf_pack"] = __get_protobuf_pack
    env.filters["local_type"] = __local_type

    env.globals["test_proto_setter"] = __test_proto_setter
    env.globals["assert_local_vs_proto_equals"] = __assert_local_vs_proto_equals
    env.globals["assert_local_equals"] = __assert_local_equals

    wpimath_dir = "/home/pjreiniger/git/allwpilib/wpimath"
    wpimath_src_dir = os.path.join(wpimath_dir, "src/main/java/edu/wpi/first/math")
    src_serde_folder = os.path.join(wpimath_src_dir, module.subfolder, "serde")

    wpimath_test_dir = os.path.join(wpimath_dir, "src/test/java/edu/wpi/first/math")
    test_serde_folder = os.path.join(wpimath_test_dir, module.subfolder, "serde")

    kwargs = dict(
        module=module,
        message=message,
    )

    lang_type = message.local_type

    proto_src = os.path.join(src_serde_folder, f"{lang_type}ProtoSerde.java")
    render_template(env, "java_serde_proto.jinja2", proto_src, **kwargs)

    struct_src = os.path.join(src_serde_folder, f"{lang_type}StructSerde.java")
    render_template(env, "java_serde_struct.jinja2", struct_src, **kwargs)

    proto_test = os.path.join(test_serde_folder, f"{lang_type}SerdeTest.java")
    if force_tests or not os.path.exists(proto_test):
        render_template(env, "java_test.jinja2", proto_test, **kwargs)
