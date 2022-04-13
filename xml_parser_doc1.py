from gettext import find
from xml.dom import minidom

xml_file = 'seatmap1.xml'

class FlightInformation:
    """This code is meant to extract the flight information from the xml file."""

    def __init__(self, xml_file=None):
        """Define the xml file to work with."""
        super().__init__()
        self.file = xml_file
        self.all_information = {}

    def get_flight_general_information(self):
        """Get the general information about the flight."""
        xml = minidom.parse(self.file)
        flight_information = {}
        flight_information['departure_time'] = xml.getElementsByTagName('ns:FlightSegmentInfo')[0].getAttribute('DepartureDateTime')
        flight_information['flight_number'] = xml.getElementsByTagName('ns:FlightSegmentInfo')[0].getAttribute('FlightNumber')
        flight_information['departure_airport'] = xml.getElementsByTagName('ns:DepartureAirport')[0].getAttribute('LocationCode')
        flight_information['arrival_airpor'] = xml.getElementsByTagName('ns:ArrivalAirport')[0].getAttribute('LocationCode')
        flight_information['equipment'] = xml.getElementsByTagName('ns:Equipment')[0].getAttribute('AirEquipType')
        return flight_information

    def get_flight_detalied_information(self):
        """Get the flight detalied information."""
        flight_information = self.get_flight_general_information()
        cabin_information = self.get_cabin_seats_information() 
        if flight_information:
            self.all_information['flight_information'] = flight_information
        if cabin_information:
            self.all_information['cabin_information'] = cabin_information
        return self.all_information

    def get_cabin_seats_information(self):
        """"Get the cabin information."""
        xml = minidom.parse(self.file)
        cabin_class = xml.getElementsByTagName('ns:CabinClass')

        # Looping through the cabins (First class and Economy).
        cabin_counter = 1
        all_cabin_information = {}
        cabin_dict = {}
        for cabin in cabin_class:
            cabin_dict[f'cabin_layout {cabin_counter}'] = cabin.getAttribute('Layout')
            row_info = cabin.getElementsByTagName('ns:RowInfo')
            row_counter = 1
            dict_of_seat_detail = {}
            # Loop for rows.
            for row_iterator in row_info:
                row_value = row_iterator.getAttribute('RowNumber')
                seats = row_iterator.getElementsByTagName('ns:SeatInfo')
                # Loop for seats.
                counter_seat_detail = 1
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
                    # Save information into a general seat dictionary.
                    dict_of_seat_detail[f' R{row_value} Seat Details #{counter_seat_detail}'] = seat_detail_dictionary
                    counter_seat_detail += 1
                row_counter +=1
            # Save seat_complete_info
            cabin_dict[f'seats info # {cabin_counter}'] = dict_of_seat_detail
            cabin_counter += 1
        all_cabin_information['seat_complete_info'] = cabin_dict
        return all_cabin_information

trial = FlightInformation(xml_file)
trial.get_flight_detalied_information()