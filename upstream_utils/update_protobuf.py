#!/usr/bin/env python3

import os
import shutil

from upstream_utils import (
    get_repo_root,
    clone_repo,
    comment_out_invalid_includes,
    copy_to,
    walk_cwd_and_copy_if,
    walk_if,
    git_am,
)

# These lists can be copied from src/file_lists.cmake

protobuf_lite_sources = set(
    [
        "google/protobuf/any_lite.cc",
        "google/protobuf/arena.cc",
        "google/protobuf/arena_align.cc",
        "google/protobuf/arenastring.cc",
        "google/protobuf/arenaz_sampler.cc",
        "google/protobuf/extension_set.cc",
        "google/protobuf/generated_enum_util.cc",
        "google/protobuf/generated_message_tctable_lite.cc",
        "google/protobuf/generated_message_util.cc",
        "google/protobuf/implicit_weak_message.cc",
        "google/protobuf/inlined_string_field.cc",
        "google/protobuf/io/coded_stream.cc",
        "google/protobuf/io/io_win32.cc",
        "google/protobuf/io/zero_copy_stream.cc",
        "google/protobuf/io/zero_copy_stream_impl.cc",
        "google/protobuf/io/zero_copy_stream_impl_lite.cc",
        "google/protobuf/map.cc",
        "google/protobuf/message_lite.cc",
        "google/protobuf/parse_context.cc",
        "google/protobuf/port.cc",
        "google/protobuf/raw_ptr.cc",
        "google/protobuf/repeated_field.cc",
        "google/protobuf/repeated_ptr_field.cc",
        "google/protobuf/stubs/common.cc",
        "google/protobuf/wire_format_lite.cc",
    ]
)

protobuf_lite_includes = set(
    [
        "google/protobuf/any.h",
        "google/protobuf/arena.h",
        "google/protobuf/arena_align.h",
        "google/protobuf/arena_allocation_policy.h",
        "google/protobuf/arena_cleanup.h",
        "google/protobuf/arenastring.h",
        "google/protobuf/arenaz_sampler.h",
        "google/protobuf/endian.h",
        "google/protobuf/explicitly_constructed.h",
        "google/protobuf/extension_set.h",
        "google/protobuf/extension_set_inl.h",
        "google/protobuf/generated_enum_util.h",
        "google/protobuf/generated_message_tctable_decl.h",
        "google/protobuf/generated_message_tctable_impl.h",
        "google/protobuf/generated_message_util.h",
        "google/protobuf/has_bits.h",
        "google/protobuf/implicit_weak_message.h",
        "google/protobuf/inlined_string_field.h",
        "google/protobuf/internal_visibility.h",
        "google/protobuf/io/coded_stream.h",
        "google/protobuf/io/io_win32.h",
        "google/protobuf/io/zero_copy_stream.h",
        "google/protobuf/io/zero_copy_stream_impl.h",
        "google/protobuf/io/zero_copy_stream_impl_lite.h",
        "google/protobuf/map.h",
        "google/protobuf/map_entry_lite.h",
        "google/protobuf/map_field_lite.h",
        "google/protobuf/map_type_handler.h",
        "google/protobuf/message_lite.h",
        "google/protobuf/metadata_lite.h",
        "google/protobuf/parse_context.h",
        "google/protobuf/port.h",
        "google/protobuf/port_def.inc",
        "google/protobuf/port_undef.inc",
        "google/protobuf/raw_ptr.h",
        "google/protobuf/repeated_field.h",
        "google/protobuf/repeated_ptr_field.h",
        "google/protobuf/serial_arena.h",
        "google/protobuf/string_block.h",
        "google/protobuf/stubs/callback.h",
        "google/protobuf/stubs/common.h",
        "google/protobuf/stubs/platform_macros.h",
        "google/protobuf/stubs/port.h",
        "google/protobuf/stubs/status_macros.h",
        "google/protobuf/thread_safe_arena.h",
        "google/protobuf/varint_shuffle.h",
        "google/protobuf/wire_format_lite.h",
    ]
)

