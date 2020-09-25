from ast import literal_eval
import regex as re
from crccheck.crc import Crc16, CrcModbus
from crccheck.checksum import Checksum16


#Used for receive frame testing for data frame type 87
eight_seven_string_hex = 'AF FA 02 87 03 FF 03 01 B1 AA 0D 0A'
#Used for receive frame testing for data frame type 87
eight_seven_string_binary = '10101111111110100000001010000111000000111111111100000011' \
                            '0000000110110001101010100000110100001010'
dataframe = []
#print(eight_seven_string_hex_convert)
eight_five_string_hex = 'AF FA 02 85 19 01 04 81 01 19 01 45 00 9A 00 9A ' \
                        '5F B4 02 A0 00 64 00 0A 03 56 00 0A 00 0C CRC 0D 0A'
eight_seven_string_hex2 = 'AF FA 02 87 03 FF 03 01'
def main():
    crc_code_check()
    user_frame = input("Would you like to receive or send frames?: Enter 1 for receive (0x85 and 0x87) or Enter 2 for"
                       " send frames (0x83 or 0x84)\n")
    if user_frame == ('1'):
        recieve_frames()

    elif user_frame == ('2'):
        set_frames()
        print(list_to_str(dataframe))
    else:
        print("I'm sorry, but you did not enter a valid input. Please enter either 1 or 2.")
#bin_to_dec function converts binary values into hexidecmial values

def crc_code_check():
    #Quick calculation
    my_hex_test = eight_seven_string_hex2.replace(" ", "")
    print(my_hex_test)
    data = bytearray.fromhex(my_hex_test)
    crc = Crc16.calc(data)
    print('Crc is ', crc)
    checksum = Checksum16.calc(data)
    print('Checksum is', checksum)
def bin_to_hex(binary_num):
    # Converting binary to initial hexidecimal string
    hex_convert = hex(int(binary_num, 2))
    # removing initial '0x' in string and changing all letters to capital letters for code logic
    hex_convert = hex_convert[2:].upper()
    # Separating the string values into a list by spaces
    hex_list = re.findall('..', hex_convert)
    return hex_list

#hex_to_dec function converts hexidecimal values into decimal values and divides by 10 to get actual value from
# RF generator
def hex_to_dec(hexidecimal):
    #get rid of spaces in string to do correct calculation
    hexidec = hexidecimal.replace(" ","")
    #convert hexidecimal to decimal
    dec_val = int(hexidec, 16)
    #Divide by ten to get actual value
    my_val = dec_val/10
    return my_val

#dec_to_hex function converts decimal values into hexidecimal values and formats value correctly
def dec_to_hex(decimal):
    # Converting decimal to initial hexidecimal string
    hex_convert = hex(int(decimal))
    # removing initial '0x' in string and changing all letters to capital letters for code logic
    hex_convert = hex_convert[2:].upper()
    # Separating the string values into a list by spaces
    hex_list = re.findall('..', hex_convert)
    return hex_list
def list_to_str(datalist):
    datastring = ' '.join([str(elem) for elem in datalist])
    datastring = str(datastring)
    return datastring
