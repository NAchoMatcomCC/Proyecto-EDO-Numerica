# import sys

# import asyncio
# from telebot.async_telebot import AsyncTeleBot, asyncio_filters
# from telebot.asyncio_storage import StateMemoryStorage
# from telebot import types
# from telebot.asyncio_handler_backends import StatesGroup, State

# # Replace with your bot token
# API_TOKEN = "8028863934:AAFxrMjKDNLJ60CoQ2_dtiLcYdRW0dI6HgQ"

# # Create bot with state storage
# state_storage = StateMemoryStorage()
# bot = AsyncTeleBot(API_TOKEN, state_storage=state_storage)

# bot.add_custom_filter(asyncio_filters.StateFilter(bot))


# # Define states
# class MyStates(StatesGroup):
#     waiting_for_name = State()
#     waiting_for_age = State()


# # Start command — enter first state
# @bot.message_handler(commands=['start'])
# async def start(message: types.Message):
#     await bot.set_state(message.from_user.id, MyStates.waiting_for_name, message.chat.id)
#     await bot.send_message(message.chat.id, "Hi! What's your name?")


# # Lambda filter: only handle messages in waiting_for_name state
# @bot.message_handler(state=MyStates.waiting_for_name)
# async def get_name(message: types.Message):
#     # Save name in state context
#     async with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
#         data['name'] = message.text

#     await bot.set_state(message.from_user.id, MyStates.waiting_for_age, message.chat.id)
#     await bot.send_message(message.chat.id, "Got it! Now, how old are you?")


# # Lambda filter: only handle numeric input in waiting_for_age state
# @bot.message_handler(
#     state=MyStates.waiting_for_age,
#     func=lambda m: m.text.isdigit()
# )
# async def get_age(message: types.Message):
#     async with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
#         data['age'] = int(message.text)
#         name = data['name']
#         age = data['age']

#     await bot.send_message(message.chat.id, f"Nice to meet you, {name}! You are {age} years old.")
#     await bot.delete_state(message.from_user.id, message.chat.id)


# # Handle invalid age input
# @bot.message_handler(state=MyStates.waiting_for_age, func=lambda m: not m.text.isdigit())
# async def invalid_age(message: types.Message):
#     await bot.send_message(message.chat.id, "Please enter a valid number for your age.")


# @bot.message_handler(commands=['ver'])
# async def Stop(message):
#     state = await bot.get_state(message.from_user.id, message.chat.id)
#     print(state)

# @bot.message_handler(commands=['stop'])
# async def Stop(message):
#     await bot.send_message(message.chat.id, 'Adios')
#     sys.exit(0)


# # Run bot
# async def main():
#     await bot.polling(non_stop=True)


# if __name__ == "__main__":
#     asyncio.run(main())


class N:
    def __init__(self):
        pass

class A(N):
    def __init__(self):
        pass

c = A()

print(isinstance(c,N))