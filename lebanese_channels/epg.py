import concurrent.futures
import datetime
import urllib
import urllib.error
from typing import List
from xml.sax.saxutils import escape

from lebanese_channels import epg_utils
from lebanese_channels import utils
from lebanese_channels.channel import Channel
from lebanese_channels.epg_data import PostURL
from lebanese_channels.program_data import ProgramData


def get_channel(channel_id, channel_name):
    return '<channel id="' + str(channel_id) + '"><display-name lang="en">' + channel_name + '</display-name></channel>'


def get_epg(channel: Channel):
    if channel.epg_data is None or channel.epg_parser is None:
        return ''

    urls = channel.epg_data.get_fetch_urls()

    response = ''
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        futures = {executor.submit(__fetch_epg, channel, url): url for url in urls}
        for future in concurrent.futures.as_completed(futures):
            response += future.result()

    post_url = channel.epg_data.get_post_url()
    if post_url is not None:
        response += __fetch_post_epg(channel, post_url)

    return response


def __fetch_epg(channel: Channel, url: str):
    try:
        html = utils.get_html_response_for(url)
        start_end_data = channel.epg_parser.parse_schedule_page(html)
        epg_utils.normalize_times(start_end_data, channel.epg_data.get_normalization())
        return get_response(start_end_data, channel.channel_id)
    except urllib.error.URLError:
        return ''


def __fetch_post_epg(channel: Channel, post_data: PostURL):
    try:
        html = utils.get_post_html_response_for(post_data)
        start_end_data = channel.epg_parser.parse_schedule_page(html)
        epg_utils.normalize_times(start_end_data, channel.epg_data.get_normalization())
        return get_response(start_end_data, channel.channel_id)
    except urllib.error.URLError:
        return ''


def get_response(program_data_list: List[ProgramData], channel_id: int):
    response = ''

    for program_data in program_data_list:
        response += '<programme start="' + date_to_string(program_data.start_time) + '" stop="' + date_to_string(
            program_data.stop_time) + '" channel="' + str(channel_id) + '">'
        response += '<title lang="en">' + program_data.name + '</title>'
        if program_data.desc is not None:
            response += '<desc lang="en">' + escape(program_data.desc) + '</desc>'
        if program_data.category is not None:
            response += '<category lang="en">' + escape(program_data.category) + '</category>'
        if program_data.icon is not None:
            response += '<icon src="' + program_data.icon + '"/>'
        response += '</programme>'

    return response


def date_to_string(date: datetime):
    return date.strftime("%Y%m%d%H%M00 %z")
