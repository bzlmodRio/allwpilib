from google.protobuf.descriptor import FieldDescriptor
from jinja2 import Environment, FileSystemLoader
from shared.protobuf_generator.generator.lib import (
    MessageClass,
    ProtobufModule,
    MessageField,
    lower_camel_case,
    render_template,
    upper_camel_case,
)
import os

PROTO_TYPE_TO_CPP_TEXT = {
    FieldDescriptor.TYPE_DOUBLE: "double",
    FieldDescriptor.TYPE_BOOL: "boolean",
    FieldDescriptor.TYPE_INT32: "int",
    FieldDescriptor.TYPE_UINT32: "int",
}


def __get_schema(message: MessageClass):
    schema = ";".join(
        field.get_schema(PROTO_TYPE_TO_CPP_TEXT) for field in message.fields
    )

    schema = '"' + schema + '"'

    if len(schema) > 30:
        schema = "\n      " + schema
    else:
        schema = " " + schema

    return schema


def __get_field_struct_size(field):
    if field.is_message:
        return f"wpi::Struct<frc::{field.message_type}>::kSize"
    elif field.protobuf_type == FieldDescriptor.TYPE_DOUBLE:
        return 8
    elif field.protobuf_type == FieldDescriptor.TYPE_INT32:
        return 4
    elif field.protobuf_type == FieldDescriptor.TYPE_UINT32:
        return 4
    else:
        raise Exception(f"Unsupported type {field.type} for field {field.name}")


def __get_struct_size(message):
    primitive_size = 0
    subclass_parts = []

    output = ""

    for field in message.fields:
        if field.is_message:
            subclass_parts.append(f"wpi::Struct<frc::{field.message_type}>::kSize")
        elif field.protobuf_type == FieldDescriptor.TYPE_DOUBLE:
            primitive_size += 8
        elif field.protobuf_type == FieldDescriptor.TYPE_INT32:
            num_doubles += 1
        elif field.protobuf_type == FieldDescriptor.TYPE_UINT32:
            num_doubles += 1
        else:
            raise Exception(f"Unsupported type {field.type} for field {field.name}")

    if primitive_size > 0:
        output += f"{primitive_size}"

    if subclass_parts and output:
        output += "+ "
    output += " + ".join(subclass_parts)

    return output


def __maybe_wrap_with_unit(field: MessageField, txt):
    if field.name.endswith("_radians"):
        return "units::radian_t{" + txt + "}"
    elif field.name.endswith("_meters"):
        return "units::meter_t{" + txt + "}"
    elif field.name.endswith("_volts"):
        return "units::volt_t{" + txt + "}"
    elif field.name.endswith("_mps"):
        return "units::meters_per_second_t{" + txt + "}"
    elif field.name.endswith("_rps"):
        return "units::radians_per_second_t{" + txt + "}"

    print("No units for ", field.name)

    return txt


def __struct_offset_name(field: MessageField):
    return (
        "k" + field.name_without_units[0].upper() + field.name_without_units[1:] + "Off"
    )


def __struct_offset_definition(message: MessageClass):
    output = ""
    last_field = None
    for field in message.fields:
        output += f"constexpr size_t {__struct_offset_name(field)} = "
        if not last_field:
            output += "0"
        else:
            output += f"{__struct_offset_name(last_field)} + {__get_field_struct_size(last_field)}"
        output += ";"

        # __get_field_struct_size

        # if field.is_message:
        #     field_size = f"wpi::Struct<frc::{field.message_type}>::kSize"
        # else:
        #     field_size = "999"

        # if last_field:
        #     output += f"{__struct_offset_name(last_field)} + {field_size}"
        # else:
        #     output += "0"
        # output += ";\n"
        last_field = field

    return output


def __struct_unpack(field: MessageField):
    constant_name = __struct_offset_name(field)

    if field.is_message:
        return f"wpi::UnpackStruct<frc::{field.message_type}, {constant_name}>(data)"

    output = f"wpi::UnpackStruct<{PROTO_TYPE_TO_CPP_TEXT[field.protobuf_type]}, {constant_name}>(data)"
    output = __maybe_wrap_with_unit(field, output)

    return output


def __struct_pack(field: MessageField):
    constant_name = __struct_offset_name(field)

    if field.is_message:
        return f"wpi::PackStruct<{constant_name}>(data, value.{__local_getter(field)})"

    output = f"wpi::PackStruct<{constant_name}>(data, value.{__local_getter(field)})"

    return output


