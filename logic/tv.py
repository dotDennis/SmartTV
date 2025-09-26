"""
Smart TV Logic
==============

This module defines the SmartTV class, which encapsulates the
core logic of the simulated Smart TV. It is independent of
networking and command handling.

Author: dotDennis
Course: IDATA2304
"""

class SmartTV:
    """
    Minimal Smart TV model with ON/OFF state and channel support

    Behavior:
        - Starts OFF by default
        - Only 'on' is valid while OFF
        - Can report current ON/OFF status
        - Maintains current channel and number of available channels
    """

    def __init__(self) -> None:
        """
        Initializes the Smart TV in the default state (OFF) with default channels.

        Attributes:
            - _is_on (bool): Power state, False by default.
            - _channels (int): Number of available channels (default: 10).
            - _current_ch (int): Currently active channel (default: 1).
        """
        self._is_on = False
        self._channels = 10
        self._current_ch = 1

    # Power controls
    def turn_on(self) -> None:
        """
        Turns the TV on.

        Returns:
            None
        """
        self._is_on = True
    
    def turn_off(self) -> None:
        """
        Turns the TV off.

        Returns:
            None
        """
        self._is_on = False

    # Query
    def is_on(self) -> bool:
        """
        Check wheter the TV is currently ON.
        
        Returns:
            bool: True if TV is ON, False if OFF.
        """
        return self._is_on

    # Channel methods, only used when TV = ON
    def get_channel_count(self) -> int:
        """
        Gets the total number of available channels.

        Returns:
            int: Number of channels (default:10).
        """
        return self._channels
    
    def get_channel(self) -> int:
        """
        Gets the currently active channel number.

        Returns:
            int: Current channel index (1-based).
        """
        return self._current_ch
    
    def set_channel(self, n: int) -> None:
        """
        Sets the TV to a specific channel.

        Args:
            n (int): The desired channel number (1-_channels).
        
        Raises:
            ValueError: If the channel number is out of range.

        Returns:
            None
        """
        if not (1 <= n <= self._channels):
            raise ValueError('Channel out of range')
        self._current_ch = n