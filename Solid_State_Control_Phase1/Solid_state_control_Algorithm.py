from crccheck.checksum import Checksum16
from crccheck.crc import CrcModbus
import regex as re

data_frame = []
# Used to receive frame testing for data frame type eighty-five or eighty-seven.
eight_seven_string_hex = "AF FA 02 87 03 FF 03 01 14 84 0D 0A"
step = 1


def main():
    user_frame = input("Would you like to receive or send frames? Enter 1 for \
        receive (0x85 and 0x87) or 2 for send frames (0x83 or 0x84): \n")
    if user_frame == ("1"):
        receive_frames()
    elif user_frame == ("2"):
        set_frames()
        hex_code = list_to_str(data_frame)
        list_final = convert(hex_code)
        print(list_final)
        for i in list_final:
            i = bytes.fromhex(i)
            print(i)
    else:
        print("Error: Please enter a valid input of either 1 or 2.")


def make_crc(send_data):
    my_hex_data = list_to_str(send_data)
    # Convert hexadecimal string to bytes.
    data = bytearray.fromhex(my_hex_data)
    # Calculate the checksum.
    crc = CrcModbus.calchex(data).upper()
    checksum = Checksum16.calchex(data)
    print("Info: Crc is ", crc)
    print("Info: Checksum is ", checksum)
    # Separate the crc into two sets of two.
    string_check = re.findall("..", crc)
    # Basically, the crc created has to be flipped so that when the crc is
    # received, the remainder is zero. Hence a crc of 'E5 92' calculated above
    # needs to be stored as '92 E5' in the string so that if the crc is
    # calculated again with '92 E5' appended at the end, the crc checksum will
    # equal zero.
    string_check = list(reversed(string_check))
    # Concert the list to string.
    string_check = list_to_str(string_check)
    return string_check


def check_crc(receive_data):
    # Quick calculation using 'len() + list slicing' to remove last K elements.
    K = 2
    # Cut off the end frame hexadecimal values before division.
    no_end_data = receive_data[: len(receive_data) - K]
    print(no_end_data)
    my_hex_data = list_to_str(no_end_data)
    print(my_hex_data)
    data = bytearray.fromhex(my_hex_data)
    crc = CrcModbus.calchex(data).upper()
    print("Info: Crc checksum is ", crc)
    return crc


def bin_to_hex(binary_num):
    # Converting binary to initial hexadecimal string.
    hex_convert = hex(int(binary_num, 2))
    # Removing initial '0x' in string and changing all letters to capital
    # letters for code logic.
    hex_convert = hex_convert[2:].upper()
    # Separating the string values into a list by spaces.
    hex_list = re.findall("..", hex_convert)
    return hex_list


# This function converts hexadecimal values into decimal values and divides by
# ten to get actual value from the RF generator.
def hex_to_dec(hexadecimal):
    # Get rid of spaces in string to do correct calculation.
    hex_dec = hexadecimal.replace(" ", "")
    # Convert hexadecimal to decimal.
    dec_val = int(hex_dec, 16)
    # Divide by ten to get actual value.
    my_val = dec_val / 10
    return my_val


# This function converts decimal values into hexadecimal values and formats
# value correctly.
def dec_to_hex(decimal):
    # Converting decimal to initial hexadecimal string.
    hex_convert = hex(int(decimal))
    print(hex_convert)
    # Removing initial '0x' in string and changing all letters to capital
    # letters for code logic.
    hex_convert = hex_convert[2:].upper()
    print(hex_convert)
    if len(hex_convert) % 2 != 0:
        hex_convert = "0" + hex_convert
    print(hex_convert)
    # Separating the string values into a list by spaces.
    hex_list = re.findall("..", hex_convert)
    return hex_list


def list_to_str(data_list):
    data_string = " ".join([str(elem) for elem in data_list])
    data_string = str(data_string)
    return data_string