def __proto_getter(field: MessageField):
    return f"{field.name}"


def __proto_setter(field: MessageField):
    if field.is_message:
        return f"mutable_{field.name}()->"
    return f"set_{field.name}"


def __local_getter(field: MessageField):
    field_name = field.name_without_units
    field_name = field_name.replace("meters", "")
    field_name = field_name.replace("volts", "")
    # field_name = field_name.replace("mps", "meters_per_second")
    # field_name = field_name.replace("rps", "radians_per_second")

    # return upper_camel_case(field_name) + "()"
    # return upper_camel_case(field_name) + "().value()"
    # return upper_camel_case(field_name) + ".value()"

    if field.is_private:
        output = upper_camel_case(field.name_without_units) + "()"
        if field.has_units:
            return output + ".value()"
        return output

    return lower_camel_case(field_name) + ".value()"


def __proto_unpack(field: MessageField):
    if field.is_message:
        return f"wpi::UnpackProtobuf<frc::{field.message_type}>(m->{__proto_getter(field)}())"

    output = f"m->{__proto_getter(field)}()"
    output = __maybe_wrap_with_unit(field, output)
    return output


def __proto_pack(field: MessageField):
    if field.is_message:
        return f"wpi::PackProtobuf(m->mutable_{__proto_getter(field)}(), value.{__local_getter(field)})"

    output = f"m->{__proto_setter(field)}(value.{__local_getter(field)})"
    return output


def __test_proto_setter(field: MessageField):
    return f"proto.{__proto_setter(field)}(kExpectedData.{__local_getter(field)});"


def __assert_local_equals(field: MessageField):
    return f"EXPECT_EQ(kExpectedData.{__local_getter(field)}, unpacked_data.{__local_getter(field)});"


def __assert_local_vs_proto_equals(field: MessageField):
    return f"EXPECT_EQ(kExpectedData.{__local_getter(field)}, proto.{__proto_getter(field)}());"


def render_message_cpp(
    module: ProtobufModule, message: MessageClass, force_tests: bool
):
    env = Environment(
        loader=FileSystemLoader("shared/protobuf_generator/generator/templates")
    )
    env.globals["get_size"] = __get_struct_size
    env.globals["get_schema"] = __get_schema
    env.globals["struct_unpack"] = __struct_unpack
    env.globals["struct_pack"] = __struct_pack
    env.globals["proto_unpack"] = __proto_unpack
    env.globals["proto_pack"] = __proto_pack
    env.globals["struct_offset_name"] = __struct_offset_name
    env.globals["struct_offset_definition"] = __struct_offset_definition

    env.globals["test_proto_setter"] = __test_proto_setter
    env.globals["assert_local_vs_proto_equals"] = __assert_local_vs_proto_equals
    env.globals["assert_local_equals"] = __assert_local_equals

    kwargs = dict(
        module=module,
        message=message,
    )

    lang_type = message.local_type

    wpimath_dir = "/home/pjreiniger/git/allwpilib/wpimath"

    wpimath_incl_dir = os.path.join(wpimath_dir, "src/main/native/include/frc")
    wpimath_incl_serde_dir = os.path.join(wpimath_incl_dir, module.subfolder, "serde")
    serde_hdr = os.path.join(wpimath_incl_serde_dir, f"{lang_type}Serde.h")
    render_template(env, "cpp_serde.h.jinja2", serde_hdr, **kwargs)

    wpimath_cpp_dir = os.path.join(wpimath_dir, "src/main/native/cpp/")
    wpimath_cpp_serde_dir = os.path.join(wpimath_cpp_dir, module.subfolder, "serde")
    serde_cpp = os.path.join(wpimath_cpp_serde_dir, f"{lang_type}Serde.cpp")
    render_template(env, "cpp_serde.cpp.jinja2", serde_cpp, **kwargs)

    wpimath_test_dir = os.path.join(wpimath_dir, "src/test/native/cpp/")
    wpimath_test_serde_dir = os.path.join(wpimath_test_dir, module.subfolder, "serde")
    serde_test = os.path.join(wpimath_test_serde_dir, f"{lang_type}SerdeTest.cpp")
    if force_tests or not os.path.exists(serde_test):
        render_template(env, "cpp_test.jinja2", serde_test, **kwargs)
