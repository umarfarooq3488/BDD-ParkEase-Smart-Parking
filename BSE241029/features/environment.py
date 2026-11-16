from parkease import ParkEase


def before_scenario(context, scenario):
    # Hook: every scenario starts with a fresh in-memory ParkEase system
    context.app = ParkEase()
    context.plate = None
    context.result = None