#Return/recieve instruction frame is composed of 6 data blaock as shown in Table below.
# All serial instruction or data use hexadecimal(HEX) format, data use高字节先传送（MSB）format.
# For example, when send 0x1234, it will send 0x12 first and then 0x34.
def recieve_frames():
    #Separating the string values into a list by spaces

    recieve_list = eight_seven_string_hex.split(" ")
    #recieve_list = eight_seven_string_hex.split(" ")
    #store the frame header data from the string
    header = recieve_list[0] + " " + recieve_list[1]
    print('Frame header is ', header)
    #store the address information from the string
    address = recieve_list[2]
    print('Address is ', address)
    #store the frame type information from the string
    frame_type = recieve_list[3]
    print('Confirm frame type is ', frame_type)
    #store the data lenght  information from the string
    length = recieve_list[4]
    print('Data length is ', length)

    #Handle frame type 87 (Return Frame) return frame.
    #Return frame is the confirmation signal from the equipment’s upper computer.
    if frame_type == '87':
        #Print frame type
        print("Frame type is 87")
        # store the Default reserve value information from the string
        reserve = recieve_list[5]
        print('Default reserve value is ', reserve)
        # store the 'Control content sent' information from the string
        control_content_sent = recieve_list[6]
        print('Control content sent is ', control_content_sent)
        # store the Instruction execution status information from the string
        instruc_exe = recieve_list[7]
        print('Instruction execution status ', instruc_exe)
        if instruc_exe =='00':
            print('Lower-end system received data and the returned data is abnormal, resend request')
        else:
            print('Lower-end system received the data and instruction executed normally')
        #Append CRC code to the dataframe
        CRC = recieve_list[8] + " " + recieve_list[9]
        #Append Frame end to the dataframe
        frame_end = recieve_list[10] + " " + recieve_list[11]

    # Data frame type 85 is the data frame. The data frame is the equipment’s working data,
    # such as voltage, current, temperature, output power, etc.
    elif frame_type =='85':
        # Print frame type
        print("Frame type is 85")
        # store the corresponding channel value information from the string
        channel = recieve_list[5]
        print('Corresponding channel value is ', channel)
        # store the warning status value information from the string
        warning_status = recieve_list[6] + " " + recieve_list[7]
        print('Warning status is ', warning_status)
        if warning_status =='04 81':
            print('Voltage/standing wave warning')
        else:
            print('No warning')
        # store the working hexidecimal voltage value information from the string
        hex_voltage = recieve_list[8] + " " + recieve_list[9]
        #convert the hexidecimal voltage to decimal and divide by 10 for actual value.
        voltage = hex_to_dec(hex_voltage)
        print('Working voltage value is ', voltage)

        # store the working hexidecimal temperature value information from the string
        hex_temp = recieve_list[10] + " " + recieve_list[11]
        # convert the hexidecimal temperature to decimal and divide by 10 for actual value.
        temp = hex_to_dec(hex_temp)
        print('Working temperature value is ', temp)

        # store the working hexidecimal current value information from the string
        hex_current = recieve_list[12] + " " + recieve_list[13]
        # convert the hexidecimal current to decimal and divide by 10 for actual value.
        current = hex_to_dec(hex_current)
        print('Working current value is ', current)

        # store the RF switch 01 RF status value information from the string
        RF_switch = recieve_list[14] + " " + recieve_list[15]
        print('RF switch number and status ', RF_switch)
        if RF_switch == '00 9A':
            print('RF switch ' + address + ' is on')
        else:
            print('RF switch ' + address + ' is off')

        # store the working hexidecimal frequency value information from the string
        hex_freq = recieve_list[16] + " " + recieve_list[17]
        # convert the hexidecimal frequency to decimal and divide by 10 for actual value.
        frequency = hex_to_dec(hex_freq)
        print('Working frequency value is ', frequency)

        # store the working hexidecimal phase value information from the string
        hex_phase = recieve_list[18] + " " + recieve_list[19]
        # convert the hexidecimal phase to decimal and divide by 10 for actual value.
        phase = hex_to_dec(hex_phase)
        print('Working phase value is ', phase)

        # store the working hexidecimal output power value information from the string
        hex_output_power = recieve_list[20] + " " + recieve_list[21]
        # convert the hexidecimal output power to decimal and get rid of space to do so actual value.
        out_p = hex_output_power.replace(" ", "")
        output_power = int(out_p, 16)
        print('Output power value is ', output_power)

        # store the working hexidecimal reflected power value information from the string
        hex_reflected_power = recieve_list[22] + " " + recieve_list[23]
        # convert the hexidecimal reflected power to to decimal and get rid of space to do so actual value.
        ref_p = hex_reflected_power.replace(" ", "")
        reflected_power = int(ref_p, 16)
        print('Reflected power value is ', reflected_power)

        # store the working hexidecimal standing wave ratio information from the string
        hex_stand_wave = recieve_list[28] + " " + recieve_list[29]
        # convert the hexidecimal standing wave ratio to decimal and divide by 10 for actual value.
        standing_wave_ratio = hex_to_dec(hex_stand_wave)
        print('Standing wave ratio value is ', standing_wave_ratio)


