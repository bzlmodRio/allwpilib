// Copyright (c) FIRST and other WPILib contributors.
// Open Source Software; you can modify and/or share it under the terms of
// the WPILib BSD license file in the root directory of this project.

#pragma once

#include <functional>
#include <limits>

#include <wpi/SymbolExports.h>
#include <wpi/sendable/Sendable.h>
#include <wpi/sendable/SendableHelper.h>

#include "units/time.h"

namespace frc {

/**
 * Implements a PID control loop.
 */
class WPILIB_DLLEXPORT PIDController
    : public wpi::Sendable,
      public wpi::SendableHelper<PIDController> {
 public:
  /**
   * Allocates a PIDController with the given constants for Kp, Ki, and Kd.
   *
   * @param Kp     The proportional coefficient. Must be >= 0.
   * @param Ki     The integral coefficient. Must be >= 0.
   * @param Kd     The derivative coefficient. Must be >= 0.
   * @param period The period between controller updates in seconds. The
   *               default is 20 milliseconds. Must be positive.
   */
  PIDController(double Kp, double Ki, double Kd,
                units::second_t period = 20_ms);

  ~PIDController() override = default;

  PIDController(const PIDController&) = default;
  PIDController& operator=(const PIDController&) = default;
  PIDController(PIDController&&) = default;
  PIDController& operator=(PIDController&&) = default;

  /**
   * Sets the PID Controller gain parameters.
   *
   * Sets the proportional, integral, and differential coefficients.
   *
   * @param Kp The proportional coefficient. Must be >= 0.
   * @param Ki The integral coefficient. Must be >= 0.
   * @param Kd The differential coefficient. Must be >= 0.
   */
  void SetPID(double Kp, double Ki, double Kd);

  /**
   * Sets the proportional coefficient of the PID controller gain.
   *
   * @param Kp The proportional coefficient. Must be >= 0.
   */
  void SetP(double Kp);

  /**
   * Sets the integral coefficient of the PID controller gain.
   *
   * @param Ki The integral coefficient. Must be >= 0.
   */
  void SetI(double Ki);

  /**
   * Sets the differential coefficient of the PID controller gain.
   *
   * @param Kd The differential coefficient. Must be >= 0.
   */
  void SetD(double Kd);

  /**
   * Sets the IZone range. When the absolute value of the position error is
   * greater than IZone, the total accumulated error will reset to zero,
   * disabling integral gain until the absolute value of the position error is
   * less than IZone. This is used to prevent integral windup. Must be
   * non-negative. Passing a value of zero will effectively disable integral
   * gain. Passing a value of infinity disables IZone functionality.
   *
   * @param iZone Maximum magnitude of error to allow integral control. Must be
   *   >= 0.
   */
  void SetIZone(double iZone);

  /**
   * Gets the proportional coefficient.
   *
   * @return proportional coefficient
   */
  double GetP() const;

  /**
   * Gets the integral coefficient.
   *
   * @return integral coefficient
   */
  double GetI() const;

  /**
   * Gets the differential coefficient.
   *
   * @return differential coefficient
   */
  double GetD() const;

  /**
   * Get the IZone range.
   *
   * @return Maximum magnitude of error to allow integral control.
   */
  double GetIZone() const;

  /**
   * Gets the period of this controller.
   *
   * @return The period of the controller.
   */
  units::second_t GetPeriod() const;

  /**
   * Gets the error tolerance of this controller.
   *
   * @return The error tolerance of the controller.
   */
  double GetErrorTolerance() const;

  /**
   * Gets the error derivative tolerance of this controller.
   *
   * @return The error derivative tolerance of the controller.
   */
  double GetErrorDerivativeTolerance() const;

  /**
   * Gets the position tolerance of this controller.
   *
   * @return The position tolerance of the controller.
   * @deprecated Use GetErrorTolerance() instead.
   */
  [[deprecated("Use the GetErrorTolerance method instead.")]]
  double GetPositionTolerance() const;

  /**
   * Gets the velocity tolerance of this controller.
   *
   * @return The velocity tolerance of the controller.
   * @deprecated Use GetErrorDerivativeTolerance() instead.
   */
  [[deprecated("Use the GetErrorDerivativeTolerance method instead.")]]
  double GetVelocityTolerance() const;

  /**
   * Gets the accumulated error used in the integral calculation of this
   * controller.
   *
   * @return The accumulated error of this controller.
   */
  double GetAccumulatedError() const;

  /**
   * Sets the setpoint for the PIDController.
   *
   * @param setpoint The desired setpoint.
   */
  void SetSetpoint(double setpoint);

  /**
   * Returns the current setpoint of the PIDController.
   *
   * @return The current setpoint.
   */
  double GetSetpoint() const;

  /**
   * Returns true if the error is within the tolerance of the setpoint.
   *
   * This will return false until at least one input value has been computed.
   */
  bool AtSetpoint() const;

  /**
   * Enables continuous input.
   *
   * Rather then using the max and min input range as constraints, it considers
   * them to be the same point and automatically calculates the shortest route
   * to the setpoint.
   *
   * @param minimumInput The minimum value expected from the input.
   * @param maximumInput The maximum value expected from the input.
   */
  void EnableContinuousInput(double minimumInput, double maximumInput);

  /**
   * Disables continuous input.
   */
  void DisableContinuousInput();

  /**
   * Returns true if continuous input is enabled.
   */
  bool IsContinuousInputEnabled() const;

  /**
   * Sets the minimum and maximum contributions of the integral term.
   *
   * The internal integrator is clamped so that the integral term's contribution
   * to the output stays between minimumIntegral and maximumIntegral. This
   * prevents integral windup.
   *
   * @param minimumIntegral The minimum contribution of the integral term.
   * @param maximumIntegral The maximum contribution of the integral term.
   */
  void SetIntegratorRange(double minimumIntegral, double maximumIntegral);

  /**
   * Sets the error which is considered tolerable for use with AtSetpoint().
   *
   * @param errorTolerance error which is tolerable.
   * @param errorDerivativeTolerance error derivative which is tolerable.
   */
  void SetTolerance(double errorTolerance,
                    double errorDerivativeTolerance =
                        std::numeric_limits<double>::infinity());

  /**
   * Returns the difference between the setpoint and the measurement.
   */
  double GetError() const;

  /**
   * Returns the error derivative.
   */
  double GetErrorDerivative() const;

  /**
   * Returns the difference between the setpoint and the measurement.
   * @deprecated Use GetError() instead.
   */
  [[deprecated("Use GetError method instead.")]]
  double GetPositionError() const;

  /**
   * Returns the velocity error.
   * @deprecated Use GetErrorDerivative() instead.
   */
  [[deprecated("Use GetErrorDerivative method instead.")]]
  double GetVelocityError() const;

  /**
   * Returns the next output of the PID controller.
   *
   * @param measurement The current measurement of the process variable.
   */
  double Calculate(double measurement);

  /**
   * Returns the next output of the PID controller.
   *
   * @param measurement The current measurement of the process variable.
   * @param setpoint The new setpoint of the controller.
   */
  double Calculate(double measurement, double setpoint);

  /**
   * Reset the previous error, the integral term, and disable the controller.
   */
  void Reset();

  void InitSendable(wpi::SendableBuilder& builder) override;

 private:
  // Factor for "proportional" control
  double m_Kp;

  // Factor for "integral" control
  double m_Ki;

  // Factor for "derivative" control
  double m_Kd;

  // The error range where "integral" control applies
  double m_iZone = std::numeric_limits<double>::infinity();

  // The period (in seconds) of the control loop running this controller
  units::second_t m_period;

  double m_maximumIntegral = 1.0;

  double m_minimumIntegral = -1.0;

  double m_maximumInput = 0;

  double m_minimumInput = 0;

  // Do the endpoints wrap around? eg. Absolute encoder
  bool m_continuous = false;

  // The error at the time of the most recent call to Calculate()
  double m_error = 0;
  double m_errorDerivative = 0;

  // The error at the time of the second-most-recent call to Calculate() (used
  // to compute velocity)
  double m_prevError = 0;

  // The sum of the errors for use in the integral calc
  double m_totalError = 0;

  // The error that is considered at setpoint.
  double m_errorTolerance = 0.05;
  double m_errorDerivativeTolerance = std::numeric_limits<double>::infinity();

  double m_setpoint = 0;
  double m_measurement = 0;

  bool m_haveSetpoint = false;
  bool m_haveMeasurement = false;
};

}  // namespace frc