# This function handles user input for values with step sizes.
def step_size_calc(step_size, min_num, max_num, val_type, unit):
    user_val = float(input("Set the working %s value. Range of values are %.1f \
        to %.1f MHz with a step size of %.1f %s\n" %(val_type, min_num, max_num,
        step_size, unit)))
    # Divide the value the user inputted by the step size.
    divided_val = user_val / step_size
    # Round the divided value to the nearest whole number.
    rounded_val = round(divided_val)
    # Multiple the rounded value times the step size to get the actual value
    # that will be sent to the generator.
    sent_value = rounded_val * step_size
    if max_num >= sent_value >= min_num:
        authorize_step = input("This function has a step size of %s. The value \
            you entered was %s. The nearest value to the number you inputted \
            is %.1f. Do you want this value sent to the generator? Enter 0 if \
            yes, enter 1 to enter a different value: \n" %(str(step_size),
            str(user_val), sent_value))
        if authorize_step == "0":
            send_content = dec_to_hex(sent_value * 10)
            send_content = " ".join(map(str, send_content))
            data_frame.append(send_content)
        else:
            step_size_calc(step_size, min_num, max_num, val_type, unit)
    else:
        print("Error: %s input is outside range (%.1f-%.1f)." %(val_type,
            min_num,max_num))
        exit()


def convert(string):
    li = list(string.split(" "))
    return li


# Return/receive instruction frame is composed of 6 data block as shown in
# table. All serial instruction or data use hexadecimal(HEX) format, data
# use高字节先传送（MSB）format. For example, when sending '0x1234', it will send
# '0x12' first and then '0x34' second.
def receive_frames():
    # Separating the string values into a list by spaces.
    receive_list = eight_seven_string_hex.split(" ")
    crc_status = check_crc(receive_list)
    if crc_status == "0000":
        print("Info: No errors occurred during data transmission.")
    else:
        print("Error: The crc checksum was not equal to zero.")
    # Store the frame header data from the string.
    header = receive_list[0] + " " + receive_list[1]
    print("Info: Frame header is ", header)
    # Store the address information from the string.
    address = receive_list[2]
    print("Info: Address is ", address)
    # Store the frame type information from the string.
    frame_type = receive_list[3]
    print("Info: Confirm frame type is ", frame_type)
    # Store the data length information from the string.
    length = receive_list[4]
    print("Info: Data length is ", length)
    # Handle frame type eighty-seven return frame. Return frame is the
    # confirmation signal from the equipment’s upper computer.
    if frame_type == "87":
        # Print frame type
        print("Info: Frame type is 87")
        # Store the default reserve value information from the string.
        reserve = receive_list[5]
        print("Info: Default reserve value is ", reserve)
        # Store the 'control content sent' information from the string.
        control_content_sent = receive_list[6]
        print("Info: Control content sent is ", control_content_sent)
        # Store the Instruction execution status information from the string.
        instruction_exe = receive_list[7]
        print("Info: Instruction execution status ", instruction_exe)
        if instruction_exe == "00":
            print("Error: Lower-end system received data and the returned data \
                is abnormal, resend request.")
        else:
            print("Info: Lower-end system received the data and instruction \
                executed normally.")
    # Data frame type eighty-five is the data frame. The data frame is the
    # equipment’s working data, such as voltage, current, temperature, output
    # power, etc.
    elif frame_type == "85":
        # Print frame type.
        print("Info: Frame type is 85")
        # Store the corresponding channel value information from the string.
        channel = receive_list[5]
        print("Info: Corresponding channel value is ", channel)
        # Store the warning status value information from the string.
        warning_status = receive_list[6] + " " + receive_list[7]
        print("Warning: Warning status is ", warning_status)
        if warning_status == "04 81":
            print("Warning: Voltage/Standing Wave")
        # Store the working hexadecimal voltage value information from the
        # string.
        hex_voltage = receive_list[8] + " " + receive_list[9]
        # Convert the hexadecimal voltage to decimal and divide by ten for
        # actual value.
        voltage = hex_to_dec(hex_voltage)
        print("Info: Working voltage value is ", voltage)
        # Store the working hexadecimal temperature value information from the
        # string.
        hex_temp = receive_list[10] + " " + receive_list[11]
        # Convert the hexadecimal temperature to decimal and divide by ten for
        # actual value.
        temp = hex_to_dec(hex_temp)
        print("Info: Working temperature value is ", temp)
        # Store the working hexadecimal current value information from the
        # string.
        hex_current = receive_list[12] + " " + receive_list[13]
        # Convert the hexadecimal current to decimal and divide by ten for
        # actual value.
        current = hex_to_dec(hex_current)
        print("Info: Working current value is ", current)
        # Store the RF switch '01' RF status value information from the string.
        rf_switch = receive_list[14] + " " + receive_list[15]
        print("Info: RF switch number and status ", rf_switch)
        if rf_switch == "00 9A":
            print("Info: RF switch %s is on" %(address))
        else:
            print("Info: RF switch %s is off" %(address))
        # Store the working hexadecimal frequency value information from the
        # string.
        hex_freq = receive_list[16] + " " + receive_list[17]
        # Convert the hexadecimal frequency to decimal and divide by ten for
        # actual value.
        frequency = hex_to_dec(hex_freq)
        print("Info: Working frequency value is ", frequency)
        # Store the working hexadecimal phase value information from the string.
        hex_phase = receive_list[18] + " " + receive_list[19]
        # Convert the hexadecimal phase to decimal and divide by ten for actual
        # value.
        phase = hex_to_dec(hex_phase)
        print("Info: Working phase value is ", phase)
        # Store the working hexadecimal output power value information from the
        # string.
        hex_output_power = receive_list[20] + " " + receive_list[21]
        # Convert the hexadecimal output power to decimal and get rid of space
        # to do so actual value.
        out_p = hex_output_power.replace(" ", "")
        output_power = int(out_p, 16)
        print("Info: Output power value is ", output_power)
        # Store the working hexadecimal reflected power value information from
        # the string.
        hex_reflected_power = receive_list[22] + " " + receive_list[23]
        # Convert the hexadecimal reflected power to to decimal and get rid of
        # space to do so actual value.
        ref_p = hex_reflected_power.replace(" ", "")
        reflected_power = int(ref_p, 16)
        print("Info: Reflected power value is ", reflected_power)
        # Store the working hexadecimal standing wave ratio information from the
        # string.
        hex_stand_wave = receive_list[28] + " " + receive_list[29]
        # Convert the hexadecimal standing wave ratio to decimal and divide by
        # ten for actual value.
        standing_wave_ratio = hex_to_dec(hex_stand_wave)
        print("Info: Standing wave ratio value is ", standing_wave_ratio)


