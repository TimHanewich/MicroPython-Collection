def transform(value:float, offset:float = 0.0, deadzone:float = 0.05, ceiling:float = 0.8) -> float:
    """
    Provide the input value from -1.0 to 1.0.
    
    offset: When untouched, the value the axis holds to naturally with no input at all. (a bias, say, for +8% input) This will be subtracted out to "center" around this value.
    deadzone: Inputs only considered above this, in either direction. Anything within will be considered as no input.
    ceiling: Beyond this level of input in either direction, max movement is considered "full" (100% input)
    """

    # subtract out the "offset" to "center around" the bias value.
    value_unoffset:float = value - offset
    
    # Settings
    discernable_range:float = ceiling - deadzone
    
    # Calculation
    over_dead_zone:float = max(abs(value_unoffset) - deadzone, 0.0)
    percent_of_dr:float = over_dead_zone / discernable_range
    constrained:float = min(percent_of_dr, 1.0)
    
    # final step = flip the signs if needed so negatives are preserved
    if value_unoffset < 0.0:
        constrained = constrained * -1
    
    return constrained