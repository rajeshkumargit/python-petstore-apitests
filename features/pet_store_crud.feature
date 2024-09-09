Feature: CRUD in pet store
    As a user, I want to create, read, update, delete pet details in pet store

    Scenario Outline: Create a new pet
        Given user creates a new pet with "<category>", "<name>", "<tag>", and "<status>"
        Then user validates successful creation of pet
        And user fetches the pet successfully
        
        Examples:
            |category|name|tag|status|
            |labrador|buddy|lovely_pet|available|

    Scenario Outline: Update an existing pet
        When user successfully updates an existing pet "<category>", "<name>", "<tag>", and "<status>"
        Then user fetches the pet successfully

        Examples:
            |category|name|tag|status|
            |labrador|ginger|cutie_pet|pending|

    Scenario Outline: Update an existing pet with form data
        Given user creates a new pet with "<category>", "<name>", "<tag>", and "<status>"
        Then user validates successful creation of pet
        When user successfully updates an existing pet with form data "<updated_name>" and "<updated_status>"
        Then user fetches the pet successfully

        Examples:
            |updated_name|updated_status|category|name|tag|status|
            |maxie|sold|bulldog|shadow|love|available|

    Scenario Outline: get pet by status
        When user successfully fetches pet by status "<status>"

        Examples:
            |status|
            |available,sold|


    Scenario Outline: Delete a pet
        Given user creates a new pet with "<category>", "<name>", "<tag>", and "<status>"
        Then user validates successful creation of pet
        When user deletes the pet successfully
        Then user is not able to fetch the pet 

        Examples:
            |category|name|tag|status|
            |beagle|bear|cutie_pet|available|



    

            
        