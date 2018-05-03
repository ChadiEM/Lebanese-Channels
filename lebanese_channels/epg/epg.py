import datetime
from typing import List
from xml.sax.saxutils import escape

from lebanese_channels.channel import Channel
from lebanese_channels.epg.program_data import ProgramData


def get_epg_channel_declaration(channel: Channel):
    return '<channel id="' + channel.get_route_name() + '"><display-name lang="en">' + channel.get_name() + '</display-name></channel> '


def get_epg_as_xml(channel: Channel):
    epg_data = channel.get_epg_data()
    if epg_data is None:
        return ''
    return __build_response(epg_data, channel.get_route_name())


def __build_response(program_data_list: List[ProgramData], channel_route_name: str):
    response = ''

    for program_data in program_data_list:
        response += '<programme start="' + __date_to_string(program_data.start_time) + '" stop="' + __date_to_string(
            program_data.stop_time) + '" channel="' + channel_route_name + '">'
        response += '<title lang="en">' + program_data.name + '</title>'
        if program_data.desc is not None:
            response += '<desc lang="en">' + escape(program_data.desc) + '</desc>'
        if program_data.category is not None:
            response += '<category lang="en">' + escape(program_data.category) + '</category>'
        if program_data.icon is not None:
            response += '<icon src="' + program_data.icon + '"/>'
        response += '</programme>'

    return response


def __date_to_string(date: datetime):
    return date.strftime("%Y%m%d%H%M00 %z")
