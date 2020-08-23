# bacon and st'eggs steganography module
# Preston Kramer

import random
import math
from PIL import Image


class Crypt:
    """
    Represents encrypted message via x,y coordinate plane
    attributes:
        key_value (int)
        coordinate_dictionary
        x_list
        y_list
    Methods:
        generate_key_value
        generate_grid_locations
    """
    def __init__(self, key, image_name, message=None,):
        """
        constructs crypt object
        Parameters:
            key (str): key for encoding/decoding image
            image_name: image to be encrypted/decrypted, format does not matter,
                must include relative file path to image
            message (str): message to be encoded
        """
        self.__message = message
        self.__key = key
        self.__image = Image.open(image_name)
        self.__decoded_message = ''
        self.__key_value = 0
        self.__key_product_values = []
        self.__coordinate_list = []
        self.__code_pixel_location_list = []
        self.__decrypt_list = []
        self.__x_list = [0]
        self.__y_list = [0]

    def get_message(self):
        """returns message"""
        return self.__message

    def get_image_size(self):
        """returns the size of the image to encode/decode"""
        return self.__image.size

    def reset_coordinate_lists(self):
        """sets x and y lists back to just containing 0"""
        self.__x_list = [0]
        self.__y_list = [0]
        self.__code_pixel_location_list = []

    def show_image(self):
        """show Crypt's image"""
        self.__image.show()

    def generate_key_value(self):
        """
        creates key value from given key, saves to class key_value attribute
        :param key: ten character string
        """
        key_value = ''

        # Adds binary value of each letter in key to key value, which is then converted to int
        for letter in self.__key:
            key_value += str(format(ord(letter), 'b'))

        self.__key_value = int(key_value)

        return self.__key_value

    def generate_grid_locations(self, length):
        """
        creates x,y grid locations for significant pixels based on seed derived from given key
        :param length: (int) length of message to be coded
        :return: sigpix_dictionary: stores x,y values of each character in message
        """
        self.generate_key_value()

        random.seed(self.__key_value)

        height = self.__image.height - 5
        width = self.__image.width - 5

        # adds dictionary of {character: [x,y]} to coordinate_list to track sigpix location
        for i in range(length):

            # generates x and y value for character until x and y not used before
            # !!! The while loops can be uncommented to ensure fidelity of the translated message,
            # ensuring no pixels are doubled. This reduces the maximum length of the encoded message

            x1 = random.randint(5, width)
            # while x1 in self.__x_list:
            #     x1 = random.randint(5, width)

            x2 = random.randint(5, width)
            # while x2 in self.__x_list:
            #     x2 = random.randint(5, width)

            x3 = random.randint(5, width)
            # while x3 in self.__x_list:
            #     x3 = random.randint(5, width)

            y1 = random.randint(5, height)
            # while y1 in self.__y_list:
            #     y1 = random.randint(5, height)

            y2 = random.randint(5, height)
            # while y2 in self.__y_list:
            #     y2 = random.randint(5, height)

            y3 = random.randint(5, height)
            # while y3 in self.__y_list:
            #     y3 = random.randint(5, height)

            self.__code_pixel_location_list.append([x1, y1, x2, y2, x3, y3])

            self.__x_list.append(x1)
            self.__x_list.append(x2)
            self.__x_list.append(x3)
            self.__y_list.append(y1)
            self.__y_list.append(y2)
            self.__y_list.append(y3)

        return self.__code_pixel_location_list

    def add_character_to_coordinates(self):
        """adds character binary values to corresponding grid lists in dictionary"""
        self.generate_grid_locations(len(self.__message))

        for i in range(len(self.__message)):

            # makes character into binary representation
            character = self.get_message()[i]
            character = ''.join(format(ord(character), 'b'))

            # creates dictionary with character as key/ corresponding grid list as value
            self.__coordinate_list.append({character: self.__code_pixel_location_list[i]})

        return self.__coordinate_list

    def encode_length(self):
        """encodes the length of the message into the image in the top two left pixels"""

        # creates base of 0's by subtracting 6 from number of digits in length
        base = '0'*(6-len(str(len(self.__message))))

        full_number = base + str(len(self.__message))

        self.__image.putpixel((0, 0), (int(full_number[0:2]), int(full_number[3:5]), int(full_number[5:])))

    def encrypt(self, save_image_name, file_type="png"):
        """
        changes pixels in code image
        Parameters:
            save_image_name (string): desired name for image file. will save as
            file_type (str): desired file type for saved image (no period required). Defaults to png
        """

        self.encode_length()

        coordinates = self.add_character_to_coordinates()

        # unpack three x and y coords for image, adjusts corresponding pixels to encode character
        for character in coordinates:
            character_binary = str(list(character.keys())[0])
            xy_list = list(character.values())[0]

            rgb_image = self.__image.convert('RGB')
            r1, g1, b1 = rgb_image.getpixel((xy_list[0],xy_list[1]))
            r2, g2, b2 = rgb_image.getpixel((xy_list[2], xy_list[3]))
            r3, g3, b3 = rgb_image.getpixel((xy_list[4], xy_list[5]))

            color_list = [r1, g1, b1, r2, g2, b2, r3, g3, b3]

            # changes color to str binary representation
            for i in range(len(color_list)):
                color_list[i] = str(bin(color_list[i]))

            for i in range(len(character_binary)):
                # if last bit not same as message bit, change to match
                if character_binary[i] != color_list[i][-1] and color_list[i][-1] == '0':
                    color_list[i] = color_list[i][0:-1] + '1'

                elif character_binary[i] != color_list[i][-1] and color_list[i][-1] == '1':
                    color_list[i] = color_list[i][:-1] + '0'

                else:
                    pass

            # put encoded pixels into image
            self.__image.putpixel((xy_list[0], xy_list[1]), (int(color_list[0], 2), int(color_list[1], 2), int(color_list[2], 2)))
            self.__image.putpixel((xy_list[2], xy_list[3]), (int(color_list[3], 2), int(color_list[4], 2), int(color_list[5], 2)))
            self.__image.putpixel((xy_list[4], xy_list[5]), (int(color_list[6], 2), int(color_list[7], 2), int(color_list[8], 2)))

        self.__image.save(save_image_name+'.'+file_type, file_type.upper())

    def decrypt(self):
        """decrypts a given image that has already been encoded by the program"""
        rgb_image = self.__image.convert('RGB')
        r, g, b = rgb_image.getpixel((0, 0))
        message_length = int(str(r)+str(g)+str(b))

        self.reset_coordinate_lists()

        grids = self.generate_grid_locations(message_length)

        # unpack rgb of correct pixels to get message
        for pixel_group in grids:
            r1, g1, b1 = rgb_image.getpixel((pixel_group[0], pixel_group[1]))
            r2, g2, b2 = rgb_image.getpixel((pixel_group[2], pixel_group[3]))
            r3, g3, b3 = rgb_image.getpixel((pixel_group[4], pixel_group[5]))

            rgb_list = [r1, g1, b1, r2, g2, b2, r3]         # can omit last two as binary character only 7 figures long

            for i in range(0, len(rgb_list)):
                rgb_list[i] = str(bin(rgb_list[i])[-1])

            decoded_binary = ''.join(rgb_list)

            decoded_letter = chr(int(decoded_binary, 2))

            if decoded_letter != '@' and decoded_letter != 'A':
                self.__decoded_message = self.__decoded_message + decoded_letter
            else:
                self.__decoded_message = self.__decoded_message + ' '

        return self.__decoded_message
