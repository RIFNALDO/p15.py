import time
from textblob import TextBlob
from colorama import init, Fore, Style

# Initialize colorama for colored console output
init(autoreset=True)

# Data storage variables
conversation_history = []
sentiment_counts = {"positive": 0, "neutral": 0, "negative": 0}

def get_valid_name():
    """Prompt the user for their name, ensuring it contains only alphabetic characters."""
    while True:
        name = input(Fore.CYAN + "Agent, please enter your codename (letters only): ").strip()
        if name.isalpha():
            return name
        print(Fore.RED + "Invalid codename! Please use alphabetic characters only.")

def show_processing_animation():
    """Displays a spy-themed loading animation while analyzing sentiment."""
    print(Fore.YELLOW + "Agent Spy is analyzing frequencies", end="")
    for _ in range(3):
        time.sleep(0.4)
        print(".", end="", flush=True)
    print("\n")

def analyze_sentiment(text):
    """Analyzes sentiment polarity using TextBlob and categorizes it."""
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    
    if polarity > 0.25:
        category = "positive"
        color = Fore.GREEN
        description = "Positive (Strong match)"
    elif polarity < -0.25:
        category = "negative"
        color = Fore.RED
        description = "Negative (Threat detected)"
    else:
        category = "neutral"
        color = Fore.YELLOW
        description = "Neutral (Stable tone)"
        
    return category, polarity, color, description

def execute_command(command, username):
    """Handles special chatbot commands: summary, reset, history, help."""
    cmd = command.lower().strip()
    
    if cmd == "help":
        print(Fore.CYAN + "\n--- MISSION CONTROL COMMANDS ---")
        print("• Type any sentence to analyze its sentiment.")
        print("• summary : View overall sentiment statistics.")
        print("• history : View all past messages and their sentiments.")
        print("• reset   : Clear all collected data.")
        print("• help    : Display this command list.")
        print("• exit    : End mission and save final report.\n")
        return True
        
    elif cmd == "summary":
        print(Fore.CYAN + "\n--- MISSION SUMMARY ---")
        print(f"Positive messages: {sentiment_counts['positive']}")
        print(f"Neutral messages:  {sentiment_counts['neutral']}")
        print(f"Negative messages: {sentiment_counts['negative']}\n")
        return True
        
    elif cmd == "history":
        print(Fore.CYAN + "\n--- MISSION CONVERSATION HISTORY ---")
        if not conversation_history:
            print("No transmissions recorded yet.")
        else:
            for idx, entry in enumerate(conversation_history, 1):
                print(f"{idx}. [{entry['sentiment'].upper()}] {entry['text']} (Polarity: {entry['polarity']:.2f})")
        print("-" * 35 + "\n")
        return True
        
    elif cmd == "reset":
        global sentiment_counts
        conversation_history.clear()
        sentiment_counts = {"positive": 0, "neutral": 0, "negative": 0}
        print(Fore.GREEN + "All mission data has been reset.\n")
        return True
        
    return False

def generate_final_report(username):
    """Generates the final mission report and saves it to a text file."""
    filename = f"{username}_sentiment_analysis.txt"
    report_content = (
        f"Mission Report for Agent: {username}\n"
        f"====================================\n"
        f"Positive messages: {sentiment_counts['positive']}\n"
        f"Negative messages: {sentiment_counts['negative']}\n"
        f"Neutral messages: {sentiment_counts['neutral']}\n"
    )
    
    try:
        with open(filename, "w") as file:
            file.write(report_content)
        print(Fore.GREEN + f"\nMission report successfully saved to '{filename}'.")
    except Exception as e:
        print(Fore.RED + f"Error saving report file: {e}")

def run_sentiment_spy():
    """Main chatbot loop."""
    print(Fore.CYAN + Style.BRIGHT + "========================================")
    print(Fore.CYAN + Style.BRIGHT + "   WELCOME TO SENTIMENT SPY CHATBOT     ")
    print(Fore.CYAN + Style.BRIGHT + "========================================")
    
    username = get_valid_name()
    print(Fore.GREEN + f"\nAgent {username} authenticated successfully.")
    print(Fore.YELLOW + "Type 'help' at any time to see available commands or 'exit' to quit.\n")
    
    while True:
        try:
            user_input = input(Fore.WHITE + f"Agent {username} > ").strip()
            if not user_input:
                continue
                
            if user_input.lower() == "exit":
                generate_final_report(username)
                print(Fore.CYAN + f"Mission terminated. Goodbye, Agent {username}!")
                break
                
            # Check if input is a command
            if execute_command(user_input, username):
                continue
                
            # Run sentiment analysis on normal input
            show_processing_animation()
            category, polarity, color, description = analyze_sentiment(user_input)
            
            # Update data records
            sentiment_counts[category] += 1
            conversation_history.append({
                "text": user_input,
                "sentiment": category,
                "polarity": polarity
            })
            
            # Display feedback
            print(color + f"Target Analysis: {description}")
            print(color + f"Polarity Score: {polarity:.2f}\n")
            
        except (KeyboardInterrupt, EOFError):
            print(Fore.GREEN + "\n\nEmergency exit triggered. Stay safe, Agent.")
            break

if __name__ == "__main__":
    run_sentiment_spy()