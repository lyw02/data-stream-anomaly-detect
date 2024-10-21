import math
import random
import time
from typing import Self, Generator

import matplotlib.pyplot as plt


class DataStream:
    """Simulate data stream"""

    @staticmethod
    def generate(normal_mu: int | float = 10, normal_sigma: int | float = 2, seasonal_amplitude: int | float = 4,
                 noise_sigma: int | float = 0.5) -> Generator[float, None, None]:
        """
        Use a generator to simulate data stream
        Normal data and random noise follow Gaussian distribution
        Seasonal data changes with time periodically, each minute of time corresponds to one period of the sine function

        Parameters
        ----------
            normal_mu : int | float
                The value that normal data distribute around (mu of Gaussian distribution)
            normal_sigma : int | float
                Deviation of normal data (sigma of Gaussian distribution)
            seasonal_amplitude : int | float
                Deviation of seasonal data (amplitude of sine wave)
            noise_sigma : int | float
                Deviation of random noise (sigma of Gaussian distribution)
        """
        if not isinstance(normal_mu, (int, float)):
            raise TypeError(f"Parameter normal_mu should be int or float, got {type(normal_mu)}")
        if not isinstance(normal_sigma, (int, float)):
            raise TypeError(f"Parameter normal_sigma should be int or float, got {type(normal_sigma)}")
        if not isinstance(seasonal_amplitude, (int, float)):
            raise TypeError(f"Parameter seasonal_amplitude should be int, got {type(seasonal_amplitude)}")
        if not isinstance(noise_sigma, (int, float)):
            raise TypeError(f"Parameter noise_sigma should be int or float, got {type(noise_sigma)}")

        while True:
            try:
                normal_data = random.gauss(normal_mu, normal_sigma)
                seasonal_data = seasonal_amplitude * math.sin(2 * math.pi * (time.time() % 60) / 60)
                noise = random.gauss(0, noise_sigma)
                yield normal_data + seasonal_data + noise
            except Exception as e:
                print(f"Error in generating data: {e}")
                continue


class MSTD:
    """
    Use moving standard deviation (MSTD) to find anomaly
    If the difference between a value and the moving average (MA) is greater than MSTD * threshold,
    it is considered as anomaly

    Parameters
    ----------
    window_size : int
        Number of adjacent items in the data list should be involved to compute MA and MSTD
    threshold: int | float
        How many times of MSTD does the difference between data and MA reaches will data be considered as anomaly
    """
    def __init__(self, window_size: int = 3, threshold: int | float = 1.2):
        if not isinstance(window_size, int):
            raise TypeError(f"window_size should be int, got {type(window_size)}")
        if not isinstance(threshold, (int, float)):
            raise TypeError(f"threshold should be int or float, got {type(threshold)}")

        self._data: list[float] = []
        self._window_size: int = window_size
        self._ma: list[float] = []  # moving average
        self._mstd: list[float] = []  # moving standard deviation
        self._threshold: int | float = threshold
        self._anomalies: list[float] = []

    def moving_average_and_moving_standard_deviation(self, value: float) -> Self:
        """Optimisation: only newly generated value and related values will be involved

        Parameters
        ----------
        value : float
            Newly generated value

        Returns
        -------
        Self
            Returns self for chain calling
        """
        if not isinstance(value, (int, float)):
            raise TypeError(f"value should be int or float, got {type(value)}")

        self._data.append(value)
        if len(self._data) >= self._window_size:
            current_window = self._data[-self._window_size:]
            window_average = sum(current_window) / self._window_size
            variance = sum((x - window_average) ** 2 for x in current_window) / self._window_size
            window_std_deviation = math.sqrt(variance)

            self._ma.append(window_average)
            self._mstd.append(window_std_deviation)
        return self

    def find_anomaly(self) -> list[float]:
        """Optimisation: only newly generated value will be tested"""
        if len(self._ma) >= 1:
            index = len(self._ma) - 1
            try:

                if abs(self._data[-1] - self._ma[index]) > self._threshold * self._mstd[index]:
                    self._anomalies.append(self._data[-1])
            except Exception as e:
                print(f"Error in detecting anomaly: {e}")
        return self._anomalies


if __name__ == "__main__":
    data_stream = DataStream.generate()
    data = []
    mstd = MSTD()
    plt.ion()
    _, ax = plt.subplots()
    for value in data_stream:
        try:
            data.append(value)
            anomaly = mstd.moving_average_and_moving_standard_deviation(value).find_anomaly()
            color = ["r" if i in anomaly else "b" for i in data]
            plt.scatter(range(len(data)), data, c=color)
            plt.legend(
                handles=[plt.Line2D([0], [0], marker="o", color="w", markerfacecolor="b", label="Normal"),
                         plt.Line2D([0], [0], marker="o", color="w", markerfacecolor="r", label="Anomaly")],
            )
            plt.title("Data stream")
            plt.xlabel("Data index")
            plt.ylabel("Data value")
            plt.draw()
            plt.pause(1)  # generate a data point each second
            print(f"data ({len(data)}): {data}")
            print(f"anomaly ({len(anomaly)}): {anomaly}")
            print("========")
        except Exception as e:
            print(f"Error in value {value}: {e}")
