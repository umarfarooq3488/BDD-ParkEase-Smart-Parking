Feature: Parking fee for petrol cars at the grace, rounding and cap boundaries
  As a registered ParkEase driver
  I want my parking fee to be charged automatically from my wallet when I exit
  So that I can leave the plaza without queuing at a payment booth

  Background:
    Given driver "Bilal" is logged in to the ParkEase app
    And the petrol car "LEA-1234" is linked to the driver's account
    And the driver's wallet balance is Rs. 1,000

  @boundary
  Scenario Outline: Petrol car parked for <stay> pays <total> in total
    Given the vehicle has been parked for <stay>
    When the vehicle leaves through the exit gate
    Then the receipt should show a parking fee of <fee>
    And the receipt should show a service charge of <service>
    And the receipt should show a total paid of <total>
    And the wallet balance should be <balance>
    And the exit gate should be open

    Examples: Free and rounding
      | stay       | fee     | service | total   | balance   |
      | 15 min 0 s | Rs. 0   | Rs. 0   | Rs. 0   | Rs. 1,000 |
      | 15 min 1 s | Rs. 100 | Rs. 20  | Rs. 120 | Rs. 880   |
      | 60 min 0 s | Rs. 100 | Rs. 20  | Rs. 120 | Rs. 880   |
      | 61 min 0 s | Rs. 160 | Rs. 20  | Rs. 180 | Rs. 820   |

    Examples: Daily cap
      | stay           | fee     | service | total   | balance |
      | 12 h 0 min 0 s | Rs. 760 | Rs. 20  | Rs. 780 | Rs. 220 |
      | 12 h 0 min 1 s | Rs. 800 | Rs. 20  | Rs. 820 | Rs. 180 |
      | 30 h 0 min 0 s | Rs. 800 | Rs. 20  | Rs. 820 | Rs. 180 |
