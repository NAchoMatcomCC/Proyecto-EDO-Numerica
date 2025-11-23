# It sounds like you’re having trouble with state handling in Python’s pyTelegramBotAPI (telebot) — especially when using StatesGroup and State in async mode.
# This is a common issue if the state is set but the handler is not triggered.
# Below is a complete, runnable example showing how to correctly use AsyncTeleBot with states, including proper registration of handlers.

# ✅ Working Example: AsyncTeleBot with States
# Pythonimport asyncio
# from telebot.async_telebot import AsyncTeleBot
# from telebot.asyncio_handler_backends import State, StatesGroup
# from telebot.asyncio_storage import StateMemoryStorage
# from telebot import types

# # Create bot with in-memory state storage
# API_TOKEN = "YOUR_BOT_TOKEN"
# bot = AsyncTeleBot(API_TOKEN, state_storage=StateMemoryStorage())

# # Define states
# class QaState(StatesGroup):
#     add_mark = State()
#     all_marks = State()

# # Start command — sets the first state
# @bot.message_handler(commands=['start'])
# async def start_handler(message: types.Message):
#     await bot.set_state(message.from_user.id, QaState.add_mark, message.chat.id)
#     await bot.send_message(message.chat.id, "Please enter a mark:")

# # Handler for add_mark state
# @bot.message_handler(state=QaState.add_mark)
# async def add_mark_handler(message: types.Message):
#     mark = message.text.strip()
#     if not mark.isdigit():
#         await bot.send_message(message.chat.id, "Please enter a valid number.")
#         return
#     await bot.send_message(message.chat.id, f"Mark '{mark}' saved!")
#     # Move to next state
#     await bot.set_state(message.from_user.id, QaState.all_marks, message.chat.id)
#     await bot.send_message(message.chat.id, "Now type 'show' to see all marks.")

# # Handler for all_marks state
# @bot.message_handler(state=QaState.all_marks)
# async def all_marks_handler(message: types.Message):
#     if message.text.lower() == "show":
#         await bot.send_message(message.chat.id, "Here are all your marks (demo).")
#         # End conversation
#         await bot.delete_state(message.from_user.id, message.chat.id)
#     else:
#         await bot.send_message(message.chat.id, "Type 'show' to see marks.")

# # Run bot
# async def main():
#     await bot.polling(non_stop=True)

# if __name__ == "__main__":
#     asyncio.run(main())


# 🔹 Key Points to Avoid State Problems


# Use state_storage
# Without StateMemoryStorage() (or Redis/Mongo storage), states won’t persist.


# Always set state with await bot.set_state(...)
# Pass user_id and chat_id explicitly.


# Register handlers with state=YourState
# If you forget this, the handler won’t trigger.


# Async vs Sync

# Use telebot.async_telebot.AsyncTeleBot for async code.
# Don’t mix sync and async handlers.



# End states when done
# Use await bot.delete_state(user_id, chat_id) to reset.



# If you want, I can also give you a debugging checklist to figure out why your current state handler isn’t firing — that would help pinpoint whether it’s a registration issue or a state storage problem.
# # Do you want me to prepare that debugging checklist?



# #//////////////////////////////////////////////////////////////////////////////////////////////////////////

# import telebot
# from telebot import types
# from telebot.handler_backends import State, StatesGroup
# from telebot.storage import StateMemoryStorage

# # --- BOT SETUP ---
# API_TOKEN = "8028863934:AAFxrMjKDNLJ60CoQ2_dtiLcYdRW0dI6HgQ"
# state_storage = StateMemoryStorage()  # In-memory state storage
# bot = telebot.TeleBot(API_TOKEN, state_storage=state_storage)

# # --- DEFINE STATES ---
# class MyStates(StatesGroup):
#     waiting_for_name = State()
#     waiting_for_age = State()

# # --- START COMMAND ---
# @bot.message_handler(commands=['start'])
# def start(message):
#     markup = types.InlineKeyboardMarkup()
#     markup.add(types.InlineKeyboardButton("Enter Name", callback_data="enter_name"))
#     bot.send_message(message.chat.id, "Choose an option:", reply_markup=markup)

# # --- CALLBACK HANDLER ---
# @bot.callback_query_handler(func=lambda call: call.data == "enter_name")
# def callback_enter_name(call):
#     bot.answer_callback_query(call.id)  # Acknowledge the callback
#     bot.send_message(call.message.chat.id, "Please enter your name:")
#     bot.set_state(call.from_user.id, MyStates.waiting_for_name, call.message.chat.id)

# # --- STATE HANDLER: WAITING FOR NAME ---
# @bot.message_handler(func= lambda msg: MyStates.waiting_for_name.name == bot.get_state(msg.from_user.id, msg.chat.id))
# def process_name(message):
#     name = message.text.strip()
#     if not name.isalpha():
#         bot.send_message(message.chat.id, "Name must contain only letters. Try again:")
#         return
#     bot.send_message(message.chat.id, f"Hi {name}! Now enter your age:")
#     bot.set_state(message.from_user.id, MyStates.waiting_for_age, message.chat.id)

# # --- STATE HANDLER: WAITING FOR AGE ---
# @bot.message_handler(state=MyStates.waiting_for_age)
# def process_age(message):
#     try:
#         age = int(message.text)
#         if age <= 0:
#             raise ValueError
#     except ValueError:
#         bot.send_message(message.chat.id, "Please enter a valid positive number for age:")
#         return

#     bot.send_message(message.chat.id, f"Got it! You are {age} years old.")
#     bot.delete_state(message.from_user.id, message.chat.id)  # End conversation







# # # --- ERROR HANDLING ---
# # @bot.message_handler(func=lambda m: True)
# # def fallback(message):
# #     bot.send_message(message.chat.id, "Please use /start to begin.")







# @bot.message_handler(commands=['stop'])
# def Stop(message):
#     bot.send_message(message.chat.id, 'Adios')
#     bot.stop_bot()

# @bot.message_handler(commands=['ver'])
# def SeeState(message):
#     print(bot.get_state(message.from_user.id, message.chat.id) == MyStates.waiting_for_name.name)
#     print(bot.get_state(message.from_user.id, message.chat.id))

# # --- RUN BOT ---
# if __name__ == "__main__":
#     print("Bot is running...")
#     bot.polling(none_stop=True)


# # How It Works

# # /start sends an inline keyboard with a button.
# # callback_query_handler catches the button press and sets the state to waiting_for_name.
# # The state-specific handler (state=MyStates.waiting_for_name) processes the next message.
# # After getting the name, it moves to waiting_for_age.
# # Once the age is received, the state is cleared.


# # ✅ Key Points

# # bot.set_state(user_id, state, chat_id) sets the conversation state.
# # @bot.message_handler(state=...) filters messages by state.
# # Always call bot.answer_callback_query(call.id) to avoid the “loading” spinner.
# # Use StateMemoryStorage for simple bots; for persistence, use StateRedisStorage or StatePickleStorage.


# # If you want, I can also give you a version that works without Telebot’s built-in state machine, using just a dictionary to track states — which is simpler but more manual.
# # Do you want me to prepare that alternative?




def F(x = 2, y = 5):
    return x + y
