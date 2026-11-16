"""In-memory model of the ParkEase exit payment (business rules R1 to R8)."""
import math
from dataclasses import dataclass
from datetime import datetime

GRACE_SECONDS = 15 * 60          # R2: up to and including 15:00 minutes is free
FIRST_HOUR_FEE = 100             # R3
EXTRA_HOUR_FEE = 60              # R3
FEE_CAP = 800                    # R4
EV_DISCOUNT_PERCENT = 25         # R5
SERVICE_CHARGE = 20              # R6

MSG_SUCCESS = "Payment successful – gate opening"
MSG_FREE = "Free exit, gate opening"
MSG_INSUFFICIENT = "Insufficient wallet balance"
MSG_NOT_LOGGED_IN = "Please log in to pay by wallet"
MSG_NOT_LINKED = "Vehicle is not linked to your account"


@dataclass
class ExitResult:
    message: str
    parking_fee: int = 0      # fee after the cap, before the EV discount
    ev_discount: int = 0
    service_charge: int = 0
    total_paid: int = 0
    gate_open: bool = False


class ParkEase:
    def __init__(self):
        self._driver = None
        self._vehicles = {}       # plate -> is_electric
        self._entries = {}        # plate -> entry datetime
        self._wallet = 0
        self.receipt = None

    # ----- account set-up (R1) -----
    def login(self, driver):
        self._driver = driver

    def logout(self):
        self._driver = None

    def is_logged_in(self):
        return self._driver is not None

    def link_vehicle(self, plate, electric):
        self._vehicles[plate] = electric

    def set_wallet(self, rupees):
        self._wallet = rupees

    def wallet_balance(self):
        return self._wallet

    # ----- entry and exit -----
    def enter(self, plate, at):
        self._entries[plate] = at

    def enter_before_exit(self, plate, duration, exit_at):
        """Records an entry so that the stay lasts exactly `duration`."""
        self._entries[plate] = exit_at - duration

    def exit_at(self, plate, at):
        seconds = int((at - self._entries[plate]).total_seconds())
        return self.exit(plate, seconds)

    def exit(self, plate, seconds_parked):
        # R1: only a logged-in driver with a linked vehicle can pay by wallet
        if not self.is_logged_in():
            return ExitResult(MSG_NOT_LOGGED_IN)
        if plate not in self._vehicles:
            return ExitResult(MSG_NOT_LINKED)

        # R2: grace period, no service charge on a free exit (R6)
        if seconds_parked <= GRACE_SECONDS:
            return ExitResult(MSG_FREE, gate_open=True)

        is_ev = self._vehicles[plate]
        fee = self.parking_fee(seconds_parked)                  # R3 + R4
        discount = fee * EV_DISCOUNT_PERCENT // 100 if is_ev else 0   # R5
        total = fee - discount + SERVICE_CHARGE                 # R6

        # R7: the wallet must cover the whole amount
        if self._wallet < total:
            return ExitResult(MSG_INSUFFICIENT, fee, discount,
                              SERVICE_CHARGE, 0, False)

        # R8: deduct, show message and receipt
        self._wallet -= total
        result = ExitResult(MSG_SUCCESS, fee, discount,
                            SERVICE_CHARGE, total, True)
        self.receipt = result
        return result

    @staticmethod
    def started_hours(seconds_parked):
        # R3: partial hours are rounded up (61 minutes = 2 hours)
        return math.ceil(seconds_parked / 3600)

    def parking_fee(self, seconds_parked):
        hours = self.started_hours(seconds_parked)
        fee = FIRST_HOUR_FEE + EXTRA_HOUR_FEE * (hours - 1)        # R3
        return min(fee, FEE_CAP)                                    # R4


def today_at(hh_mm):
    """Helper that turns '09:00' into a datetime on a fixed test day."""
    t = datetime.strptime(hh_mm, "%H:%M")
    return datetime(2026, 11, 17, t.hour, t.minute)

