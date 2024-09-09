Feature: Upload Pet Image
    As a user, I want to upload an image of a pet

    Scenario: Add a new pet image successfully
        When user uploads an image "test_data/image.jpg" to the petstore
        Then image is successfully uploaded

     
        