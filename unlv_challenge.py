'''
Collin Gordon
Zappos Coding Challenge
Encrypted Cat - Python
This project is designed to read an encrypted message from the bytes in a *.bmp 
file with an enigma machine by taking the least significant bits from each byte 
and recombining them into new bytes that contain an ASCII table, plans for each 
rotor of the enigma machine, and the encrypted message. This solution does not 
produce a correct answer, but it meets all the checkpoints except the correctly 
encrypted message.
'''


'''
IMPORTS
'''

from bitarray import bitarray
from os       import SEEK_SET


'''
CLASSES
'''


'''
This class represents each rotor of the enigma machine. It is initialized with a static wheel and a scrambled wheel.
The class contains functions that set the wheels as well as code the letter passed to the rotor and step the rotor
appropriately
'''
class Rotor():

    def __init__(self, static = [], scrambled = [], start = -1):

        self.setStat(static)
        self.setScram(scrambled)

        if start != -1:
            self.step(start)

    # sets the static wheel
    def setStat(self, static): 
        self.statwheel = static.copy()

    # sets the scrambled wheel.
    def setScram(self, scrambled):
        self.scramwheel = scrambled.copy()

    # This function codes the character passed to it. If the character is outbound (meaning on its way to the reflector)
    # then the function passes the character through the scrambled wheel. If the character is inbound (meaning it is
    # going to be output), then the character is passed through the static wheel.
    def code(self, char, mode):
        if mode == 'outbound':
            index = self.scramwheel[self.statwheel.index(char)]

        elif mode == 'inbound':
            index = self.statwheel[self.scramwheel.index(char)]

        return index

    # Steps the rotor one position by bringing the last element to the front of the list. If the pos parameter is not
    # the default value, the step function steps until the pos parameter is the first element in the list.
    def step(self, pos = -1):
        
        if pos == -1:
            temp = self.scramwheel.index(self.scramwheel[-1])
        else:
            temp = self.scramwheel.index(pos)

        self.scramwheel = self.scramwheel[temp:] + self.scramwheel[:temp]

'''
MAIN PROGRAM FUNCTIONS
'''

'''
This function reflects the character passed to it based on a configuration of the reflector of an enigma machine. Since
the reflector in the machine is made of 47 pairs of letters it would make sense to group the reflector in tuples.
However, we keep track of the pairs by finding out if the position of the letter on the reflector is odd or even. If the
position is odd, we reflect to the letter before it and if it is even, we reflect to the letter after it.
This function takes the reflector list and the  character being processed as parameters and returns the reflected
character.
'''
def reflect(reflector, char):

    position = reflector.index(char)
    return reflector[position + 1] if position % 2 == 0 else reflector[position - 1]

'''
This function runs the operations of the enigma machine. It processes each
encrypted character one at a time and rotates the rotors to match the 
specification. It takes in the hidden message, all three rotors, the notch 
values, and the reflector and returns the decrypted message.
'''
def enigma(hide, rot1, rot2, rot3, ref, notch1, notch2):
    newMsg = []

    for char in hide:


        if rot2.scramwheel[0] == notch2:
            rot3.step()
        if rot1.scramwheel[0] == notch1:
            rot2.step()

        rot1.step()


        outChar = rot3.code(rot2.code(rot1.code(char, 'outbound'), 'outbound'), 'outbound')
        refChar = reflect(ref, outChar)
        inChar = rot1.code(rot2.code(rot3.code(refChar, 'inbound'), 'inbound'), 'inbound')

        newMsg.append(inChar)

    return newMsg

'''
This function reads bytes from the file and extracts the least significant bit
from each byte and returns a bitarray of least significant bits to the calling
program.
'''
def readFile():
    
    newBits = bitarray() # initializing bitarray of least significant bits
    
    with open('unlv_challenge.bmp', 'rb') as inFile: # opening file

        inFile.seek(54, SEEK_SET) # seeking to the position of the pixel array
        byte = inFile.read(1)     # reading one byte
        
        while byte != b"": # reading bytes until the end of file
            
            bits = bitarray()
            bits.frombytes(byte)
            newBits.append(bits[7])
            byte = inFile.read(1)
                       
    inFile.close()
    return newBits



'''
Main function
'''
def main():
    
    array = bytearray((readFile()).tobytes()) # getting least significant bits

    for i in range(4): # removing the first four bytes that are not 
        del array[0]   # part of the message (per the specification)

    # building the elements of the enigma machine
    # using the specified indices of the array of bytes
    # each rotor, the reflector, and the static wheel are all
    # made from the 94 printable ASCII characters
    # rotor1start, rotor2,start, rotor3start are all the starting positions
    # of the rotors at the time of encryption. Since enigma machines must have
    # the same set up at the time of the encryption and decryption these values
    # allow us to ensure we can get the encrypted message.
    
    staticWheel      = list(array[0 : 94])
    reflector        = list(array[94 : 188])
    rotor1scram      = list(array[188 : 282])
    rotor2scram      = list(array[282 : 376])
    rotor3scram      = list(array[376 : 470])
    firstNotch       = int(array[470])
    secondNotch      = int(array[471])
    rotor1start      = int(array[472])
    rotor2start      = int(array[473])
    rotor3start      = int(array[474])
    hiddenMsg        = list(array[475 : 514])

    #initializing rotors
    rotor1 = Rotor(staticWheel, rotor1scram, rotor1start)
    rotor2 = Rotor(staticWheel, rotor2scram, rotor2start)
    rotor3 = Rotor(staticWheel, rotor3scram, rotor3start)
 
    msg = enigma(hiddenMsg, rotor1, rotor2, rotor3, reflector,
                 firstNotch, secondNotch)

    print(''.join(chr(i) for i in msg)) # displaying message


'''
MAIN PROGRAM EXECUTION
'''

if __name__ == '__main__':
    main()
