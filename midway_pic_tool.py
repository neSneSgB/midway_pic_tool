#!/usr/bin/env python3

#Atari/Midway/Williams Security PIC Tool
#Original algorithm written by Aaron Giles for MAME's midwayic.c::generate_serial_data, 2007
#Reworked by Pat Daderko (DogP) to a standalone C program, 2022
#Modified and ported to Python by neSneSgB, 2024
import os
import sys
import random
import argparse
from argparse import RawTextHelpFormatter
import shutil

pic_size = 31
pic_data = [0] * 16
serial_digit = [0] * 9
modfile = 0

parser = argparse.ArgumentParser(description='Atari/Midway/Williams Security PIC Tool\n\nNew values modify original file unless -n is specified\n'
                                                                                              'The first 3 digits of the serial (game ID) will not be modified\n'
                                                                                              'Filename only will print PIC information', formatter_class=RawTextHelpFormatter)
parser.add_argument('filename')
parser.add_argument('-s', '--serial', help='New SN (0-999999), "random" to generate a random number')
parser.add_argument('-m', '--month', help='New MM (1-12)', type=int)
parser.add_argument('-d', '--day', help='New DD (0-30)', type=int)
parser.add_argument('-y', '--year', help='New YYYY (1980-2155)', type=int)
parser.add_argument('-n', '--new', help='Create new copy instead of modifying original file', action='store_true')
args = parser.parse_args()
input_pic = args.filename

#make sure file is at least as long as necessary (will read/modify bytes 0-30)
if os.path.getsize(input_pic) < pic_size:
    print ("Error: File size too small.")
    sys.exit(1)


