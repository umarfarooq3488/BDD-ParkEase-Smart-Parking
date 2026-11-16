# ParkEase BDD tests (Automated Software Testing, Assignment 2)

In-memory `ParkEase` model (rules R1 to R8) automated with **behave**.

## Setup (once)

    pip install -r requirements.txt

## Run all tests

    python -m behave

The console shows the pretty output and the HTML report is written to `reports/report.html`.

## Run one group by tag

    python -m behave --tags=@smoke
    python -m behave --tags=@boundary
    python -m behave --tags=@negative

## Layout

    parkease/parkease.py              ParkEase model and ExitResult
    features/exit_payment.feature     C1 (@smoke) and EV cap check (@boundary)
    features/fee_boundaries.feature   C2 Scenario Outline (@boundary)
    features/insufficient_balance.feature  C3 (@negative)
    features/environment.py           before_scenario hook
    features/steps/parkease_steps.py  step definitions and custom types
    .github/workflows/smoke.yml       CI: @smoke on every push
