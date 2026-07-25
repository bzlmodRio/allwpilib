// Copyright (c) FIRST and other WPILib contributors.
// Open Source Software; you can modify and/or share it under the terms of
// the WPILib BSD license file in the root directory of this project.

#include "wpi/backend/DataLogTelemetryBackend.hpp"

#include <stdint.h>

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
#include "wpi/telemetry/Telemetry.hpp"
#include "wpi/telemetry/TelemetryRegistry.hpp"
#include "wpi/util/Logger.hpp"
#include "wpi/util/MemoryBuffer.hpp"
#include "wpi/util/raw_ostream.hpp"

class DataLogTelemetryBackendTest : public ::testing::Test {
 public:
  DataLogTelemetryBackendTest()
      : log{msglog, std::make_unique<wpi::util::raw_uvector_ostream>(data)},
        backend{std::make_shared<wpi::backend::DataLogTelemetryBackend>(
            log, "/Telemetry")} {
    wpi::TelemetryRegistry::Reset();
    wpi::TelemetryRegistry::RegisterBackend("", backend);
  }

  ~DataLogTelemetryBackendTest() override { wpi::TelemetryRegistry::Reset(); }

  std::unordered_map<std::string, std::vector<int64_t>>
  ReadIntegerArrayValues() {
    log.Flush();

    wpi::log::DataLogReader reader{
        wpi::util::MemoryBuffer::GetMemBufferCopy(data, "test")};
    EXPECT_TRUE(reader.IsValid());

    std::unordered_map<int, std::string> entries;
    std::unordered_map<std::string, std::vector<int64_t>> values;
    for (const auto& record : reader) {
      if (record.IsStart()) {
        wpi::log::StartRecordData start;
        EXPECT_TRUE(record.GetStartData(&start));
        entries.emplace(start.entry, start.name);
        EXPECT_EQ(std::string_view{"int64[]"}, start.type);
      } else if (!record.IsControl()) {
        auto it = entries.find(record.GetEntry());
        if (it != entries.end()) {
          std::vector<int64_t> value;
          EXPECT_TRUE(record.GetIntegerArray(&value));
          values[it->second] = std::move(value);
        }
      }
    }
    return values;
  }

  wpi::util::Logger msglog;
  std::vector<uint8_t> data;
  wpi::log::DataLogWriter log;
  std::shared_ptr<wpi::backend::DataLogTelemetryBackend> backend;
};

TEST_F(DataLogTelemetryBackendTest, LogsIntegralArraysAsIntegerArrays) {
  const int16_t shortValues[] = {1, 2};
  const int32_t intValues[] = {3, 4};
  const int64_t longValues[] = {5, 6};

  wpi::Telemetry::Log("shorts", std::span<const int16_t>{shortValues});
  wpi::Telemetry::Log("ints", std::span<const int32_t>{intValues});
  wpi::Telemetry::Log("longs", std::span<const int64_t>{longValues});

  auto values = ReadIntegerArrayValues();

  EXPECT_EQ((std::vector<int64_t>{1, 2}), values["/Telemetry/shorts"]);
  EXPECT_EQ((std::vector<int64_t>{3, 4}), values["/Telemetry/ints"]);
  EXPECT_EQ((std::vector<int64_t>{5, 6}), values["/Telemetry/longs"]);
}
