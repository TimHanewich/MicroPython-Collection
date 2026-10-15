def transform(ival:float) -> float:
    """
    Provide the input as a float from 0.0 to 1.0 and get the output as a range from -1.0 and 1.0, but with a center dead zone and outer dead zone applied!
    """
        
    # convert to -1.0 to 1.0 range
    full_range:float = (ival * 2) - 1.0
    
    # Settings
    dead_zone:float = 0.15      # Inputs only considered below -10% and above 10%. Anything in between -10% and 10% will be treated as no input.
    ceiling = 0.9              # 80% in either direction max movement is considered "full" (100% input)
    discernable_range:float = ceiling - dead_zone
    
    # Calculation
    over_dead_zone:float = max(abs(full_range) - dead_zone, 0.0)
    percent_of_dr:float = over_dead_zone / discernable_range
    constrained:float = min(percent_of_dr, 1.0)
    
    # final step = flip the signs if needed so negatives are preserved
    if full_range < 0.0:
        constrained = constrained * -1
    
    return constrained