from shared.protobuf_generator.generator.java_helpers import render_message_java
from shared.protobuf_generator.generator.cpp_helpers import render_message_cpp

from shared.protobuf_generator.generator.lib import ProtobufModule


def main():
    proto_files = [
        ("controller", "controller"),
        ("geometry2d", "geometry"),
        ("geometry3d", "geometry"),
        ("kinematics", "kinematics"),
        ("plant", "system/plant"),
        ("spline", "spline"),
        ("system", "system"),
        ("trajectory", "trajectory"),
        ("wpimath", "."),
    ]

    force_tests = True

    modules = []

    for proto_file, output_directory in proto_files:
        module_name = proto_file + "_pb2"

        modules.append(ProtobufModule(proto_file, module_name))

    message_types_to_ignore = [
        "DifferentialDriveFeedforward",
        "MecanumDriveKinematics",
        "SimpleMotorFeedforward",
        "MecanumDriveMotorVoltages",
        "SwerveDriveKinematics",
        "DCMotor",
        "CubicHermiteSpline",
        "QuinticHermiteSpline",
        "Matrix",
        "Vector",
        "LinearSystem",
        "Trajectory",
    ]

    message_types_to_do = []

    for module in modules:
        for message in module.messages:
            if message.local_type in message_types_to_ignore:
                print(f"Ignoring {message.local_type}")
                continue

            if message_types_to_do:
                if message.local_type not in message_types_to_do:
                    continue

            render_message_java(module, message, force_tests)
            render_message_cpp(module, message, force_tests)


if __name__ == "__main__":
    main()