# The instruction send frame is composed of seven data blocks as shown in the
# table. All serial instruction or data use hexadecimal(HEX) format.
def set_frames():
    # Set the value of the send frame header. Always 'A5 5A'.
    send_frame_type = input("Which frame type do you want to send? The \
        instruction frame (83) or the request frame (84)? Input 83 for \
        instruction frame or 84 for request frame: \n")
    # Set the frame header value. Does not change.
    send_header = "A5 5A"
    data_frame.append(send_header)
    print("Info: Frame header value is ", send_header)
    # Set the value of the send address.
    send_address = input("Which address would you like to set/request data \
        too: \n")
    data_frame.append(send_address)
    print("Info: Address to set/request data is ", send_address)
    # Eighty-four is the request frame. To ensure the successful communication
    # without losing data, this communication protocol uses single communication
    # initialization 'This agreement uses unilateral communication'，which means
    # all communication will start from upper-end computer. The request frame
    # includes the request working data and working status from the upper-end
    # computer. The return content can refer to serial return instruction frame
    # structure.
    if send_frame_type == "84":
        # Print which frame we are in.
        print("Info: Data frame type is ", send_frame_type)
        data_frame.append(send_frame_type)
        # Define what control content we want to access. If '0x02', then we want
        # to request channel working status. If '0xFF', we want to read an
        # address.
        send_control = input("Which control type would you like to set/request \
            data too for the '0x84' data frame? Enter (02) to request channel \
            working status. Enter (FF) to request access to an address: \n")
        data_frame.append(send_control)
        send_length = "01"
        data_frame.append(send_length)
        # If we want to request channel working status.
        if send_control == "02":
            # Requesting corresponding channel '0x06'. Can be from '0x01' to
            # '0x06'.
            send_content = input("Input the channel you want the working \
                status of. Values can be in between '01' and '06': \n")
            data_frame.append(send_content)
            print("Info: Corresponding channel is ", send_content)
        # If we want to request access to a address.
        elif send_control == "FF":
            # Set address you want to read from '0x01' to '0xFF'.
            send_content = input("Input the address you want access to. Values \
                can be in between '01' and 'FF'.\n")
            data_frame.append(send_content)
            print("Info: Corresponding address to request to read from is ",
                send_content)
        # Crc check code.
        crc = make_crc(data_frame)
        data_frame.append(crc)
        frame_end = "0D 0A"
        data_frame.append(frame_end)
    # Instruction send frame is eighty-three. When the user needs to set the
    # power source, this must be '0x83'; after sending the control instruction,
    # there is one return confirmation message for lower-end computer.
    elif send_frame_type == "83":
        data_frame.append(send_frame_type)
        send_control = input("Which control type would you like to set/request \
            data too for the '0x83' data frame?\n"
            "If you would like to set the working mode, enter '02'.\n"
            "If you would like to turn the power on or off, enter '03'.\n"
            "If you would like to open or close the RF switch, enter '04'.\n"
            "If you want to adjust the power, enter '05'.\n"
            "If you want to change the phase, enter '06'.\n"
            "If you want to turn the warning switch on or off, enter '09'\n"
            "If you want to set the Baud rate setting, enter '0A'\n"
            "If you want to change the address settings, enter '0B'\n"
            "If you want to change the network parameters, enter '0C'\n"
            "If you want to reset the program, enter '0F'\n"
            "If you want to change the working frequency, enter '12'\n")
        data_frame.append(send_control)
        # If we want to set the mode to either frequency or phase.
        if send_control == "02":
            # Set the data length.
            send_length = "01"
            data_frame.append(send_length)
            # Set the mode.
            send_content = input("Set the mode: Enter '00' for frequency mode \
                or '01' for phase mode: \n")
            if send_content == "00":
                print("Info: Entering frequency mode")
                data_frame.append(send_content)
            elif send_content == "01":
                print("Info: Entering phase mode")
                data_frame.append(send_content)
            else:
                print("Error: Not valid mode. Choose either frequency mode \
                    (00) or phase mode (01)")
        # If we want to turn the power on or off.
        elif send_control == "03":
            # Set the data length.
            send_length = "01"
            data_frame.append(send_length)
            # Set the power switch status.
            send_content = input("Set the power switch status: Enter '00' to \
                turn the power on or '01' to turn the power off: \n")
            if send_content == "00":
                print("Info: Power on")
                data_frame.append(send_content)
            elif send_content == "01":
                print("Info: Power off")
                data_frame.append(send_content)
            else:
                print("Error: Not valid power status. Choose either power on \
                    (00) or power off (01)")
        # If we want to turn the RF switch on or off.
        elif send_control == "04":
            # Set data_length.
            send_length = "02"
            data_frame.append(send_length)
            # Control corresponding channel '0x01-0x06'.
            send_channel = input("What channel do you want to set the RF \
                switch value (from 0x01-0x06): \n")
            data_frame.append(send_channel)
            # RF switch status.
            send_content = input("Set the RF switch status: Enter '00' to \
                close the RF switch or '01' to open the RF switch.")
            if send_content == "00":
                print("Info: RF close")
                data_frame.append(send_content)
            elif send_content == "01":
                print("Info: Rf open")
                data_frame.append(send_content)
            else:
                print("Error: Not valid RF status. Choose either RF close (00) \
                    or RF open (01)")
        # If we want to adjust the power.
        elif send_control == "05":
            # Set data_length.
            send_length = "03"
            data_frame.append(send_length)
            # Control corresponding channel '0x01' to '0x06'
            send_channel = input("What channel do you want to set the power \
                value ('0x01' to '0x06'): \n")
            data_frame.append(send_channel)
            # What are we sending.
            value_sent = "power"
            # Step size of 1W.
            step = 1
            # Step size unit.
            unit = "W"
            # Maximum value.
            max_val = 160
            # Minimum value.
            min_val = 1
            step_size_calc(step, min_val, max_val, value_sent, unit)
        # If we want to adjust the phase of the wave.
        elif send_control == "06":
            # Set data_length.
            send_length = "03"
            data_frame.append(send_length)
            # Control corresponding channel '0x01' to '0x06'.
            send_channel = input("What channel do you want to set the phase \
                value ('0x01' to '0x06')")
            data_frame.append(send_channel)
            # What are we sending.
            value_sent = "phase"
            # Step size of 5.6 degrees.
            step = 5.6
            # Step size unit.
            unit = "degrees"
            # Maximum value.
            max_val = 360
            # Minimum value.
            min_val = 0
            step_size_calc(step, min_val, max_val, value_sent, unit)
        # If we want to set the warning switch status.
        elif send_control == "09":
            # Set data_length.
            send_length = "01"
            data_frame.append(send_length)
            # Warning status.
            send_content =  input("Set the warning switch status: Enter '00' \
                to turn the warning off or '01' to turn the warning on: \n")
            if send_content == "00":
                print("Info: Warning turned off")
                data_frame.append(send_content)
            elif send_content == "01":
                print("Info: Warning turned on")
                data_frame.append(send_content)
            else:
                print("Error: Not valid warning switch status. Choose either \
                    warning off (00) or warning on (01)")
        # If we want to set the baud rate.
        elif send_control == "0A":
            baud_rate_constant_string = "Baud rate is "
            # Set data_length.
            send_length = "01"
            data_frame.append(send_length)
            # Baud rate choices: 115200, 57600, 38400, 19200, 9600.
            baud_rate = int(input("Enter the baud rate('115200', '57600', \
                '38400', '19200', or '9600'): \n"))
            if baud_rate == 115200:
                send_content = "00"
                print(baud_rate_constant_string, baud_rate)
                data_frame.append(send_content)
            elif baud_rate == 57600:
                send_content = "01"
                print(baud_rate_constant_string, baud_rate)
                data_frame.append(send_content)
            elif baud_rate == 38400:
                send_content = "02"
                print(baud_rate_constant_string, baud_rate)
                data_frame.append(send_content)
            elif baud_rate == 19200:
                send_content = "03"
                print(baud_rate_constant_string, baud_rate)
                data_frame.append(send_content)
            elif baud_rate == 9600:
                send_content = "04"
                print(baud_rate_constant_string, baud_rate)
                data_frame.append(send_content)
            else:
                print("Error: Not a valid baud rate. Choose either '115200', \
                    '57600', '38400', '19200', or '9600'")
        # If we want to change the address settings.
        elif send_control == "0B":
            send_length = "01"
            data_frame.append(send_length)
            # Address settings values can be from 0-254
            send_content = input("Enter the address setting change ('0' to \
                '254'): \n")
            data_frame.append(send_content)

        # If we want to set the network parameter.
        elif send_control == "0C":
            send_length = "12"
            data_frame.append(send_length)
            # Do not think we will need to adjust this. But can be IP, subnet
            # mask, gateway.
            send_content = input("Enter IP, subnet mask, gateway: \n")
            data_frame.append(send_content)

        # IF we want to reset the program to it's initial state.
        elif send_control == "0F":
            # Set data_length.
            send_length = "01"
            data_frame.append(send_length)
            # Reset program.
            send_content = input("If you want to reset the program, enter \
                '01': \n")
            if send_content == "01":
                print("Info: Program resetting...")
                data_frame.append(send_content)
            else:
                print("Error: Not valid program reset value. Choose '01' if \
                    you want to reset the program.")
        # If we want to change the working frequency.
        elif send_control == "12":
            # Set data_length.
            send_length = "03"
            data_frame.append(send_length)
            # Control corresponding channel '0x01' to '0x06'.
            send_channel = input("What channel do you want to set the \
                frequency value ('0x01' to '0x06'): \n")
            data_frame.append(send_channel)
            # What are we sending.
            value_sent = "frequency"
            # Step size of 1MHz.
            step = 1
            # Unit of step size.
            unit = "MHz"
            # Maximum value.
            max_val = 2500
            # Minimum value.
            min_val = 2450
            step_size_calc(step, min_val, max_val, value_sent, unit)
        # Crc check code.
        crc = make_crc(data_frame)
        data_frame.append(crc)
        frame_end = "0D 0A"
        data_frame.append(frame_end)
    else:
        print("Error: Invalid instruction frame type. Frame type should be \
            '0x83' or '0x84'")


if __name__ == "__main__":
    main()
