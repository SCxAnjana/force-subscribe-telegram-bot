import time
import logging
from Config import Config
from pyrogram import Client, filters
from sql_helpers import forceSubscribe_sql as sql
from pyrogram.types import ChatPermissions, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors.exceptions.bad_request_400 import UserNotParticipant, UsernameNotOccupied, ChatAdminRequired, PeerIdInvalid

logging.basicConfig(level=logging.INFO)

static_data_filter = filters.create(lambda _, __, query: query.data == "onUnMuteRequest")
@Client.on_callback_query(static_data_filter)
def _onUnMuteRequest(client, cb):
  user_id = cb.from_user.id
  chat_id = cb.message.chat.id
  chat_db = sql.fs_settings(chat_id)
  if chat_db:
    channel = chat_db.channel
    chat_member = client.get_chat_member(chat_id, user_id)
    if chat_member.restricted_by:
      if chat_member.restricted_by.id == (client.get_me()).id:
          try:
            client.get_chat_member(channel, user_id)
            client.unban_chat_member(chat_id, user_id)
            if cb.message.reply_to_message.from_user.id == user_id:
              cb.message.delete()
          except UserNotParticipant:
            client.answer_callback_query(cb.id, text="❗ අපේ Youtube Updates Channel එක Join වී 'UnMute Me' බටනය Click කරන්න 😕.❗ 𝗝𝗼𝗶𝗻 𝘁𝗵𝗲 𝗺𝗲𝗻𝘁𝗶𝗼𝗻𝗲𝗱 '𝗰𝗵𝗮𝗻𝗻𝗲𝗹' 𝗮𝗻𝗱 𝗽𝗿𝗲𝘀𝘀 𝘁𝗵𝗲 '𝗨𝗻𝗠𝘂𝘁𝗲 𝗠𝗲' 𝗯𝘂𝘁𝘁𝗼𝗻 𝗮𝗴𝗮𝗶𝗻.😕", show_alert=True)
      else:
        client.answer_callback_query(cb.id, text="❗ වෙනත් හේතුවක් මත Admin වරයකු විසින් Mute කර ඇත 🙁.❗ 𝗬𝗼𝘂 𝗮𝗿𝗲 𝗺𝘂𝘁𝗲𝗱 𝗯𝘆 𝗮𝗱𝗺𝗶𝗻𝘀 𝗳𝗼𝗿 𝗼𝘁𝗵𝗲𝗿 𝗿𝗲𝗮𝘀𝗼𝗻𝘀 🙁. ❗", show_alert=True)
    else:
      if not client.get_chat_member(chat_id, (client.get_me()).id).status == 'administrator':
        client.send_message(chat_id, f"❗ **{cb.from_user.mention} is trying to UnMute himself but i can't unmute him because i am not an admin in this chat add me as admin again.**\n__#Leaving this chat...__")
        client.leave_chat(chat_id)
      else:
        client.answer_callback_query(cb.id, text="❗ සමූහය තුල මැසේජ් දැමිය හැකිනම් මෙය Click කිරීමෙන් වළකින්න 🙄. ❗ 𝗪𝗮𝗿𝗻𝗶𝗻𝗴: 𝗗𝗼𝗻'𝘁 𝗰𝗹𝗶𝗰𝗸 𝘁𝗵𝗲 𝗯𝘂𝘁𝘁𝗼𝗻 𝗶𝗳 𝘆𝗼𝘂 𝗰𝗮𝗻 𝘀𝗽𝗲𝗮𝗸 𝗳𝗿𝗲𝗲𝗹𝘆 🙄.", show_alert=True)