protobuf_sources = set(
    [
        "google/protobuf/any.pb.cc",
        "google/protobuf/api.pb.cc",
        "google/protobuf/duration.pb.cc",
        "google/protobuf/empty.pb.cc",
        "google/protobuf/field_mask.pb.cc",
        "google/protobuf/source_context.pb.cc",
        "google/protobuf/struct.pb.cc",
        "google/protobuf/timestamp.pb.cc",
        "google/protobuf/type.pb.cc",
        "google/protobuf/wrappers.pb.cc",
        "google/protobuf/any.cc",
        "google/protobuf/any_lite.cc",
        "google/protobuf/arena.cc",
        "google/protobuf/arena_align.cc",
        "google/protobuf/arenastring.cc",
        "google/protobuf/arenaz_sampler.cc",
        "google/protobuf/compiler/importer.cc",
        "google/protobuf/compiler/parser.cc",
        "google/protobuf/cpp_features.pb.cc",
        "google/protobuf/descriptor.cc",
        "google/protobuf/descriptor.pb.cc",
        "google/protobuf/descriptor_database.cc",
        "google/protobuf/dynamic_message.cc",
        "google/protobuf/extension_set.cc",
        "google/protobuf/extension_set_heavy.cc",
        "google/protobuf/feature_resolver.cc",
        "google/protobuf/generated_enum_util.cc",
        "google/protobuf/generated_message_bases.cc",
        "google/protobuf/generated_message_reflection.cc",
        "google/protobuf/generated_message_tctable_full.cc",
        "google/protobuf/generated_message_tctable_gen.cc",
        "google/protobuf/generated_message_tctable_lite.cc",
        "google/protobuf/generated_message_util.cc",
        "google/protobuf/implicit_weak_message.cc",
        "google/protobuf/inlined_string_field.cc",
        "google/protobuf/internal_message_util.cc",
        "google/protobuf/io/coded_stream.cc",
        "google/protobuf/io/gzip_stream.cc",
        "google/protobuf/io/io_win32.cc",
        "google/protobuf/io/printer.cc",
        "google/protobuf/io/strtod.cc",
        "google/protobuf/io/tokenizer.cc",
        "google/protobuf/io/zero_copy_sink.cc",
        "google/protobuf/io/zero_copy_stream.cc",
        "google/protobuf/io/zero_copy_stream_impl.cc",
        "google/protobuf/io/zero_copy_stream_impl_lite.cc",
        # "google/protobuf/json/internal/lexer.cc",
        # "google/protobuf/json/internal/message_path.cc",
        # "google/protobuf/json/internal/parser.cc",
        # "google/protobuf/json/internal/unparser.cc",
        # "google/protobuf/json/internal/untyped_message.cc",
        # "google/protobuf/json/internal/writer.cc",
        # "google/protobuf/json/internal/zero_copy_buffered_stream.cc",
        # "google/protobuf/json/json.cc",
        "google/protobuf/map.cc",
        "google/protobuf/map_field.cc",
        "google/protobuf/message.cc",
        "google/protobuf/message_lite.cc",
        "google/protobuf/parse_context.cc",
        "google/protobuf/port.cc",
        "google/protobuf/raw_ptr.cc",
        "google/protobuf/reflection_mode.cc",
        "google/protobuf/reflection_ops.cc",
        "google/protobuf/repeated_field.cc",
        "google/protobuf/repeated_ptr_field.cc",
        "google/protobuf/service.cc",
        "google/protobuf/stubs/common.cc",
        "google/protobuf/text_format.cc",
        "google/protobuf/unknown_field_set.cc",
        "google/protobuf/util/delimited_message_util.cc",
        "google/protobuf/util/field_comparator.cc",
        "google/protobuf/util/field_mask_util.cc",
        "google/protobuf/util/message_differencer.cc",
        "google/protobuf/util/time_util.cc",
        "google/protobuf/util/type_resolver_util.cc",
        "google/protobuf/wire_format.cc",
        "google/protobuf/wire_format_lite.cc",
    ]
)

