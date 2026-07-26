// Copyright (c) FIRST and other WPILib contributors.
// Open Source Software; you can modify and/or share it under the terms of
// the WPILib BSD license file in the root directory of this project.

#include "wpi/backend/DataLogTelemetryBackend.hpp"

#include <stdint.h>

#include <array>
#include <memory>
#include <span>
#include <string>
#include <string_view>
#include <unordered_map>
#include <utility>
#include <vector>

#include <gtest/gtest.h>

#include "wpi/datalog/DataLogReader.hpp"
#include "wpi/datalog/DataLogWriter.hpp"
#include "wpi/math/geometry/Translation2d.hpp"
#include "wpi/math/geometry/proto/Translation2dProto.hpp"
#include "wpi/math/geometry/struct/Translation2dStruct.hpp"
#include "wpi/telemetry/Telemetry.hpp"
#include "wpi/telemetry/TelemetryRegistry.hpp"
#include "wpi/units/length.hpp"
#include "wpi/util/Logger.hpp"
#include "wpi/util/MemoryBuffer.hpp"
#include "wpi/util/json.hpp"
#include "wpi/util/protobuf/Protobuf.hpp"
#include "wpi/util/raw_ostream.hpp"
#include "wpi/util/struct/Struct.hpp"

class DataLogTelemetryBackendTest : public ::testing::Test {
 public:
  struct EntryData {
    std::string type;
    std::string metadata;
    std::vector<std::vector<uint8_t>> records;
  };

  struct LogSnapshot {
    std::unordered_map<std::string, EntryData> entries;
  };

  DataLogTelemetryBackendTest()
      : log{msglog, std::make_unique<wpi::util::raw_uvector_ostream>(data)},
        backend{std::make_shared<wpi::backend::DataLogTelemetryBackend>(
            log, "/Telemetry")} {
    wpi::TelemetryRegistry::Reset();
    wpi::TelemetryRegistry::RegisterBackend("", backend);
  }

  ~DataLogTelemetryBackendTest() override { wpi::TelemetryRegistry::Reset(); }

  LogSnapshot ReadSnapshot() {
    log.Flush();

    wpi::log::DataLogReader reader{
        wpi::util::MemoryBuffer::GetMemBufferCopy(data, "test")};
    EXPECT_TRUE(reader.IsValid());

    std::unordered_map<int, std::string> names;
    LogSnapshot snapshot;
    for (const auto& record : reader) {
      if (record.IsStart()) {
        wpi::log::StartRecordData start;
        EXPECT_TRUE(record.GetStartData(&start));
        names.emplace(start.entry, start.name);
        auto& entry = snapshot.entries[std::string{start.name}];
        entry.type = start.type;
        entry.metadata = start.metadata;
      } else if (record.IsSetMetadata()) {
        wpi::log::MetadataRecordData metadata;
        EXPECT_TRUE(record.GetSetMetadataData(&metadata));
        auto it = names.find(metadata.entry);
        if (it != names.end()) {
          snapshot.entries[it->second].metadata = metadata.metadata;
        }
      } else if (!record.IsControl()) {
        auto it = names.find(record.GetEntry());
        if (it != names.end()) {
          auto raw = record.GetRaw();
          snapshot.entries[it->second].records.emplace_back(raw.begin(),
                                                            raw.end());
        }
      }
    }
    return snapshot;
  }

  static const EntryData& Entry(const LogSnapshot& snapshot,
                                std::string_view name) {
    return snapshot.entries.at(std::string{"/Telemetry/"} + std::string{name});
  }

  static const std::vector<uint8_t>& Last(const EntryData& entry) {
    EXPECT_FALSE(entry.records.empty());
    return entry.records.back();
  }

  static bool HasEntryWithType(const LogSnapshot& snapshot,
                               std::string_view type) {
    for (const auto& item : snapshot.entries) {
      if (item.second.type == type) {
        return true;
      }
    }
    return false;
  }

  static bool DecodeBoolean(const std::vector<uint8_t>& raw) {
    wpi::log::DataLogRecord record{1, 0, raw};
    bool value = false;
    EXPECT_TRUE(record.GetBoolean(&value));
    return value;
  }

  static int64_t DecodeInteger(const std::vector<uint8_t>& raw) {
    wpi::log::DataLogRecord record{1, 0, raw};
    int64_t value = 0;
    EXPECT_TRUE(record.GetInteger(&value));
    return value;
  }

