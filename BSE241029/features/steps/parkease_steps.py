import re
from datetime import timedelta

import parse
from behave import given, when, then, register_type

from parkease import today_at

# ---------------------------------------------------------------------------
# Custom parameter types
# ---------------------------------------------------------------------------
@parse.with_pattern(r"Rs\. \d{1,3}(?:,\d{3})*")
def parse_amount(text):
    """'Rs. 1,000' -> 1000"""
    return int(text[len("Rs. "):].replace(",", ""))


@parse.with_pattern(r"\d+ (?:h|min|s)(?: \d+ (?:min|s))*")
def parse_duration(text):
    """'3 h 40 min', '15 min 1 s', '12 h 0 min 1 s' -> timedelta"""
    units = {"h": "hours", "min": "minutes", "s": "seconds"}
    parts = {units[u]: int(n) for n, u in re.findall(r"(\d+) (h|min|s)", text)}
    return timedelta(**parts)


@parse.with_pattern(r"\d{2}:\d{2}")
def parse_clock(text):
    return today_at(text)


@parse.with_pattern(r"electric vehicle|petrol car")
def parse_kind(text):
    return text == "electric vehicle"


register_type(Amount=parse_amount, Duration=parse_duration,
              Clock=parse_clock, Electric=parse_kind)

FIXED_EXIT_TIME = today_at("23:59") + timedelta(days=2)


def rs(value):
    return f"Rs. {value:,}"


def expect_amount(what, expected, actual):
    assert actual == expected, f"{what}: expected {rs(expected)} but was {rs(actual)}"


# ---------------------------------------------------------------------------
# Given
# ---------------------------------------------------------------------------
@given('driver "{name}" is logged in to the ParkEase app')
def step_logged_in(context, name):
    context.app.login(name)


@given('the {electric:Electric} "{plate}" is linked to the driver\'s account')
def step_link_vehicle(context, electric, plate):
    context.app.link_vehicle(plate, electric)
    context.plate = plate


@given("the driver's wallet balance is {amount:Amount}")
def step_wallet(context, amount):
    context.app.set_wallet(amount)
    context.balance_before = amount


@given("the vehicle entered the plaza at {time:Clock}")
def step_entered_at(context, time):
    context.app.enter(context.plate, time)


@given("the vehicle has been parked for {stay:Duration}")
def step_parked_for(context, stay):
    context.app.enter_before_exit(context.plate, stay, FIXED_EXIT_TIME)


# ---------------------------------------------------------------------------
# When
# ---------------------------------------------------------------------------
@when("the vehicle leaves through the exit gate at {time:Clock}")
def step_exit_at(context, time):
    context.result = context.app.exit_at(context.plate, time)


@when("the vehicle leaves through the exit gate")
def step_exit(context):
    context.result = context.app.exit_at(context.plate, FIXED_EXIT_TIME)


# ---------------------------------------------------------------------------
# Then
# ---------------------------------------------------------------------------
@then('the app should show "{message}"')
def step_message(context, message):
    actual = context.result.message
    assert actual == message, f'Message: expected "{message}" but was "{actual}"'


@then("the receipt should show a parking fee of {amount:Amount}")
def step_fee(context, amount):
    expect_amount("Parking fee", amount, context.result.parking_fee)


@then("the receipt should show an EV discount of {amount:Amount}")
def step_discount(context, amount):
    expect_amount("EV discount", amount, context.result.ev_discount)


@then("the receipt should show a service charge of {amount:Amount}")
def step_service(context, amount):
    expect_amount("Service charge", amount, context.result.service_charge)


@then("the receipt should show a total paid of {amount:Amount}")
def step_total(context, amount):
    expect_amount("Total paid", amount, context.result.total_paid)


@then("the wallet balance should be {amount:Amount}")
def step_balance(context, amount):
    expect_amount("Wallet balance", amount, context.app.wallet_balance())


@then("no amount should be deducted from the wallet")
def step_nothing_deducted(context):
    expect_amount("Wallet balance (unchanged)", context.balance_before,
                  context.app.wallet_balance())


@then("the exit gate should be open")
def step_gate_open(context):
    assert context.result.gate_open, "Gate: expected OPEN but was CLOSED"


@then("the exit gate should stay closed")
def step_gate_closed(context):
    assert not context.result.gate_open, "Gate: expected CLOSED but was OPEN"