@Client.on_message(filters.text & ~filters.private & ~filters.edited, group=1)
def _check_member(client, message):
  chat_id = message.chat.id
  chat_db = sql.fs_settings(chat_id)
  if chat_db:
    user_id = message.from_user.id
    if not client.get_chat_member(chat_id, user_id).status in ("administrator", "creator") and not user_id in Config.SUDO_USERS:
      channel = chat_db.channel
      try:
        client.get_chat_member(channel, user_id)
      except UserNotParticipant:
        try:
          buttons = [[
              InlineKeyboardButton('𝗝𝗼𝗶𝗻 𝗡𝗼𝘄 📛', url=f"https://t.me/{channel}")
          ],[
              InlineKeyboardButton('𝗨𝗻𝗠𝘂𝘁𝗲 𝗠𝗲 ✅', callback_data='onUnMuteRequest')
          ]]
          reply_markup = InlineKeyboardMarkup(buttons)
          sent_message = client.send_photo(
              message.chat.id,
              'pic.jpg',
              caption=f"{message.from_user.mention} ඔයා තාම අපේ Youtube Updates Channel එකට Join වෙලා නැහැනේ 😕 Please ඒකට Join වෙලා. පහල Unmute Button එක දෙන්න..🤗 \nඑතකොට ඔයාට ලේසියෙන්ම අපේ Group එකෙන් Fims & Tv Series ලබාගන්න පුලුවන් වේවී😊👍,😕 𝘆𝗼𝘂 𝗮𝗿𝗲 𝗻𝗼𝘁 𝘀𝘂𝗯𝘀𝗰𝗿𝗶𝗯𝗲𝗱 𝘁𝗼 𝗺𝘆 𝗰𝗵𝗮𝗻𝗻𝗲𝗹 𝘆𝗲𝘁. 𝗣𝗹𝗲𝗮𝘀𝗲 𝗷𝗼𝗶𝗻 𝗮𝗻𝗱 𝗽𝗿𝗲𝘀𝘀 𝘁𝗵𝗲 𝗯𝘂𝘁𝘁𝗼𝗻 𝗯𝗲𝗹𝗼𝘄 𝘁𝗼 𝘂𝗻𝗺𝘂𝘁𝗲 𝘆𝗼𝘂𝗿𝘀𝗲𝗹𝗳 😊.",
              reply_to_message_id=message.message_id,
              reply_markup=reply_markup
          )
          client.restrict_chat_member(chat_id, user_id, ChatPermissions(can_send_messages=False))
        except ChatAdminRequired:
          sent_message.edit("❗ **I am not an admin here.**\n__Make me admin with ban user permission and add me again.\n#Leaving this chat...__")
          client.leave_chat(chat_id)
      except ChatAdminRequired:
        client.send_message(chat_id, text=f"❗ **I am not an admin in @{channel}**\n__Make me admin in the channel and add me again.\n#Leaving this chat...__")
        client.leave_chat(chat_id)


@Client.on_message(filters.command(["forcesubscribe", "fsub"]) & ~filters.private)
def config(client, message):
  user = client.get_chat_member(message.chat.id, message.from_user.id)
  if user.status is "creator" or user.user.id in Config.SUDO_USERS:
    chat_id = message.chat.id
    if len(message.command) > 1:
      input_str = message.command[1]
      input_str = input_str.replace("@", "")
      if input_str.lower() in ("off", "no", "disable"):
        sql.disapprove(chat_id)
        message.reply_text("❌ **Force Subscribe is Disabled Successfully.**")
      elif input_str.lower() in ('clear'):
        sent_message = message.reply_text('**Unmuting all members who are muted by me...**')
        try:
          for chat_member in client.get_chat_members(message.chat.id, filter="restricted"):
            if chat_member.restricted_by.id == (client.get_me()).id:
                client.unban_chat_member(chat_id, chat_member.user.id)
                time.sleep(1)
          sent_message.edit('✅ **UnMuted all members who are muted by me.**')
        except ChatAdminRequired:
          sent_message.edit('❗ **I am not an admin in this chat.**\n__I can\'t unmute members because i am not an admin in this chat make me admin with ban user permission.__')
      else:
        try:
          client.get_chat_member(input_str, "me")
          sql.add_channel(chat_id, input_str)
          message.reply_text(f"✅ **Force Subscribe is Enabled**\n__Force Subscribe is enabled, all the group members have to subscribe this [channel](https://t.me/{input_str}) in order to send messages in this group.__", disable_web_page_preview=True)
        except UserNotParticipant:
          message.reply_text(f"❗ **Not an Admin in the Channel**\n__I am not an admin in the [channel](https://t.me/{input_str}). Add me as a admin in order to enable ForceSubscribe.__", disable_web_page_preview=True)
        except (UsernameNotOccupied, PeerIdInvalid):
          message.reply_text(f"❗ **Invalid Channel Username.**")
        except Exception as err:
          message.reply_text(f"❗ **ERROR:** ```{err}```")
    else:
      if sql.fs_settings(chat_id):
        message.reply_text(f"✅ **Force Subscribe is enabled in this chat.**\n__For this [Channel](https://t.me/{sql.fs_settings(chat_id).channel})__", disable_web_page_preview=True)
      else:
        message.reply_text("❌ **Force Subscribe is disabled in this chat.**")
  else:
      message.reply_text("❗ **Group Creator Required**\n__You have to be the group creator to do that.__")