  static float DecodeFloat(const std::vector<uint8_t>& raw) {
    wpi::log::DataLogRecord record{1, 0, raw};
    float value = 0.0f;
    EXPECT_TRUE(record.GetFloat(&value));
    return value;
  }

  static double DecodeDouble(const std::vector<uint8_t>& raw) {
    wpi::log::DataLogRecord record{1, 0, raw};
    double value = 0.0;
    EXPECT_TRUE(record.GetDouble(&value));
    return value;
  }

  static std::string DecodeString(const std::vector<uint8_t>& raw) {
    wpi::log::DataLogRecord record{1, 0, raw};
    std::string_view value;
    EXPECT_TRUE(record.GetString(&value));
    return std::string{value};
  }

  static std::vector<int> DecodeBooleanArray(const std::vector<uint8_t>& raw) {
    wpi::log::DataLogRecord record{1, 0, raw};
    std::vector<int> value;
    EXPECT_TRUE(record.GetBooleanArray(&value));
    return value;
  }

  static std::vector<int64_t> DecodeIntegerArray(
      const std::vector<uint8_t>& raw) {
    wpi::log::DataLogRecord record{1, 0, raw};
    std::vector<int64_t> value;
    EXPECT_TRUE(record.GetIntegerArray(&value));
    return value;
  }

  static std::vector<float> DecodeFloatArray(const std::vector<uint8_t>& raw) {
    wpi::log::DataLogRecord record{1, 0, raw};
    std::vector<float> value;
    EXPECT_TRUE(record.GetFloatArray(&value));
    return value;
  }

  static std::vector<double> DecodeDoubleArray(
      const std::vector<uint8_t>& raw) {
    wpi::log::DataLogRecord record{1, 0, raw};
    std::vector<double> value;
    EXPECT_TRUE(record.GetDoubleArray(&value));
    return value;
  }

  static std::vector<std::string> DecodeStringArray(
      const std::vector<uint8_t>& raw) {
    wpi::log::DataLogRecord record{1, 0, raw};
    std::vector<std::string_view> views;
    EXPECT_TRUE(record.GetStringArray(&views));
    return {views.begin(), views.end()};
  }

  static wpi::math::Translation2d DecodeTranslation(
      const std::vector<uint8_t>& raw) {
    return wpi::util::UnpackStruct<wpi::math::Translation2d>(
        std::span<const uint8_t>{raw.data(), raw.size()});
  }

  static std::vector<wpi::math::Translation2d> DecodeTranslationArray(
      const std::vector<uint8_t>& raw) {
    constexpr size_t kStructSize =
        wpi::util::Struct<wpi::math::Translation2d>::GetSize();
    EXPECT_EQ(0u, raw.size() % kStructSize);
    std::vector<wpi::math::Translation2d> values;
    for (size_t offset = 0; offset < raw.size(); offset += kStructSize) {
      values.emplace_back(wpi::util::UnpackStruct<wpi::math::Translation2d>(
          std::span<const uint8_t>{raw.data() + offset, kStructSize}));
    }
    return values;
  }

  static wpi::math::Translation2d DecodeTranslationProto(
      const std::vector<uint8_t>& raw) {
    wpi::util::ProtobufMessage<wpi::math::Translation2d> msg;
    auto value = msg.Unpack(raw);
    EXPECT_TRUE(value.has_value());
    return value.value_or(wpi::math::Translation2d{});
  }

  static void ExpectTranslationEq(const wpi::math::Translation2d& expected,
                                  const wpi::math::Translation2d& actual) {
    EXPECT_DOUBLE_EQ(expected.X().value(), actual.X().value());
    EXPECT_DOUBLE_EQ(expected.Y().value(), actual.Y().value());
  }

  wpi::util::Logger msglog;
  std::vector<uint8_t> data;
  wpi::log::DataLogWriter log;
  std::shared_ptr<wpi::backend::DataLogTelemetryBackend> backend;
};

