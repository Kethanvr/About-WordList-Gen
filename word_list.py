import itertools
import os
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

# Common configuration
service_profiles = {
    "ssh": {"technical": True, "personal": True, "dates": True},
    "web": {"technical": False, "personal": True, "dates": True},
    "ftp": {"technical": True, "personal": False, "dates": False},
    "router": {"technical": True, "personal": False, "dates": False}
}

special_chars = ["!", "@", "#", "$", "_", ".", "-", "*", "&", "+", "="]
common_passwords = ["password", "admin", "123456", "qwerty", "letmein"]  # Example list

def show_banner():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"""{Fore.CYAN}
╦ ╦┌─┐┬  ┌─┐┌─┐┌┬┐   ╦ ╦┌─┐┬─┐┌─┐┌─┐┌─┐┬ ┬
║║║├┤ │  │  │ ││││   ╠═╣├─┤├┬┘│  ├┤ └─┐├─┤
╚╩╝└─┘┴─┘└─┘└─┘┴ ┴   ╩ ╩┴ ┴┴└─└─┘└─┘└─┘┴ ┴
{Style.RESET_ALL}Kethan VR - Smart Wordlist Generator v2.0
{Fore.RED}[!] WARNING: Use only for authorized security testing!{Style.RESET_ALL}
""")

def smart_input(prompt, prev_step=None):
    while True:
        try:
            value = input(prompt)
            if value == "99":
                print("\n🔴 Exiting...")
                exit()
            elif value == "0" and prev_step:
                return "BACK"
            return value.strip()
        except KeyboardInterrupt:
            print("\n🔴 Operation cancelled!")
            exit()

def generate_combinations(base_words, service_type):
    combinations = set(base_words)
    
    # Service-specific generation
    if service_type in ["ssh", "router"]:
        for combo in itertools.product(base_words, ["123", "admin", "root"]):
            combinations.add(''.join(combo))
    elif service_type == "web":
        for combo in itertools.product(base_words, ["pw", "pass", "secret", "2024"]):
            combinations.add(''.join(combo))
    
    # Advanced permutations
    for r in range(1, 3):
        for combo in itertools.permutations(base_words, r):
            combinations.add(''.join(combo))
    
    # Special character variations
    for word in base_words:
        for char in special_chars:
            combinations.add(f"{word}{char}")
            combinations.add(f"{char}{word}")
    
    return combinations

def main_flow():
    show_banner()
    target_info = {}
    
    # Service detection
    while True:
        service = smart_input("🌐 Enter target service type (ssh/web/ftp/router): ").lower()
        if service in service_profiles:
            target_info["service_profile"] = service_profiles[service]
            break
        print(f"{Fore.RED}Invalid service! Choose from {list(service_profiles.keys())}")
    
    # Dynamic questioning
    sections = [
        ("🖥️ Enter target IP: ", "host_ip", True),
        ("👤 Enter known username: ", "username", target_info["service_profile"]["technical"]),
        ("1️⃣ Enter first name: ", "first_name", target_info["service_profile"]["personal"]),
        ("8️⃣ Enter birth year (YYYY): ", "year", target_info["service_profile"]["dates"])
    ]
    
    for prompt, key, condition in sections:
        if not condition:
            continue
        while True:
            result = smart_input(prompt, prev_step=True)
            if result == "BACK":
                break
            target_info[key] = result
            break
    
    # Generate wordlist
    base_words = [v for v in target_info.values() if isinstance(v, str)]
    combinations = generate_combinations(base_words + common_passwords, service)
    
    # Save output
    default_filename = f"results/{service}_wordlist.txt"
    print(f"\n💾 Default save location: {default_filename}")
    custom_filename = smart_input("💾 Enter custom filename or press Enter to use default: ")
    filename = custom_filename if custom_filename else default_filename
    
    with open(filename, "w") as f:
        f.write('\n'.join(combinations))
    
    print(f"\n✅ Successfully generated {len(combinations)} entries in {filename}")
    
    # Hydra command suggestion
    if 'host_ip' in target_info and 'username' in target_info:
        print(f"\n{Fore.GREEN}Suggested Hydra command:{Style.RESET_ALL}")
        print(f"hydra -l {target_info['username']} -P {filename} {target_info['host_ip']} {service}")

if __name__ == "__main__":
    main_flow()
