
from typing import Callable

def rk4_x_dt(fun: Callable[float, float], x: float, dt: float) -> float:
    h = dt

    k1 = fun(x)
    k2 = fun(x + h * 0.5 * k1)
    k3 = fun(x + h * 0.5 * k2)
    k4 = fun(x + h * k3)
    
    return x + h / 6.0 * (k1 + 2.0 * k2 + 2.0 * k3 + k4)


def rk4_x_u_dt(fun: Callable[float, float], x: float, u: float, dt: float) -> float:
    h = dt

    k1 = fun(x, u)
    k2 = fun(x + h * 0.5 * k1, u)
    k3 = fun(x + h * 0.5 * k2, u)
    k4 = fun(x + h * k3, u)

    return x + h / 6.0 * (k1 + 2.0 * k2 + 2.0 * k3 + k4)


def rk4_t_y_dt(fun: Callable[float, float], t, y, dt):
    h = dt

    k1 = fun(t, y)
    k2 = fun(t + dt * 0.5, y + h * k1 * 0.5)
    k3 = fun(t + dt * 0.5, y + h * k2 * 0.5)
    k4 = fun(t + dt, y + h * k3)

    return y + h / 6.0 * (k1 + 2.0 * k2 + 2.0 * k3 + k4)


def rkdp_x_y_dt(fun, x, u, dt, max_error = 1e-6):
    A = [
      [1.0 / 5.0],
      [3.0 / 40.0, 9.0 / 40.0],
      [44.0 / 45.0, -56.0 / 15.0, 32.0 / 9.0],
      [19372.0 / 6561.0, -25360.0 / 2187.0, 64448.0 / 6561.0, -212.0 / 729.0],
      [9017.0 / 3168.0, -355.0 / 33.0, 46732.0 / 5247.0, 49.0 / 176.0, -5103.0 / 18656.0],
      [35.0 / 384.0, 0.0, 500.0 / 1113.0, 125.0 / 192.0, -2187.0 / 6784.0, 11.0 / 84.0]
    ]

    b1 = [35.0 / 384.0, 0.0, 500.0 / 1113.0, 125.0 / 192.0, -2187.0 / 6784.0, 11.0 / 84.0, 0.0]

    b2 = [
      5179.0 / 57600.0,
      0.0,
      7571.0 / 16695.0,
      393.0 / 640.0,
      -92097.0 / 339200.0,
      187.0 / 2100.0,
      1.0 / 40.0
    ]

    newX = [0.0]
    truncation_error = 0.0

    dt_elapsed = 0.0
    h = dt

    first_time = True
    while dt_elapsed < dt:
        if not first_time and truncationError > maxError:
            break

        first_time = True

        h = min(h, dt - dt_elapsed)

        k1 = fun(x, u)
        k2 = fun(x + h * (A[0][0] * k1), u)
        k3 = fun(x + h * (A[1][0] * k1 + A[1][1] * k2), u)
        k4 = fun(x + h * (A[2][0] * k1 + A[2][1] * k2 + A[2][2] * k3), u)
        k5 = fun(x + h * (A[3][0] * k1 + A[3][1] * k2 + A[3][2] * k3 + A[3][3] * k4), u)
        k6 = fun(x + h * (A[4][0] * k1 + A[4][1] * k2 + A[4][2] * k3 + A[4][3] * k4 + A[4][4] * k5), u)


        new_x = x + h * (A[5][0] * k1 + A[5][1] * k2 + A[5][2] * k3 +
                        A[5][3] * k4 + A[5][4] * k5 + A[5][5] * k6)
        k7 = fun(new_x, u)
        
        truncationError = (h * ((b1[0] - b2[0]) * k1 + (b1[1] - b2[1]) * k2 +
                                (b1[2] - b2[2]) * k3 + (b1[3] - b2[3]) * k4 +
                                (b1[4] - b2[4]) * k5 + (b1[5] - b2[5]) * k6 +
                                (b1[6] - b2[6]) * k7))

        if truncation_error == 0.0:
            h = dt - dt_elapsed
        else:
            h = h * 0.9 * math.pow(max_error / truncation_error, 1.0 / 5.0)


        dt_elapsed += h
        x = new_x

    return x



def rkdp_t_y_dt(fun, t, y, dt, max_error = 1e-6):
    A = [
      [1.0 / 5.0],
      [3.0 / 40.0, 9.0 / 40.0],
      [44.0 / 45.0, -56.0 / 15.0, 32.0 / 9.0],
      [19372.0 / 6561.0, -25360.0 / 2187.0, 64448.0 / 6561.0, -212.0 / 729.0],
      [9017.0 / 3168.0, -355.0 / 33.0, 46732.0 / 5247.0, 49.0 / 176.0, -5103.0 / 18656.0],
      [35.0 / 384.0, 0.0, 500.0 / 1113.0, 125.0 / 192.0, -2187.0 / 6784.0, 11.0 / 84.0]
    ]

    b1 = [35.0 / 384.0, 0.0, 500.0 / 1113.0, 125.0 / 192.0, -2187.0 / 6784.0, 11.0 / 84.0, 0.0]

    b2 = [
      5179.0 / 57600.0,
      0.0,
      7571.0 / 16695.0,
      393.0 / 640.0,
      -92097.0 / 339200.0,
      187.0 / 2100.0,
      1.0 / 40.0
    ]

    c = [1.0 / 5.0, 3.0 / 10.0, 4.0 / 5.0,
                                           8.0 / 9.0, 1.0,        1.0]

    newX = [0.0]
    truncation_error = 0.0

    dt_elapsed = 0.0
    h = dt

    first_time = True
    while dt_elapsed < dt:
        if not first_time and truncationError > maxError:
            break
        first_time = True

        h = min(h, dt - dt_elapsed)

        k1 = fun(t, y)
        k2 = fun(t + h * c[0], y + h * (A[0][0] * k1))
        k3 = fun(t + h * c[1], y + h * (A[1][0] * k1 + A[1][1] * k2))
        k4 = fun(t + h * c[2], y + h * (A[2][0] * k1 + A[2][1] * k2 + A[2][2] * k3))
        k5 = fun(t + h * c[3], y + h * (A[3][0] * k1 + A[3][1] * k2 + A[3][2] * k3 + A[3][3] * k4))
        k6 = fun(t + h * c[4], y + h * (A[4][0] * k1 + A[4][1] * k2 + A[4][2] * k3 + A[4][3] * k4 + A[4][4] * k5))

        new_y = y + h * (A[5][0] * k1 + A[5][1] * k2 + A[5][2] * k3 +
                        A[5][3] * k4 + A[5][4] * k5 + A[5][5] * k6)
        k7 = fun(t + h * c[5], new_y)

        truncation_error = (h * ((b1[0] - b2[0]) * k1 + (b1[1] - b2[1]) * k2 +
                                (b1[2] - b2[2]) * k3 + (b1[3] - b2[3]) * k4 +
                                (b1[4] - b2[4]) * k5 + (b1[5] - b2[5]) * k6 +
                                (b1[6] - b2[6]) * k7))
                                
        h = h * 0.9 * pow(max_error / truncation_error, 1.0 / 5.0)

        dt_elapsed += h
        y = new_y

    return y