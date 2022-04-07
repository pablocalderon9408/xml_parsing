from typing import final
from xml.dom import minidom

xml_file = 'seatmap2.xml'
xml = minidom.parse(xml_file)

seats_type_position = {
    'A': 'WINDOW',
    'B': ' ',
    'C': 'AISLE',
    'D': 'AISLE',
    'E': ' ',
    'F': 'WINDOW',
}

shopping_response_id = xml.getElementsByTagName('ResponseID')[0].firstChild.data

prices_dict = {}

a_la_carte_offer = xml.getElementsByTagName('ALaCarteOffer')[0].getAttribute('OfferID')
a_la_carte_offer = xml.getElementsByTagName('ALaCarteOffer')[0].getAttribute('Owner')

a_la_carte_offer_items = xml.getElementsByTagName('ALaCarteOfferItem')

# Loop through the A La Carte Offer Items.
for item in a_la_carte_offer_items:
    offer_item_id = item.getAttribute('OfferItemID')
    # Loop through the A La Carte Offer Items nodes (Eligibility, UnitPrice, Service.)
    for tree in item.childNodes:
        if tree.nodeName != '#text':
            if tree.nodeName == 'Eligibility':
                # Loop through the Eligibility.
                for eligibility in tree.childNodes:
                    if eligibility.nodeName != '#text':
                        segment_ref = eligibility.firstChild.data
            if tree.nodeName == 'UnitPriceDetail':
                # Loop through the UnitPriceDetail.
                for price in tree.childNodes:
                    if price.nodeName != '#text':
                        for currency in price.childNodes:
                            if currency.nodeName != '#text':
                                price_value = currency.firstChild.data
                                price_currency = currency.getAttribute('Code')
            if tree.nodeName == 'Service':
                service_id = tree.getAttribute('ServiceID')
                # Loop through the Service.
                for service in tree.childNodes:
                    if service.nodeName != '#text':
                        service_id = service.firstChild.data


seat_maps = xml.getElementsByTagName('SeatMap')

for seat_map in seat_maps:
    for seg in seat_map.childNodes:
        if seg.nodeName == 'SegmentRef':
            segment_ref = seg.firstChild.data
        if seg.nodeName == 'Cabin':
            for cabin in seg.childNodes:
                if cabin.nodeName == 'CabinLayout':
                    for layout in cabin.childNodes:
                        if layout.nodeName == 'Columns':
                            position = layout.getAttribute('Position')
                            try:
                                type_of_seat = layout.firstChild.data
                            except AttributeError:
                                type_of_seat = "Middle"
                        if layout.nodeName == 'Rows':
                            for row in layout.childNodes:
                                if row.nodeName == 'First':
                                    initial_seat_row = row.firstChild.data
                                if row.nodeName == 'Last':
                                    final_seat_row = row.firstChild.data
                if cabin.nodeName == 'Row':
                    for number in cabin.childNodes:
                        if number.nodeName == 'Seat':
                            seat_definition_ref = []
                            for seat_info in number.childNodes:
                                if seat_info.nodeName == 'Column':
                                    seat_letter = seat_info.firstChild.data
                                if seat_info.nodeName == 'OfferItemRefs':
                                    offer_item_refs = seat_info.firstChild.data
                                if seat_info.nodeName == 'SeatDefinitionRef':
                                    seat_definition_ref.append(seat_info.firstChild.data)
                            import ipdb ; ipdb.set_trace()
                        if number.nodeName == 'Number':
                            pass