TEST_F(DataLogTelemetryBackendTest, LogsScalarDataTypes) {
  wpi::Telemetry::Log("boolean", true);
  wpi::Telemetry::Log("byte", int8_t{2});
  wpi::Telemetry::Log("short", int16_t{3});
  wpi::Telemetry::Log("int", int32_t{4});
  wpi::Telemetry::Log("long", int64_t{5});
  wpi::Telemetry::Log("float", 6.25f);
  wpi::Telemetry::Log("double", 7.5);
  wpi::Telemetry::Log("string", "ready");
  wpi::Telemetry::Log("json", std::string_view{"{\"ok\":true}"},
                      std::string_view{"json"});

  auto snapshot = ReadSnapshot();

  EXPECT_EQ("boolean", Entry(snapshot, "boolean").type);
  EXPECT_TRUE(DecodeBoolean(Last(Entry(snapshot, "boolean"))));
  EXPECT_EQ("int64", Entry(snapshot, "byte").type);
  EXPECT_EQ(2, DecodeInteger(Last(Entry(snapshot, "byte"))));
  EXPECT_EQ("int64", Entry(snapshot, "short").type);
  EXPECT_EQ(3, DecodeInteger(Last(Entry(snapshot, "short"))));
  EXPECT_EQ("int64", Entry(snapshot, "int").type);
  EXPECT_EQ(4, DecodeInteger(Last(Entry(snapshot, "int"))));
  EXPECT_EQ("int64", Entry(snapshot, "long").type);
  EXPECT_EQ(5, DecodeInteger(Last(Entry(snapshot, "long"))));
  EXPECT_EQ("float", Entry(snapshot, "float").type);
  EXPECT_FLOAT_EQ(6.25f, DecodeFloat(Last(Entry(snapshot, "float"))));
  EXPECT_EQ("double", Entry(snapshot, "double").type);
  EXPECT_DOUBLE_EQ(7.5, DecodeDouble(Last(Entry(snapshot, "double"))));
  EXPECT_EQ("string", Entry(snapshot, "string").type);
  EXPECT_EQ("ready", DecodeString(Last(Entry(snapshot, "string"))));
  EXPECT_EQ("json", Entry(snapshot, "json").type);
  EXPECT_EQ("{\"ok\":true}", DecodeString(Last(Entry(snapshot, "json"))));
}

TEST_F(DataLogTelemetryBackendTest, LogsArrayAndRawDataTypes) {
  const bool boolValues[] = {true, false};
  const int16_t shortValues[] = {1, 2};
  const int32_t intValues[] = {3, 4};
  const int64_t longValues[] = {5, 6};
  const float floatValues[] = {7.25f, 8.5f};
  const double doubleValues[] = {9.25, 10.5};
  const std::string stringValues[] = {"a", "b"};
  const std::string_view stringViewValues[] = {"c", "d"};
  const uint8_t rawValues[] = {11, 12, 13};
  const uint8_t customRawValues[] = {14, 15};

  wpi::Telemetry::Log("booleans", boolValues);
  wpi::Telemetry::Log("shorts", shortValues);
  wpi::Telemetry::Log("ints", intValues);
  wpi::Telemetry::Log("longs", longValues);
  wpi::Telemetry::Log("floats", floatValues);
  wpi::Telemetry::Log("doubles", doubleValues);
  wpi::Telemetry::Log("strings", stringValues);
  wpi::Telemetry::Log("stringViews", stringViewValues);
  wpi::Telemetry::Log("raw", rawValues);
  wpi::Telemetry::Log("customRaw", std::span<const uint8_t>{customRawValues},
                      "custom");

  auto snapshot = ReadSnapshot();

  EXPECT_EQ("boolean[]", Entry(snapshot, "booleans").type);
  EXPECT_EQ((std::vector<int>{1, 0}),
            DecodeBooleanArray(Last(Entry(snapshot, "booleans"))));
  EXPECT_EQ("int64[]", Entry(snapshot, "shorts").type);
  EXPECT_EQ((std::vector<int64_t>{1, 2}),
            DecodeIntegerArray(Last(Entry(snapshot, "shorts"))));
  EXPECT_EQ("int64[]", Entry(snapshot, "ints").type);
  EXPECT_EQ((std::vector<int64_t>{3, 4}),
            DecodeIntegerArray(Last(Entry(snapshot, "ints"))));
  EXPECT_EQ("int64[]", Entry(snapshot, "longs").type);
  EXPECT_EQ((std::vector<int64_t>{5, 6}),
            DecodeIntegerArray(Last(Entry(snapshot, "longs"))));
  EXPECT_EQ("float[]", Entry(snapshot, "floats").type);
  EXPECT_EQ((std::vector<float>{7.25f, 8.5f}),
            DecodeFloatArray(Last(Entry(snapshot, "floats"))));
  EXPECT_EQ("double[]", Entry(snapshot, "doubles").type);
  EXPECT_EQ((std::vector<double>{9.25, 10.5}),
            DecodeDoubleArray(Last(Entry(snapshot, "doubles"))));
  EXPECT_EQ("string[]", Entry(snapshot, "strings").type);
  EXPECT_EQ((std::vector<std::string>{"a", "b"}),
            DecodeStringArray(Last(Entry(snapshot, "strings"))));
  EXPECT_EQ("string[]", Entry(snapshot, "stringViews").type);
  EXPECT_EQ((std::vector<std::string>{"c", "d"}),
            DecodeStringArray(Last(Entry(snapshot, "stringViews"))));
  EXPECT_EQ("raw", Entry(snapshot, "raw").type);
  EXPECT_EQ((std::vector<uint8_t>{11, 12, 13}), Last(Entry(snapshot, "raw")));
  EXPECT_EQ("custom", Entry(snapshot, "customRaw").type);
  EXPECT_EQ((std::vector<uint8_t>{14, 15}), Last(Entry(snapshot, "customRaw")));
}

