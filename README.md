Problem Statement 3 - Trigger Word Detection


Introduction

The importance of touch free interaction has never been more important in the post covid world. Touch free interfaces are not only safer from contact born diseases they are also much more convenient to use. You use touch free and voice based tools every day from your vacuum machine to your mobile phone and your car has touch free components to make the interaction seamless. The issue is that even the labs at Apple, Google, and Amazon have yet to crack the holy grail of creating a robust wakeword detection system that is resilient to mispredictions. That’s where you come in.


Problem Statement

You are required to develop a web based or mobile application that can interphase with the microphone on the device and provide visual feedback to the user based on the word that was spoken.


The model at a later stage is expected to run on an edge device with limited resources, you are expected to design the model in such a way that it can be deployed on a Raspberry Pi 3 or a STM32H747II.


Data

You will be provided samples of the wake words door open, door stop, and door close.

You can find the dataset here: Trigger Word Detection


Keep in mind that you are free to choose your own data as well as long you believe that it is relevant to the given problem statement.



Technical Challenges

Extremely diverse data conditions: The model is expected to perform with a high accuracy on a diverse set of environmental conditions such as areas with background noise and the audio patterns of a diverse gender and pronunciations of the same word.  


Compute Limitation: Being that the model must be deployed on a low compute device the model is expected to utilize under 8MB of RAM and 16MB of ROM at any given time. You are expected to produce some kind of proof to back up the claims that the model is only utilizing the above mentioned resources.


Algorithm Efficiency: The time taken to perform a prediction must be less than the length of the audio used for the inference to be considered realtime.


Deliverables

An intuitive full stack application where users can record audio using the microphone of the device it is running on.
A model capable of notifying the user whenever the words door open, door close, or door stop are spoken by the user.
A description to support the claim that the model can be deployed on a Raspberry Pi or an STM32H747II
Detailed documentation on the development, AI implementation strategies, and user instructions.