#The instruction send frame is composed of 7 data block as shown in Table 1.
# All serial instruction or data use hexadecimal(HEX) format
def set_frames():
    # Set the value of the send frame header. Always 'A5 5A'
    send_frame_type = input('Which frame type do you want to send: the instruction frame (83) or the request frame (84)?'
                            'Input 83 for instruction frame or 84 for request frame.\n')
    #Set the frame header value, does not change
    send_header = 'A5 5A'
    dataframe.append(send_header)
    print('Frame header value is set to ', send_header)
    # Set the value of the send address
    send_address = input('Which address would you like to set/request data too.?')
    dataframe.append(send_address)
    print('Address to set/request data', send_address)



    # 84 is the request frame. To ensure the successful communication without losing data, this communication protocol
    # uses single communication initialization “This agreement uses unilateral communication”，which means all
    # communication will start from upper-end computer. The request frame includes the request working data and working
    # status from the upper-end computer. The return content can referrer to serial return instruction frame structure.

    if send_frame_type == '84':
        #Print which frame we are in
        print('Data frame type is ', send_frame_type)
        dataframe.append(send_frame_type)
        #Define what control content we want to access. If '0x02', then we want to request channel working status.
        #If '0xFF', we want to read an address.

        send_control = input('Which control type would you like to set/request data too for the 0x84 dataframe?\n'
                             'Enter 02 to request channel working status. Enter FF to request access to an address.\n')
        dataframe.append(send_control)
        send_length = 1
        dataframe.append(send_length)
        #If we want to request channel working status, do the following
        if send_control == '02':
            #Requesting corresponding channel '0x06'. Can be from '0x01 to 0x06'
            send_content = '06'
            dataframe.append(send_content)
            print('Corresponding channel is ', send_content)
        #If we want to request access to a address
        elif send_control == 'FF':
            #Set address you want to read from (0x01-0xFF)
            send_content = '01'
            dataframe.append(send_content)
            print('Corresponding address to request to read from is ', send_content)
        #CRC check code
        CRC = 'B1 AA'
        dataframe.append(CRC)
        frame_end = '0D 0A'
        dataframe.append(frame_end)
    # Instruction send frame is 83. when the user needs to set the power source, this must be 0x83; after sending the
    # control instruction， there is one return confirmation message for lower-end computer.
    elif send_frame_type == '83':
        dataframe.append(send_frame_type)
        send_control = input('Which control type would you like to set/request data too for the 0x83 dataframe?\n'
                             'If you would like to set the working mode, enter 02.\n'
                             'If you would like to turn the power on or off, enter 03.\n'
                             'If you would like to open or close the RF switch, enter 04.\n'
                             'If you want to adjust the power, enter 05.\n'
                             'If you want to change the phase, enter 06.\n'
                             'If you want to turn the warning switch on or off, enter 09\n'
                             'If you want to set the Baud rate setting, enter 0A\n'
                             'If you want to change the address settings, enter 0B\n'
                             'If you want to change the network parameters, enter 0C\n'
                             'If you want to reset the program, enter 0F\n'
                             'If you want to change the working frequency, enter 12\n')
        dataframe.append(send_control)
        #If we want to set the mode to either Frequency or Phase
        if send_control == '02':
            #set the data length
            send_length = '01'
            dataframe.append(send_length)
            #Set the mode
            send_content = input('Set the mode: Enter 00 for Frequency Mode or 01 for Phase mode.')
            if send_content == '00':
                print('Frequency Mode')
                dataframe.append(send_content)
            elif send_content == '01':
                print('Phase mode')
                dataframe.append(send_content)
            else:
                print('Not valid mode. Choose either Frequency Mode (00) or Phase Mode (01)')

        #If we want to turn the power on or off
        elif send_control == '03':
            #set the data length
            send_length = '01'
            dataframe.append(send_length)
            #set the power switch status
            send_content = input('Set the power switch status: Enter 00 to turn the power on or 01 to turn the power off.')
            if send_content == '00':
                print('Power on')
                dataframe.append(send_content)
            elif send_content == '01':
                print('Power off')
                dataframe.append(send_content)
            else:
                print('Not valid power status. Choose either Power on (00) or Phase off (01)')

        #If we want to turn the RF switch on or off
        elif send_control == '04':
            # Set data_length
            send_length = '02'
            dataframe.append(send_length)
            #Control corresponding channel '0x01-0x06'
            send_channel = input('What channel do you want to set the RF switch value (from 0x01-0x06)')
            dataframe.append(send_channel)


            #RF switch status
            send_content = input('Set the RF switch status: Enter 00 to close the RF switch or 01 to open the RF switch.')
            if send_content == '00':
                print('RF close')
                dataframe.append(send_content)
            elif send_content == '01':
                print('Rf open')
                dataframe.append(send_content)
            else:
                print('Not valid RF status. Choose either RF close (00) or RF open (01)')

        #If we want to adjust the power
        elif send_control == '05':

            # Set data_length
            send_length = '03'
            dataframe.append(send_length)
            # Control corresponding channel '0x01-0x06'
            send_channel = input('What channel do you want to set the power value (from 0x01-0x06)')
            dataframe.append(send_channel)
            # Power adjustment value. Step size 1 W. Range: 1-160 W
            power = float(input('Set the power adjustment value. Range of values are 1-160 (W) with step size of 1 W.\n'
                          'For example, entering 100 means 100 Watts.'))
            if (160 >= power >= 1):
                send_content = dec_to_hex(power)
                send_content = ' '.join(map(str, send_content))
                dataframe.append(send_content)
            else:
                print('Error, power input is outside range (1-160).')

        #If we want to adjust the phase of the wave
        elif send_control == '06':
            # Set data_length
            send_length = '03'
            dataframe.append(send_length)
            # Control corresponding channel '0x01-0x06'
            send_channel = input('What channel do you want to set the phase value (from 0x01-0x06)')
            dataframe.append(send_channel)
            # Phase value. Step size 5.6 degrees. Range: 0-360 degrees
            phase = float(input('Set the phase value. Range of values are 0-360 degrees with step size of 5.6 degrees\n'
                          'For example, entering 22.4 means 22.4 degrees'))
            print('Phase is type ', type(phase))
            if (360 >= phase >= 0):
                send_content = dec_to_hex(phase*10)
                send_content = ' '.join(map(str, send_content))
                dataframe.append(send_content)
            else:
                print('Error, power input is outside range (1-160).')

        #If we want to set the warning switch status
        elif send_control == '09':
            # Set data_length
            send_length = '01'
            dataframe.append(send_length)
            # Warning status
            send_content =  input('Set the warning switch status: Enter 00 to turn the warning off or 01 to turn the warning on.')
            if send_content == '00':
                print('Warning off')
                dataframe.append(send_content)
            elif send_content == '01':
                print('Warning on')
                dataframe.append(send_content)
            else:
                print('Not valid warning switch status. Choose either Warning off (00) or Warning on (01)')

        #If we want to set the baud rate
        elif send_control == '0A':
            # Set data_length
            send_length = '01'
            dataframe.append(send_length)
            # Baud rate. Choices: 115200, 57600, 38400, 19200, 9600.
            baud_rate = int(input('Enter the baud rate. 115200, 57600, 38400, 19200, or 9600.'))

            if baud_rate == 115200:
                send_content = '00'
                print('Baud rate is ', baud_rate)
                dataframe.append(send_content)
            elif baud_rate == 57600:
                send_content = '01'
                print('Baud rate is ', baud_rate)
                dataframe.append(send_content)
            elif baud_rate == 38400:
                send_content = '02'
                print('Baud rate is ', baud_rate)
                dataframe.append(send_content)
            elif baud_rate == 19200:
                send_content = '03'
                print('Baud rate is ', baud_rate)
                dataframe.append(send_content)
            elif baud_rate == 9600:
                send_content = '04'
                print('Baud rate is ', baud_rate)
                dataframe.append(send_content)
            else:
                print('Not a valid baud rate. Choose either 115200, 57600, 38400, 19200, or 9600')

        #If we want to change the address settings
        elif send_control == '0B':
            send_length = '01'
            dataframe.append(send_length)
            #Address settings values can be from 0-254
            send_content = input('Enter the address setting change (choose int from 0-254)')
            dataframe.append(send_content)

        #If we want to set the network parameter
        elif send_control == '0C':
            send_length = '12'
            dataframe.append(send_length)
            #Don't think we will need to adjust this. But can be IP, subnet mask, gateway
            send_content = input('Enter IP, subnet mask, gateway')
            dataframe.append(send_content)

        #IF we want to reset the program to it's initial state
        elif send_control == '0F':
            # Set data_length
            send_length = '01'
            dataframe.append(send_length)
            # Reset program?
            send_content = input('If you want to reset the program, enter 01.')
            if send_content == '01':
                print('Program will reset.')
                dataframe.append(send_content)
            else:
                print("Not valid program reset value. Choose '01' if you want to reset the program.")

        #If we want to change the working frequency
        elif send_control == '12':
            # Set data_length
            send_length = '03'
            dataframe.append(send_length)
            # Control corresponding channel '0x01-0x06'
            send_channel = input('What channel do you want to set the frequency value (from 0x01-0x06)')
            dataframe.append(send_channel)
            frequency = float(input('Set the working frequency value. Range of values are 2450 to 2500 MHz with step size of 1 MHz\n'
                'For example, entering 2450.0 means 2450 MHzs'))
            if (2500 >= frequency >= 2450):
                send_content = dec_to_hex(frequency * 10)
                send_content = ' '.join(map(str,send_content))
                dataframe.append(send_content)
            else:
                print('Error, frequency input is outside range (1-160).')
        # CRC check code
        CRC = 'B1 AA'
        dataframe.append(CRC)
        frame_end = '0D 0A'
        dataframe.append(frame_end)
    else:
        print('Invalid instruction frame type. Frame type should be 0x83 or 0x84')

if __name__ == '__main__':
    main()







#For instruction send frame type 0x83.when the user needs to set the power source, this must be 0x83;
# after sending the control instruction， there is one return confirmation message for lower-end computer(下位机)，
# refer to serial return instruction frame structure“Serial port return instruction frame structure”