TEST_F(DataLogTelemetryBackendTest, LogsStructAndProtobufDataTypes) {
  const wpi::math::Translation2d value{wpi::units::meter_t{1.25},
                                       wpi::units::meter_t{2.5}};
  const std::array<wpi::math::Translation2d, 2> array{
      value, wpi::math::Translation2d{wpi::units::meter_t{3.75},
                                      wpi::units::meter_t{4.5}}};
  wpi::util::ProtobufMessage<wpi::math::Translation2d> msg;
  const std::string structType{std::string_view{
      wpi::util::GetStructTypeString<wpi::math::Translation2d>()}};
  const std::string protoType = msg.GetTypeString();

  wpi::Telemetry::Log("translation", value);
  wpi::Telemetry::Log("translations", std::span<const wpi::math::Translation2d>{
                                          array.data(), array.size()});
  wpi::Telemetry::Log("translationProto", value,
                      wpi::util::ProtobufMessage<wpi::math::Translation2d>{});

  auto snapshot = ReadSnapshot();

  EXPECT_EQ(structType, Entry(snapshot, "translation").type);
  ExpectTranslationEq(value,
                      DecodeTranslation(Last(Entry(snapshot, "translation"))));
  EXPECT_EQ(structType + "[]", Entry(snapshot, "translations").type);
  auto decodedArray =
      DecodeTranslationArray(Last(Entry(snapshot, "translations")));
  ASSERT_EQ(2u, decodedArray.size());
  ExpectTranslationEq(array[0], decodedArray[0]);
  ExpectTranslationEq(array[1], decodedArray[1]);
  EXPECT_EQ(protoType, Entry(snapshot, "translationProto").type);
  ExpectTranslationEq(
      value, DecodeTranslationProto(Last(Entry(snapshot, "translationProto"))));

  EXPECT_EQ("structschema", snapshot.entries.at("/.schema/" + structType).type);
  EXPECT_TRUE(HasEntryWithType(snapshot, "proto:FileDescriptorProto"));
}

TEST_F(DataLogTelemetryBackendTest, AppliesTelemetryProperties) {
  wpi::Telemetry::SetProperty("speed", "min", "0");
  wpi::Telemetry::SetProperty("speed", "unit", "\"m/s\"");
  wpi::Telemetry::Log("speed", 4.0);
  wpi::Telemetry::SetProperty("speed", "max", "10");

  auto snapshot = ReadSnapshot();
  const auto& speed = Entry(snapshot, "speed");

  auto metadata = wpi::util::json::parse(speed.metadata);
  ASSERT_TRUE(metadata);
  ASSERT_TRUE((*metadata)["min"].is_number());
  ASSERT_TRUE((*metadata)["max"].is_number());
  ASSERT_TRUE((*metadata)["unit"].is_string());
  EXPECT_EQ(0.0, (*metadata)["min"].get_number());
  EXPECT_EQ(10.0, (*metadata)["max"].get_number());
  EXPECT_EQ("m/s", (*metadata)["unit"].get_string());
}

TEST_F(DataLogTelemetryBackendTest, HonorsKeepDuplicates) {
  wpi::Telemetry::Log("normal", int64_t{1});
  wpi::Telemetry::Log("normal", int64_t{1});
  wpi::Telemetry::KeepDuplicates("duplicates");
  wpi::Telemetry::Log("duplicates", int64_t{2});
  wpi::Telemetry::Log("duplicates", int64_t{2});

  auto snapshot = ReadSnapshot();

  EXPECT_EQ(1u, Entry(snapshot, "normal").records.size());
  EXPECT_EQ(2u, Entry(snapshot, "duplicates").records.size());
}
