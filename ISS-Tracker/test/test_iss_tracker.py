import pytest
import math

from iss_tracker import calculate_average_speed, get_instantaneous_speed

def test_calculate_average_speed():
    # Sample data
    data = [
        {'x_dot': 1, 'y_dot': 2, 'z_dot': 3},
        {'x_dot': 2, 'y_dot': 3, 'z_dot': 4},
        {'x_dot': 3, 'y_dot': 4, 'z_dot': 5}
    ]
    # Expected average speed
    expected_average_speed = (math.sqrt(1**2 + 2**2 + 3**2) + math.sqrt(2**2 + 3**2 + 4**2) + math.sqrt(3**2 + 4**2 + 5**2)) / 3
    result = calculate_average_speed(data)
    assert result == expected_average_speed

def test_get_instantaneous_speed():
    # Sample epoch data
    epoch_data = {'x_dot': 1, 'y_dot': 2, 'z_dot': 3}
    # Expected instantaneous speed
    expected_speed = math.sqrt(1**2 + 2**2 + 3**2)
    result = get_instantaneous_speed(epoch_data)
    assert result == expected_speed