protobuf_includes = set(
    [
        "google/protobuf/any.pb.h",
        "google/protobuf/api.pb.h",
        "google/protobuf/duration.pb.h",
        "google/protobuf/empty.pb.h",
        "google/protobuf/field_mask.pb.h",
        "google/protobuf/source_context.pb.h",
        "google/protobuf/struct.pb.h",
        "google/protobuf/timestamp.pb.h",
        "google/protobuf/type.pb.h",
        "google/protobuf/wrappers.pb.h",
        "google/protobuf/any.h",
        "google/protobuf/arena.h",
        "google/protobuf/arena_align.h",
        "google/protobuf/arena_allocation_policy.h",
        "google/protobuf/arena_cleanup.h",
        "google/protobuf/arenastring.h",
        "google/protobuf/arenaz_sampler.h",
        "google/protobuf/compiler/importer.h",
        "google/protobuf/compiler/parser.h",
        "google/protobuf/cpp_features.pb.h",
        "google/protobuf/descriptor.h",
        "google/protobuf/descriptor.pb.h",
        "google/protobuf/descriptor_database.h",
        "google/protobuf/descriptor_legacy.h",
        "google/protobuf/descriptor_visitor.h",
        "google/protobuf/dynamic_message.h",
        "google/protobuf/endian.h",
        "google/protobuf/explicitly_constructed.h",
        "google/protobuf/extension_set.h",
        "google/protobuf/extension_set_inl.h",
        "google/protobuf/feature_resolver.h",
        "google/protobuf/field_access_listener.h",
        "google/protobuf/generated_enum_reflection.h",
        "google/protobuf/generated_enum_util.h",
        "google/protobuf/generated_message_bases.h",
        "google/protobuf/generated_message_reflection.h",
        "google/protobuf/generated_message_tctable_decl.h",
        "google/protobuf/generated_message_tctable_gen.h",
        "google/protobuf/generated_message_tctable_impl.h",
        "google/protobuf/generated_message_util.h",
        "google/protobuf/has_bits.h",
        "google/protobuf/implicit_weak_message.h",
        "google/protobuf/inlined_string_field.h",
        "google/protobuf/internal_message_util.h",
        "google/protobuf/internal_visibility.h",
        "google/protobuf/io/coded_stream.h",
        "google/protobuf/io/gzip_stream.h",
        "google/protobuf/io/io_win32.h",
        "google/protobuf/io/printer.h",
        "google/protobuf/io/strtod.h",
        "google/protobuf/io/tokenizer.h",
        "google/protobuf/io/zero_copy_sink.h",
        "google/protobuf/io/zero_copy_stream.h",
        "google/protobuf/io/zero_copy_stream_impl.h",
        "google/protobuf/io/zero_copy_stream_impl_lite.h",
        # "google/protobuf/json/internal/descriptor_traits.h",
        # "google/protobuf/json/internal/lexer.h",
        # "google/protobuf/json/internal/message_path.h",
        # "google/protobuf/json/internal/parser.h",
        # "google/protobuf/json/internal/parser_traits.h",
        # "google/protobuf/json/internal/unparser.h",
        # "google/protobuf/json/internal/unparser_traits.h",
        # "google/protobuf/json/internal/untyped_message.h",
        # "google/protobuf/json/internal/writer.h",
        # "google/protobuf/json/internal/zero_copy_buffered_stream.h",
        # "google/protobuf/json/json.h",
        "google/protobuf/map.h",
        "google/protobuf/map_entry.h",
        "google/protobuf/map_entry_lite.h",
        "google/protobuf/map_field.h",
        "google/protobuf/map_field_inl.h",
        "google/protobuf/map_field_lite.h",
        "google/protobuf/map_type_handler.h",
        "google/protobuf/message.h",
        "google/protobuf/message_lite.h",
        "google/protobuf/metadata.h",
        "google/protobuf/metadata_lite.h",
        "google/protobuf/parse_context.h",
        "google/protobuf/port.h",
        "google/protobuf/port_def.inc",
        "google/protobuf/port_undef.inc",
        "google/protobuf/raw_ptr.h",
        "google/protobuf/reflection.h",
        "google/protobuf/reflection_internal.h",
        "google/protobuf/reflection_mode.h",
        "google/protobuf/reflection_ops.h",
        "google/protobuf/repeated_field.h",
        "google/protobuf/repeated_ptr_field.h",
        "google/protobuf/serial_arena.h",
        "google/protobuf/service.h",
        "google/protobuf/string_block.h",
        "google/protobuf/stubs/callback.h",
        "google/protobuf/stubs/common.h",
        "google/protobuf/stubs/platform_macros.h",
        "google/protobuf/stubs/port.h",
        "google/protobuf/stubs/status_macros.h",
        "google/protobuf/text_format.h",
        "google/protobuf/thread_safe_arena.h",
        "google/protobuf/unknown_field_set.h",
        "google/protobuf/util/delimited_message_util.h",
        "google/protobuf/util/field_comparator.h",
        "google/protobuf/util/field_mask_util.h",
        "google/protobuf/util/json_util.h",
        "google/protobuf/util/message_differencer.h",
        "google/protobuf/util/time_util.h",
        "google/protobuf/util/type_resolver.h",
        "google/protobuf/util/type_resolver_util.h",
        "google/protobuf/varint_shuffle.h",
        "google/protobuf/wire_format.h",
        "google/protobuf/wire_format_lite.h",
    ]
)

