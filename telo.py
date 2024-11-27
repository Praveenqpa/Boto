from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackContext, ConversationHandler, filters
from termcolor import colored

# Define states for the conversation
NOZZLE1, NOZZLE2, NOZZLE3, NOZZLE4, NOZZLE1_SECOND, NOZZLE2_SECOND, NOZZLE3_SECOND, NOZZLE4_SECOND, G_PAY = range(9)

# Replace 'YOUR_BOT_TOKEN' with the token you got from BotFather
TOKEN = '7785472365:AAEFdqwO_PxOtrV2ja0Jnr09ZW1ZyF0f6Bs'

# Start command handler
async def start(update: Update, context: CallbackContext):
    await update.message.reply_text("Welcome to Praveen Calculator!\nType /calculate to start the calculation.")

# Function to start the calculation
async def calculate(update: Update, context: CallbackContext):
    await update.message.reply_text("Enter the reading values for \nNozzle 1, 2, 3, 4:")
    return NOZZLE1  # Move to the first state (NOZZLE1)

# Function to handle Nozzle 1 input
async def nozzle1(update: Update, context: CallbackContext):
    context.user_data['a'] = float(update.message.text)
    await update.message.reply_text("Nozzle 2: ")
    return NOZZLE2  # Move to the next state (NOZZLE2)

# Function to handle Nozzle 2 input
async def nozzle2(update: Update, context: CallbackContext):
    context.user_data['b'] = float(update.message.text)
    await update.message.reply_text("Nozzle 3: ")
    return NOZZLE3  # Move to the next state (NOZZLE3)

# Function to handle Nozzle 3 input
async def nozzle3(update: Update, context: CallbackContext):
    context.user_data['c'] = float(update.message.text)
    await update.message.reply_text("Nozzle 4: ")
    return NOZZLE4  # Move to the next state (NOZZLE4)

# Function to handle Nozzle 4 input
async def nozzle4(update: Update, context: CallbackContext):
    context.user_data['d'] = float(update.message.text)
    await update.message.reply_text("Enter the second set of readings for \nNozzle 1, 2, 3, 4:")
    return NOZZLE1_SECOND  # Move to the next state (NOZZLE1_SECOND)

# Function to handle second Nozzle 1 input
async def nozzle1_second(update: Update, context: CallbackContext):
    context.user_data['e'] = float(update.message.text)
    await update.message.reply_text("Nozzle 2: ")
    return NOZZLE2_SECOND  # Move to the next state (NOZZLE2_SECOND)

# Function to handle second Nozzle 2 input
async def nozzle2_second(update: Update, context: CallbackContext):
    context.user_data['f'] = float(update.message.text)
    await update.message.reply_text("Nozzle 3: ")
    return NOZZLE3_SECOND  # Move to the next state (NOZZLE3_SECOND)

# Function to handle second Nozzle 3 input
async def nozzle3_second(update: Update, context: CallbackContext):
    context.user_data['g'] = float(update.message.text)
    await update.message.reply_text("Nozzle 4: ")
    return NOZZLE4_SECOND  # Move to the next state (NOZZLE4_SECOND)

# Function to handle second Nozzle 4 input
async def nozzle4_second(update: Update, context: CallbackContext):
    context.user_data['h'] = float(update.message.text)
    await update.message.reply_text("Enter All Amounts for Gpay : ")
    return G_PAY  # Move to the next state (G_PAY)

# Function to handle Gpay amounts input
async def gpay(update: Update, context: CallbackContext):
    gpay_amounts = list(map(float, update.message.text.split()))
    context.user_data['gpay'] = sum(gpay_amounts)
    a, b, c, d = context.user_data['a'], context.user_data['b'], context.user_data['c'], context.user_data['d']
    e, f, g, h = context.user_data['e'], context.user_data['f'], context.user_data['g'], context.user_data['h']
    
    # Perform the calculations
    i = a - e
    j = b - f
    k = c - g
    l = d - h
    de = i + j
    pe = k + l
    so = de * 94.87
    po = pe * 103.74
    go = so + po

    # Display results to the user
    result = (
        f"Nozzle 1 Litre is {i}\n"
        f"Nozzle 2 Litre is {j}\n"
        f"Nozzle 3 Litre is {k}\n"
        f"Nozzle 4 Litre is {l}\n"
        f"Total Diesel Litre is {de}\n"
        f"Total Petrol Litre is {pe}\n"
        f"Total Amount Diesel is {so}\n"
        f"Total Amount Petrol is {po}\n"
        f"Total Amount is {go}"
    )

    # Calculate the balance
    total_gpay = context.user_data['gpay']
    top = total_gpay - go
    if total_gpay > go:
        result += f"\nExcess = {top}"
    elif total_gpay < go:
        result += f"\nLoss = {top}"
    elif total_gpay == go:
        result += f"\nTally"
    
    await update.message.reply_text(result)
    return ConversationHandler.END  # End the conversation

# Function to cancel the conversation
async def cancel(update: Update, context: CallbackContext):
    await update.message.reply_text("Calculation cancelled.")
    return ConversationHandler.END

def main():
    # Create the Application and pass the bot's token
    application = Application.builder().token(TOKEN).build()

    # Define the conversation handler
    conversation_handler = ConversationHandler(
        entry_points=[CommandHandler('calculate', calculate)],
        states={
            NOZZLE1: [MessageHandler(filters.TEXT & ~filters.COMMAND, nozzle1)],
            NOZZLE2: [MessageHandler(filters.TEXT & ~filters.COMMAND, nozzle2)],
            NOZZLE3: [MessageHandler(filters.TEXT & ~filters.COMMAND, nozzle3)],
            NOZZLE4: [MessageHandler(filters.TEXT & ~filters.COMMAND, nozzle4)],
            NOZZLE1_SECOND: [MessageHandler(filters.TEXT & ~filters.COMMAND, nozzle1_second)],
            NOZZLE2_SECOND: [MessageHandler(filters.TEXT & ~filters.COMMAND, nozzle2_second)],
            NOZZLE3_SECOND: [MessageHandler(filters.TEXT & ~filters.COMMAND, nozzle3_second)],
            NOZZLE4_SECOND: [MessageHandler(filters.TEXT & ~filters.COMMAND, nozzle4_second)],
            G_PAY: [MessageHandler(filters.TEXT & ~filters.COMMAND, gpay)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    # Register handlers
    application.add_handler(conversation_handler)

    # Start polling for updates
    application.run_polling()

if __name__ == "__main__":
    main()