%graphics_toolkit('gnuplot');

data = dlmread('3V.csv', '\t'); % Load the CSV file (assuming comma-separated values)

x = data(:, 1); % Extract the first column for x-axis
y = data(:, 2); % Extract the second column for y-axis

% Interpolate to generate more data points
x_interp = linspace(min(x), max(x), 1000); % Generate 100 points between the min and max of x
y_interp = interp1(x, y, x_interp, 'linear'); % Perform linear interpolation

%plot(x, y) % Plot interpolated data
plot(x_interp, y_interp) % Plot interpolated data
xlabel('I of A'); % Set the label for x-axis
ylabel('Y-axis Label'); % Set the label for y-axis
title('Smooth Plot of X vs Y'); % Set the title for the plo
pause; % Pause to keep the plot window open