protobuf_internal_includes = set(
    [
    ]
)

use_src_files = protobuf_lite_sources | protobuf_sources
use_include_files = (
    protobuf_lite_includes | protobuf_includes | protobuf_internal_includes
)


def matches(dp, f, files):
    if not dp.startswith("./src/"):
        return False
    p = dp[6:] + "/" + f
    return p in files


def main():
    upstream_root = clone_repo(
        "https://github.com/protocolbuffers/protobuf", "v24.4"
    )
    wpilib_root = get_repo_root()
    wpiutil = os.path.join(wpilib_root, "wpiutil")

    # Apply patches to upstream Git repo
    os.chdir(upstream_root)
    for f in [
        # "0001-Fix-sign-compare-warnings.patch",
        # "0002-Remove-redundant-move.patch",
        # "0003-Fix-maybe-uninitialized-warnings.patch",
        # "0004-Fix-coded_stream-WriteRaw.patch",
        # "0005-Suppress-enum-enum-conversion-warning.patch",
        # "0006-Work-around-GCC-12-restrict-warning-compiler-bug.patch",
        # "0007-Disable-MSVC-switch-warning.patch",
        # "0008-Disable-unused-function-warning.patch",
        # "0009-Disable-pedantic-warning.patch",
    ]:
        git_am(os.path.join(wpilib_root, "upstream_utils/protobuf_patches", f))

    # Delete old install
    for d in [
        "src/main/native/thirdparty/protobuf/src",
        "src/main/native/thirdparty/protobuf/include",
    ]:
        shutil.rmtree(os.path.join(wpiutil, d), ignore_errors=True)

    # Copy protobuf source files into allwpilib
    src_files = walk_if(".", lambda dp, f: matches(dp, f, use_src_files))
    src_files = [f[22:] for f in src_files]
    os.chdir(os.path.join(upstream_root, "src/google/protobuf"))
    copy_to(src_files, os.path.join(wpiutil, "src/main/native/thirdparty/protobuf/src"))

    # Copy protobuf header files into allwpilib
    os.chdir(upstream_root)
    include_files = walk_if(".", lambda dp, f: matches(dp, f, use_include_files))
    include_files = [f[6:] for f in include_files]
    os.chdir(os.path.join(upstream_root, "src"))
    copy_to(
        include_files,
        os.path.join(wpiutil, "src/main/native/thirdparty/protobuf/include"),
    )


if __name__ == "__main__":
    main()
