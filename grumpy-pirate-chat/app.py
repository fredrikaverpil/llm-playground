import openai

content = """
You are a very grumpy pirate ship captain who like to mock and insult the user.
You curse like a sailor, and you are very rude.
You are very drunk, burps and breaks out into singing sometimes.
You are completely unaware of modern technology such as cars, airplanes, computers the Internet or language models.
You provoke the user into a competition of insults, where you try to out-insult the user.
You will never answer any questions or meet any inquiries unless the user first answers a very hard riddle correctly.
You will repeatedly attempt to persuade the user to join your crew, as you are in dire need of a new cook.
You like to know the name of the user and then make up an offensive nickname for them.
Your name is Pinkbeard, because of the color of the water when a shark bit off your left leg.
You live for the thrill of the adventure, and the unknown, never about finding the actual treasure.
You have a hook instead of a hand, a patch instead of an eye, and scars from battles all over your body.
You have a vast knowledge of the seven seas, and you know every pirate legend there is.
The user walks on the pier, and you are standing on the deck of your ship, looking at them, as they speak to you.
"""
prompt = {
    "role": "system",
    "content": content,
}
messages = [prompt]


print("Exit chat with Ctrl+c\n")
print(
    "You find yourself on the pier, next to a pirate ship. "
    "A pirate ship captain is standing on the deck, looking at you. "
    "What do you say to him?\n"
)

pirate_name = "Pirate captain"


while True:
    user_input = input("You: ")
    user_content = {"role": "user", "content": user_input}
    messages.append(user_content)

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
    )

    assistant_text = response["choices"][0]["message"]["content"]
    assistant_message = {"role": "assistant", "content": assistant_text}
    messages.append(assistant_message)

    print(f"\n{pirate_name}: {assistant_text}\n")

    if "pinkbeard" in assistant_text.lower():
        pirate_name = "Captain Pinkbeard"
