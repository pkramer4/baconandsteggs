# baconandsteggs
Written by Preston Kramer
The Bacon and St'eggs steganography python module

Utilizing the module is easy. First, create a Crypt object. If encrypting an image, the parameters are (in order): the key (a string), the image name, relative file path of the image to encode, and the message to encrypt. The message parameter defaults to None, which will come into play when decrypting images The key can be 2,000 characters long.
Next, simply call the encrypt() method on the Crypt object. encrypt takes 2 parameters: the desired file name for the encrypted file as a string, and the photo filetype extension. Allowable filetypes are rng, jpeg, and pdf. The filetype will deafault to png.

An example is below:

encoder = Crypt('thekeyislove', 'images/code_image.py', 'I love You, Chloe')
encoder.encrypt('encoded_image', jpg)

The encoded_image will then be saved into the same directory from which the python file was run.

Decrypting a message is also just as easy. create a Crypt object by passing the key and relative file path of the file to be decoded. Then call the decrypt() method on the Crypt object. The message is returned by the method. If an incorrect key is used to create the object, an incorrect message will be displayed. An example is below:

decoder = Crypt('thekeyislove', 'encoded_image.jpg')
deoder.decrypt()
