#!/usr/bin/env python
#
# A library that provides a Python interface to the Telegram Bot API
# Copyright (C) 2015-2018
# Leandro Toledo de Souza <devs@python-telegram-bot.org>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser Public License for more details.
#
# You should have received a copy of the GNU Lesser Public License
# along with this program.  If not, see [http://www.gnu.org/licenses/].
"""This module contains the classes that represent Telegram InlineQueryResultGif."""

from python_telegram_bot_master.telegram import InlineQueryResult


class InlineQueryResultGif(InlineQueryResult):
    """
    Represents a link to an animated GIF file. By default, this animated GIF file will be sent by
    the user with optional caption. Alternatively, you can use :attr:`input_message_content` to
    send a message with the specified content instead of the animation.

    Attributes:
        type (:obj:`str`): 'gif'.
        id (:obj:`str`): Unique identifier for this result, 1-64 bytes.
        gif_url (:obj:`str`): A valid URL for the GIF file. File size must not exceed 1MB.
        gif_width (:obj:`int`): Optional. Width of the GIF.
        gif_height (:obj:`int`): Optional. Height of the GIF.
        gif_duration (:obj:`int`): Optional. Duration of the GIF.
        thumb_url (:obj:`str`): URL of the static thumbnail for the result (jpeg or gif).
        title (:obj:`str`): Optional. Title for the result.
        caption (:obj:`str`): Optional. Caption, 0-1024 characters
        parse_mode (:obj:`str`): Optional. Send Markdown or HTML, if you want Telegram apps to show
            bold, italic, fixed-width text or inline URLs in the media caption. See the constants
            in :class:`telegram.ParseMode` for the available modes.
        reply_markup (:class:`telegram.InlineKeyboardMarkup`): Optional. Inline keyboard attached
            to the message.
        input_message_content (:class:`telegram.InputMessageContent`): Optional. Content of the
            message to be sent instead of the gif.

    Args:
        id (:obj:`str`): Unique identifier for this result, 1-64 bytes.
        gif_url (:obj:`str`): A valid URL for the GIF file. File size must not exceed 1MB.
        gif_width (:obj:`int`, optional): Width of the GIF.
        gif_height (:obj:`int`, optional): Height of the GIF.
        gif_duration (:obj:`int`, optional): Duration of the GIF
        thumb_url (:obj:`str`): URL of the static thumbnail for the result (jpeg or gif).
        title (:obj:`str`, optional): Title for the result.caption (:obj:`str`, optional):
        caption (:obj:`str`, optional): Caption, 0-1024 characters
        parse_mode (:obj:`str`, optional): Send Markdown or HTML, if you want Telegram apps to show
            bold, italic, fixed-width text or inline URLs in the media caption. See the constants
            in :class:`telegram.ParseMode` for the available modes.
        reply_markup (:class:`telegram.InlineKeyboardMarkup`, optional): Inline keyboard attached
            to the message.
        input_message_content (:class:`telegram.InputMessageContent`, optional): Content of the
            message to be sent instead of the gif.
        **kwargs (:obj:`dict`): Arbitrary keyword arguments.

    """

    def __init__(self,
                 id,
                 gif_url,
                 thumb_url,
                 gif_width=None,
                 gif_height=None,
                 title=None,
                 caption=None,
                 reply_markup=None,
                 input_message_content=None,
                 gif_duration=None,
                 parse_mode=None,
                 **kwargs):

        # Required
        super(InlineQueryResultGif, self).__init__('gif', id)
        self.gif_url = gif_url
        self.thumb_url = thumb_url

        # Optionals
        if gif_width:
            self.gif_width = gif_width
        if gif_height:
            self.gif_height = gif_height
        if gif_duration:
            self.gif_duration = gif_duration
        if title:
            self.title = title
        if caption:
            self.caption = caption
        if parse_mode:
            self.parse_mode = parse_mode
        if reply_markup:
            self.reply_markup = reply_markup
        if input_message_content:
            self.input_message_content = input_message_content
