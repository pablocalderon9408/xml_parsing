from gettext import find
from xml.dom import minidom

xml_file = 'seatmap1.xml'
xml = minidom.parse(xml_file)

all_information = {}
flight_information = {}
seats_information = {}

# General information about the flight.
flight_information['departure_time'] = xml.getElementsByTagName('ns:FlightSegmentInfo')[0].getAttribute('DepartureDateTime')
flight_information['flight_number'] = xml.getElementsByTagName('ns:FlightSegmentInfo')[0].getAttribute('FlightNumber')
flight_information['departure_airport'] = xml.getElementsByTagName('ns:DepartureAirport')[0].getAttribute('LocationCode')
flight_information['arrival_airpor'] = xml.getElementsByTagName('ns:ArrivalAirport')[0].getAttribute('LocationCode')
flight_information['equipment'] = xml.getElementsByTagName('ns:Equipment')[0].getAttribute('AirEquipType')

# Send general information about the flight to the dictionary.
all_information['flight_information'] = flight_information

# Start parsing the seatmap file.
cabin_class = xml.getElementsByTagName('ns:CabinClass')

# Looping through the cabins (First class and Economy).
cabin_counter = 1
cabin_dict = {}
for cabin in cabin_class:
    cabin_dict[f'cabin_layout {cabin_counter}'] = cabin.getAttribute('Layout')
    row_info = cabin.getElementsByTagName('ns:RowInfo')
    row_dict = {}
    row_counter = 1
    dict_of_seat_detail = {}
    # Loop for rows.
    for row_iterator in row_info:
        row_value = row_iterator.getAttribute('RowNumber')
        seats = row_iterator.getElementsByTagName('ns:SeatInfo')
        # Loop for seats.
        counter_seat_detail = 1
        # dict_of_seat_detail[f'Row {row_counter}'] = row_counter
        for seat_detail in seats:
            # Initialize a seat detail dict.
            seat_detail_dictionary = {}
            seat_detail_dictionary['plane_section'] = seat_detail.getAttribute('PlaneSection')
            for child in seat_detail.childNodes:
                if child.nodeName == 'ns:Summary' :
                    seat_detail_dictionary['seat_number'] = child.getAttribute("SeatNumber")
                    seat_detail_dictionary['availability'] = child.getAttribute("AvailableInd")
                if child.nodeName == 'ns:Features':
                    seat_detail_dictionary['features'] = child.firstChild.data
            # seat_detail_dictionary['seat_number'] = seat_detail.childNodes[1].getAttribute("SeatNumber")
            # seat_detail_dictionary['features'] = seat_detail.childNodes[3].firstChild.data
            # Save information into a general seat dictionary.
            dict_of_seat_detail[f' R{row_value} Seat Details #{counter_seat_detail}'] = seat_detail_dictionary
            counter_seat_detail += 1
        row_counter +=1
    # Save seat_complete_info
    cabin_dict[f'seats info # {cabin_counter}'] = dict_of_seat_detail
    cabin_counter += 1
print('===========================================================================================================')
all_information['seat_complete_info'] = cabin_dict
print(all_information)