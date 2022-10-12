class LiPo:

    v_full = None # "full" voltage. usually 4.2V in a typical single-cell LiPo
    v_dead = None # "dead" voltage. usually 3.4V in a typical single-cell LiPo

    def __init__(self, volts_full:float = 4.2, volts_dead:float = 3.4) -> None:
        self.v_full = volts_full
        self.v_dead = volts_dead

    def percentage(self, volts:float) -> float:
        percent = (volts - self.v_dead) / (self.v_full - self.v_dead)
        if percent > 1.0:
            return 1.0
        elif percent < 0.0:
            return 0.0
        else:
            return percent
