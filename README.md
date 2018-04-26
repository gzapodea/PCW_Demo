# **Partner Connection Week 2018 Demo**

This repo is used to share sample code that will be used for the Partner Connection Week Demo.

The demo will require:
 - Equipment: IOS-XE devices, Catalyst 9000 switch, DNA Center
 - Guest Shell enabled, configured, able to reach the Internet
 - requests Python package installed, Guest Shell default Python version
 - RESTCONF configured
 - ServiceNow account
 - Spark Account
 - Some customizations will be required for your ServiceNow instance:
    - create an account enabled for REST APIs access
    - UI Policy to the "incident" table to add "close_notes" and "close_code" when closing an incident
    - business rule that will trigger the Spark Integration
    - configure the ServiceNow to Spark Integration using the example from https://apphub.webex.com/categories/all/integrations/servicenow-cisco-systems
 
Download the entire folder {PCW_Demo} to your device flash memory.

The demo includes:
 - uplink failure detection using EEM will create, update and close ServiceNow incident
 - redundant power supply failure will create, update, close ServiceNow incident, turn on/off the LED Blue Beacon
 - unauthorized configuration change will roll back configurations made by user
 - IT Personal assistant will create Spark Room for manager at the arrival at his office and update with all urgent incidents.