#PIC data is scrambled in flash dump (order looks to be identical for all dumps)
#from disassembly of PIC code, order from flash dump to pic_data array (0-15) is: 6, 14, 3, 8, 0, 12, 7, 9, 11, 1, 15, 4, 2, 10, 5, 13
#need to skip RETLW opcodes (0x08) in file
with open(input_pic, 'r+b') as pic:
    pic.seek(6*2)
    pic_data[0] = pic.read(1)[0]
    pic.seek(14*2)
    pic_data[1] = pic.read(1)[0]
    pic.seek(3*2)
    pic_data[2] = pic.read(1)[0]
    pic.seek(8*2)
    pic_data[3] = pic.read(1)[0]
    pic.seek(0*2)
    pic_data[4] = pic.read(1)[0]
    pic.seek(12*2)
    pic_data[5] = pic.read(1)[0]
    pic.seek(7*2)
    pic_data[6] = pic.read(1)[0]
    pic.seek(9*2)
    pic_data[7] = pic.read(1)[0]
    pic.seek(11*2)
    pic_data[8] = pic.read(1)[0]
    pic.seek(1*2)
    pic_data[9] = pic.read(1)[0]
    pic.seek(15*2)
    pic_data[10] = pic.read(1)[0]
    pic.seek(4*2)
    pic_data[11] = pic.read(1)[0]
    pic.seek(2*2)
    pic_data[12] = pic.read(1)[0]
    pic.seek(10*2)
    pic_data[13] = pic.read(1)[0]
    pic.seek(5*2)
    pic_data[14] = pic.read(1)[0]
    pic.seek(13*2)
    pic_data[15] = pic.read(1)[0]

    #determine original serial number
    temp = ((((pic_data[9] << 16) | (pic_data[8] << 8) | pic_data[7]) - 0x1f3f0) / 0x1bcd) - 5 * pic_data[13]
    serial_digit[1] = int((temp / 100) % 10)
    serial_digit[7] = int((temp / 10) % 10)
    serial_digit[4] = int(temp % 10)

    temp = int(((((pic_data[6] << 24) | (pic_data[5] << 16) | (pic_data[4] << 8) | pic_data[3]) - 0x71e259) / 0x107f) - 2 * pic_data[13] - pic_data[12])
    serial_digit[2] = int((temp / 10000) % 10)
    serial_digit[0] = int((temp / 100) % 10)
    serial_digit[8] = int((temp / 10) % 10)
    serial_digit[6] = int(temp % 10)

    temp = int(((((pic_data[2]<<16)|(pic_data[1]<<8)|pic_data[0])-0x3d74)/0x245)-pic_data[12])
    serial_digit[3] = int((temp / 100) % 10)
    serial_digit[5] = int((temp / 10) % 10)
    serial_gameid = int((serial_digit[0] * 100) + (serial_digit[1] * 10) + serial_digit[2])

    serial_number = int(serial_digit[3] * 100000 + serial_digit[4] * 10000 + serial_digit[5] * 1000 + serial_digit[6] * 100 + serial_digit[7] * 10 + serial_digit[8])

    match serial_gameid:
        case 231:
            gametitle = "Bio F.R.E.A.K.S"
        case 236:
            gametitle = "Off Road Challenge"
        case 310:
            gametitle = "Wayne Gretzky's 3D Hockey"
        case 314:
            gametitle = "Mace: The Dark Age"
        case 315:
            gametitle = "San Francisco Rush"
        case 322:
            gametitle = "Gauntlet Legends"
        case 324:
            gametitle = "Vapor TRX"
        case 328:
            gametitle = "California Speed"
        case 330:
            gametitle = "Tenth Degree"
        case 331:
            gametitle = "San Francisco Rush The Rock: Alcatraz Edition"
        case 336:
            gametitle = "San Francisco Rush 2049"
        case 342:
            gametitle = "Midway Skins Game"
        case 346:
            gametitle = "Gauntlet Dark Legacy"
        case 348:
            gametitle = "San Francisco Rush 2049 Tournament Edition"
        case 352:
            gametitle = "San Francisco Rush 2049 Special Edition"
        case 419:
            gametitle = "Revolution X"
        case 430:
            gametitle = "WWF Wrestlemania"
        case 439:
            gametitle = "Mortal Kombat 3"
        case 444:
            gametitle = "NFL Blitz"
        case 449:
            gametitle = "Cruis'n World"
        case 452:
            gametitle = "War Gods"
        case 459:
            gametitle = "NBA Hangtime"
        case 461:
            gametitle = "Mortal Kombat 4"
        case 463:
            gametitle = "Ultimate Mortal Kombat 3"
        case 465:
            gametitle = "Rampage World Tour"
        case 467:
            gametitle = "NBA Showtime"
        case 468:
            gametitle = "Invasion: The Abductors"
        case 471:
            gametitle = "Hyperdrive"
        case 472:
            gametitle = "Cruis'n Exotica"
        case 481:
            gametitle = "NFL Blitz '99"
        case 486:
            gametitle = "Carnevil"
        case 491:
            gametitle = "The Grid"
        case 494:
            gametitle = "NFL Blitz 2000"
        case 528:
            gametitle = "Development PIC"
        case _:
            gametitle = "Unknown game"
    print (f'Game detected: {gametitle}')
    print(f'Original S/N: {"".join(map(str, serial_digit))}')

    #determine original date
    temp = int(((pic_data[10] << 8) | pic_data[11]))
    year = int((temp / 0x174) + 1980)
    temp -= int(((year - 1980) * 0x174))
    month = int((temp / 0x1f) + 1)
    day = int(temp - ((month - 1) * 0x1f))  #day appears to be 0-30, not 1-31 (as displayed by Rush games at least)
    print(f'Original date: {month}/{day}/{year}')

    if args.serial: #change serial if requested
        modfile = 1
        if args.serial == 'random':
            print ("Random serial requested")
            temp = random.randint(0,999999)
        elif args.serial.isdecimal():
            temp = int(args.serial)
        else: #other string input
            print("Warning: Invalid serial entered\nSerial not modified")
            temp = serial_number
            modfile = 0
        serial_number = temp

    if args.month: #change month if requested
        temp = args.month
        if 1 <= temp <= 12:
            month = temp
            modfile = 1
        else:
            print("Warning: Invalid month entered\nMonth not modified")

    if args.day: #change day if requested
        temp = args.day
        #if temp == 31: #user might have forgotten that the range is 0-30, not 1-31
        #    temp = 30
        if 0 <= temp <= 30:
            day = temp
            modfile = 1
        else:
            print("Warning: Invalid day entered\nDay not modified")

    if args.year: #change year if requested
        temp = args.year
        if 1980 <= temp <= 2155:
            year = temp
            modfile = 1
        else:
            print("Warning: Invalid year entered\nYear not modified")

    if modfile == 1: #if any values changed, update and modify file
        serial_digit[3] = int((serial_number / 100000) % 10)
        serial_digit[4] = int((serial_number / 10000) % 10)
        serial_digit[5] = int((serial_number / 1000) % 10)
        serial_digit[6] = int((serial_number / 100) % 10)
        serial_digit[7] = int((serial_number / 10) % 10)
        serial_digit[8] = int((serial_number / 1) % 10)
        temp = ((serial_digit[4] + serial_digit[7] * 10 + serial_digit[1] * 100) + 5 * pic_data[13]) * 0x1bcd + 0x1f3f0
        pic_data[7] = temp & 0xff
        pic_data[8] = (temp >> 8) & 0xff
        pic_data[9] = (temp >> 16) & 0xff

        temp = ((serial_digit[6] + serial_digit[8] * 10 + serial_digit[0] * 100 + serial_digit[2] * 10000) + 2 * pic_data[13] + pic_data[12]) * 0x107f + 0x71e259
        pic_data[3] = temp & 0xff
        pic_data[4] = (temp >> 8) & 0xff
        pic_data[5] = (temp >> 16) & 0xff
        pic_data[6] = (temp >> 24) & 0xff

        temp = ((serial_digit[5] * 10 + serial_digit[3] * 100) + pic_data[12]) * 0x245 + 0x3d74
        pic_data[0] = temp & 0xff
        pic_data[1] = (temp >> 8) & 0xff
        pic_data[2] = (temp >> 16) & 0xff

        temp = 0x174 * (year - 1980) + 0x1f * (month - 1) + day
        pic_data[10] = (temp >> 8) & 0xff
        pic_data[11] = temp & 0xff

        if args.new: # new file requested
            oldpic = os.path.splitext(input_pic)
            newpic = oldpic[0] + "_" + "".join(map(str, serial_digit)) + "_" + str(month) + "_" + str(day) + "_" + str(year)
            newpic = newpic + oldpic[1]
            picmod = open(newpic, 'x')
            shutil.copyfile(args.filename, newpic)
            pic.close()
            picmod.close()
            pic = open(newpic, 'r+b') # open new pic in place of original
        # put pic_data into file
        pic.seek(6*2)
        pic.write(pic_data[0].to_bytes(1, byteorder='little'))
        pic.seek(14*2)
        pic.write(pic_data[1].to_bytes(1, byteorder='little'))
        pic.seek(3*2)
        pic.write(pic_data[2].to_bytes(1, byteorder='little'))
        pic.seek(8*2)
        pic.write(pic_data[3].to_bytes(1, byteorder='little'))
        pic.seek(0*2)
        pic.write(pic_data[4].to_bytes(1, byteorder='little'))
        pic.seek(12*2)
        pic.write(pic_data[5].to_bytes(1, byteorder='little'))
        pic.seek(7*2)
        pic.write(pic_data[6].to_bytes(1, byteorder='little'))
        pic.seek(9*2)
        pic.write(pic_data[7].to_bytes(1, byteorder='little'))
        pic.seek(11*2)
        pic.write(pic_data[8].to_bytes(1, byteorder='little'))
        pic.seek(1*2)
        pic.write(pic_data[9].to_bytes(1, byteorder='little'))
        pic.seek(15*2)
        pic.write(pic_data[10].to_bytes(1, byteorder='little'))
        pic.seek(4*2)
        pic.write(pic_data[11].to_bytes(1, byteorder='little'))
        pic.seek(2*2)
        pic.write(pic_data[12].to_bytes(1, byteorder='little'))
        pic.seek(10*2)
        pic.write(pic_data[13].to_bytes(1, byteorder='little'))
        pic.seek(5*2)
        pic.write(pic_data[14].to_bytes(1, byteorder='little')) #looks to be unused
        pic.seek(13*2)
        pic.write(pic_data[15].to_bytes(1, byteorder='little')) #looks to be unused

        print(f'New S/N: {"".join(map(str, serial_digit))}')
        print(f'New Date: {month}/{day}/{year}')
        print(f'Saving to {pic.name}')
        pic.close()
        sys.exit(0)
