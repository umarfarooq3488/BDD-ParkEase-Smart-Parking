Feature: Automatic exit payment from the ParkEase wallet
  As a registered ParkEase driver
  I want my parking fee to be charged automatically from my wallet when I exit
  So that I can leave the plaza without queuing at a payment booth

  @smoke
  Scenario: Registered EV driver pays for a 3 hour 40 minute stay from the wallet
    Given driver "Ayesha" is logged in to the ParkEase app
    And the electric vehicle "LEB-2046" is linked to the driver's account
    And the driver's wallet balance is Rs. 1,000
    And the vehicle entered the plaza at 09:00
    When the vehicle leaves through the exit gate at 12:40
    Then the app should show "Payment successful – gate opening"
    And the receipt should show a parking fee of Rs. 280
    And the receipt should show an EV discount of Rs. 70
    And the receipt should show a service charge of Rs. 20
    And the receipt should show a total paid of Rs. 230
    And the wallet balance should be Rs. 770
    And the exit gate should be open

  @boundary
  Scenario: EV discount is applied after the Rs. 800 cap
    Given driver "Ayesha" is logged in to the ParkEase app
    And the electric vehicle "LEB-2046" is linked to the driver's account
    And the driver's wallet balance is Rs. 1,000
    And the vehicle has been parked for 20 h 0 min
    When the vehicle leaves through the exit gate
    Then the app should show "Payment successful – gate opening"
    And the receipt should show a parking fee of Rs. 800
    And the receipt should show an EV discount of Rs. 200
    And the receipt should show a service charge of Rs. 20
    And the receipt should show a total paid of Rs. 620
    And the wallet balance should be Rs. 380
