# Efficient Data Stream Anomaly Detection

## Algorithm selection

Since in this case, the data stream generates data at regular intervals, the criterion for determining anomalies should be whether data in the time sequence deviates too much from the average level of the data within a certain range before and after it. Therefore, I use Moving Standard Deviation (MSTD) algorithm to detect anomalies.

The first step is computing moving average (MA). Given a list `lst` and a window size `n`, avarage value of every `n` continuous items in `lst` will be computed and form a new list `ma`. This process works like a 1D convolution with a `[1/n] * n` kernel, which means an item in `ma` contains information of previous and next corresponding items in `lst`.

The second step is computing MSTD. This means to compute standard deviation in each window, i.e. how items differ from the average value inside the window.

To detect anomalies, traverse the input data, and compute the difference between data items and corresponding MA items. This shows the difference between actual input and average value inside the window. If the absolute value of the difference is larger than corresponding MSTD item (times a threshold), it indicates the data deviation is too large, so the data will be considered anomaly.

## Data Stream Simulation

A generator function is used to simulate data stream. A generator only generates data when needed, so it is suitable for continuously generating real-time data effectively.

Each piece of data is the sum of 3 parts: normal data, seasonal data, and random noise.

Normal data follows Gaussian distribution (normal distribution), which means the data mostly distribute around a value but fluctuate around it.

Seasonal data follows a sine wave, which changes periodically. The variable of the sine function is time in seconds, which means the period ("season") is one minute.

Random noise data also follows Gaussian distribution around 0, which means the data is small positive or negative values.

## Algorithm effectiveness analysis and optimisation

By definition, given a data list with `n` items, and window size `w`, to compute MA and MSTD, `(n - w + 1)` windows should be traversed. Inside each window, `w` items should be traversed. Therefore, the time complexity of computing MA and MSTD is `O(2 × (n - w + 1) × w)`. And when detecting anomalies, `(n - w + 1)` items should be traversed. Thus, the overall time complexity is `O((2w + 1)(n - w + 1)) = O(2nw - 2w^2 + w + n + 1) ~ O(nw)`, since `w` is usually much smaller than `n`.

The performance bottleneck is that every time when the data stream generates a new value, the MA, MSTD and anomalies should be computed for the whole list, even though mosst of them have already been computed, except the new generated value.

Therefore, the optimisation is that old results will be saved and only newly generated value is involved in computation. For computing MA and MSTD, only newest `w` items will be involved, so the time complexity is `O(w)`. For detecting anomalies, only newest value will be tested, so time complecity is `O(1)`. Therefore, the optimised overall time complexity is `O(w)`.

## Ensure robust error handling and data validation

I use try...exception sentences for error handling in functions, and print error information if occurred.

I use type annotations for static type check, and use explicit if statements for runtime type check which will raise errors if type of any parameter doesn't match.

## Visualisation

Matplotlib is used for visualisation. Data are plotted on a 2D scatter plot, where x-axis represents data index, and y-axis represents data value. Blue scatters denotes normal values, and red scatters denotes anomalies. Every second when a new value is generated, the plot will be updated.