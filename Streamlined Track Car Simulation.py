import numpy as np
import matplotlib.pyplot as plt


class TrackSimulator:
    def __init__(self):

        self.altitude = 50.0
        self.gravity = 9.81


        self.mass = float(input("Enter Mass: "))
        self.frontal_area = 1.95
        self.drag_coef = 0.32
        self.lift_coef = -0.85
        self.rolling_res = 0.012
        self.wheel_radius = 0.315
        self.max_brake_force = 14000.0


        self.idle_rpm = 1200.0
        self.max_rpm = 8500.0
        self.shift_target = 8200.0
        self.gear_ratios = [3.01, 2.04, 1.57, 1.28, 1.09, 0.95]
        self.final_drive = 4.10
        self.transmission_eff = 0.88


        self.current_gear = 0
        self.is_shifting = False
        self.shift_timer = 0.0
        self.shift_duration = 0.12


        self.dyno_rpm = np.array([1200, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 8500])
        self.dyno_torque = np.array([180, 240, 310, 365, 410, 425, 400, 350, 280])

    def get_air_density(self):
        """Standard ISA air density approximation."""
        p0, t0 = 101325.0, 288.15
        temp = t0 - (0.0065 * self.altitude)
        pressure = p0 * (1.0 - (0.0065 * self.altitude) / t0) ** 5.255
        return max(0.1, pressure / (287.05 * temp))

    def get_torque(self, rpm):
        """Interpolates engine torque from the dyno map."""
        if rpm < self.dyno_rpm[0]: return self.dyno_torque[0]
        if rpm > self.max_rpm: return 0.0
        return np.interp(rpm, self.dyno_rpm, self.dyno_torque)

    def run(self, total_time=32.0, dt=0.005):
        steps = int(total_time / dt)

        t_list, vel_list, rpm_list, gear_list, drag_list, drive_list = [], [], [], [], [], []

        velocity = 2.0
        position = 0.0
        engine_rpm = 1500.0
        rho = self.get_air_density()

        for i in range(steps):
            t = i * dt

            throttle = 1.0 if t <= 22.0 else 0.0
            brake = 0.0 if t <= 22.0 else 1.0

            if self.is_shifting:
                self.shift_timer -= dt
                engine_rpm = max(self.idle_rpm, engine_rpm - 4000.0 * dt)
                if self.shift_timer <= 0:
                    self.is_shifting = False
            else:
                if throttle > 0 and engine_rpm >= self.shift_target and self.current_gear < len(self.gear_ratios) - 1:
                    self.current_gear += 1
                    self.is_shifting = True
                    self.shift_timer = self.shift_duration


            v_sq = velocity ** 2
            f_drag = 0.5 * rho * v_sq * self.drag_coef * self.frontal_area
            f_downforce = 0.5 * rho * v_sq * abs(self.lift_coef) * self.frontal_area
            f_rolling = self.rolling_res * ((self.mass * self.gravity) + f_downforce)
            f_brake = brake * self.max_brake_force

            f_drive = 0.0
            if not self.is_shifting and throttle > 0:
                total_ratio = self.gear_ratios[self.current_gear] * self.final_drive
                torque = self.get_torque(engine_rpm) * throttle
                wheel_torque = torque * total_ratio * self.transmission_eff
                f_drive = wheel_torque / self.wheel_radius

            f_net = f_drive - f_drag - f_rolling - f_brake
            acceleration = f_net / self.mass

            velocity += acceleration * dt
            velocity = max(0.0, velocity)
            position += velocity * dt

            if not self.is_shifting:
                total_ratio = self.gear_ratios[self.current_gear] * self.final_drive
                wheel_rps = velocity / (2.0 * np.pi * self.wheel_radius)
                engine_rpm = wheel_rps * total_ratio * 60.0
                engine_rpm = max(self.idle_rpm, min(engine_rpm, self.max_rpm))

            t_list.append(t)
            vel_list.append(velocity * 3.6)  # Convert to km/h
            rpm_list.append(engine_rpm)
            gear_list.append(self.current_gear + 1)
            drag_list.append(f_drag / 1000.0)  # kN
            drive_list.append(f_drive / 1000.0)  # kN

        return np.array(t_list), np.array(vel_list), np.array(rpm_list), np.array(gear_list), np.array(
            drag_list), np.array(drive_list)


if __name__ == "__main__":
    sim = TrackSimulator()
    t, vel, rpm, gear, drag, drive = sim.run()

    # Simple, clean 3-panel dashboard
    fig, axs = plt.subplots(1, 3, figsize=(15, 5))
    fig.suptitle("Streamlined Track Car Simulation", fontsize=14, fontweight='bold')

    # 1. Speed Profile
    axs[0].plot(t, vel, color='tab:blue', linewidth=2)
    axs[0].set_title("Speed (km/h)")
    axs[0].set_xlabel("Time (s)")
    axs[0].grid(True, alpha=0.5)


    axs[1].plot(t, rpm, color='tab:red', linewidth=1.5, label='RPM')
    axs[1].set_title("Engine RPM & Gears")
    axs[1].set_xlabel("Time (s)")
    axs[1].grid(True, alpha=0.5)

    ax_g = axs[1].twinx()
    ax_g.plot(t, gear, color='tab:orange', linestyle=':', linewidth=2, label='Gear')
    ax_g.set_ylim(0.5, 6.5)


    axs[2].plot(t, drive, color='tab:green', label='Drive Force (kN)')
    axs[2].plot(t, drag, color='tab:purple', label='Aero Drag (kN)')
    axs[2].set_title("Longitudinal Forces")
    axs[2].set_xlabel("Time (s)")
    axs[2].legend()
    axs[2].grid(True, alpha=0.5)

    plt.tight_layout()
    plt.show()