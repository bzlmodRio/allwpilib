// Copyright (c) FIRST and other WPILib contributors.
// Open Source Software; you can modify and/or share it under the terms of
// the WPILib BSD license file in the root directory of this project.

package org.wpilib.backend;

import static org.junit.jupiter.api.Assertions.assertArrayEquals;
import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.io.ByteArrayOutputStream;
import java.nio.ByteBuffer;
import java.util.HashMap;
import java.util.Map;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.wpilib.datalog.DataLogReader;
import org.wpilib.datalog.DataLogRecord;
import org.wpilib.datalog.DataLogWriter;
import org.wpilib.telemetry.Telemetry;
import org.wpilib.telemetry.TelemetryRegistry;

class DataLogTelemetryBackendTest {
  private ByteArrayOutputStream m_data;
  private DataLogWriter m_log;

  @BeforeEach
  void setUp() {
    m_data = new ByteArrayOutputStream();
    m_log = new DataLogWriter(m_data);
    TelemetryRegistry.reset();
    TelemetryRegistry.registerBackend("", new DataLogTelemetryBackend(m_log, "/Telemetry"));
  }

  @AfterEach
  void tearDown() {
    TelemetryRegistry.reset();
    m_log.close();
  }

  @Test
  void logsIntegralArraysAsIntegerArrays() {
    Telemetry.log("shorts", new short[] {1, 2});
    Telemetry.log("ints", new int[] {3, 4});
    Telemetry.log("longs", new long[] {5, 6});

    Map<String, long[]> values = readIntegerArrayValues();

    assertArrayEquals(new long[] {1, 2}, values.get("/Telemetry/shorts"));
    assertArrayEquals(new long[] {3, 4}, values.get("/Telemetry/ints"));
    assertArrayEquals(new long[] {5, 6}, values.get("/Telemetry/longs"));
  }

  private Map<String, long[]> readIntegerArrayValues() {
    m_log.flush();

    Map<Integer, String> entries = new HashMap<>();
    Map<String, long[]> values = new HashMap<>();
    DataLogReader reader = new DataLogReader(ByteBuffer.wrap(m_data.toByteArray()));
    assertTrue(reader.isValid());

    for (DataLogRecord record : reader) {
      if (record.isStart()) {
        DataLogRecord.StartRecordData start = record.getStartData();
        entries.put(start.entry, start.name);
        assertEquals("int64[]", start.type);
      } else if (!record.isControl()) {
        String name = entries.get(record.getEntry());
        if (name != null) {
          values.put(name, record.getIntegerArray());
        }
      }
    }

    return values;
  }
}
