Feature: Exit is refused when the wallet cannot cover the total payable
  As a registered ParkEase driver
  I want my parking fee to be charged automatically from my wallet when I exit
  So that I can leave the plaza without queuing at a payment booth

  @negative
  Scenario: Wallet is Rs. 1 short of the total payable
    Given driver "Bilal" is logged in to the ParkEase app
    And the petrol car "LEA-1234" is linked to the driver's account
    And the driver's wallet balance is Rs. 239
    And the vehicle entered the plaza at 10:00
    When the vehicle leaves through the exit gate at 12:10
    Then the app should show "Insufficient wallet balance"
    And no amount should be deducted from the wallet
    And the wallet balance should be Rs. 239
    And the exit gate should stay closed
